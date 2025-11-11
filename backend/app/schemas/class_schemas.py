"""
Pydantic schemas for class API responses.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel


class TopMissingWordResponse(BaseModel):
    """Top missing word information."""
    word: str
    students_missing: int

    class Config:
        from_attributes = True


class CommonlyMisusedWordResponse(BaseModel):
    """Commonly misused word information."""
    word: str
    misuse_count: int

    class Config:
        from_attributes = True


class ClassRecommendationResponse(BaseModel):
    """Class-wide book recommendation."""
    book_id: int
    title: str
    author: Optional[str] = None
    reading_level: Optional[float] = None
    students_recommended_count: int
    avg_match_score: float

    class Config:
        from_attributes = True


class ClassStatsResponse(BaseModel):
    """Class-wide statistics."""
    total_students: int
    avg_vocab_mastery_percent: float
    reading_level_distribution: Dict[str, int]
    top_missing_words: List[TopMissingWordResponse]
    commonly_misused_words: List[CommonlyMisusedWordResponse]

    class Config:
        from_attributes = True

