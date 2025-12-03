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
        context_vr_handbook = VectorStore().semantic_search(config.VECTOR_STORE_KNOWLEDGE_BASE_ID, input['search_query'])
        self.has_additional_prompt = read_prompt('info_structure_prompt.txt')
        return context_vr_handbook
        
    def _get_definition(self):
         return {
                "type": "function",
                "name": get_function_name(__file__),
                "description": "Retrieves system usage instructions or tutorials about how to use the 3D environment system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_query": {
                            "type": "string",
                            "description": "The user question that will be used to search for tutorials or instructions",
                        },
                    },
                    "required": ["search_query"],
                },
            }