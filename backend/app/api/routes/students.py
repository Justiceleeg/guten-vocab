"""
Student API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.student_service import get_all_students, get_student_by_id
from app.schemas.student import StudentListResponse, StudentDetailResponse

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
