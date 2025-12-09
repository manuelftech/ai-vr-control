from repositories.vr_states_repository import StateRepository
from services.tools.base_tool import _Tool
from core.utils import get_file_name

class _RealTimeStates(_Tool):
    """
    Manages the chat history to provide a way for the Agent to know previous questions asked
    """
    def _get_function(self, input):
        # Search the real time element's status and return it
        state_details = StateRepository().search(tag=input['tag'])
        return state_details
        
    def _get_description(self):
         return {
                "type": "function",
                "name": get_file_name(__file__),
                "description": "Generates statistics of the virtual reality tag state.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tag": {
                            "type": "string",
                            "description": "The tag of the virtual reality element that will be used to provide information to the user about its state.",
                        },
                    },
                    "required": ["tag"],
                },
            }