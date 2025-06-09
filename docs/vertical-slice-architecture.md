# 🏗️ Vertical Slice Architecture Guide

## 📖 Overview

Vertical Slice Architecture is a software architecture pattern that organizes code around **features** rather than technical layers. Instead of having separate folders for controllers, services, and repositories, each feature contains all the code needed to implement that functionality.

## 🎯 Core Principles

### 1. **Feature-Based Organization**
```
src/
├── users/           # User management feature
│   ├── api.py       # HTTP endpoints
│   ├── schemas.py   # Request/response models
│   ├── service.py   # Business logic
│   └── models.py    # Database models
├── auth/            # Authentication feature
│   ├── api.py
│   ├── schemas.py
│   └── service.py
└── shared/          # Cross-cutting concerns
    ├── database.py
    ├── config.py
    └── middleware.py
```

### 2. **Minimal Coupling Between Slices**
- Each feature slice is **independent**
- Communication happens through **well-defined interfaces**
- Shared code lives in the `shared/` directory

### 3. **Cohesive Feature Implementation**
- All code for a feature is **co-located**
- Easy to find and modify feature-specific logic
- Clear ownership and responsibility boundaries

## 🔄 Traditional Layered vs Vertical Slice

### ❌ Traditional Layered Architecture
```
src/
├── controllers/     # All HTTP handlers
│   ├── user_controller.py
│   └── auth_controller.py
├── services/        # All business logic
│   ├── user_service.py
│   └── auth_service.py
├── repositories/    # All data access
│   ├── user_repository.py
│   └── auth_repository.py
└── models/          # All database models
    ├── user.py
    └── auth.py
```

**Problems:**
- 🔄 Feature changes require touching multiple layers
- 🔍 Hard to locate all code for a specific feature
- 🧩 High coupling between layers
- 📈 Difficult to scale team development

### ✅ Vertical Slice Architecture
```
src/
├── users/           # Complete user feature
│   ├── api.py       # User HTTP endpoints
│   ├── schemas.py   # User request/response models
│   ├── service.py   # User business logic
│   └── models.py    # User database models
├── auth/            # Complete auth feature
│   ├── api.py       # Auth HTTP endpoints
│   ├── schemas.py   # Auth request/response models
│   └── service.py   # Auth business logic
└── shared/          # Shared utilities
```

**Benefits:**
- 🎯 Feature changes are localized to one directory
- 🔍 Easy to find all related code
- 🧩 Low coupling between features
- 📈 Teams can work on different features independently

## 🏛️ Implementation Patterns

### 1. **Feature Module Structure**

Each feature follows a consistent structure:

```python
# users/api.py - HTTP layer
from fastapi import APIRouter, Depends
from .schemas import UserCreateRequest, UserResponse
from .service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(
    request: UserCreateRequest,
    service: UserService = Depends()
):
    return await service.create_user(request)
```

```python
# users/schemas.py - Data contracts
from pydantic import BaseModel, EmailStr

class UserCreateRequest(BaseModel):
    email: EmailStr
    full_name: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    
    class Config:
        from_attributes = True
```

```python
# users/service.py - Business logic
from .schemas import UserCreateRequest, UserResponse
from .models import User
from ..shared.database import get_session

class UserService:
    async def create_user(self, request: UserCreateRequest) -> UserResponse:
        # Business logic here
        user = User(email=request.email, full_name=request.full_name)
        # Save to database
        return UserResponse.model_validate(user)
```

### 2. **Cross-Feature Communication**

When features need to communicate:

```python
# orders/service.py
from ..users.service import UserService
from ..shared.events import EventBus

class OrderService:
    def __init__(self, user_service: UserService, event_bus: EventBus):
        self.user_service = user_service
        self.event_bus = event_bus
    
    async def create_order(self, user_id: int, items: list):
        # Validate user exists
        user = await self.user_service.get_user(user_id)
        
        # Create order
        order = Order(user_id=user_id, items=items)
        
        # Publish event for other features
        await self.event_bus.publish("order_created", order.dict())
        
        return order
```

### 3. **Shared Components**

Common functionality lives in `shared/`:

```python
# shared/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
```

## 🛠️ PyCharm Integration

### 1. **Feature-Based Navigation**

PyCharm's project structure aligns perfectly with vertical slices:

- **Project tool window** shows features as top-level folders
- **Navigate to file** (Cmd+Shift+O) quickly finds feature files
- **Find in path** (Cmd+Shift+F) can be scoped to specific features

### 2. **Run Configurations**

Create feature-specific run configurations:

```xml
<!-- .idea/runConfigurations/Test_Users_Feature.xml -->
<configuration name="Test Users Feature" type="PythonConfigurationType">
  <module name="fastapi-vertical-slice-pycharm" />
  <option name="SCRIPT_NAME" value="$PROJECT_DIR$/tests/users" />
  <option name="PARAMETERS" value="-v" />
  <option name="SHOW_COMMAND_LINE" value="false" />
  <option name="EMULATE_TERMINAL" value="false" />
  <option name="MODULE_MODE" value="true" />
  <option name="REDIRECT_INPUT" value="false" />
  <option name="INPUT_FILE" value="" />
  <method v="2" />
</configuration>
```

### 3. **Code Generation Templates**

Create PyCharm file templates for new features:

```python
# File Template: Feature API
from fastapi import APIRouter, Depends
from .schemas import ${FEATURE_NAME}CreateRequest, ${FEATURE_NAME}Response
from .service import ${FEATURE_NAME}Service

router = APIRouter(prefix="/${FEATURE_NAME_LOWER}", tags=["${FEATURE_NAME_LOWER}"])

@router.post("/", response_model=${FEATURE_NAME}Response)
async def create_${FEATURE_NAME_LOWER}(
    request: ${FEATURE_NAME}CreateRequest,
    service: ${FEATURE_NAME}Service = Depends()
):
    return await service.create_${FEATURE_NAME_LOWER}(request)
```

## 📊 Benefits and Trade-offs

### ✅ Benefits

1. **Developer Productivity**
   - Faster feature development
   - Easier onboarding for new team members
   - Clearer code ownership

2. **Maintainability**
   - Localized changes reduce regression risk
   - Easier to refactor individual features
   - Better code organization

3. **Team Scalability**
   - Multiple teams can work on different features
   - Reduced merge conflicts
   - Clear feature boundaries

4. **Testing**
   - Feature-specific test suites
   - Easier to achieve high test coverage
   - Faster test execution for specific features

### ⚠️ Trade-offs

1. **Code Duplication**
   - Some code might be duplicated across features
   - Need to be careful about shared logic

2. **Cross-Feature Dependencies**
   - Can become complex if not managed properly
   - Requires good interface design

3. **Learning Curve**
   - Different from traditional layered architecture
   - Team needs to understand the patterns

## 🎯 Best Practices

### 1. **Keep Features Independent**
```python
# ❌ Don't do this - direct dependency
from ..orders.models import Order

class UserService:
    def get_user_orders(self, user_id: int):
        return Order.query.filter_by(user_id=user_id).all()

# ✅ Do this - use interfaces
from ..shared.interfaces import OrderServiceInterface

class UserService:
    def __init__(self, order_service: OrderServiceInterface):
        self.order_service = order_service
    
    async def get_user_orders(self, user_id: int):
        return await self.order_service.get_orders_by_user(user_id)
```

### 2. **Use Dependency Injection**
```python
# shared/dependencies.py
from fastapi import Depends
from .database import get_session

def get_user_service(session = Depends(get_session)):
    return UserService(session)

# users/api.py
@router.get("/{user_id}")
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return await service.get_user(user_id)
```

### 3. **Define Clear Interfaces**
```python
# shared/interfaces.py
from abc import ABC, abstractmethod
from typing import List

class NotificationServiceInterface(ABC):
    @abstractmethod
    async def send_email(self, to: str, subject: str, body: str) -> bool:
        pass

# notifications/service.py
class EmailNotificationService(NotificationServiceInterface):
    async def send_email(self, to: str, subject: str, body: str) -> bool:
        # Implementation here
        pass
```

### 4. **Organize Shared Code Properly**
```
shared/
├── interfaces/      # Abstract interfaces
├── exceptions/      # Custom exceptions
├── middleware/      # HTTP middleware
├── events/          # Event system
├── utils/           # Utility functions
└── database.py      # Database connection
```

## 🔄 Migration from Layered Architecture

### Step 1: Identify Features
List all the features in your application:
- User management
- Authentication
- Product catalog
- Order processing
- Payment handling

### Step 2: Create Feature Directories
```bash
mkdir -p src/{users,auth,products,orders,payments}
```

### Step 3: Move Code by Feature
Move related files from different layers into feature directories:

```bash
# Move user-related code
mv src/controllers/user_controller.py src/users/api.py
mv src/services/user_service.py src/users/service.py
mv src/models/user.py src/users/models.py
```

### Step 4: Update Imports
Update import statements to reflect new structure:

```python
# Before
from services.user_service import UserService

# After
from ..users.service import UserService
```

### Step 5: Refactor Dependencies
Remove tight coupling between layers and introduce proper dependency injection.

## 📚 Further Reading

- [Vertical Slice Architecture by Jimmy Bogard](https://jimmybogard.com/vertical-slice-architecture/)
- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Feature Slices for ASP.NET Core MVC](https://docs.microsoft.com/en-us/aspnet/core/mvc/controllers/areas)

## 🤝 Contributing

When adding new features to this template:

1. Follow the established feature structure
2. Add appropriate tests in `tests/{feature_name}/`
3. Update this documentation if you introduce new patterns
4. Ensure features remain independent and loosely coupled 