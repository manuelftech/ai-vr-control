from services.tools.base_tool import _Tool
from core.utils import get_function_name, search_vector_store, read_prompt
from config import config

class _InstructionsVR(_Tool):
    """
    Manages the appending of new prompts to the current workflow depending on the user intent,
    thus saving tokens in a subsequent API call
    """
    def _get_function(self, input):
        # Semantic search and appending of the returned context to the new prompt
        context_info = search_vector_store(config.VECTOR_STORE_KNOWLEDGE_BASE_ID, input['previous_prompt'])
        instructions = read_prompt('instructions_virtual_reality.txt')

        self.has_additional_prompt = f"""
            User Request: {input["previous_prompt"]}

            Guidance: Utilize the provided context to address the user's query: {context_info}

            Execution Plan: Perform the following steps and actions: {instructions}
            """
        
    def _get_definition(self):
         return {
                "type": "function",
                "name": get_function_name(__file__),
                "description": "Retrieves relevant system usage instructions and documentation by searching the knowledge base for a given query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "previous_prompt": {
                            "type": "string",
                            "description": "The natural language search query or topic the user is asking about (e.g., 'How this system works?', 'Explain how to use this environment', 'provide the system documentation?'). This query is used for a semantic search to locate the most relevant instructions.",
                        },
                    },
                    "required": ["previous_prompt"],
                },
            }