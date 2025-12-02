from core.utils import get_function_name, read_prompt
from repository.vr_repository import VRRepository
from services.tools.base_tool import _Tool

class _GenerateStatistics(_Tool):
    """
    Manages the chat history to provide a way for the Agent to know previous questions asked
    """
    def _get_function(self, input):
        # Search the real time element's status and return it
        real_time_states = VRRepository().search_system_statistics()
        self.has_additional_prompt = read_prompt('info_structure_prompt.txt')
        return real_time_states
        
    def _get_definition(self):
         return {
                "type": "function",
                "name": get_function_name(__file__),
                "description": "Generates statistics of the virtual reality states."
            }