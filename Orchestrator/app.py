from config.drive import Drive
from controllers.vr_controller import router
from config.logger import configure_logger
from config.openai_agent import ChatGPT
from config.redis_db import RedisClient
from fastapi import FastAPI
from config import config
import uvicorn

if __name__ == "__main__":
    # Set up log
    configure_logger()

    # Set up Services' configurations
    ChatGPT()
    Drive()
    RedisClient()

    # Initialize the Server
    app = FastAPI()
    app.include_router(router)
    uvicorn.run(app, host="0.0.0.0", port=config.PORT)