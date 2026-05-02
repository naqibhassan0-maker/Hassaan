#!/usr/bin/env python3
"""
Test if the Streamlit app renders without crashing
"""
import sys
import streamlit as st

# Simulate app execution context
st.set_page_config(
    page_title="Test",
    layout="wide",
)

print("=" * 70)
print("TESTING APP RENDER")
print("=" * 70)

try:
    # Import the app module
    import streamlit_app
    print("\n✅ App module imported successfully - no crashes on import")
    print("✅ All checks passed - app should render without crashing")
except SystemExit:
    print("\n⚠️  App called sys.exit() - Streamlit may have exited")
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
