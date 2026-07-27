"""
Sentiment prediction routes.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..core.ml_models import model_manager
from ..models.prediction import Prediction
from ..schemas.sentiment import PredictRequest, PredictResponse, PredictionHistory
from ..dependencies import get_current_user
from ..models.user import User

router = APIRouter(prefix="/sentiment", tags=["Sentiment"])


@router.post("/predict", response_model=PredictResponse)
def predict(
    request: PredictRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Predict sentiment for a single text input.

    Args:
        request: Text and model choice.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        Sentiment prediction with confidence score.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    if request.model == "distilbert":
        result = model_manager.predict_bert(request.text)
    else:
        result = model_manager.predict_baseline(request.text)

    prediction = Prediction(
        user_id=current_user.id,
        text=request.text,
        sentiment=result["sentiment"],
        confidence=result["confidence"],
        model_used=request.model
    )
    db.add(prediction)
    db.commit()

    return {
        "success": True,
        "result": {
            "text": request.text,
            "sentiment": result["sentiment"],
            "confidence": result["confidence"],
            "model_used": request.model
        }
    }


@router.get("/history", response_model=List[PredictionHistory])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get prediction history for the authenticated user.

    Returns:
        List of past predictions ordered by most recent.
    """
    return (
        db.query(Prediction)
        .filter(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .limit(100)
        .all()
    )
