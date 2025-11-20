from Orchestrator.services.tools.manipulate_vr_state import _VirtualRealityTool
from Orchestrator.services.tools.general_information import _GeneralInformationTool
from Orchestrator.services.tools.prompt_handling import _PromptTool
import logging
import json
logging.basicConfig(level=logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ToolManager():
    def __init__(self):
        self.tool_definitions = self._get_tool_definitions()
        self.prompt_handling_definition = _PromptTool().definition

    def _get_tools():
        return [
            _VirtualRealityTool(), 
            _GeneralInformationTool()
            ]

    def _get_tool_functions(self):
        return [tool.function for tool in self._get_tools()]

    def _get_tool_definitions(self):
        return [tool.definition for tool in self._get_tools()]
    
    def _identify_function(self, item):
        for function in self._get_tool_functions():
            if item.name == function.__name__:
                logger.debug("Function called: %s", function.__name__)
                result = function(json.loads(item.arguments))
                logger.debug("Function result: %s", result)
                return result

    def call_tool(self, chatbot_response):
        for item in chatbot_response.output:
            if item.type == "function_call":
                result = self._identify_function(item)
                return {
                    "type": "function_call_output",
                    "call_id": item.call_id, 
                    "output": json.dumps({"result": result})
                    }

    def prompt_handling(self, chatbot_response):
        for item in chatbot_response.output:
            if item.type == "function_call":
                prompt_tool = _PromptTool()
                if item.name == prompt_tool.function.__name__:
                    prompt = prompt_tool.function(json.loads(item.arguments))
                    return {
                        "role": "system",
                        "content": json.dumps({"result": prompt})
                        }