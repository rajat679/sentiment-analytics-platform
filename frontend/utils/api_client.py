"""
HTTP client for communicating with the FastAPI backend.

All API calls from the frontend go through this module.
This centralizes error handling and token management.
"""

import httpx
import streamlit as st
from typing import Optional

API_BASE_URL = "http://localhost:8000"


def get_headers() -> dict:
    """Return auth headers if token exists in session state."""
    token = st.session_state.get("token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def register(email: str, username: str, password: str) -> dict:
    """Register a new user account."""
    response = httpx.post(
        f"{API_BASE_URL}/auth/register",
        json={"email": email, "username": username, "password": password}
    )
    return response.json() if response.status_code == 201 else {"error": response.json().get("detail", "Registration failed")}


def login(email: str, password: str) -> Optional[str]:
    """Login and return JWT token or None."""
    response = httpx.post(
        f"{API_BASE_URL}/auth/login",
        json={"email": email, "password": password}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None


def predict_sentiment(text: str, model: str = "svm") -> dict:
    """Predict sentiment for a single text."""
    response = httpx.post(
        f"{API_BASE_URL}/sentiment/predict",
        json={"text": text, "model": model},
        headers=get_headers(),
        timeout=60.0
    )
    if response.status_code == 200:
        return response.json()
    return {"error": "Prediction failed"}


def get_history() -> list:
    """Get prediction history for current user."""
    response = httpx.get(
        f"{API_BASE_URL}/sentiment/history",
        headers=get_headers()
    )
    if response.status_code == 200:
        return response.json()
    return []
