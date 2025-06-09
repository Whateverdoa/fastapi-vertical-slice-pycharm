# 🚀 FastAPI Vertical Slice Architecture - PyCharm Edition

A production-ready FastAPI template optimized for **PyCharm Professional** workflows, featuring vertical slice architecture and hybrid development approach.

## 🎯 PyCharm-Optimized Approach

This template is specifically designed for PyCharm users who prefer:
- **Local development** with intelligent code completion
- **Services in Docker** (database, Redis, etc.)
- **Native debugging** without container complexity
- **Integrated database tools**
- **One-click run configurations**

## 🏗️ Architecture

```
🏢 Vertical Slice Structure
├── 📦 users/           # Complete user feature
│   ├── api.py         # FastAPI routes
│   ├── service.py     # Business logic
│   ├── models.py      # Database models
│   ├── schemas.py     # Pydantic schemas
│   └── tests/         # Feature tests
├── 📦 auth/           # Authentication feature
└── 📦 shared/         # Cross-cutting concerns
```

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone <repository-url>
cd fastapi-vertical-slice-pycharm
```

### 2. Environment Setup
```bash
# Copy PyCharm environment template
cp .env.pycharm.example .env

# Run PyCharm setup script
python scripts/setup-pycharm.py
```

### 3. Start Services
```bash
# Start only Docker services (DB, Redis, etc.)
make services-up

# Or use PyCharm run configuration: "Start Services"
```

### 4. Run Application
- **Option A**: Use PyCharm run configuration `FastAPI Dev Server`
- **Option B**: Command line: `make dev-local`

### 5. Open PyCharm
The project includes pre-configured:
- ✅ Database connections
- ✅ Run/Debug configurations
- ✅ Code style settings
- ✅ File watchers
- ✅ Docker integration

## 🔧 PyCharm Features

### Database Integration
- **Built-in database browser** with schema visualization
- **Query console** for SQL development
- **Visual relationship diagrams**
- **Migration tools integration**

### Debugging
- **Native Python debugging** (no Docker complexity)
- **Breakpoints in business logic**
- **Variable inspection**
- **Call stack analysis**

### Code Quality
- **Real-time code analysis**
- **Automatic formatting** on save
- **Import optimization**
- **Type checking integration**

### Run Configurations
| Configuration | Purpose |
|---------------|---------|
| `FastAPI Dev Server` | Start application locally |
| `Run Tests` | Execute test suite |
| `Start Services` | Launch Docker services |
| `Database Migration` | Apply/create migrations |
| `Code Format` | Format entire codebase |

## 🐳 Docker Strategy

### Hybrid Approach
- **Services in containers**: PostgreSQL, Redis, Elasticsearch
- **Application runs locally**: Better debugging and IDE integration

```yaml
# docker-compose.services.yml - Only external services
services:
  postgres:
    image: postgres:15
    ports: ["5432:5432"]
  
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
```

### Full Containerization Option
```bash
# If you prefer everything in Docker
make docker-full
```

## 📂 Project Structure

```
fastapi-vertical-slice-pycharm/
├── .idea/                          # PyCharm configuration
│   ├── runConfigurations/          # One-click run setups
│   ├── dataSources.xml             # Database connections
│   ├── codeStyles/                 # Code formatting rules
│   └── inspectionProfiles/         # Code quality rules
├── src/
│   ├── users/                      # User management slice
│   ├── auth/                       # Authentication slice
│   ├── shared/                     # Shared utilities
│   └── main.py                     # FastAPI application
├── tests/                          # Test suite
├── scripts/                        # Development scripts
├── docker-compose.services.yml     # Services only
├── docker-compose.full.yml         # Full containerization
├── pyproject.toml                  # uv configuration
└── requirements-local.txt          # Local development deps
```

## 🔄 Development Workflow

### Daily Development
1. **Start PyCharm** → Project opens with all configurations
2. **Run "Start Services"** → Docker services start
3. **Run "FastAPI Dev Server"** → Application starts locally
4. **Code & Debug** → Full PyCharm integration
5. **Run Tests** → One-click testing

### Database Work
1. **Open Database tab** → Pre-configured connections
2. **Browse schema** → Visual table relationships
3. **Write queries** → Built-in console
4. **Run migrations** → Integrated tools

### Code Quality
- **Format on save** → Automatic Black formatting
- **Import sorting** → isort integration
- **Type checking** → mypy integration
- **Linting** → flake8 integration

## 🧪 Testing

### PyCharm Integration
```python
# Test with PyCharm's test runner
pytest tests/                    # All tests
pytest tests/users/             # Feature tests
pytest tests/integration/       # Integration tests
```

### Coverage
```bash
make test-coverage              # Generate coverage report
```

## 📊 Database Development

### Migrations
```bash
make migration msg="Add user table"    # Create migration
make migrate                          # Apply migrations
make migration-rollback               # Rollback last migration
```

### PyCharm Database Tools
- **Schema comparison**
- **Data export/import**
- **Query history**
- **Table editor**

## 🚀 Deployment

### Local Testing
```bash
make docker-full                # Test full containerization
```

### Production
```bash
make build-prod                 # Build production image
make deploy                     # Deploy to staging/production
```

## 🔧 Configuration

### Environment Variables
```bash
# .env.pycharm.example
DATABASE_URL=postgresql://user:pass@localhost:5432/myapp
REDIS_URL=redis://localhost:6379
DEBUG=true
LOG_LEVEL=debug
```

### PyCharm Settings
All PyCharm configurations are version-controlled:
- Code style (Black, 88 chars)
- Inspections (type hints, unused imports)
- File watchers (auto-format)
- Run configurations

## 🆚 vs VS Code Template

| Feature | PyCharm Template | VS Code Template |
|---------|------------------|------------------|
| **Development** | Local + Docker services | Full containerization |
| **Debugging** | Native PyCharm debugger | Docker debugging |
| **Database** | Built-in tools | External tools |
| **Code Intelligence** | Advanced PyCharm features | Extensions |
| **Setup Complexity** | Medium (service dependencies) | Low (everything containerized) |

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Follow code style**: Use PyCharm's formatting
4. **Add tests**: Maintain coverage
5. **Submit PR**: Include description

## 📚 Documentation

- [**Vertical Slice Architecture**](docs/architecture.md)
- [**PyCharm Workflow**](docs/pycharm-workflow.md)
- [**Database Guide**](docs/database.md)
- [**Deployment Guide**](docs/deployment.md)

## 🏷️ License

MIT License - see [LICENSE](LICENSE) file.

---

**Happy coding with PyCharm! 🐍✨** 