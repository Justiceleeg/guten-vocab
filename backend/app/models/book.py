"""
Book models for vocabulary recommendation engine.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import UniqueConstraint
from app.database import Base


class Book(Base):
    """
    Book model representing Project Gutenberg books.
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    author = Column(String(255), nullable=True)
    gutenberg_id = Column(Integer, unique=True, nullable=True)
    reading_level = Column(Float, nullable=True, index=True)
    total_words = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    book_vocabulary = relationship(
        "BookVocabulary",
        back_populates="book",
        cascade="all, delete-orphan",
    )
    student_recommendations = relationship(
        "StudentRecommendation",
        back_populates="book",
        cascade="all, delete-orphan",
    )
    class_recommendations = relationship(
        "ClassRecommendation",
        back_populates="book",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"


class BookVocabulary(Base):
    """
    Book vocabulary model representing vocabulary word occurrences in books.
    """
    __tablename__ = "book_vocabulary"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    word_id = Column(Integer, ForeignKey("vocabulary_words.id", ondelete="CASCADE"), nullable=False, index=True)
    occurrence_count = Column(Integer, nullable=False)

    # Unique constraint on (book_id, word_id)
    __table_args__ = (UniqueConstraint("book_id", "word_id", name="uq_book_vocabulary"),)

    # Relationships
    book = relationship("Book", back_populates="book_vocabulary")
    word = relationship("VocabularyWord", back_populates="book_vocabulary")

    def __repr__(self):
        return f"<BookVocabulary(id={self.id}, book_id={self.book_id}, word_id={self.word_id}, count={self.occurrence_count})>"

