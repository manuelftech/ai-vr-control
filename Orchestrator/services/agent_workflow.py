from config.exception_handlers.invalid_agent_request_error import InvalidAgentResponseError
from schemas.conversation_state_response import ConversationStateResponse
from schemas.vr_state_response import VRStateResponse
from repositories.vr_states_repository import StateRepository
from services.tools.tool_manager import tool_manager
from config.openai_agent import OpenAIAgent
from agents import trace
from config.config_vars import config
from core.utils import read_file
from fastapi.encoders import jsonable_encoder
import json
import structlog
logger = structlog.get_logger()

class AgentWorkflow():
    """
    Manages the complete workflow and subsequent function tools calls
    """

    async def stream_vr_info(self, prompt, conversation_id):
        instructions = [{"role": "user", "content": prompt}]

        waiting_message_displayed = False
        complete_tool_params = None
        complete_text_response = str()
        with trace("Element_State_Inquiry_Flow"): 
            stream = await OpenAIAgent().run_agent(
                name=config.AGENT_STATES,
                instructions=instructions,
                conversation_id=conversation_id,
                tools=tool_manager.tools,
                stream=True
            )

            async for event in stream.stream_events():
                # If it does not need a tool we yield the received text
                if hasattr(event, 'data') and event.data.type == 'response.output_text.delta':
                    complete_text_response += event.data.delta
                    yield event.data.delta
                if hasattr(event, 'data') and event.data.type == 'response.output_item.added' and event.data.item.type == 'function_call':
                    complete_tool_params = {}
                    complete_tool_params[event.data.output_index] = event.data.item
                    logger.debug("Agent needs function tool: %s", event.data.item.name)
                    if not waiting_message_displayed:
                        yield config.AGENT_WAITING_MESSAGE
                
                # If it needs a function tool, we log its function parameters
                if hasattr(event, 'data') and event.data.type == 'response.function_call_arguments.delta' and complete_tool_params[event.data.output_index]:
                    complete_tool_params[event.data.output_index].arguments += event.data.delta

                if hasattr(event, 'data') and event.data.type == 'response.completed':
                    if not complete_tool_params:
                        logger.debug("Streaming completed. Output: %s", complete_text_response)
                        continue
                
                if hasattr(event, 'data') and event.data.type == 'response.completed':
                    logger.debug("Executing function tool: %s", complete_tool_params)
                    complete_tool_params = None
                    if not waiting_message_displayed:
                        waiting_message_displayed = True
                        yield config.AGENT_DATA_FOUND_MESSAGE

    async def save_initial_vr_state(self, content, conversation_id):
        # Saves the initial Virtual Reality state to Redis
        await StateRepository().save(content=jsonable_encoder(content), conversation_id=conversation_id)

    async def clear_cache(self, conversation_id):
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
        
        # The agent is initialized with its main instructions given only once, and then remembered by the conversation_id
        conv_id_info = OpenAIAgent().get_conversation_id("vr_state")
        # We provide the instructions to understand how to structure its state response
        instructions_states = [
            {"role": "system", "content": f"conversation_id: {conv_id_template}"},
            {"role": "system", "content": read_file("vr_json_field_descriptions.txt")},
            {"role": "system", "content": read_file("limit_response_length.txt")}]
        
        await OpenAIAgent().run_agent(
                    name=config.AGENT_STATES,
                    instructions=instructions_states,
                    conversation_id=conv_id_info)
        logger.debug("Conversation ids created, template: %s, info: %s", conv_id_template, conv_id_info)

        return ConversationStateResponse(conv_id_info=conv_id_info, conv_id_template=conv_id_template)
    
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