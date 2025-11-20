from config.environment import config
from config.chat import chatgpt_client
from Orchestrator.services.tools.tool_manager import dynamic_prompt_handling, tools_definitions, tool_functions
import logging
from core.prompt_manager import read_prompt
import json
logging.basicConfig(level=logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def ask_chatbot(prompt):
    chat_history = [{"role": "user", "content": """Discern the user intent, if the user asks about 
                   wanting to know how to use the system, you will return 'tutorial' if the user 
                   wants to modify the contents of the elements or to change something, then 
                   return the same question the user asked, without any modification"""}]
    
    response = chatgpt_client.responses.create(
        model=config.LLM_MODEL,
        tools=dynamic_prompt_handling(),
        input=chat_history,
    )

    chat_history.extend(response.output)
    chat_history.append(call_tools(response.output))

    # Append new prompt
    few_shot_prompt = read_prompt("few_shot_redis_query.txt")
    chat_history.append({
         'role': 'system',
         'content': few_shot_prompt
    })

    logger.debug("Complete chat history:")
    logger.debug(chat_history)

    response = chatgpt_client.responses.create(
        model=config.LLM_MODEL,
        tools=tools_definitions(),
        input=chat_history,
    )

    logger.debug("Complete output:")
    logger.debug(response.model_dump_json(indent=2))
    logger.info("Chatbot Response:\n" + response.output_text)

    return json.loads(response.output_text)

def call_tools(chatbot_response):
    for item in chatbot_response.output:
        if item.type == "function_call":
            result = identify_function(item, tool_functions)
            return {
                 "type": "function_call_output",
                 "call_id": item.call_id, 
                 "output": json.dumps({"result": result})
                 }

def identify_function(item, tool_functions):
    for function in tool_functions():
        if item.name == function.__name__:
                return function(json.loads(item.arguments))