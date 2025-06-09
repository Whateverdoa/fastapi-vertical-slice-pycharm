"""
FastAPI Application Entry Point

This module creates and configures the FastAPI application with all necessary
middleware, routers, and startup/shutdown event handlers.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from shared.config import settings
from shared.database import create_tables, get_engine
from shared.logging import setup_logging
from shared.middleware import LoggingMiddleware, RequestIDMiddleware
from shared.exceptions import setup_exception_handlers

# Import routers
from auth.api import router as auth_router
from users.api import router as users_router


logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan event handler for FastAPI application.
    
    Handles startup and shutdown events:
    - Database table creation
    - Connection pool initialization
    - Cleanup on shutdown
    """
    # Startup
    logger.info("🚀 Starting FastAPI application", version=settings.APP_VERSION)
    
    # Create database tables
    await create_tables()
    logger.info("✅ Database tables created/verified")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down FastAPI application")
    
    # Close database connections
    engine = get_engine()
    await engine.dispose()
    logger.info("✅ Database connections closed")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    # Setup logging first
    setup_logging()
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="FastAPI Vertical Slice Architecture - PyCharm Edition",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )
    
    # Add middleware (order matters!)
    add_middleware(app)
    
    # Setup exception handlers
    setup_exception_handlers(app)
    
    # Include routers
    include_routers(app)
    
    return app


def add_middleware(app: FastAPI) -> None:
    """Add all middleware to the FastAPI application."""
    
    # Security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )
    
    # Custom middleware
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(LoggingMiddleware)


def include_routers(app: FastAPI) -> None:
    """Include all API routers."""
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint for monitoring."""
        return {
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "debug": settings.DEBUG,
        }
    
    # API v1 routes
    app.include_router(
        auth_router,
        prefix="/api/v1/auth",
        tags=["Authentication"],
    )
    
    app.include_router(
        users_router,
        prefix="/api/v1/users",
        tags=["Users"],
    )


# Create the app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    # This allows running the app with: python src/main.py
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    ) 