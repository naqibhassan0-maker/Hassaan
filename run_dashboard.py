#!/usr/bin/env python3
"""
Smart Money Concepts Dashboard - Direct Launcher
Installs dependencies and starts Streamlit directly.
"""

import subprocess
import sys
import os

def main():
    os.chdir('/workspaces/Hassaan')
    
    print("\n" + "="*70)
    print("🚀 Smart Money Concepts Dashboard Launcher")
    print("="*70 + "\n")
    
    # Step 1: Install dependencies
    print("📦 Installing dependencies...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Dependencies installed successfully!\n")
    else:
        print("⚠️  Installation completed with warnings\n")
    
    # Step 2: Launch Streamlit
    print("="*70)
    print("🎯 Starting Streamlit Dashboard...")
    print("="*70)
    print("\n📊 Dashboard URL: http://localhost:8501")
    print("🌐 Network URL: http://[IP]:8501")
    print("\n✨ Press Ctrl+C to stop the dashboard\n")
    
    # Launch streamlit
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--logger.level=error"],
        cwd="/workspaces/Hassaan"
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
