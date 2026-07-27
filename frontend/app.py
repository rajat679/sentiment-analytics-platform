"""
Streamlit application entry point.

Handles routing between pages and authentication state.
"""

import streamlit as st
from frontend.components.theme import apply_theme
from frontend.views.login import show_login_page
from frontend.views.dashboard import show_dashboard
from frontend.views.predict import show_predict_page
from frontend.views.upload import show_upload_page


st.set_page_config(
    page_title="AI Sentiment Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()

# Initialize session state
if "token" not in st.session_state:
    st.session_state["token"] = None

# Route based on authentication
if not st.session_state["token"]:
    show_login_page()
else:
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🧠 Sentiment Analytics")
        st.markdown(f"👤 {st.session_state.get('email', '')}")
        st.divider()

        page = st.radio(
            "Navigate",
            options=["Dashboard", "Predict", "Batch Upload"],
            label_visibility="collapsed"
        )

        st.divider()

        # Dark/light mode toggle
        dark_mode = st.toggle("🌙 Dark Mode", value=True)

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # Render selected page
    if page == "Dashboard":
        show_dashboard()
    elif page == "Predict":
        show_predict_page()
    elif page == "Batch Upload":
        show_upload_page()
