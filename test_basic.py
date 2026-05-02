#!/usr/bin/env python3
"""
Ultra-simple test to check if Streamlit works at all
"""
import sys
print(f"Python: {sys.executable}")
print(f"Version: {sys.version}")

try:
    import streamlit as st
    print(f"Streamlit imported: {st.__version__}")
except ImportError as e:
    print(f"Streamlit import failed: {e}")
    sys.exit(1)

# Test basic streamlit
st.set_page_config(page_title="Test", layout="wide")
st.title("Test Page")
st.write("If you see this, Streamlit is working!")
st.write(f"Python: {sys.version}")
st.write(f"Streamlit: {st.__version__}")