from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from typing import Dict, Any
import json
import ast
import os
load_dotenv()

class ConfigVar(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- OpenAI Configuration ---
    LLM_API_KEY: str
    LLM_MODEL: str
    VECTOR_STORE_KNOWLEDGE_BASE_ID: str

    # --- Redis Configuration ---
    REDIS_HOST: str
    REDIS_PASSWORD: str
    REDIS_PORT: str
    VR_INDEX: str
    VR_KEY_PREFIX: str
    REDIS_SEARCH_LIMIT: int

    # --- GCP Configuration ---
    SCOPES: list[str]
    SERVICE_ACCOUNT_FILE: str
    DRIVE_PROMPT_FILES: list[str]

    # --- App Configuration ---
    PORT: int
    ENDPOINT_PREFIX: str
    LOGGER_FORMAT: str
    LOGGER_LEVEL: int
    LOGGER_DATE_FORMAT: str
    LOGGER_COLOR_FORMAT: Dict[str, str]
    CHAT_GENERIC_FULFILLED_MESSAGE: Dict[str, str]

config = ConfigVar()