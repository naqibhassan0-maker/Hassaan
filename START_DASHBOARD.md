# 🚀 Dashboard Launch Guide

Your Smart Money Concepts dashboard is ready to run! Here are the easiest ways to get it started:

---

## **Option 1: Python Launcher (Easiest - Recommended)**

This automatically installs dependencies and starts everything:

```bash
python3 run_dashboard.py
```

✅ Best for: First-time setup, automated installation

---

## **Option 2: Start Script (Linux/Mac)**

```bash
chmod +x start.py
python3 start.py
```

✅ Best for: Development, full error reporting

---

## **Option 3: Manual Commands (Full Control)**

Run these commands one at a time in your terminal:

```bash
# 1. Navigate to project
cd /workspaces/Hassaan

# 2. Activate environment (if using venv)
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start dashboard
streamlit run streamlit_app.py
```

✅ Best for: Troubleshooting, understanding each step

---

## **Option 4: From Any Directory**

```bash
python3 /workspaces/Hassaan/run_dashboard.py
```

---

## **What Happens When Running**

You'll see:

```
📦 Installing dependencies...
✅ Dependencies installed successfully!

======================================================================
🎯 Starting Streamlit Dashboard...
======================================================================

📊 Dashboard URL: http://localhost:8501
🌐 Network URL: http://[IP]:8501

✨ Press Ctrl+C to stop the dashboard
```

Then open your browser to: **http://localhost:8501**

---

## **Dashboard Features**

Once open, you'll see 5 main tabs:

| Tab | Description |
|-----|------------|
| 📡 **Live Signals** | Real-time SMC signals for BTC, ETH, Gold, S&P 500, EUR/USD |
| 📊 **Executive Summary** | Overview of Smart Money Concepts |
| 🎯 **Top 20 Signals** | Ranked signals with edge impact |
| 📖 **Signal Details** | Deep-dive explanations of each signal |
| 📚 **Data Sources** | Free & paid API references |
| ⚙️ **Risk & Execution** | Risk management and filters |
| 🚀 **Deployment Notes** | Hosting on Streamlit Cloud |

---

## **Troubleshooting**

### Port 8501 already in use?
```bash
streamlit run streamlit_app.py --server.port=8502
```

### Dependencies won't install?
```bash
pip install --upgrade pip
pip install --force-reinstall -r requirements.txt
```

### Check if everything is set up:
```bash
python3 test_imports.py
```

### Clear cache and restart:
```bash
rm -rf ~/.streamlit/
python3 run_dashboard.py
```

---

## **Quick Reference**

| Task | Command |
|------|---------|
| **Start (Easiest)** | `python3 run_dashboard.py` |
| **Verify setup** | `python3 test_imports.py` |
| **Manual start** | `streamlit run streamlit_app.py` |
| **Different port** | `streamlit run streamlit_app.py --server.port=8502` |
| **Stop dashboard** | `Ctrl+C` in terminal |

---

## **Ready?**

👉 **Pick Option 1 above and run:**

```bash
python3 run_dashboard.py
```

The dashboard will start automatically! 🎉
