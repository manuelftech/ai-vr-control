from schemas.vr_state_response import VRStateResponse
from repositories.vr_states_repository import StateRepository
from services.tools.tool_manager import tools
from config.openai_agent import OpenAIAgent
from config.exception_handlers.invalid_agent_request_error import InvalidAgentResponseError
from agents import trace
from config.config_vars import config
from core.utils import read_file
from fastapi.encoders import jsonable_encoder
import structlog
import asyncio
import json
logger = structlog.get_logger()

class AgentWorkflow():
    """
    Manages the complete workflow and subsequent function tools calls
    """

    async def stream_vr_info(self, prompt, conversation_id):
        instructions = [
            {"role": "system", "content": read_file("vr_json_field_descriptions.txt")},
            {"role": "system", "content": read_file("limit_response_length.txt")},
            {"role": "user", "content": prompt}]

        workflow_completed = False
        while not workflow_completed:
            with trace("Element_State_Inquiry_Flow"): 
                stream = await OpenAIAgent().run_agent(
                    name="ElementStateReporter",
                    instructions=instructions,
                    conversation_id=conversation_id,
                    tools=tools.descriptions,
                    stream=True
                )

                complete_tool_params = None
                complete_text_response = ""
                for event in stream:
                    # If it does not need a tool we yield the received text
                    if event.type == 'response.output_text.delta':
                        complete_text_response += event.delta
                        yield event.delta

                    if event.type == 'response.output_item.added' and event.item.type == 'function_call':
                        complete_tool_params = {}
                        complete_tool_params[event.output_index] = event.item
                        yield config.AGENT_WAITING_MESSAGE
                    
                    # If it needs a tool we gather the function parameters
                    if event.type == 'response.function_call_arguments.delta' and complete_tool_params[event.output_index]:
                        complete_tool_params[event.output_index].arguments += event.delta

                    if event.type == 'response.completed':
                        if complete_tool_params:
                            # We choose the function tool that is going to be invoked
                            agent_history += complete_tool_params
                            agent_history += self.invoke_tool(complete_tool_params)
                        else:
                            workflow_completed = True
    
    def invoke_tool(self, item):
        # Executes the function logic depending on the tool the agent needs to use
        function_tool = [tool.function if tool.description['name'] == item.name else None for tool in self.tools.functions]
        result = function_tool(json.loads(item.arguments))
        return { "type": "function_call_output",
                 "call_id": item.call_id, 
                 "output": json.dumps({"result": result, "status": "Function called successfully"})
                }

    def apply_template_state(self, agent_response):
        try:
            return VRStateResponse.model_validate_json(agent_response)
        except:
            raise InvalidAgentResponseError()

    async def save_initial_vr_state(self, content, conversation_id):
        # Saves the initial Virtual Reality state to Redis
        await StateRepository().save(content=jsonable_encoder(content), conversation_id=conversation_id)

    async def clear_cache(self, conversation_id):
        await StateRepository().delete(conversation_id=conversation_id)

    async def update_vr_state(self, states, conversation_id):
        await StateRepository().update(content=states, conversation_id=conversation_id)

    def create_conversation(self):
        logger.info("Creating Conversation id")
        conversation_id = OpenAIAgent().get_conversation_id()
        logger.debug("Conversation id created: %s", conversation_id)
        return conversation_id
    
    async def get_vr_template(self, prompt, conversation_id):
        # We provide the instructions to understand how to structure its state response
        instructions = [
            {"role": "system", "content": read_file("vr_json_field_descriptions.txt")},
            {"role": "system", "content": read_file("few_shot_virtual_manipulation.txt")},
            {"role": "user", "content": prompt}
            ]

        with trace("Json_Template_Generation_Flow"): 
            response = await OpenAIAgent().run_agent(
                name="JsonTemplateGenerator",
                instructions=instructions,
                conversation_id=conversation_id,
                output_type=VRStateResponse
            )
        if not response.final_output.Tag:
            raise InvalidAgentResponseError("Missing Tag")
        return response.final_output