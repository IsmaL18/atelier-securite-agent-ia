#!/usr/bin/env python3
"""
Script to run the conference agent Streamlit application.

This script checks the environment and launches the Streamlit UI.
"""

import os
import subprocess
import sys
from pathlib import Path


def main() -> None:
    """
    Main entry point.
    """
    print("Grosse Conf 2026 - Agent IA")
    print("=" * 50)
    
    # Get project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Add src to Python path
    src_path = project_root / "src"
    sys.path.insert(0, str(src_path))
    
    print("\nLaunching Streamlit application...")
    
    # Run Streamlit
    streamlit_app = src_path / "conference_agent" / "ui" / "app.py"
    
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(streamlit_app)],
            check=True,
        )
    except KeyboardInterrupt:
        print("\n\ncApplication stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error running Streamlit: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
