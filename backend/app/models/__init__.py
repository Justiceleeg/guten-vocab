"""
SQLAlchemy models for Vocabulary Recommendation Engine.
"""
from app.database import Base

# Import all models to ensure they're registered with Base
from app.models.student import Student
from app.models.vocabulary import VocabularyWord, StudentVocabulary
from app.models.book import Book, BookVocabulary
from app.models.recommendation import StudentRecommendation, ClassRecommendation

__all__ = [
    "Base",
    "Student",
    "VocabularyWord",
    "StudentVocabulary",
    "Book",
    "BookVocabulary",
    "StudentRecommendation",
    "ClassRecommendation",
]
