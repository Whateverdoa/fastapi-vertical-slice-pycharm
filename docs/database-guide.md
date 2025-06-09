# 🗄️ Database Guide

## 📖 Overview

This guide covers database setup, management, and best practices for the FastAPI Vertical Slice Architecture template. It focuses on PostgreSQL with SQLAlchemy 2.0, Alembic migrations, and PyCharm Professional database tools.

## 🐘 PostgreSQL Setup

### 1. **Docker Configuration**

#### Development Environment
```yaml
# docker-compose.services.yml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: fastapi_dev
      POSTGRES_USER: fastapi_user
      POSTGRES_PASSWORD: fastapi_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
```

#### Start Services
```bash
# Start PostgreSQL and Redis
make services-up

# Or using Docker Compose directly
docker-compose -f docker-compose.services.yml up -d
```

### 2. **Database Configuration**

#### Environment Variables
```bash
# .env
DATABASE_URL=postgresql+asyncpg://fastapi_user:fastapi_password@localhost:5432/fastapi_dev
DATABASE_ECHO=false
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
```

#### Connection Settings
```python
# src/shared/config.py
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = Field(..., description="PostgreSQL connection string")
    database_echo: bool = Field(False, description="Enable SQL query logging")
    database_pool_size: int = Field(10, description="Connection pool size")
    database_max_overflow: int = Field(20, description="Max overflow connections")
    
    @field_validator('database_url')
    def validate_database_url(cls, v):
        if not v.startswith('postgresql'):
            raise ValueError('DATABASE_URL must be PostgreSQL')
        return v
```

### 3. **Initial Database Setup**

#### SQL Initialization
```sql
-- scripts/init-db.sql
-- Create additional databases for testing
CREATE DATABASE fastapi_test;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE fastapi_dev TO fastapi_user;
GRANT ALL PRIVILEGES ON DATABASE fastapi_test TO fastapi_user;

-- Create extensions
\c fastapi_dev;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Sample data for development
INSERT INTO users (email, full_name, is_active) VALUES 
  ('admin@example.com', 'Admin User', true),
  ('user@example.com', 'Regular User', true);
```

## 🔗 SQLAlchemy 2.0 Integration

### 1. **Database Connection**

#### Async Engine Setup
```python
# src/shared/database.py
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import DeclarativeBase
from .config import get_settings

settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,   # Recycle connections every hour
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

# Dependency for FastAPI
async def get_session() -> AsyncSession:
    """Get database session for dependency injection."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### 2. **Model Definition**

#### Base Model Pattern
```python
# src/shared/models.py
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
```

#### Feature-Specific Models
```python
# src/users/models.py
from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column
from ..shared.database import Base
from ..shared.models import TimestampMixin

class User(Base, TimestampMixin):
    """User model with vertical slice architecture."""
    
    __tablename__ = "users"
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # User fields
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Optional fields
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    bio: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}')>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
```

## 🔄 Database Migrations with Alembic

### 1. **Migration Workflow**

#### Creating Migrations
```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add user table"

# Create empty migration for custom changes
alembic revision -m "Add custom indexes"

# Show current migration status
alembic current

# Show migration history
alembic history --verbose
```

#### Running Migrations
```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade +1

# Downgrade one migration
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade abc123
```

## 🛠️ PyCharm Database Tools

### 1. **Database Tool Window Setup**

#### Connection Configuration
1. **View → Tool Windows → Database**
2. **+ (Add) → Data Source → PostgreSQL**
3. **Configuration**:
   ```
   Host: localhost
   Port: 5432
   Database: fastapi_dev
   User: fastapi_user
   Password: fastapi_password
   ```
4. **Test Connection** to verify setup
5. **Apply** and **OK**

### 2. **Database Navigation**

#### Schema Browser Features
- **Tables**: View structure, columns, constraints
- **Views**: Browse and edit views
- **Functions**: Navigate stored procedures
- **Indexes**: Review index definitions
- **Sequences**: Manage auto-increment sequences

#### Quick Actions
- **Double-click table**: Open data viewer
- **Right-click → Scripts**: Generate SQL scripts
- **Ctrl+B**: Navigate to table definition
- **F4**: Edit table structure

### 3. **Query Console**

#### SQL Development
```sql
-- Query console features
-- 1. Syntax highlighting
-- 2. Code completion
-- 3. Error detection
-- 4. Results visualization

-- Example queries for development
SELECT u.*, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.is_active = true
GROUP BY u.id
ORDER BY u.created_at DESC;

-- Performance analysis
EXPLAIN ANALYZE 
SELECT * FROM users 
WHERE email ILIKE '%example%';
```

## 🧪 Testing with Databases

### 1. **Test Database Setup**

#### Test Configuration
```python
# tests/conftest.py
import asyncio
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.shared.database import Base

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://fastapi_user:fastapi_password@localhost:5432/fastapi_test"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

@pytest.fixture
async def test_session(test_engine):
    """Create test database session."""
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()
```

### 2. **Database Test Patterns**

#### Service Testing
```python
# tests/users/test_service.py
import pytest
from src.users.service import UserService
from src.users.schemas import UserCreateRequest

@pytest.mark.asyncio
async def test_create_user(test_session):
    """Test user creation."""
    service = UserService(test_session)
    request = UserCreateRequest(
        email="test@example.com",
        full_name="Test User",
        bio="Test bio"
    )
    
    user = await service.create_user(request)
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.is_active is True
```

## 🔧 Performance Optimization

### 1. **Query Optimization**

#### Index Strategies
```sql
-- Essential indexes for users table
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
CREATE INDEX CONCURRENTLY idx_users_active_created ON users(is_active, created_at DESC);
CREATE INDEX CONCURRENTLY idx_users_name_search ON users USING gin(to_tsvector('english', full_name));

-- Composite indexes for common queries
CREATE INDEX CONCURRENTLY idx_orders_user_status ON orders(user_id, status);
CREATE INDEX CONCURRENTLY idx_orders_created_amount ON orders(created_at DESC, total_amount);
```

#### Performance Monitoring
```python
# Performance monitoring in service
import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)

def log_query_time(func):
    """Decorator to log query execution time."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        execution_time = time.time() - start_time
        
        if execution_time > 0.1:  # Log slow queries
            logger.warning(
                f"Slow query in {func.__name__}: {execution_time:.3f}s"
            )
        
        return result
    return wrapper
```

### 2. **Connection Pooling**

#### Advanced Pool Configuration
```python
# src/shared/database.py
from sqlalchemy.pool import QueuePool

engine = create_async_engine(
    settings.database_url,
    # Connection pool settings
    poolclass=QueuePool,
    pool_size=20,           # Number of persistent connections
    max_overflow=30,        # Additional connections when needed
    pool_pre_ping=True,     # Validate connections before use
    pool_recycle=3600,      # Recycle connections every hour
    
    # Connection timeout settings
    connect_args={
        "command_timeout": 60,
        "server_settings": {
            "application_name": "fastapi-app",
            "timezone": "UTC",
        }
    }
)
```

## 📊 Monitoring and Maintenance

### 1. **Database Health Checks**

#### Health Monitoring
```python
# src/shared/health.py
from sqlalchemy import text
from .database import engine

async def check_database_health() -> dict:
    """Check database connectivity and performance."""
    try:
        async with engine.begin() as conn:
            # Test connection
            await conn.execute(text("SELECT 1"))
            
            # Check active connections
            result = await conn.execute(text("""
                SELECT count(*) as active_connections
                FROM pg_stat_activity
                WHERE state = 'active'
            """))
            active_connections = result.scalar()
            
            return {
                "status": "healthy",
                "active_connections": active_connections,
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
```

### 2. **Backup and Recovery**

#### Automated Backups
```bash
#!/bin/bash
# scripts/backup-database.sh

set -e

BACKUP_DIR="/backups"
DATABASE_URL="postgresql://fastapi_user:fastapi_password@localhost:5432/fastapi_dev"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/fastapi_backup_$TIMESTAMP.sql"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Create database backup
pg_dump "$DATABASE_URL" > "$BACKUP_FILE"

# Compress backup
gzip "$BACKUP_FILE"

# Keep only last 30 days of backups
find "$BACKUP_DIR" -name "fastapi_backup_*.sql.gz" -mtime +30 -delete

echo "Backup completed: ${BACKUP_FILE}.gz"
```

## 🚀 Production Considerations

### 1. **Security Best Practices**

#### Connection Security
```python
# Production database configuration
DATABASE_URL = "postgresql+asyncpg://user:password@db-host:5432/production_db?sslmode=require"

# Connection with SSL
engine = create_async_engine(
    DATABASE_URL,
    connect_args={
        "ssl": True,
        "server_settings": {
            "application_name": "fastapi-production",
        }
    }
)
```

#### Access Control
```sql
-- Create application-specific database user
CREATE USER fastapi_app WITH PASSWORD 'secure_password';

-- Grant minimal required permissions
GRANT CONNECT ON DATABASE production_db TO fastapi_app;
GRANT USAGE ON SCHEMA public TO fastapi_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO fastapi_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO fastapi_app;

-- Revoke unnecessary permissions
REVOKE CREATE ON SCHEMA public FROM fastapi_app;
```

### 2. **High Availability Setup**

#### Read Replicas
```python
# Multiple database connections
class DatabaseManager:
    def __init__(self):
        self.write_engine = create_async_engine(PRIMARY_DATABASE_URL)
        self.read_engine = create_async_engine(REPLICA_DATABASE_URL)
    
    async def get_write_session(self) -> AsyncSession:
        """Get session for write operations."""
        async with AsyncSessionLocal(bind=self.write_engine) as session:
            yield session
    
    async def get_read_session(self) -> AsyncSession:
        """Get session for read operations."""
        async with AsyncSessionLocal(bind=self.read_engine) as session:
            yield session
```

## 📚 Additional Resources

### 1. **Documentation Links**
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PyCharm Database Tools](https://www.jetbrains.com/help/pycharm/database-tool-window.html)

### 2. **Best Practices**
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [SQLAlchemy Best Practices](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Database Design Patterns](https://martinfowler.com/eaaCatalog/) 