import streamlit as st
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Chat - Chatbot Pembelajaran Algoritma",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create necessary directories if they don't exist
Path("pages").mkdir(exist_ok=True)
Path("data").mkdir(exist_ok=True)
Path("logs").mkdir(exist_ok=True)
Path("uploads").mkdir(exist_ok=True)

# Redirect to Chat page
st.markdown("""
<meta http-equiv="refresh" content="0; url=/Chat" />
""", unsafe_allow_html=True)

# Fallback message
st.info("🔄 Redirecting to Chat page...")
st.markdown("If you are not redirected automatically, please click **Chat** in the sidebar.")