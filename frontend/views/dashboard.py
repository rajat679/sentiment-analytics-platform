"""
Main analytics dashboard page.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from frontend.utils.api_client import get_history
from frontend.components.theme import sentiment_badge


def show_dashboard():
    """Render the main analytics dashboard."""

    st.markdown('<p class="main-header">📊 Analytics Dashboard</p>', unsafe_allow_html=True)
    st.markdown(f"Welcome back, **{st.session_state.get('email', 'User')}**")
    st.divider()

    history = get_history()

    if not history:
        st.info("No predictions yet. Go to **Predict** to analyse your first text!")
        return

    df = pd.DataFrame(history)
    df["created_at"] = pd.to_datetime(df["created_at"])

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Predictions", len(df))
    with col2:
        positive_pct = (df["sentiment"] == "positive").mean() * 100
        st.metric("Positive", f"{positive_pct:.1f}%")
    with col3:
        negative_pct = (df["sentiment"] == "negative").mean() * 100
        st.metric("Negative", f"{negative_pct:.1f}%")
    with col4:
        avg_confidence = df["confidence"].mean() * 100
        st.metric("Avg Confidence", f"{avg_confidence:.1f}%")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sentiment Distribution")
        sentiment_counts = df["sentiment"].value_counts()
        fig = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            color=sentiment_counts.index,
            color_discrete_map={
                "positive": "#2ecc71",
                "negative": "#e74c3c",
                "neutral": "#f39c12"
            },
            hole=0.4
        )
        fig.update_layout(showlegend=True, height=300, margin=dict(t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Predictions Over Time")
        df_time = df.set_index("created_at").resample("h").size().reset_index()
        df_time.columns = ["time", "count"]
        fig2 = px.bar(df_time, x="time", y="count", color_discrete_sequence=["#667eea"])
        fig2.update_layout(height=300, margin=dict(t=0, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Recent Predictions")

    for _, row in df.head(10).iterrows():
        with st.container():
            c1, c2, c3 = st.columns([4, 1, 1])
            with c1:
                st.write(f"📝 {row['text'][:100]}...")
            with c2:
                st.markdown(sentiment_badge(row["sentiment"]), unsafe_allow_html=True)
            with c3:
                st.write(f"{row['confidence']*100:.0f}% conf")
        st.divider()
