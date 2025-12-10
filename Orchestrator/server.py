from config.exception_handlers.exception_handler import global_exception_handler, validation_exception_handler, agent_request_handler
from config.exception_handlers.invalid_agent_request_error import InvalidAgentResponseError
from fastapi.exceptions import RequestValidationError
from controllers.vr_controller import router
from config.logger import configure_logger
from config.openai_agent import OpenAIAgent
from config.redis_db import RedisClient
from config.config_vars import config
from fastapi import FastAPI, Request
from config.drive import Drive
import uvicorn
import time
import uuid
import structlog
logger = structlog.get_logger()
server = FastAPI()

@server.middleware("http")
async def middleware_logging(req: Request, call_next):
    request_id=str(uuid.uuid4())
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        method=req.method,
        path=req.url.path,
        client_ip=req.client.host)

    body = await req.body()
    try:
        log_body = body.decode('utf-8') if body else None
        logger.debug("Request: %s", log_body)
    except UnicodeDecodeError as e:
        logger.error(e)
    
    time_counter = time.perf_counter()
    res = await call_next(req)

    structlog.contextvars.bind_contextvars(
        status_code=res.status_code,
        response_time_ms=f"{(time.perf_counter() - time_counter)*1000:.1f}")
    
    return res

server.add_exception_handler(RequestValidationError, validation_exception_handler)
server.add_exception_handler(InvalidAgentResponseError, agent_request_handler)
server.add_exception_handler(Exception, global_exception_handler)

if __name__ == "__main__":
    # Validate OpenAI connection
    OpenAIAgent()
    # Validate Drive connection and downloads default configuration files
    Drive()
    # Validate database connection and cleans cache
    RedisClient()
    # Initialize the Server
    server.include_router(router)

    # Cofigure log format
    configure_logger()
    uvicorn.run(server, host="0.0.0.0", port=config.APP_PORT, log_config=None, access_log=False)
