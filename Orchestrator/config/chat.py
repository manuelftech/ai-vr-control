from openai import OpenAI
import config

class ChatGPT():
    _singleton = None
    _is_already_initialized = False

    def __init__(self):
        if not self._is_already_initialized:
            self.client = self._connect()
            self.connection_status = "Connected"
            self._is_already_initialized = True

    def _connect(self):
        try:
            return OpenAI(api_key=config.LLM_API_KEY)
        except Exception as e:
            raise Exception(e)
    
    def get_status(self):
        return self.connection_status

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(ChatGPT, cls).__new__(cls)
        return cls._singleton