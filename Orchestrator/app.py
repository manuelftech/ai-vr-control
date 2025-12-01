from controllers.vr_controller import router
from config.logger import configure_logger
from config.openai_agent import ChatGPT
from config.redis_db import RedisClient
from config.config_vars import config
from config.drive import Drive
from fastapi import FastAPI
import uvicorn

if __name__ == "__main__":
    # Set up log
    configure_logger()

    # Set up Services' configurations
    # Validate OpenAI connection
    ChatGPT()
    # Validate Drive connection and downloads default configuration files
    Drive()
    # Validate database connection and cleans cache
    RedisClient()

    # Initialize the Server
    app = FastAPI()
    app.include_router(router)
    uvicorn.run(app, host="0.0.0.0", port=config.PORT)