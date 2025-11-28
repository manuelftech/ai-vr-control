from repository.vr_repository import VRRepository
from services.tools.base_tool import _Tool
from core.utils import get_function_name

class _AgentMemoryContext(_Tool):
    """
    Manages the chat history to provide a way for the Agent to know previous questions asked
    """
    def _get_function(self, input):
        # Search the chat history and return it
        chat_history = VRRepository().search("@Tag:{history}")

        self.has_additional_prompt = f"""
            Take the following agent chat history as context to 
            answer the user question: {chat_history}.

            User question: {input['previous_prompt']}
            """
        
    def _get_definition(self):
         return {
                "type": "function",
                "name": get_function_name(__file__),
                "description": "Retrieves the chat history to understand previously asked questions.",
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