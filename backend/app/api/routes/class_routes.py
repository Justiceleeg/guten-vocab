"""
Class API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.class_service import get_class_stats, get_class_recommendations
from app.schemas.class_schemas import ClassStatsResponse, ClassRecommendationResponse

router = APIRouter()


@router.get("/stats", response_model=ClassStatsResponse)
async def get_class_statistics(db: Session = Depends(get_db)):
    """
    Get class-wide statistics.
    
    Returns:
        Class-wide statistics including total students, average vocabulary mastery,
        reading level distribution, top missing words, and commonly misused words
    """
    try:
        return get_class_stats(db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching class statistics: {str(e)}"
        )


@router.get("/recommendations", response_model=List[ClassRecommendationResponse])
async def get_class_book_recommendations(db: Session = Depends(get_db)):
    """
    Get top 2 class-wide book recommendations.
    
    Returns:
        List of top 2 class-wide book recommendations
    """
    try:
        return get_class_recommendations(db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching class recommendations: {str(e)}"
        )
