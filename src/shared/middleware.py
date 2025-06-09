"""Custom middleware - placeholder"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add request ID to each request."""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests."""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        return response 