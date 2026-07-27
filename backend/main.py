"""
FastAPI application entry point.

This file creates the FastAPI app, registers all routers,
sets up CORS, and creates database tables on startup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.core.database import engine
from backend.api.models import user, prediction
from backend.api.routes import auth, sentiment

# Create all database tables
user.Base.metadata.create_all(bind=engine)
prediction.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Customer Sentiment Analytics API",
    description="Production-ready sentiment analysis API powered by DistilBERT",
    version="1.0.0"
)

# CORS — allows Streamlit frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(sentiment.router)


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "AI Customer Sentiment Analytics API",
        "docs": "/docs",
        "health": "/health"
    }
