"""
Single text prediction page.
"""

import streamlit as st
import plotly.graph_objects as go
from frontend.utils.api_client import predict_sentiment
from frontend.components.theme import sentiment_badge


def show_predict_page():
    """Render the sentiment prediction page."""

    st.markdown('<p class="main-header">🔍 Predict Sentiment</p>', unsafe_allow_html=True)
    st.markdown("Analyse the sentiment of any text using our AI models.")
    st.divider()

    col1, col2 = st.columns([3, 1])
    with col1:
        text_input = st.text_area(
            "Enter text to analyse",
            placeholder="Type or paste customer feedback, tweet, or review here...",
            height=150
        )
    with col2:
        model_choice = st.selectbox(
            "Model",
            options=["svm", "distilbert"],
            format_func=lambda x: "⚡ SVM (Fast)" if x == "svm" else "🤖 DistilBERT (Accurate)"
        )
        st.caption("SVM: ~0.1s | DistilBERT: ~2s")

    if st.button("Analyse Sentiment", type="primary", use_container_width=True):
        if not text_input.strip():
            st.warning("Please enter some text to analyse.")
            return

        with st.spinner("Analysing sentiment..."):
            result = predict_sentiment(text_input, model_choice)

        if "error" in result:
            st.error("Prediction failed. Please try again.")
            return

        pred = result["result"]
        sentiment = pred["sentiment"]
        confidence = pred["confidence"]

        st.divider()
        st.subheader("Result")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Sentiment:** {sentiment_badge(sentiment)}", unsafe_allow_html=True)
        with col2:
            st.metric("Confidence", f"{confidence*100:.1f}%")
        with col3:
            st.metric("Model", pred["model_used"].upper())

        # Confidence gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence * 100,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Confidence Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#667eea"},
                "steps": [
                    {"range": [0, 50], "color": "#f8d7da"},
                    {"range": [50, 75], "color": "#fff3cd"},
                    {"range": [75, 100], "color": "#d4edda"}
                ]
            }
        ))
        fig.update_layout(height=250, margin=dict(t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)
