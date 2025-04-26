import uuid
import sys
import time
import functools
from loguru import logger
from fastapi import Request
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from app.core.global_define import ErrorResponse


def setup_logging():
    # Remove all existing handlers
    logger.remove()
    
    # Add console handler with request_id context
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>request_id={extra[request_id]}</cyan> | <white>{message}</white>",
        level="INFO",
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # # # Add file handler with request_id context
    # logger.add(
    #     "logs/app.log",
    #     format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | request_id={extra[request_id]} | {message}",
    #     rotation="500 MB",
    #     retention="10 days",
    #     level="INFO",
    # )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        log = logger.bind(request_id=request_id)
        log.info(f"Request started: {request.method} {request.url.path}")

        start_time = time.time()
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            log.info(f"Request completed: {request.method} {request.url.path} in {process_time:.2f}s")
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as e:
            log.error(f"Request failed: {request.method} {request.url.path} - {str(e)}")
            raise


def get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", str(uuid.uuid4()))


def log_service_call(service_name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):

            request_id = kwargs.get("request_id", "")
            if not request_id and "request" in kwargs:
                request_id = get_request_id(kwargs["request"])

            log = logger.bind(request_id=request_id)
            t_begin = time.time()
            
            log.info("Call {service}.{func} with input {args} {kwargs}", service=service_name, func=func.__name__, args=args, kwargs=kwargs)
            try:
                result = await func(*args, **kwargs)
                log.info("Call completed: {service}.{func} in {time:.2f}s", 
                        service=service_name, func=func.__name__, time=time.time() - t_begin)
                return result
            except Exception as e:
                log.error("Call failed: {service}.{func} - {error}", 
                         service=service_name, func=func.__name__, error=str(e))
                return ErrorResponse.DEFAULT
        return wrapper
    return decorator 