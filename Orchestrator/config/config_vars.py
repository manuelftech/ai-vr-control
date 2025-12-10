from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()

class ConfigVar(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- OpenAI Configuration ---
    LLM_MODEL: str
    VECTOR_STORE_KNOWLEDGE_BASE_ID: str
    AGENT_WAITING_MESSAGE: str
    AGENT_TEMPLATE: str
    AGENT_STATES: str
    AGENT_DATA_FOUND_MESSAGE: str

    # --- Redis Configuration ---
    REDIS_HOST: str
    REDIS_PASSWORD: str
    REDIS_PORT: str
    VR_INDEX: str
    VR_KEY_PREFIX: str
    REDIS_SEARCH_LIMIT: int
    CONVERSATION_ID_SEARCH: str
    TAG_SEARCH: str

    # --- GCP Configuration ---
    SCOPES: list[str]
    SERVICE_ACCOUNT_FILE: str
    DRIVE_CONFIG_FILES: list[str]

    # --- App Configuration ---
    APP_PORT: int
    ENDPOINT_PREFIX: str

config = ConfigVar()