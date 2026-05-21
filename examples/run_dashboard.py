"""
Quick start script to run the AI Race Engineer Copilot dashboard
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_environment():
    """Check if environment is properly configured"""
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    required_vars = [
        'IBM_WATSONX_API_KEY',
        'IBM_WATSONX_PROJECT_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  Warning: Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nThe dashboard will run in demo mode.")
        print("To enable full IBM Granite functionality, set these variables in your .env file.\n")
    else:
        print("✓ Environment configured correctly")
    
    return len(missing_vars) == 0

def main():
    """Main entry point"""
    print("=" * 60)
    print("🏎️  AI RACE ENGINEER COPILOT")
    print("=" * 60)
    print()
    
    # Check environment
    env_ok = check_environment()
    
    print("\nStarting Streamlit dashboard...")
    print("Dashboard will open in your browser at http://localhost:8501")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Run Streamlit
    import subprocess
    
    app_path = project_root / "frontend" / "app.py"
    
    try:
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path),
            "--server.headless",
            "false"
        ])
    except KeyboardInterrupt:
        print("\n\nShutting down dashboard...")
        print("Goodbye! 🏁")

if __name__ == "__main__":
    main()

# Made with Bob
