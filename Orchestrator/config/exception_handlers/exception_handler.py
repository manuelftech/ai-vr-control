from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from config.exception_handlers.invalid_agent_request_error import InvalidAgentResponseError
from starlette.status import HTTP_422_UNPROCESSABLE_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST
import structlog
import structlog.contextvars
import structlog
logger = structlog.get_logger()

def handle_exception(exc: Exception, status_code: int, message: str):
    logger.error(f"HTTP Status {status_code}: {message}", exc_info=exc)
    structlog.contextvars.bind_contextvars(error_details=str(exc))
    request_id = structlog.contextvars.get_contextvars().get("request_id", "N/A")
    raise HTTPException(status_code=status_code, detail={"request_id": request_id})

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return handle_exception(exc, HTTP_422_UNPROCESSABLE_CONTENT, "Invalid request data")

async def agent_request_handler(request: Request, exc: InvalidAgentResponseError):
    return handle_exception(exc, HTTP_400_BAD_REQUEST, "Invalid request made by the user")

async def global_exception_handler(request: Request, exc: Exception):
    return handle_exception(exc, HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error")