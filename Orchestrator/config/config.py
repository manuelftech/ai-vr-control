from dotenv import load_dotenv
import os
load_dotenv()

# REDIS_HOST = os.environ.get("REDIS_HOST")
# REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
# REDIS_PORT = os.environ.get("REDIS_PORT")
# INDEX_NAME = os.environ.get("INDEX_NAME")
# KEY_PREFIX = os.environ.get("KEY_PREFIX")
# LLM_API_KEY = os.environ.get("LLM_API_KEY")
# LLM_MODEL = os.environ.get("LLM_MODEL")
# ENDPOINT_PREFIX = os.environ.get("ENDPOINT_PREFIX")
# LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL")
# LOGGER_FORMAT = os.environ.get("LOGGER_FORMAT")
# VECTOR_STORE_KNOWLEDGE_BASE_ID = os.environ.get("VECTOR_STORE_KNOWLEDGE_BASE_ID")

REDIS_HOST = 'localhost'
REDIS_PASSWORD = "123456" 
REDIS_PORT = 6379
INDEX_NAME = "VRStateIdx"
KEY_PREFIX = "VRState:"
LLM_API_KEY = "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"
LLM_MODEL = "gpt-5-nano-2025-08-07"
ENDPOINT_PREFIX = "/virtual-reality-environment"
LOGGING_LEVEL = 10 # DEBUG = 10, CRITICAL = 50, FATAL = CRITICAL, ERROR = 40, WARNING = 30, WARN = WARNING, INFO = 20, NOTSET = 0
LOGGER_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
VECTOR_STORE_KNOWLEDGE_BASE_ID = "vs_6920beaaf5b88191a913085f8fe88a1b"