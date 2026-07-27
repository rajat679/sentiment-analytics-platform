"""
Pydantic schemas for sentiment prediction endpoints.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PredictRequest(BaseModel):
    """Schema for single text prediction request."""
    text: str
    model: str = "distilbert"


class PredictionResult(BaseModel):
    """Schema for a single prediction result."""
    text: str
    sentiment: str
    confidence: float
    model_used: str


class PredictResponse(BaseModel):
    """Schema for prediction API response."""
    success: bool
    result: PredictionResult


class PredictionHistory(BaseModel):
    """Schema for prediction history item."""
    id: int
    text: str
    sentiment: str
    confidence: float
    model_used: str
    created_at: datetime

    class Config:
        from_attributes = True
