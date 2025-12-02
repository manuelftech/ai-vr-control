from repository.vr_repository import VRRepository
from services.tools.system_instructions import _HowToUseSystem
from services.tools.generate_statistics import _GenerateStatistics
from config.openai_agent import ChatGPT
from config.config_vars import config
from core.utils import read_prompt
import logging
import json
import ast
logger = logging.getLogger(__name__)

class Workflow():
    """
    Manages the complete workflow and subsequent function calls and prompt appending
    """
    def __init__(self):
        # We obtain all the JSON definitions of the tools to be used
        self.tool_definitions = self._get_tool_definitions()
        self.has_additional_prompt = True

    def _get_tools(self):
        # Add more tools as needed
        return [
            _GenerateStatistics(),
            _HowToUseSystem(),
            ]
    
    def start(self, prompt):
        agent_context = self.get_agent_context()
        chat_history = agent_context + [{"role": "user", "content": prompt}]

        # If we need to ask again and continue our workflow, we append subsequent responses
        while self.has_additional_prompt:
            # We send the prompt to the agent
            response = ChatGPT().client.responses.create(
                model=config.LLM_MODEL,
                tools=self.tool_definitions,
                input=chat_history,
            )
            
            # We find the tools to be used during the workflow
            chat_history.extend(self._call_tool(response.output))

        # Get the final result of the workflow
        logger.info("Final response: %s", json.dumps(chat_history[-1]))
        return chat_history[-1]
    
    def get_agent_context(self):
        real_time_states_summary = VRRepository().get_real_time_summary()
        main_prompt = {"role": "system", "content": read_prompt('main_prompt.txt')}
        chat_history = VRRepository().search_chat_history()
        chat_history.append(real_time_states_summary)
        chat_history.append(main_prompt)
        return chat_history


    def _call_tool(self, agent_response):
        # Executes the function logic depending on the tool the chat needs to use
        for item in agent_response:
            if item.type == "function_call":
                result = self._find_function(item)
                agent_response.append({"type": "function_call_output", "call_id": item.call_id, 
                    "output": json.dumps({"result": result, "status": "Function called successfully"})})
                # If the workflow continues and needs an additional prompt, we append it
                if self.has_additional_prompt:
                    logger.debug("Additional prompt: %s", self.has_additional_prompt)
                    agent_response.append({"role": "system", "content": self.has_additional_prompt})
                return agent_response
        # If there are no additional prompts and no function calls, we return the final result
        self.has_additional_prompt = False
        agent_response.append(self._format_result(agent_response))
        return agent_response
    
    def _find_function(self, item):
        for tool in self._get_tool_functions():
            if item.name == tool.definition['name']:
                logger.debug("Function called: %s", tool.definition['name'])
                result = tool.function(json.loads(item.arguments))
                # We pass the value of the child instance to know if we should continue our workflow
                self.has_additional_prompt = tool.has_additional_prompt
                logger.debug("Function result: %s", result)
                return result
    
    def _format_result(self, agent_response):
        try:
            return ast.literal_eval(agent_response[-1].content[-1].text)
        except:
            raise NotImplementedError("The action provided does not return a JSON Template %s", agent_response[-1].content[-1].text)
    
    def _get_tool_functions(self):
        return [tool for tool in self._get_tools()]

    def _get_tool_definitions(self):
        return [tool.definition for tool in self._get_tools()]