"""
Pydantic schemas for student API responses.
"""
from typing import List, Optional
from pydantic import BaseModel


class VocabMasteryResponse(BaseModel):
    """Vocabulary mastery metrics."""
    total_grade_level_words: int
    words_mastered: int
    mastery_percent: float

    class Config:
        from_attributes = True


class MisusedWordResponse(BaseModel):
    """Misused word information."""
    word_id: int
    word: str
    correct_count: int
    incorrect_count: int
    example: Optional[str] = None

    class Config:
        from_attributes = True


class BookRecommendationResponse(BaseModel):
    """Book recommendation for a student."""
    book_id: int
    title: str
    author: Optional[str] = None
    reading_level: Optional[float] = None
    match_score: float
    known_words_percent: float
    new_words_count: int

    class Config:
        from_attributes = True


class StudentListResponse(BaseModel):
    """Student list item with basic information."""
    id: int
    name: str
    reading_level: float
    assigned_grade: int
    vocab_mastery_percent: float

    class Config:
        from_attributes = True


class StudentDetailResponse(BaseModel):
    """Detailed student profile."""
    id: int
    name: str
    reading_level: float
    assigned_grade: int
    vocab_mastery: VocabMasteryResponse
    missing_words: List[str]
    misused_words: List[MisusedWordResponse]
    book_recommendations: List[BookRecommendationResponse]

    class Config:
        from_attributes = True

