#!/usr/bin/env python3
"""
Quick sanity check - run dashboard and report status
"""
import subprocess, sys, os, time

print("=" * 70)
print("🚀 SMART MONEY CONCEPTS DASHBOARD - FINAL SANITY CHECK")
print("=" * 70)

port = 8511
cmd = [sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py', f'--server.port={port}']

print(f"\n📋 Launch command:")
print(f"   {' '.join(cmd)}\n")

print("Starting dashboard...")
print(f"✓ Will be available at: http://localhost:{port}")
print(f"✓ Network access: http://$(hostname -I):{port}")

print("\n" + "=" * 70)
print("📊 Dashboard is starting...")
print("=" * 70)
print("\nPress Ctrl+C to stop\n")

try:
    subprocess.run(cmd, cwd=os.getcwd())
except KeyboardInterrupt:
    print("\n\n✓ Dashboard stopped.")
