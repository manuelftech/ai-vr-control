from schemas.vr_state_response import VRStateResponse
from repositories.vr_states_repository import StateRepository
from services.tools.tool_manager import tool_manager
from config.openai_agent import OpenAIAgent
from config.exception_handlers.invalid_agent_request_error import InvalidAgentResponseError
from agents import trace
from config.config_vars import config
from core.utils import read_file
from fastapi.encoders import jsonable_encoder
import structlog
from schemas.conversation_state_response import ConversationStateResponse
import json
logger = structlog.get_logger()

class AgentWorkflow():
    """
    Manages the complete workflow and subsequent function tools calls
    """

    async def stream_vr_info(self, prompt, conversation_id):
        instructions = [{"role": "user", "content": prompt}]

        workflow_completed = False
        while not workflow_completed:
            with trace("Element_State_Inquiry_Flow"): 
                stream = await OpenAIAgent().run_agent(
                    name=config.AGENT_STATES,
                    instructions=instructions,
                    conversation_id=conversation_id,
                    tools=tool_manager.tools,
                    stream=True
                )

                complete_tool_params = None
                complete_text_response = ""
                async for event in stream.stream_events():
                    # If it does not need a tool we yield the received text
                    if hasattr(event, 'data') and event.data.type == 'response.output_text.delta':
                        complete_text_response += event.data.delta
                        yield event.data.delta

                    if hasattr(event, 'data') and event.data.type == 'response.output_item.added' and event.data.item.type == 'function_call':
                        complete_tool_params = {}
                        complete_tool_params[event.data.output_index] = event.data.item
                        yield config.AGENT_WAITING_MESSAGE
                    
                    # If it needs a tool we gather the function parameters
                    if event.type == 'response.function_call_arguments.delta' and complete_tool_params[event.output_index]:
                        complete_tool_params[event.output_index].arguments += event.data

                    if hasattr(event, 'data') and event.data.type == 'response.completed':
                        if complete_tool_params:
                            # We choose the function tool that is going to be invoked
                            agent_history += complete_tool_params
                            agent_history += self.invoke_tool(complete_tool_params)
                        else:
                            workflow_completed = True
    
    def invoke_tool(self, item):
        # Executes the function logic depending on the tool the agent needs to use
        function_tool = [func if item.name == func.__name__ else None for func in tool_manager.tools]
        result = function_tool(json.loads(item.arguments))
        return { "type": "function_call_output",
                 "call_id": item.call_id, 
                 "output": json.dumps({"result": result, "status": "Function called successfully"})
                }

    async def save_initial_vr_state(self, content, conversation_id):
        # Saves the initial Virtual Reality state to Redis
        await StateRepository().save(content=jsonable_encoder(content), conversation_id=conversation_id)

    async def clear_cache(self, conversation_ids):
        for conversation_id in conversation_ids:
            await StateRepository().delete(conversation_id=conversation_id)

    async def update_vr_state(self, states, conversation_id):
        await StateRepository().update(content=states, conversation_id=conversation_id)

    async def create_conversation(self):
        logger.info("Creating Conversation ids")
        conv_id_template = OpenAIAgent().get_conversation_id("vr_template")
        # We provide the instructions to understand how to structure its state response
        instructions_template = [
            {"role": "system", "content": read_file("vr_json_field_descriptions.txt")},
            {"role": "system", "content": read_file("few_shot_virtual_manipulation.txt")}]
        
        # The agent is initialized with its main instructions given only once, and then remembered by the conversation_id
        await OpenAIAgent().run_agent(
                name=config.AGENT_TEMPLATE,
                instructions=instructions_template,
                conversation_id=conv_id_template)
        logger.debug("Conversation id template created: %s", conv_id_template)

        # The agent is initialized with its main instructions given only once, and then remembered by the conversation_id
        conv_id_state = OpenAIAgent().get_conversation_id("vr_state")
        # We provide the instructions to understand how to structure its state response
        instructions_states = [
            {"role": "system", "content": read_file("vr_json_field_descriptions.txt")},
            {"role": "system", "content": read_file("limit_response_length.txt")}]
        
        await OpenAIAgent().run_agent(
                    name=config.AGENT_STATES,
                    instructions=instructions_states,
                    conversation_id=conv_id_state)
        logger.debug("Conversation id state created: %s", conv_id_state)

        return ConversationStateResponse(conv_id_state=conv_id_state, conv_id_template=conv_id_template)
    
    async def get_vr_template(self, prompt, conversation_id):
        instructions = [
            {"role": "user", "content": prompt}
            ]

        with trace("Json_Template_Generation_Flow"): 
            response = await OpenAIAgent().run_agent(
                name=config.AGENT_TEMPLATE,
                instructions=instructions,
                conversation_id=conversation_id,
                output_type=VRStateResponse
            )

        if not response.final_output.Tag:
            raise InvalidAgentResponseError(f"User did not request to modify states, User prompt: {prompt}")
        return response.final_output