#!/usr/bin/env python3
"""
Script to run the conference agent Streamlit application.

This script checks the environment and launches the Streamlit UI.
"""

import os
import subprocess
import sys
from pathlib import Path


def check_environment() -> bool:
    """
    Check if the environment is properly configured.
    
    Returns:
        True if environment is ready, False otherwise
    """
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Warning: .env file not found")
        print("   Creating from .env.example...")
        
        example_file = Path(".env.example")
        if example_file.exists():
            import shutil
            shutil.copy(example_file, env_file)
            print("Created .env file")
            print("   Please edit .env with your configuration")
        else:
            print("✗ Error: .env.example not found")
            return False
    
    return True


def main() -> None:
    """
    Main entry point.
    """
    print("🤖 Grosse Conférence 2026 - Agent IA")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Get project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Add src to Python path
    src_path = project_root / "src"
    sys.path.insert(0, str(src_path))
    
    print("\nEnvironment ready")
    print("\n🚀 Launching Streamlit application...")
    print("   URL: http://localhost:8501\n")
    
    # Run Streamlit
    streamlit_app = src_path / "conference_agent" / "ui" / "app.py"
    
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(streamlit_app)],
            check=True,
        )
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error running Streamlit: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
