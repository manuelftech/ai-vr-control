from Orchestrator.services.tools.base_tool import _Tool
from core.prompt_manager import read_prompt

class _PromptTool(_Tool):
    """
    Manages the appending of new prompts to the current workflow depending on the user intent,
    thus saving tokens in a subsequent API call
    """
    def _get_function(self, input):
          original_prompt = input["etcetc"]
          match input["intent"]:
               case '':
                    return f"{read_prompt('few_shot_redis_query.txt')} {original_prompt}"
               case '':
                    return f"{read_prompt('no_shot_knowledge_base.txt')} {original_prompt}"
               case _:
                    return original_prompt
               
    def _get_definition(self):
         return {
               "type": "function",
               "name": "user_intent",
               "description": "Understands the user intent: Wanting to know how to use the system (tutorial), or else, return the same question the user asked",
               "parameters": {
                    "type": "object",
                    "properties": {
                         "intent": {
                         "type": "string",
                         "description": "The entire user question if the user wants to modify something, or the text 'tutorial' if the user's intent is to know something",
                         },
                    },
                    "required": ["intent"],
               },
          }