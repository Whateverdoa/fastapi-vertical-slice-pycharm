#!/usr/bin/env python3
"""
PyCharm Environment Setup Script

This script sets up the development environment for PyCharm users.
It handles environment files, dependencies, and initial configuration.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, cwd: Path = None) -> bool:
    """Run a shell command and return success status."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"❌ Command failed: {cmd}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Error running command '{cmd}': {e}")
        return False


def check_requirements() -> bool:
    """Check if required tools are installed."""
    print("🔍 Checking requirements...")
    
    requirements = {
        "python": "python --version",
        "docker": "docker --version",
        "docker-compose": "docker-compose --version",
        "uv": "uv --version",
    }
    
    missing = []
    for tool, cmd in requirements.items():
        if not run_command(cmd):
            missing.append(tool)
    
    if missing:
        print(f"❌ Missing required tools: {', '.join(missing)}")
        print("\nPlease install:")
        if "uv" in missing:
            print("  uv: curl -LsSf https://astral.sh/uv/install.sh | sh")
        if "docker" in missing:
            print("  Docker: https://docs.docker.com/get-docker/")
        return False
    
    print("✅ All requirements satisfied")
    return True


def setup_environment():
    """Set up environment file."""
    print("📄 Setting up environment file...")
    
    env_example = Path("env.pycharm.example")
    env_file = Path(".env")
    
    if not env_example.exists():
        print(f"❌ {env_example} not found")
        return False
    
    if env_file.exists():
        print(f"⚠️  .env already exists, backing up to .env.backup")
        shutil.copy(env_file, ".env.backup")
    
    shutil.copy(env_example, env_file)
    print(f"✅ Created .env from {env_example}")
    return True


def install_dependencies():
    """Install Python dependencies."""
    print("📦 Installing dependencies...")
    
    # Install main dependencies
    if not run_command("uv pip install -e ."):
        return False
    
    # Install development dependencies
    if not run_command('uv pip install -e ".[dev]"'):
        return False
    
    print("✅ Dependencies installed")
    return True


def setup_pre_commit():
    """Set up pre-commit hooks."""
    print("🪝 Setting up pre-commit hooks...")
    
    if not run_command("pre-commit install"):
        print("⚠️  Failed to install pre-commit hooks (optional)")
        return True
    
    print("✅ Pre-commit hooks installed")
    return True


def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    
    directories = [
        "logs",
        "uploads",
        "alembic/versions",
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")
    return True


def setup_database_connection():
    """Set up PyCharm database connection instructions."""
    print("🗄️  Database connection setup...")
    
    print("""
📋 To connect PyCharm to the database:

1. Start services: make services-up
2. Open PyCharm Database tool (View → Tool Windows → Database)
3. Click + → Data Source → PostgreSQL
4. Configure connection:
   - Host: localhost
   - Port: 5432
   - Database: fastapi_app
   - User: postgres
   - Password: postgres
5. Test connection and apply

The database will be available at:
postgresql://postgres:postgres@localhost:5432/fastapi_app
    """)
    return True


def main():
    """Main setup function."""
    print("🚀 FastAPI Vertical Slice - PyCharm Setup")
    print("=========================================")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Run this script from the project root directory")
        sys.exit(1)
    
    steps = [
        ("Checking requirements", check_requirements),
        ("Setting up environment", setup_environment),
        ("Installing dependencies", install_dependencies),
        ("Setting up pre-commit", setup_pre_commit),
        ("Creating directories", create_directories),
        ("Database connection info", setup_database_connection),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"❌ Setup failed at: {step_name}")
            sys.exit(1)
    
    print("\n🎉 PyCharm setup complete!")
    print("\nNext steps:")
    print("1. Start services: make services-up")
    print("2. Open project in PyCharm")
    print("3. Use 'FastAPI Dev Server' run configuration")
    print("4. Set up database connection in PyCharm")
    print("\nHappy coding! 🐍✨")


if __name__ == "__main__":
    main() 