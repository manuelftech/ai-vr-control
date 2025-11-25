from dotenv import load_dotenv
import json
import ast
import os
load_dotenv()

# --- App Configuration ---
PORT = int(os.environ.get("PORT"))
ENDPOINT_PREFIX = os.environ.get("ENDPOINT_PREFIX")
LOGGER_FORMAT = os.environ.get("LOGGER_FORMAT")

# --- OpenAI Configuration ---
LLM_API_KEY = os.environ.get("LLM_API_KEY")
LLM_MODEL = os.environ.get("LLM_MODEL")
VECTOR_STORE_KNOWLEDGE_BASE_ID = os.environ.get("VECTOR_STORE_KNOWLEDGE_BASE_ID")

# --- Redis Configuration ---
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDIS_PORT = int(os.environ.get("REDIS_PORT"))
INDEX_NAME = os.environ.get("INDEX_NAME")
KEY_PREFIX = os.environ.get("KEY_PREFIX")

# --- GCP Configuration ---
SCOPES = ast.literal_eval(os.environ.get("SCOPES"))
SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_FILE")
DRIVE_PROMPT_FILES = json.loads(os.environ.get("DRIVE_PROMPT_FILES"))