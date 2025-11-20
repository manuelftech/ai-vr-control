from Orchestrator.services.tools.base_tool import Tool

class _GeneralInformationTool(Tool):
    """
    Manages the appending of new prompts to the current workflow depending on the user intent,
    thus saving tokens in a subsequent API call
    """
    def _get_function(self, input):
          original_prompt = input["etcetc"]
          return ''
        
    def _get_definition(self):
         return {
                "type": "function",
                "name": "get_formatted_knowledge_base",
                "description": "Find the instructions to manipulate the 3D environment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_text": {
                            "type": "string",
                            "description": "search_text for semantic search to find general knowledge",
                        },
                    },
                    "required": ["search_text"],
                },
            }