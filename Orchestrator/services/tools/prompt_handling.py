from services.tools.base_tool import _Tool
from core.utils import read_prompt

class _PromptTool(_Tool):
    """
    Manages the appending of new prompts to the current workflow depending on the user intent,
    thus saving tokens in a subsequent API call
    """
    def __init__(self):
        super().__init__("additional_prompt")
    
    def _get_function(self, input):
          original_prompt = input["intent"]
          match input["intent"]:
               case 'instruction':
                    return f"{read_prompt('few_shot_redis_query.txt')} {original_prompt}"
               case 'update_vr_state':
                    return f"{read_prompt('no_shot_knowledge_base.txt')} {original_prompt}"
               case _:
                    return None
               
               
    def _get_definition(self):
         return {
               "type": "function",
               "name": self.function_name,
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