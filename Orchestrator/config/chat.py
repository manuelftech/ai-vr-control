from openai import OpenAI
from config.environment import config

class ChatGPTClient():
    def __init__(self):
        self.client = self.connect()
        self.connection_status = "Connected"

    def connect(self):
        try:
            return OpenAI(api_key=config.LLM_API_KEY)
        except Exception as e:
            raise Exception(e)
    
    def get_status(self):
        return self.connection_status

chatgpt = ChatGPTClient()