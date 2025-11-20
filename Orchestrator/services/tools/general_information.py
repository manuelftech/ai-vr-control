from Orchestrator.services.tools.base_tool import _Tool

class _GeneralInformationTool(_Tool):
    """
    Manages the appending of new prompts to the current workflow depending on the user intent,
    thus saving tokens in a subsequent API call
    """
    def __init__(self):
        super().__init__("general_information")
    
    def _get_function(self, input):
          search_subject = input["subject"]
          # Do semantic search on the PDF chunks that have the instructions to use the program
          return """
            In order to manipulate this 3D environment, you must use the keyboard that is floating in this livingroom, you can ask to modify the state of the elements of the environment, for example, you may ask 'I want all the cubes to float and turn green', and they will indeed start floating and become green, then you may ask: 'make all the cubes fall' and the cubes will fall, you can control what is happening in this Virtual environment
            """
        
    def _get_definition(self):
         return {
                "type": "function",
                "name": self.function_name,
                "description": "Find the instructions to manipulate the 3D environment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subject": {
                            "type": "string",
                            "description": "search_text for semantic search to find general knowledge",
                        },
                    },
                    "required": ["subject"],
                },
            }