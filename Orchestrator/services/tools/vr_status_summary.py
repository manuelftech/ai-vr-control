from core.utils import get_function_name, read_prompt
from repository.vr_repository import VRRepository
from services.tools.base_tool import _Tool

class _VRStatusSummary(_Tool):
    """
    Manages the chat history to provide a way for the Agent to know previous questions asked
    """
    def _get_function(self, input):
        # Search the chat history and return it
        vr_status = VRRepository().search_vr_summary()
        instructions = read_prompt('summarize_vr_status.txt')

        self.has_additional_prompt = f"""
            <Virtual Reality elements state:> 
            {vr_status}

            {instructions}

            <User request:> {input['previous_prompt']}
                """
        
    def _get_definition(self):
         return {
                "type": "function",
                "name": get_function_name(__file__),
                "description": "Retrieves the summary of the virtual reality status, to understand in what state the objects currently are.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "previous_prompt": {
                            "type": "string",
                            "description": "The prompt the user asked the agent",
                        },
                    },
                    "required": ["previous_prompt"],
                },
            }