#!/usr/bin/env python3
"""
Minimal test of Live Signals section
"""
import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Live Signals Test", layout="wide")
st.title("Live Signals Test")

# Core navbar
page = st.sidebar.radio("Navigation", ["Live Signals", "Other"])
st.write(f"✓ Page: {page}")

if page == "Live Signals":
    st.header("📡 Live SMC Signals")
    st.write("Starting render...")
    
    auto_refresh = st.checkbox("Auto-refresh", value=True)
    st.write( f"✓ Checkbox: {auto_refresh}")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        assets = {"Bitcoin": "BTC-USD", "Ethereum": "ETH-USD"}
    with col2:
        timeframe = st.selectbox("Timeframe", ["15m", "1h", "1d"])
    
    st.write(f"✓ Timeframe: {timeframe}")
    st.divider()
    
    cols = st.columns(len(assets))
    loaded = 0
    
    for i, (name, ticker) in enumerate(assets.items()):
        with cols[i]:
            with st.spinner(f"Loading {name}..."):
                try:
                    st.write(f"Downloading {name}...")
                    data = yf.download(ticker, period="5d", interval="15m", progress=False)
                    
                    if data is None:
                        st.warning(f"No data for {name}")
                        continue
                    
                    if isinstance(data.columns, pd.MultiIndex):
                        data.columns = data.columns.get_level_values(0)
                    
                    if not all(c in data.columns for c in ['Close']):
                        st.warning(f"Missing columns")
                        continue
                    
                    price = float(data['Close'].iloc[-1])
                    st.metric(f"{name} Price", f"${price:.2f}")
                    st.write(f"✓ {name} rendered")
                    loaded += 1
                    
                except Exception as e:
                    st.error(f"Error: {str(e)[:50]}")
    
    st.write(f"\n✓✓✓ Loaded assets: {loaded}")
    if loaded == 0:
        st.warning("No assets loaded!")

st.write("✓✓✓ Page complete")
