from config.config_vars import config
from openai import OpenAI
from agents import Agent, Runner
import logging
logger = logging.getLogger(__name__)

class OpenAIAgent():
    _singleton = None
    _is_already_initialized = False

    def __init__(self):
        if not self._is_already_initialized:
            #self.runner = self._get_runner()
            self._is_already_initialized = True

    def _get_runner(self):
        logger.info("Validating connection to OpenAI")
        runner = Runner()
        try:
            runner.run_sync(
                starting_agent=Agent(name="startup validation", model=config.LLM_MODEL),
                input="Respond yes",
                max_turns=1
            )
        except Exception as e:
            logger.info("Error connecting to OpenAI")
            raise Exception(e)
        logger.info("Successfully connected to OpenAI")
        return runner
    
    def run_agent(self, name, instructions, tools, conversation_id, stream=False):
        agent = Agent(
                name=name,
                instructions=instructions,
                model=config.LLM_MODEL,
                conversation_id=conversation_id,
                tools=tools
            )
        if stream:
            return self.runner.run_streamed(agent=agent)
        return self.runner.run(agent=agent)
    
    def get_conversation_id(self):
        conversation = OpenAI().conversations.create(
            metadata={"topic": "Virtual Reality State"},
            items=[{"type": "message", "role": "assistant", 
                    "content": "The virtual reality state conversation has been initialized"}]
        )
        return conversation.id
    
    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(OpenAIAgent, cls).__new__(cls)
        return cls._singleton