#!/usr/bin/env python3
"""
Streamlit app with detailed timing for debugging blank page issue
"""
import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Smart Money Concepts Dashboard", page_icon="📊", layout="wide")

start_time = time.time()
def log_time(msg):
    elapsed = time.time() - start_time
    st.write(f"[{elapsed:.2f}s] {msg}")

log_time("🔷 App started")

st.title("📈 Smart Money Concepts Dashboard")
st.caption("Executive summary, signal framework, and live institutional signals overlay.")
log_time("✓ Title rendered")

try:
    page = st.sidebar.radio(
        "Navigation",
        [
            "Live Signals",
            "Executive Summary",
            "Top 20 Signals",
            "Signal Details",
            "Data Sources",
            "Risk & Execution",
            "Deployment Notes",
        ],
    )
    log_time(f"✓ Navigation rendered: page={page}")
except Exception as e:
    st.error(f"Navigation failed: {e}")
    page = "Live Signals"
    log_time(f"✗ Navigation error, defaulted to: {page}")

if not page:
    page = "Live Signals"
    log_time("⚠️  No page selected, defaulted")

if page == "Live Signals":
    log_time("🔷 Rendering Live Signals")
    st.header("📡 Live SMC Signals")
    log_time("✓ Header rendered")
    
    st.markdown("Real-time SMC signal detection.")
    log_time("✓ Markdown rendered")
    
    auto_refresh = st.checkbox("Auto-refresh", value=True)
    log_time(f"✓ Checkbox rendered: {auto_refresh}")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        assets = {
            "Bitcoin": "BTC-USD",
            "Ethereum": "ETH-USD",
        }
    log_time(f"✓ Asset list created: {len(assets)} assets")
    
    with col2:
        timeframe = st.selectbox("Timeframe", ["15m", "1h", "1d"])
    log_time(f"✓ Timeframe selectbox: {timeframe}")
    
    st.divider()
    log_time("✓ Divider rendered")
    
    cols = st.columns(len(assets))
    log_time(f"✓ Created {len(assets)} columns")
    
    loaded = 0
    for i, (name, ticker) in enumerate(assets.items()):
        with cols[i]:
            log_time(f"  🔷 Loading {name}...")
            with st.spinner(f"Loading {name}..."):
                try:
                    data = yf.download(ticker, period="5d", interval="15m", progress=False)
                    log_time(f"    ✓ Downloaded {name}")
                    
                    if isinstance(data.columns, pd.MultiIndex):
                        data.columns = data.columns.get_level_values(0)
                        log_time(f"    ✓ Flattened columns for {name}")
                    
                    if len(data) < 2:
                        st.warning(f"Not enough data")
                        log_time(f"    ✗ Insufficient data for {name}")
                        continue
                    
                    price = float(data['Close'].iloc[-1])
                    st.metric(f"{name} Price", f"${price:.2f}")
                    log_time(f"    ✓ Rendered {name}")
                    loaded += 1
                    
                except Exception as e:
                    st.error(f"{name} error: {str(e)[:40]}")
                    log_time(f"    ✗ {name} failed: {e}")
    
    log_time(f"✓ Loop complete: {loaded} assets loaded")
    
    if loaded == 0:
        st.warning("⚠️  No assets loaded")
        log_time("⚠️  WARNING: No assets loaded!")
    
    st.write("---")
    log_time("✓✓✓ LIVE SIGNALS COMPLETE ✓✓✓")

else:
    st.info(f"Page: {page} (implementation pending)")
    log_time(f"✓ Showing info page: {page}")

log_time("✓✓✓ APP COMPLETE ✓✓✓")
