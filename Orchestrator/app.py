from controllers.vr_controller import router
from config.logger import configure_logger
from config.openai_agent import ChatGPT
from config.redis_db import RedisClient
from config.config_vars import config
from fastapi import FastAPI, Request
from config.drive import Drive
import uvicorn
import logging
import time
import structlog
import uuid

app = FastAPI()
configure_logger()
logger = logging.getLogger(__name__)

@app.middleware("http")
async def logging_middleware(req: Request, call_next):
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=str(uuid.uuid4()),
        method=req.method,
        path=req.url.path,
        client_ip=req.client.host)

    body = await req.body()
    try:
        # Attempt to decode the body (e.g., as JSON or text) for logging
        # If the content type is JSON, you might use json.loads(body)
        log_body = body.decode('utf-8') if body else None
        logger.info("Endpoint %s request: %s", req.url.path, log_body)
    except UnicodeDecodeError:
        logger.info("Error processing request body of endpoint %s",req.url.path )
    
    time_counter = time.perf_counter()
    try:
        res = await call_next(body)
    except Exception as e:
        logger.error("Unhandled exception", exc_info=True)
        raise e

    structlog.contextvars.bind_contextvars(
        status_code=res.status_code,
        response_time_ms=f"{(time.perf_counter() - time_counter)*1000:.1f}")

    if res.status_code >= 500:
        logger.error("Server error %s", res.status_code)
    elif res.status_code >= 400:
        logger.warning("Client error %s", res.status_code)
    logger.debug("Endpoint response: %s", res)
    return res



if __name__ == "__main__":
    # Validate OpenAI connection
    ChatGPT()
    # Validate Drive connection and downloads default configuration files
    Drive()
    # Validate database connection and cleans cache
    RedisClient()
    # Initialize the Server
    app.include_router(router)
    uvicorn.run(app, host="0.0.0.0", port=config.PORT)