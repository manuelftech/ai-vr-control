from Orchestrator.services.tools.manipulate_vr_state import get_formatted_vr_state
from Orchestrator.services.tools.platform_instructions import get_platform_instructions
from core.prompt_manager import read_prompt

def tool_functions():
    return [
        get_formatted_vr_state,
        get_platform_instructions,
        get_user_intent
    ]

def dynamic_prompt_handling():
     # Dinamically adding prompts to save tokens in every subsequent ChatGPT API call  
    return [{
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
        }]

def get_user_intent(input):
     # Dinamically adding prompts to save tokens in every subsequent ChatGPT API call
    few_shot_prompt = read_prompt("few_shot_redis_query.txt")
    return f"""{few_shot_prompt} {input['question']}
    """

def tools_definitions():
    return [
        {
            "type": "function",
            "name": "get_formatted_vr_state",
            "description": "Format your response for proper handling",
            "parameters": {
                "type": "object",
                "properties": {
                    "template": {
                        "type": "string",
                        "description": "A template with a Redis Query and properties to update",
                    },
                },
                "required": ["template"],
            },
        },
        {
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
        },
    ]