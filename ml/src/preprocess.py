"""
Text preprocessing pipeline for sentiment analysis.

This module provides production-ready text cleaning, normalization,
and vectorization functions used by both the training pipeline
and the FastAPI backend for real-time inference.
"""

import html
import re
import joblib
import numpy as np
from pathlib import Path
from typing import Optional

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

# Ensure required NLTK data is available
try:
    STOP_WORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords", quiet=True)
    STOP_WORDS = set(stopwords.words("english"))

try:
    word_tokenize("test")
except LookupError:
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)

lemmatizer = WordNetLemmatizer()

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODELS_BASELINE = PROJECT_ROOT / "ml" / "models" / "baseline"


def clean_text(text: str) -> str:
    """
    Clean raw text by removing noise elements.

    Removes HTML entities, @mentions, URLs, hashtag symbols,
    special characters, and normalizes whitespace.

    Args:
        text: Raw input text string.

    Returns:
        Cleaned lowercase text string.
    """
    if not isinstance(text, str):
        return ""

    text = html.unescape(text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"#(\w+)", r"\1", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()

    return text


def lemmatize_text(text: str) -> str:
    """
    Tokenize, remove stop words, and lemmatize text.

    Args:
        text: Cleaned text string.

    Returns:
        Lemmatized text string with stop words removed.
    """
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()

    tokens = [
        lemmatizer.lemmatize(token)
        for token in tokens
        if token not in STOP_WORDS and len(token) > 2
    ]

    return " ".join(tokens)


def preprocess_text(text: str, lemmatize: bool = True) -> str:
    """
    Full preprocessing pipeline for a single text input.

    This is the main function called by the FastAPI backend
    for real-time inference.

    Args:
        text: Raw input text (tweet or review).
        lemmatize: Apply lemmatization. Set True for baseline ML models,
                   False for transformer models.

    Returns:
        Fully preprocessed text string.
    """
    if not isinstance(text, str) or len(text.strip()) == 0:
        return ""

    text = clean_text(text)

    if not text:
        return ""

    if lemmatize:
        text = lemmatize_text(text)

    return text


def load_vectorizer(path: Optional[Path] = None) -> TfidfVectorizer:
    """
    Load the fitted TF-IDF vectorizer from disk.

    Args:
        path: Optional custom path to vectorizer .pkl file.

    Returns:
        Fitted TfidfVectorizer instance.

    Raises:
        FileNotFoundError: If vectorizer file does not exist.
    """
    vectorizer_path = path or (MODELS_BASELINE / "tfidf_vectorizer.pkl")
    if not vectorizer_path.exists():
        raise FileNotFoundError(
            f"Vectorizer not found at {vectorizer_path}. "
            "Run the preprocessing notebook first."
        )
    return joblib.load(vectorizer_path)


def load_label_encoder(path: Optional[Path] = None):
    """
    Load the fitted LabelEncoder from disk.

    Args:
        path: Optional custom path to encoder .pkl file.

    Returns:
        Fitted LabelEncoder instance.

    Raises:
        FileNotFoundError: If encoder file does not exist.
    """
    encoder_path = path or (MODELS_BASELINE / "label_encoder.pkl")
    if not encoder_path.exists():
        raise FileNotFoundError(
            f"Label encoder not found at {encoder_path}. "
            "Run the preprocessing notebook first."
        )
    return joblib.load(encoder_path)


def vectorize_text(text: str, vectorizer: TfidfVectorizer) -> np.ndarray:
    """
    Preprocess and vectorize a single text input for inference.

    Args:
        text: Raw input text.
        vectorizer: Fitted TfidfVectorizer instance.

    Returns:
        Sparse matrix row ready for model prediction.
    """
    cleaned = preprocess_text(text, lemmatize=True)
    return vectorizer.transform([cleaned])
