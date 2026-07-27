"""
Dark/light mode theme configuration for Streamlit.
"""

import streamlit as st


def apply_theme():
    """Apply custom CSS for professional styling with dark/light support."""
    st.markdown("""
    <style>
    /* Main container */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    /* Sentiment badges */
    .sentiment-positive {
        background: #d4edda;
        color: #155724;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .sentiment-negative {
        background: #f8d7da;
        color: #721c24;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .sentiment-neutral {
        background: #fff3cd;
        color: #856404;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 1.1rem;
    }

    /* Cards */
    .metric-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


def sentiment_badge(sentiment: str) -> str:
    """Return HTML badge for a sentiment value."""
    icons = {"positive": "😊", "negative": "😞", "neutral": "😐"}
    icon = icons.get(sentiment, "❓")
    return f'<span class="sentiment-{sentiment}">{icon} {sentiment.capitalize()}</span>'
