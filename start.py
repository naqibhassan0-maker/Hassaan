#!/usr/bin/env python3
"""
Smart Money Concepts Dashboard - Python Startup Handler
Ensures all dependencies are installed before launching the app.
"""

import socket
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

def find_free_port(start=8501, end=8510):
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(('localhost', port))
                return port
            except OSError:
                continue
    raise RuntimeError('No free port available between 8501 and 8510')


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
    port = find_free_port(8501, 8510)
    print("\n" + "=" * 70)
    print("✨ All checks passed! Starting dashboard...")
    print(f"📊 Access at: http://localhost:{port}")
    print("=" * 70 + "\n")
    
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "streamlit_app.py",
        f"--server.port={port}",
        "--server.address=0.0.0.0",
        "--server.enableCORS=false",
        "--server.headless=true",
    ])

if __name__ == "__main__":
    main()
