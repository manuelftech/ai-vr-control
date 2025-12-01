from config.config_vars import config
from openai import OpenAI
import logging
logger = logging.getLogger(__name__)

class ChatGPT():
    _singleton = None
    _is_already_initialized = False

    def __init__(self):
        if not self._is_already_initialized:
            self.client = self._connect()
            self._is_already_initialized = True

    def _connect(self):
        logger.debug("Connecting to OpenAI agent")
        try:
            agent = OpenAI(api_key=config.LLM_API_KEY)
            agent.models.list()
            logger.debug("Successfuly connected to OpenAI agent")
            return agent
        except Exception as e:
            raise Exception(e)

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(ChatGPT, cls).__new__(cls)
        return cls._singleton