from Orchestrator.services.tools.manipulate_vr_state import _VirtualRealityTool
from Orchestrator.services.tools.general_information import _GeneralInformationTool
from Orchestrator.services.tools.prompt_handling import _PromptTool
from Orchestrator.core.utils import read_prompt
import logging
import json
logging.basicConfig(level=logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ToolManager():
    def __init__(self):
        # We obtain all the JSON definitions of the tools to be used
        self.tool_definitions = self._get_tool_definitions()
        # We initialize our first prompt, which allow us to choose from a variety of prompts to append
        self.prompt_handling_definition = [_PromptTool().definition]
        self.initialize_chat_history = self._initialize_chat_history

    def _get_tools(self):
        # Add more tools as needed
        return [
            _VirtualRealityTool(), 
            _GeneralInformationTool()
            ]

    def _get_tool_functions(self):
        return [(tool.function_name, tool.function) for tool in self._get_tools()]

    def _get_tool_definitions(self):
        return [tool.definition for tool in self._get_tools()]
    
    def _identify_function(self, item):
        for (function_name, function) in self._get_tool_functions():
            if item.name == function_name:
                logger.debug("Function called: %s", function_name)
                result = function(json.loads(item.arguments))
                logger.debug("Function result: %s", result)
                return result

    def call_tool(self, chatbot_response):
        # Executes the function logic depending on the tool the chat needs to use
        for item in chatbot_response.output:
            if item.type == "function_call":
                result = self._identify_function(item)
                return {
                    "type": "function_call_output",
                    "call_id": item.call_id, 
                    "output": json.dumps({"result": result})
                    }

    def prompt_handling(self, additional_prompt, user_prompt):
        # Chooses from a variety of prompts to add to the chat history
        match additional_prompt:
               case 'instruction':
                    return {
                        "role": "system",
                        "content": f"{read_prompt('few_shot_redis_query.txt')} {user_prompt}"
                        }
               case 'update_vr_state':
                    return {
                        "role": "system",
                        "content": f"{read_prompt('no_shot_knowledge_base.txt')} {user_prompt}"
                        }
               case _:
                    raise RuntimeError("No additional_prompt received")
    
    def _initialize_chat_history(slef, prompt):
        # First prompt to be added, where we identify the user's intentions to then append additional prompts
        base_prompt_user_intent = read_prompt("base_prompt_identify_intent.txt")
        return [{"role": "user", "content": f"{base_prompt_user_intent} {prompt}"}]