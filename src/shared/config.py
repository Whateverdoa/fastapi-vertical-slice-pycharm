"""
Application Configuration

This module handles all application settings using Pydantic Settings
for type-safe environment variable management.
"""

from typing import List, Literal

from pydantic import Field, PostgresDsn, RedisDsn, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings are type-safe and validated using Pydantic.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Application settings
    APP_NAME: str = Field(default="FastAPI Vertical Slice", description="Application name")
    APP_VERSION: str = Field(default="0.1.0", description="Application version")
    DEBUG: bool = Field(default=False, description="Debug mode")
    
    # Server settings
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    RELOAD: bool = Field(default=False, description="Auto-reload on code changes")
    
    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )
    
    # Security
    SECRET_KEY: str = Field(..., description="Secret key for signing tokens")
    JWT_SECRET_KEY: str = Field(..., description="JWT secret key")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, description="Access token expiration in minutes"
    )
    
    # Database
    DATABASE_URL: PostgresDsn = Field(..., description="PostgreSQL database URL")
    DATABASE_ECHO: bool = Field(default=False, description="Echo SQL queries")
    
    # Redis
    REDIS_URL: RedisDsn = Field(default="redis://localhost:6379/0", description="Redis URL")
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    ALLOWED_METHODS: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "PATCH"],
        description="Allowed HTTP methods"
    )
    ALLOWED_HEADERS: List[str] = Field(
        default=["*"],
        description="Allowed HTTP headers"
    )
    ALLOWED_HOSTS: List[str] = Field(
        default=["*"],
        description="Allowed hosts for security"
    )
    
    # Email settings (optional)
    SMTP_HOST: str = Field(default="", description="SMTP server host")
    SMTP_PORT: int = Field(default=587, description="SMTP server port")
    SMTP_USER: str = Field(default="", description="SMTP username")
    SMTP_PASSWORD: str = Field(default="", description="SMTP password")
    SMTP_FROM: str = Field(default="", description="Default sender email")
    
    # Celery settings
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/1",
        description="Celery broker URL"
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/2",
        description="Celery result backend URL"
    )
    
    # Monitoring
    SENTRY_DSN: str = Field(default="", description="Sentry DSN for error tracking")
    PROMETHEUS_ENABLED: bool = Field(default=False, description="Enable Prometheus metrics")
    
    # File upload settings
    MAX_UPLOAD_SIZE: int = Field(default=10485760, description="Max upload size in bytes (10MB)")
    UPLOAD_DIR: str = Field(default="uploads/", description="Upload directory")
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = Field(default=20, description="Default pagination page size")
    MAX_PAGE_SIZE: int = Field(default=100, description="Maximum pagination page size")
    
    # Feature flags
    FEATURE_USER_REGISTRATION: bool = Field(default=True, description="Enable user registration")
    FEATURE_EMAIL_VERIFICATION: bool = Field(default=False, description="Enable email verification")
    FEATURE_RATE_LIMITING: bool = Field(default=True, description="Enable rate limiting")
    
    @validator("DATABASE_URL", pre=True)
    def validate_database_url(cls, v):
        """Validate database URL format."""
        if isinstance(v, str) and not v.startswith("postgresql"):
            raise ValueError("DATABASE_URL must be a PostgreSQL URL")
        return v
    
    @validator("SECRET_KEY", "JWT_SECRET_KEY")
    def validate_secret_keys(cls, v):
        """Validate that secret keys are not default values."""
        if v in ["your-super-secret-key-change-in-production", "jwt-secret-key-change-in-production"]:
            raise ValueError("Please change the default secret key in production")
        return v
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_allowed_origins(cls, v):
        """Parse ALLOWED_ORIGINS from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("ALLOWED_METHODS", pre=True)
    def parse_allowed_methods(cls, v):
        """Parse ALLOWED_METHODS from string or list."""
        if isinstance(v, str):
            return [method.strip().upper() for method in v.split(",")]
        return v
    
    @validator("ALLOWED_HEADERS", pre=True)
    def parse_allowed_headers(cls, v):
        """Parse ALLOWED_HEADERS from string or list."""
        if isinstance(v, str):
            return [header.strip() for header in v.split(",")]
        return v
    
    @validator("ALLOWED_HOSTS", pre=True)
    def parse_allowed_hosts(cls, v):
        """Parse ALLOWED_HOSTS from string or list."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get application settings.
    
    This function is useful for dependency injection in FastAPI.
    
    Returns:
        Settings: Application settings instance
    """
    return settings 