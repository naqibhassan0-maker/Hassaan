#!/usr/bin/env python3
"""
Start Streamlit app and show what user would see
"""
import subprocess, sys, os, time, urllib.request

"""
Port and app settings
"""
port = 8508
app_file = 'test_signals_debug.py'

"""
Start Streamlit server
"""
print("🚀 Starting Streamlit server...")
cmd = [sys.executable, '-m', 'streamlit', 'run', app_file, f'--server.port={port}', '--server.headless=true']
proc = subprocess.Popen(cmd, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

print("⏳ Waiting for server to start...")
time.sleep(8)

"""
Fetch the page like a browser would
"""
try:
    url = f'http://127.0.0.1:{port}/'
    print(f"🌐 GET {url}")
    with urllib.request.urlopen(url, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='replace')
    
    print(f"\n✓ Response received ({len(html)} chars)")
    
    # Look for our debug messages
    for marker in ['[0.', 'App started', 'Title rendered', 'Navigation', 'Live Signals', 'Complete']:
        if marker in html:
            print(f"  ✓ Found: '{marker}'")
    
    # Check for warnings/errors
    if 'warning' in html.lower():
        print("  ⚠️  Found warning in output")
    if 'error' in html.lower():
        print("  ❌ Found error in output")
        
except Exception as e:
    print(f"✗ Failed to fetch: {type(e).__name__}: {e}")
finally:
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except:
        proc.kill()
    print("\n✓ Server stopped")
