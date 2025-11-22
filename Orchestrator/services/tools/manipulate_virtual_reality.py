from services.tools.base_tool import _Tool
from core.utils import get_function_name, read_prompt

class _ManipulateVR(_Tool):
    """
    Adds an additional prompt to enhace the workflow to manipulate the virtual reality environment
    """
    def _get_function(self, input):
        # We need to use self.has_additional_prompt if we want to make a subsequent call to the chatbot with an additional prompt
        instructions = read_prompt('format_virtual_reality_query.txt')
        self.has_additional_prompt = f"""
            {instructions}

            {input['previous_prompt']}
        """

    def _get_definition(self):
         return {
                "type": "function",
                "name": get_function_name(__file__),
                "description": "Extracts the structured query template from a user's previous prompt to prepare for manipulating a virtual 3D environment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "previous_prompt": {
                            "type": "string",
                            "description": "The preceding natural language prompt provided by the user, which potentially contains a query template that needs to be identified and extracted.",
                        },
                    },
                    "required": ["previous_prompt"],
                },
            }