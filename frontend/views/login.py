"""
Login and registration page.
"""

import streamlit as st
from frontend.utils.api_client import login, register


def show_login_page():
    """Render the login/register page."""

    st.markdown('<p class="main-header">🧠 Sentiment Analytics</p>', unsafe_allow_html=True)
    st.markdown("#### AI-Powered Customer Sentiment Platform")
    st.divider()

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    with tab1:
        st.subheader("Welcome back")
        email = st.text_input("Email", key="login_email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", use_container_width=True, type="primary"):
            if email and password:
                with st.spinner("Logging in..."):
                    token = login(email, password)
                if token:
                    st.session_state["token"] = token
                    st.session_state["email"] = email
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
            else:
                st.warning("Please fill in all fields")

    with tab2:
        st.subheader("Create account")
        reg_email = st.text_input("Email", key="reg_email", placeholder="you@example.com")
        reg_username = st.text_input("Username", key="reg_username", placeholder="yourname")
        reg_password = st.text_input("Password", type="password", key="reg_password")

        if st.button("Register", use_container_width=True, type="primary"):
            if reg_email and reg_username and reg_password:
                with st.spinner("Creating account..."):
                    result = register(reg_email, reg_username, reg_password)
                if "error" not in result:
                    st.success("Account created! Please login.")
                else:
                    st.error(result["error"])
            else:
                st.warning("Please fill in all fields")
