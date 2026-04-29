#!/usr/bin/env python3
"""
Smart Money Concepts Dashboard - Python Startup Handler
Ensures all dependencies are installed before launching the app.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command and handle errors."""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False

def main():
    print("\n" + "=" * 70)
    print("🚀 Smart Money Concepts Dashboard - Startup")
    print("=" * 70 + "\n")
    
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Step 1: Upgrade pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip --quiet", 
                       "Upgrading pip"):
        print("⚠️  Warning: pip upgrade had issues, but continuing...")
    
    # Step 2: Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt --quiet",
                       "Installing dependencies"):
        print("❌ Failed to install dependencies!")
        sys.exit(1)
    
    # Step 3: Verify imports
    print("\n📦 Verifying imports...")
    if subprocess.run([sys.executable, "test_imports.py"]).returncode != 0:
        print("❌ Import verification failed!")
        sys.exit(1)
    
    # Step 4: Launch Streamlit
    print("\n" + "=" * 70)
    print("✨ All checks passed! Starting dashboard...")
    print("📊 Access at: http://localhost:8501")
    print("=" * 70 + "\n")
    
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])

if __name__ == "__main__":
    main()
