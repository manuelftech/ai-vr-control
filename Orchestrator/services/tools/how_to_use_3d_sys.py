from core.utils import get_function_name, read_prompt
from repository.vector_store import VectorStore
from config.config_vars import config
from services.tools.base_tool import _Tool

class _HowToUseSystem(_Tool):
    """
    Manages the appending of new prompts to the current workflow depending on the user intent,
    thus saving tokens in a subsequent API call
    """
    def _get_function(self, input):
        # Semantic search and appending of the returned context to the new prompt
        context_vr_handbook = VectorStore().semantic_search(config.VECTOR_STORE_KNOWLEDGE_BASE_ID, input['previous_prompt'])
        instructions = read_prompt('description_state.txt')

        self.has_additional_prompt = f"""
            <Instructions>: {instructions}

            <Context>: {context_vr_handbook}

            <User Question>: {input['previous_prompt']}
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