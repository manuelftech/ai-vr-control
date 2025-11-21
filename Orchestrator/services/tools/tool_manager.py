from services.tools.general_information import _GeneralInformationTool
from services.tools.format_query_template_vr import _FormatQueryVR
from services.tools.manipulate_vr import _VirtualRealityTool
import logging
import json

logger = logging.getLogger(__name__)

class ToolManager():
    def __init__(self):
        # We obtain all the JSON definitions of the tools to be used
        self.tool_definitions = self._get_tool_definitions()
        self.continue_workflow = True

    def _get_tools(self):
        # Add more tools as needed
        return [
            _VirtualRealityTool(), 
            _GeneralInformationTool(),
            _FormatQueryVR()
            ]

    def _get_tool_functions(self):
        return [(tool.function_name, tool.function) for tool in self._get_tools()]

    def _get_tool_definitions(self):
        return [tool.definition for tool in self._get_tools()]
    
    def _find_function(self, item):
        for (function_name, function) in self._get_tool_functions():
            if item.name == function_name:
                logger.debug("Function called: %s", function_name)
                result = function(json.loads(item.arguments))
                logger.debug("Function result: %s", result)
                return result

    def call_tool(self, chatbot_response):
        # Executes the function logic depending on the tool the chat needs to use
        for item in chatbot_response:
            if item.type == "function_call":
                result = self._find_function(item)
                workflow = []
                # Wee return the response from the function logic
                workflow.append({
                    "type": "function_call_output","call_id": item.call_id, 
                    "output": json.dumps({"result": result})})
                # If the workflow continues and needs an additional prompt, we return it as well
                if result["continue_workflow"]:
                    workflow.append({"role": "system","content": result["additional_prompt"]})
                    self.continue_workflow = True
                else:
                    self.continue_workflow = False
                return workflow