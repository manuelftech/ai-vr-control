from dotenv import load_dotenv
import os
load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDIS_PORT = os.environ.get("REDIS_PORT")
INDEX_NAME = os.environ.get("INDEX_NAME")
KEY_PREFIX = os.environ.get("KEY_PREFIX")
LLM_API_KEY = os.environ.get("LLM_API_KEY")
LLM_MODEL = os.environ.get("LLM_MODEL")
ENDPOINT_PREFIX = os.environ.get("ENDPOINT_PREFIX")
LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL")
LOGGER_FORMAT = os.environ.get("LOGGER_FORMAT")
VECTOR_STORE_KNOWLEDGE_BASE_ID = os.environ.get("VECTOR_STORE_KNOWLEDGE_BASE_ID")