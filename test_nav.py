#!/usr/bin/env python3
"""
Test navigation rendering
"""
import streamlit as st

st.set_page_config(page_title="Test", layout="wide")

st.title("Test App")

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
    st.write(f"✅ Page selected: {page}")
except Exception as e:
    st.error(f"❌ Navigation failed: {e}")
    page = "Live Signals"

st.write(f"Current page: {page}")

if page == "Live Signals":
    st.write("✅ Live Signals page loaded")
elif page == "Executive Summary":
    st.write("✅ Executive Summary page loaded")
else:
    st.write(f"✅ Page '{page}' loaded")
