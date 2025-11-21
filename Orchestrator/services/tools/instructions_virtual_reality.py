from services.tools.base_tool import _Tool
from core.utils import get_function_name
from core.utils import read_prompt
from config.chat import ChatGPT

class _InstructionsVR(_Tool):
    """
    Manages the appending of new prompts to the current workflow depending on the user intent,
    thus saving tokens in a subsequent API call
    """
    def _get_function(self, input):
        # Do semantic search and append this to the prompt to summarize it
        vector_store = ChatGPT().client.vector_stores.retrieve("")

        results = ChatGPT().client.vector_stores.search(
            vector_store_id=vector_store.id,
            query=input['previous_prompt'],
        )

        # Concatenate all the returned information to pass it to the new prompt
        context_info = ""
        for info in results['data']:
            complete_information += f"{info['content']['text']}\n"
        
        self.has_additional_prompt = f"""
            {read_prompt('instructions_virtual_reality.txt')}
            Context: {context_info}
            Answer the user: {input['previous_prompt']} 
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