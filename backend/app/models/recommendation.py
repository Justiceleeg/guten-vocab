"""
Recommendation models for vocabulary recommendation engine.
"""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class StudentRecommendation(Base):
    """
    Student book recommendation model representing personalized book recommendations for students.
    """
    __tablename__ = "student_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    match_score = Column(Float, nullable=False)
    known_words_percent = Column(Float, nullable=False)
    new_words_count = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    student = relationship("Student", back_populates="recommendations")
    book = relationship("Book", back_populates="student_recommendations")

    def __repr__(self):
        return f"<StudentRecommendation(id={self.id}, student_id={self.student_id}, book_id={self.book_id}, score={self.match_score})>"


class ClassRecommendation(Base):
    """
    Class-wide book recommendation model representing books recommended for the entire class.
    """
    __tablename__ = "class_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    match_score = Column(Float, nullable=False)
    students_recommended_count = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Index on match_score for sorting
    __table_args__ = (
        Index("idx_class_recs_score", match_score.desc()),
    )

    # Relationships
    book = relationship("Book", back_populates="class_recommendations")

    def __repr__(self):
        return f"<ClassRecommendation(id={self.id}, book_id={self.book_id}, score={self.match_score}, count={self.students_recommended_count})>"

