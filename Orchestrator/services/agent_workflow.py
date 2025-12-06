from repository.vr_repository import VRRepository
from services.tools.tool_manager import ToolManager
from config.openai_agent import ChatGPT
from config.config_vars import config
from core.utils import read_file
import logging
import json
logger = logging.getLogger(__name__)

class AgentWorkflow():
    """
    Manages the complete workflow and subsequent function tools calls
    """

    def __init__(self):
        self.tools = ToolManager()

    async def stream_vr_info(self, prompt, user_id):
        # We provide the agent with the information of previous interactions with the user
        previous_agent_history = VRRepository().search_all("previous_agent_history")
        
        agent_history = [
            {"role": "assistant", "content": previous_agent_history},
            {"role": "system", "content": read_file("limit_response_length.txt")},
            {"role": "user", "content": prompt}]

        workflow_completed = False
        while not workflow_completed:
            stream = ChatGPT().client.responses.create(
                model=config.LLM_MODEL,
                input=agent_history,
                tools=self.tools.descriptions,
                stream=True)

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
            # Summarizes the previous agent history to make its episodic memory more concise
        self.summarize_conversation_history(prompt=complete_text_response, user_id=user_id)

    def summarize_conversation_history(prompt, user_id):
        # We provide the agent with the information of previous interactions with the user
        previous_agent_history = VRRepository().search_all("previous_agent_history")
        agent_history = [
            {"role": "assistant", "content": previous_agent_history},
            {"role": "system", "content": read_file("summarize_previous_history.txt")}]

        response = ChatGPT().client.responses.create(
            model=config.LLM_MODEL,
            input=agent_history)
            
        # We delete the previously generated conversation history
        VRRepository().delete(prompt=prompt, user_id=user_id, namespace="message_history")
        # We generate this episodic information in the Database
        VRRepository().save(prompt=prompt, user_id=user_id, namespace="message_history")

    def invoke_tool(self, item):
        # Executes the function logic depending on the tool the agent needs to use
        function_tool = [tool.function if tool.description['name'] == item.name else None for tool in self.tools.functions]
        result = function_tool(json.loads(item.arguments))
        return {"type": "function_call_output",
                "call_id": item.call_id, 
                "output": json.dumps({"result": result, "status": "Function called successfully"})}
            
    def get_vr_template(self, prompt):
        # We provide the instructions to understand how to structure its state response
        agent_history = [
            {"role": "system", "content": read_file("vr_json_field_descriptions.txt")},
            {"role": "system", "content": read_file("few_shot_virtual_manipulation.txt")},
            {"role": "user", "content": prompt}]

        response = ChatGPT().client.responses.create(
            model=config.LLM_MODEL,
            input=agent_history)
            
        # We return the final json template provided by the agent
        return response.output[-1].content[-1].text