#!/usr/bin/env python3
"""
Simple launcher for the Smart Money Concepts Dashboard
"""
import subprocess
import sys

print("🚀 Starting Smart Money Concepts Dashboard...")
print("📊 URL: http://localhost:8501")
print("Press Ctrl+C to stop")

try:
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0"
    ])
except KeyboardInterrupt:
    print("\n👋 Dashboard stopped.")