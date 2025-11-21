from services.tools.base_tool import _Tool
from core.utils import read_prompt

class _VirtualRealityTool(_Tool):
    """
    Manages the virtual environment, updating its state using a Redis Database
    """
    def __init__(self):
        super().__init__("manipulate_virtual_reality")
    
    def _get_function(self, input):
        result = {"properties_to_update": []}
        
        result["continue_workflow"] = True
        result["additional_prompt"] = read_prompt('few_shot_virtual_reality.txt')
        return result

    def _get_definition(self):
         return {
                "type": "function",
                "name": self.function_name,
                "description": "Format your response for proper handling",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "template": {
                            "type": "string",
                            "description": "A template with a Redis Query and properties to update",
                        },
                    },
                    "required": ["template"],
                },
            }