"""
Quick start script to run the AI Race Engineer Copilot dashboard.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.ai.watsonx_config import get_watsonx_config, load_environment, mask_secret


def check_environment() -> bool:
    """Check if the watsonx environment is properly configured."""
    load_environment()
    config = get_watsonx_config()

    required_vars = {
        "IBM_WATSONX_APIKEY": bool(config.api_key),
        "IBM_WATSONX_PROJECT_ID": bool(config.project_id),
        "IBM_WATSONX_URL": bool(config.url),
    }
    missing_vars = [name for name, exists in required_vars.items() if not exists]

    if missing_vars:
        print("Warning: Missing environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nThe dashboard will run in mock mode until these are fixed.\n")
    else:
        print("Environment configured correctly")

    print("API KEY EXISTS:", bool(config.api_key))
    print("PROJECT ID EXISTS:", bool(config.project_id))
    print("URL:", config.url)
    print("API KEY MASKED:", mask_secret(config.api_key))
    print("PROJECT ID MASKED:", mask_secret(config.project_id))

    return not missing_vars


def main():
    """Main entry point."""
    print("=" * 60)
    print("AI RACE ENGINEER COPILOT")
    print("=" * 60)
    print()

    check_environment()

    print("\nStarting React dashboard...")
    print("Dashboard will open in your browser at http://localhost:5173")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    print()

    frontend_path = PROJECT_ROOT / "frontend"

    try:
        subprocess.run(
            [
                "npm",
                "run",
                "dev",
                "--",
                "--host",
                "0.0.0.0",
                "--port",
                "5173",
            ],
            cwd=frontend_path,
        )
    except KeyboardInterrupt:
        print("\n\nShutting down dashboard...")
        print("Goodbye!")


if __name__ == "__main__":
    main()
