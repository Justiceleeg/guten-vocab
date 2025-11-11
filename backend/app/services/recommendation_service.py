"""
Recommendation service for fetching book recommendations.
"""
from typing import List
from sqlalchemy.orm import Session

from app.models.recommendation import StudentRecommendation
from app.schemas.student import BookRecommendationResponse


def get_student_recommendations(db: Session, student_id: int) -> List[BookRecommendationResponse]:
    """
    Get book recommendations for a student.
    
    Args:
        db: Database session
        student_id: Student ID
        
    Returns:
        List of book recommendation responses
    """
    recommendations = db.query(StudentRecommendation).filter(
        StudentRecommendation.student_id == student_id
    ).order_by(StudentRecommendation.match_score.desc()).limit(3).all()
    
    result = []
    for rec in recommendations:
        book = rec.book
        result.append(BookRecommendationResponse(
            book_id=book.id,
            title=book.title,
            author=book.author,
            reading_level=book.reading_level,
            match_score=rec.match_score,
            known_words_percent=rec.known_words_percent,
            new_words_count=rec.new_words_count
        ))
    
    return result

