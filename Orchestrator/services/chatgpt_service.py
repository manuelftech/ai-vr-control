from services.tools.tool_manager import ToolManager
from config.environment import config
from core.utils import read_prompt
import logging
import json
from config.chat import chatgpt

logger = logging.getLogger(__name__)

def ask_chatbot(prompt):
    tools = ToolManager()
    chat_history = [{"role": "user", "content": f"{read_prompt("base_prompt_identify_intent.txt")} {prompt}"}]

    response = chatgpt.client.responses.create(
        model=config.LLM_MODEL,
        tools=tools.prompt_handling_definition,
        input=chat_history,
    )

    # Add the initial response to the chat history
    chat_history.extend(response.output)

    # If the function requires an additional tool, we continue the workflow
    while tools.continue_workflow:
        chat_history.append(tools.call_tool(response.output))
        response = chatgpt.client.responses.create(
            model=config.LLM_MODEL,
            tools=tools.tool_definitions,
            input=chat_history)

    # Get the final result of the workflow
    result = json.loads(chat_history[-1]['output'])['result']
    logger.info("Final response: %s" + result)
    return result