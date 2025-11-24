from openai import OpenAI
from config import config
import logging
logger = logging.getLogger(__name__)

class ChatGPT():
    _singleton = None
    _is_already_initialized = False

    def __init__(self):
        if not self._is_already_initialized:
            self.client = self._connect()
            self.connection_status = "Connected"
            self._is_already_initialized = True

    def _connect(self):
        logger.debug("Connecting to OpenAI agent")
        try:
            agent = OpenAI(api_key=config.LLM_API_KEY)
            logger.debug("Successfuly connected to OpenAI agent")
            return agent
        except Exception as e:
            raise Exception(e)
    
    def get_status(self):
        return self.connection_status

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(ChatGPT, cls).__new__(cls)
        return cls._singleton