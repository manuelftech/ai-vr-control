from fastapi.responses import StreamingResponse
from controllers.vr_controller import router
from config.logger import configure_logger
from config.openai_agent import OpenAIAgent
from config.redis_db import RedisClient
from config.config_vars import config
from fastapi import FastAPI, Request
from config.drive import Drive
import uvicorn
import logging
import time
import structlog
import uuid

configure_logger()
logger = logging.getLogger(__name__)

app = FastAPI()
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
        log_body = body.decode('utf-8') if body else None
        logger.info("Endpoint %s request: %s", req.url.path, log_body)
    except UnicodeDecodeError:
        logger.info("Error processing request body of endpoint %s", req.url.path )
    
    time_counter = time.perf_counter()
    res = await call_next(req)

    structlog.contextvars.bind_contextvars(
        status_code=res.status_code,
        response_time_ms=f"{(time.perf_counter() - time_counter)*1000:.1f}")

    if res.status_code >= 400:
        logger.error("HTTP Error %s", res.status_code)
    
    return res

if __name__ == "__main__":
    # Validate OpenAI connection
    OpenAIAgent()
    # Validate Drive connection and downloads default configuration files
    Drive()
    # Validate database connection and cleans cache
    RedisClient()
    # Initialize the Server
    app.include_router(router)
    uvicorn.run(app, host="0.0.0.0", port=config.APP_PORT)