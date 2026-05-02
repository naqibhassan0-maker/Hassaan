#!/usr/bin/env python3
"""
Show the actual error from the Streamlit app
"""
import subprocess, sys, os, time, urllib.request

port = 8509
cmd = [sys.executable, '-m', 'streamlit', 'run', 'test_signals_debug.py', f'--server.port={port}', '--server.headless=true']
proc = subprocess.Popen(cmd, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
time.sleep(10)

try:
    url = f'http://127.0.0.1:{port}/'  
    with urllib.request.urlopen(url, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='replace')
    
    # Extract error info
    import json
    import re
    
    # Look for error fields in JSON
    json_matches = re.findall(r'"typeValue":"(\w+)"[^}]*?"value":"([^"]+)"', html)
    for type_val, msg in json_matches[:5]:
        print(f"{type_val}: {msg}")
        
    # Look for plaintext error
    error_matches = re.findall(r'error["\']?\s*:\s*["\']?([^"\'}\n]+)', html, re.I)
    for err in error_matches[:5]:
        print(f"Error: {err[:100]}")
    
    # Look for exception
    exc_matches = re.findall(r'Exception["\']?\s*:\s*["\']?([^"\'}\n]+)', html)
    for exc in exc_matches[:3]:
        print(f"Exception: {exc[:100]}")
        
except Exception as e:
    print(f"Error: {e}")
finally:
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except:
        proc.kill()
