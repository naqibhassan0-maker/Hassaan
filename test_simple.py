import streamlit as st

st.set_page_config(page_title="Test Dashboard", layout="wide")

st.title("Test Dashboard")
st.write("This is a test to see if Streamlit renders")

page = st.sidebar.radio("Navigation", ["Test Page", "Another Page"])

if page == "Test Page":
    st.header("Test Page")
    st.write("Content here")
elif page == "Another Page":
    st.header("Another Page")
    st.write("More content")