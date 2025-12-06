from repository.vr_repository import VRRepository
from services.tools.base_tool import _Tool
from core.utils import get_file_name

class _RealTimeStates(_Tool):
    """
    Manages the chat history to provide a way for the Agent to know previous questions asked
    """
    def _get_function(self, input):
        # Search the real time element's status and return it
        real_time_states = VRRepository().get_real_time_states(input[''])
        return real_time_states
        
    def _get_description(self):
         return {
                "type": "function",
                "name": get_file_name(__file__),
                "description": "Generates statistics of the virtual reality states."
            }