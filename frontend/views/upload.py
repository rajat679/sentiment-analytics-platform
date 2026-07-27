"""
CSV batch upload and prediction page.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import time
from frontend.utils.api_client import predict_sentiment


def show_upload_page():
    """Render the CSV upload and batch prediction page."""

    st.markdown('<p class="main-header">📁 Batch Analysis</p>', unsafe_allow_html=True)
    st.markdown("Upload a CSV file to analyse sentiment for multiple texts at once.")
    st.divider()

    st.info("**CSV Format:** Your file must have a column named `text` containing the reviews or tweets.")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is None:
        st.markdown("#### Sample CSV format:")
        sample = pd.DataFrame({
            "text": [
                "The flight was amazing!",
                "Terrible customer service",
                "Average experience overall"
            ]
        })
        st.dataframe(sample, use_container_width=True)
        return

    df = pd.read_csv(uploaded_file)

    if "text" not in df.columns:
        st.error("CSV must have a column named 'text'")
        return

    st.success(f"✅ Loaded {len(df):,} rows")
    st.dataframe(df.head(5), use_container_width=True)

    model_choice = st.selectbox(
        "Model",
        options=["svm", "distilbert"],
        format_func=lambda x: "⚡ SVM (Fast)" if x == "svm" else "🤖 DistilBERT (Accurate)"
    )

    max_rows = st.slider("Max rows to analyse", 10, min(500, len(df)), min(100, len(df)))

    if st.button("Run Batch Analysis", type="primary", use_container_width=True):
        df_sample = df.head(max_rows).copy()
        results = []

        progress = st.progress(0)
        status = st.empty()

        for i, row in enumerate(df_sample.itertuples()):
            result = predict_sentiment(str(row.text), model_choice)
            if "result" in result:
                results.append({
                    "text": row.text,
                    "sentiment": result["result"]["sentiment"],
                    "confidence": result["result"]["confidence"]
                })
            progress.progress((i + 1) / len(df_sample))
            status.text(f"Analysing {i+1}/{len(df_sample)}...")

        status.text("✅ Analysis complete!")

        results_df = pd.DataFrame(results)

        st.divider()
        st.subheader("Results")

        col1, col2 = st.columns(2)
        with col1:
            counts = results_df["sentiment"].value_counts()
            fig = px.pie(
                values=counts.values,
                names=counts.index,
                color=counts.index,
                color_discrete_map={
                    "positive": "#2ecc71",
                    "negative": "#e74c3c",
                    "neutral": "#f39c12"
                },
                title="Sentiment Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.metric("Positive", f"{(results_df['sentiment']=='positive').mean()*100:.1f}%")
            st.metric("Negative", f"{(results_df['sentiment']=='negative').mean()*100:.1f}%")
            st.metric("Neutral", f"{(results_df['sentiment']=='neutral').mean()*100:.1f}%")
            avg_conf = results_df["confidence"].mean()
            st.metric("Avg Confidence", f"{avg_conf*100:.1f}%")

        st.subheader("Detailed Results")
        st.dataframe(results_df, use_container_width=True)

        csv = results_df.to_csv(index=False)
        st.download_button(
            "⬇️ Download Results CSV",
            csv,
            "sentiment_results.csv",
            "text/csv",
            use_container_width=True
        )
