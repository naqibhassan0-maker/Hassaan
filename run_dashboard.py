#!/usr/bin/env python3
"""
Smart Money Concepts Dashboard - Direct Launcher
Installs dependencies and starts Streamlit directly.
"""

import socket
import subprocess
import sys
import os

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
    port = find_free_port(8501, 8510)
    print("="*70)
    print("🎯 Starting Streamlit Dashboard...")
    print("="*70)
    print(f"\n📊 Dashboard URL: http://localhost:{port}")
    print(f"🌐 Network URL: http://[IP]:{port}")
    print("\n✨ Press Ctrl+C to stop the dashboard\n")
    
    # Launch streamlit
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "streamlit_app.py",
            f"--server.port={port}",
            "--logger.level=error",
        ],
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
