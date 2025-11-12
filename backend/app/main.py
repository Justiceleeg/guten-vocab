"""
FastAPI application entry point for Vocabulary Recommendation Engine.
"""

import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db
from app.api.routes import students, class_routes, books

app = FastAPI(
    title="Vocabulary Recommendation Engine API",
    description="API for analyzing student vocabulary and generating book recommendations",
    version="0.1.0",
)

# Configure CORS for frontend integration
# Allow localhost for development and production frontend URL from environment
allowed_origins = [
    "http://localhost:3000",  # Next.js default port (development)
]

# Add production frontend URL from environment variable if set
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    # Ensure URL has protocol
    if not frontend_url.startswith("http"):
        frontend_url = f"https://{frontend_url}"
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - returns API information."""
    return {
        "message": "Vocabulary Recommendation Engine API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint for monitoring."""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {str(e)}",
        )


# Register API routes
app.include_router(students.router, prefix="/api/students", tags=["students"])
app.include_router(class_routes.router, prefix="/api/class", tags=["class"])
app.include_router(books.router, prefix="/api/books", tags=["books"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

