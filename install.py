"""
Installer script for Transcript CLI.
Automatically updates transcript.cmd with the correct paths based on installation location.
"""

import os
import sys
from pathlib import Path


def main():
    # Get the directory where this script is located (installation directory)
    install_dir = Path(__file__).parent.resolve()
    
    # Paths
    venv_python = install_dir / "venv" / "Scripts" / "python.exe"
    transcript_py = install_dir / "transcript.py"
    transcript_cmd = install_dir / "transcript_bin" / "transcript.cmd"
    
    # Verify required files exist
    if not transcript_py.exists():
        print(f"Error: transcript.py not found at {transcript_py}")
        sys.exit(1)
    
    if not transcript_cmd.parent.exists():
        print(f"Error: transcript_bin folder not found at {transcript_cmd.parent}")
        sys.exit(1)
    
    # Generate the new transcript.cmd content
    cmd_content = f'''@echo off
"{venv_python}" "{transcript_py}" %*
'''
    
    # Write the updated transcript.cmd
    transcript_cmd.write_text(cmd_content, encoding="utf-8")
    
    print(f"Successfully updated: {transcript_cmd}")
    print(f"  Python: {venv_python}")
    print(f"  Script: {transcript_py}")
    print()
    print("Next steps:")
    print(f"  1. Create venv: python -m venv venv")
    print(f"  2. Install deps: venv\\Scripts\\pip install requests python-dotenv pydub")
    print(f"  3. Add to PATH: {transcript_cmd.parent}")
    print(f"  4. Configure .env with your SONIOX_API_KEY")


if __name__ == "__main__":
    main()
