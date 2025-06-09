"""Exception handlers - placeholder"""

from fastapi import FastAPI


def setup_exception_handlers(app: FastAPI):
    """Setup global exception handlers."""
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        return {"error": "Internal server error"} 