import os
from dotenv import load_dotenv
load_dotenv()

class Config():
    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
    REDIS_PORT = os.environ.get("REDIS_PORT")
    INDEX_NAME = os.environ.get("INDEX_NAME")
    KEY_PREFIX = os.environ.get("KEY_PREFIX")
    LLM_API_KEY = os.environ.get("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")

config = Config()