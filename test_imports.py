#!/usr/bin/env python3
"""
Diagnostic script to test if all required packages are installed and importable.
"""

import sys
import os

print("=" * 70)
print("PYTHON ENVIRONMENT DIAGNOSTIC")
print("=" * 70)
print(f"\nPython Executable: {sys.executable}")
print(f"Python Version: {sys.version}")
print(f"Python Path:")
for path in sys.path:
    print(f"  - {path}")

print(f"\nCurrent Directory: {os.getcwd()}")
print(f"Working Directory: {os.path.abspath('.')}")

print("\n" + "=" * 70)
print("TESTING IMPORTS")
print("=" * 70)

packages = [
    ("streamlit", "st"),
    ("yfinance", "yf"),
    ("pandas", "pd"),
    ("datetime", "datetime"),
]

failed_imports = []

for package_name, alias in packages:
    try:
        if package_name == "datetime":
            from datetime import datetime, timedelta
            print(f"✅ {package_name}: Successfully imported")
        else:
            __import__(package_name)
            print(f"✅ {package_name}: Successfully imported")
    except ImportError as e:
        print(f"❌ {package_name}: FAILED - {e}")
        failed_imports.append((package_name, str(e)))

print("\n" + "=" * 70)
if failed_imports:
    print(f"⚠️  {len(failed_imports)} IMPORT(S) FAILED:")
    for pkg, err in failed_imports:
        print(f"   - {pkg}: {err}")
    print("\n🔧 SUGGESTED FIXES:")
    print("   Run: pip install --upgrade streamlit yfinance pandas")
    sys.exit(1)
else:
    print("✅ ALL IMPORTS SUCCESSFUL!")
    print("\n✨ The Streamlit app should run without import errors.")
    sys.exit(0)

print("=" * 70)
