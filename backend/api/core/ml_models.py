"""
ML model loading and inference utilities.

Models are loaded once at startup and reused for all requests.
This is critical for performance — loading BERT takes ~2 seconds.
"""

import joblib
import torch
import numpy as np
from pathlib import Path
from typing import Optional
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

# Fix: go up 3 levels from backend/api/core/ to project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODELS_BASELINE = PROJECT_ROOT / "ml" / "models" / "baseline"
MODELS_ADVANCED = PROJECT_ROOT / "ml" / "models" / "advanced"

DEVICE = (
    torch.device("mps") if torch.backends.mps.is_available()
    else torch.device("cuda") if torch.cuda.is_available()
    else torch.device("cpu")
)


class ModelManager:
    def __init__(self):
        self._vectorizer = None
        self._label_encoder = None
        self._baseline_model = None
        self._bert_model = None
        self._bert_tokenizer = None

    def _load_baseline_artifacts(self):
        if self._vectorizer is None:
            self._vectorizer = joblib.load(MODELS_BASELINE / "tfidf_vectorizer.pkl")
            self._label_encoder = joblib.load(MODELS_BASELINE / "label_encoder.pkl")
            self._baseline_model = joblib.load(MODELS_BASELINE / "best_baseline_model.pkl")

    def _load_bert_artifacts(self):
        if self._bert_model is None:
            bert_path = MODELS_ADVANCED / "distilbert_sentiment"
            self._bert_tokenizer = DistilBertTokenizerFast.from_pretrained(str(bert_path))
            self._bert_model = DistilBertForSequenceClassification.from_pretrained(
                str(bert_path)
            ).to(DEVICE)
            self._bert_model.eval()

    def predict_baseline(self, text: str) -> dict:
        import sys
        sys.path.insert(0, str(PROJECT_ROOT))
        from ml.src.preprocess import preprocess_text

        self._load_baseline_artifacts()
        cleaned = preprocess_text(text, lemmatize=True)
        vector = self._vectorizer.transform([cleaned])
        prediction = self._baseline_model.predict(vector)[0]
        sentiment = self._label_encoder.inverse_transform([prediction])[0]

        try:
            proba = self._baseline_model.predict_proba(vector)[0]
            confidence = float(np.max(proba))
        except AttributeError:
            confidence = 0.85

        return {"sentiment": sentiment, "confidence": confidence}

    def predict_bert(self, text: str) -> dict:
        import sys
        sys.path.insert(0, str(PROJECT_ROOT))
        from ml.src.preprocess import clean_text

        self._load_bert_artifacts()
        cleaned = clean_text(text)
        inputs = self._bert_tokenizer(
            cleaned,
            max_length=128,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        input_ids = inputs["input_ids"].to(DEVICE)
        attention_mask = inputs["attention_mask"].to(DEVICE)

        with torch.no_grad():
            outputs = self._bert_model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

        probs = torch.softmax(outputs.logits, dim=1).cpu().numpy()[0]
        pred_idx = int(np.argmax(probs))
        confidence = float(np.max(probs))

        classes = ["negative", "neutral", "positive"]
        sentiment = classes[pred_idx]

        return {"sentiment": sentiment, "confidence": confidence}


model_manager = ModelManager()
