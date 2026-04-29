# Troubleshooting Guide

## Issue: "ModuleNotFoundError: No module named 'yfinance'"

### Causes
1. Dependencies not installed
2. Wrong Python interpreter being used
3. Virtual environment issues
4. Conflicting package versions

### Solutions

#### Solution 1: Use the Startup Script (Easiest)
```bash
python3 start.py
```
This handles all dependency installation automatically.

#### Solution 2: Manual Installation
```bash
# Upgrade pip first
python3 -m pip install --upgrade pip

# Install all dependencies
python3 -m pip install -r requirements.txt

# Verify it works
python3 test_imports.py

# Run the app
streamlit run streamlit_app.py
```

#### Solution 3: Force Reinstall
```bash
# Remove existing packages (optional)
pip uninstall streamlit yfinance pandas -y

# Reinstall fresh
pip install streamlit>=1.28.0 yfinance>=0.2.32 pandas>=2.0.0

# Test
python3 test_imports.py
```

#### Solution 4: Virtual Environment (Isolated)
```bash
# Create a clean virtual environment
python3 -m venv dashboard_env

# Activate it
# On Linux/Mac:
source dashboard_env/bin/activate
# On Windows:
dashboard_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run streamlit_app.py
```

#### Solution 5: Using Alternative Package Manager
```bash
# If pip has issues, try:
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt --no-cache-dir
```

---

## Issue: "Streamlit not found" or similar

This usually means Streamlit is not installed or not in PATH.

```bash
# Verify Streamlit installation
python3 -c "import streamlit; print(streamlit.__version__)"

# If that fails, reinstall:
pip install --upgrade streamlit

# Run using module syntax (more reliable):
python3 -m streamlit run streamlit_app.py
```

---

## Issue: "yfinance" works but signals not showing

1. Check internet connection (yfinance needs to download data from Yahoo Finance)
2. Yahoo Finance might be blocking requests temporarily
3. Try refreshing the page or restarting the app

```bash
# Test yfinance directly
python3 -c "import yfinance as yf; data = yf.download('BTC-USD', period='1d'); print(data)"
```

---

## Diagnostic Steps

### Step 1: Verify Python Version
```bash
python3 --version  # Should be 3.8+
```

### Step 2: Check Installed Packages
```bash
python3 -m pip list | grep -E "streamlit|yfinance|pandas"
```

### Step 3: Run Import Test
```bash
python3 test_imports.py
```

### Step 4: Try Starting the App
```bash
python3 start.py
```

---

## Getting Help

If issues persist:

1. **Check Python Path**
   ```bash
   which python3
   which streamlit
   ```

2. **Check for Virtual Environment Activation**
   - Make sure you're not in a conflicting venv

3. **Clear Cache and Reinstall**
   ```bash
   pip install --no-cache-dir -r requirements.txt --force-reinstall
   ```

4. **Check System Permissions**
   ```bash
   # Ensure pip can write to site-packages
   python3 -m pip install --user -r requirements.txt
   ```

---

## Quick Reference: Install Commands

| Method | Command |
|--------|---------|
| **Automatic** | `python3 start.py` |
| **Manual** | `pip install -r requirements.txt` |
| **Upgrade** | `pip install --upgrade -r requirements.txt` |
| **Force Fresh** | `pip install --no-cache-dir --force-reinstall -r requirements.txt` |
| **User Install** | `pip install --user -r requirements.txt` |

---

## Files in This Project

- `streamlit_app.py` — Main dashboard (has import error handling)
- `requirements.txt` — List of dependencies
- `test_imports.py` — Diagnostic script to verify imports
- `start.py` — **Recommended:** Auto-install and launch script
- `run.sh` — Bash version of startup script (Linux/Mac)
