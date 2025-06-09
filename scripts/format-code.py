#!/usr/bin/env python3
"""
Code Formatting Script

Runs Black and isort to format the codebase.
This script is used by the PyCharm "Code Format" run configuration.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr:
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False


def main():
    """Main formatting function."""
    print("🎨 Code Formatting")
    print("==================")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Run this script from the project root directory")
        sys.exit(1)
    
    # List of formatting commands
    commands = [
        ("isort src tests", "Sorting imports with isort"),
        ("black src tests", "Formatting code with Black"),
    ]
    
    success = True
    for cmd, description in commands:
        if not run_command(cmd, description):
            success = False
    
    if success:
        print("\n🎉 Code formatting completed successfully!")
    else:
        print("\n❌ Code formatting completed with errors")
        sys.exit(1)


if __name__ == "__main__":
    main() 