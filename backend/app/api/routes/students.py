"""
Student API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.services.student_service import get_all_students, get_student_by_id, dismiss_vocabulary_issue
from app.schemas.student import StudentListResponse, StudentDetailResponse


# Request schema for dismissal
class DismissVocabularyRequest(BaseModel):
    reason: str  # 'addressed' or 'ai_error'


# Response schema for dismissal
class DismissVocabularyResponse(BaseModel):
    success: bool
    dismissed_at: str


router = APIRouter()


@router.get("", response_model=List[StudentListResponse])
async def get_students(db: Session = Depends(get_db)):
    """
    Get list of all students with basic information.
    
    Returns:
        List of students with id, name, reading_level, assigned_grade, and vocab_mastery_percent
    """
    try:
        return get_all_students(db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching students: {str(e)}"
        )


@router.get("/{student_id}", response_model=StudentDetailResponse)
async def get_student(student_id: int, db: Session = Depends(get_db)):
    """
    Get detailed student profile.
    
    Args:
        student_id: Student ID
        
    Returns:
        Detailed student profile with vocabulary mastery, missing words, misused words, and book recommendations
        
    Raises:
        404: If student not found
    """
    try:
        student = get_student_by_id(db, student_id)
        if student is None:
            raise HTTPException(
                status_code=404,
                detail=f"Student with id {student_id} not found"
            )
        return student
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching student: {str(e)}"
        )


@router.post("/{student_id}/vocabulary/{word_id}/dismiss", response_model=DismissVocabularyResponse)
async def dismiss_vocabulary(
    student_id: int,
    word_id: int,
    request: DismissVocabularyRequest,
    db: Session = Depends(get_db)
):
    """
    Dismiss a vocabulary issue for a student.
    
    Args:
        student_id: Student ID
        word_id: Vocabulary word ID
        request: Dismissal request with reason ('addressed' or 'ai_error')
        
    Returns:
        Success status and dismissal timestamp
        
    Raises:
        400: If reason is invalid
        404: If student or word not found
    """
    # Validate reason
    if request.reason not in ['addressed', 'ai_error']:
        raise HTTPException(
            status_code=400,
            detail="Invalid dismiss reason. Must be 'addressed' or 'ai_error'"
        )
    
    try:
        dismissed_at = dismiss_vocabulary_issue(db, student_id, word_id, request.reason)
        
        if dismissed_at is None:
            raise HTTPException(
                status_code=404,
                detail="Vocabulary issue not found"
            )
        
        return DismissVocabularyResponse(
            success=True,
            dismissed_at=dismissed_at.isoformat()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error dismissing vocabulary: {str(e)}"
        )
