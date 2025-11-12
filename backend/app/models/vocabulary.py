"""
Vocabulary models for vocabulary recommendation engine.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, ARRAY, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import UniqueConstraint, CheckConstraint
from app.database import Base


class VocabularyWord(Base):
    """
    Vocabulary word model representing words in the master vocabulary list (grades 5-8).
    """
    __tablename__ = "vocabulary_words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), nullable=False, unique=True, index=True)
    grade_level = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    student_vocabulary = relationship(
        "StudentVocabulary",
        back_populates="word",
        cascade="all, delete-orphan",
    )
    book_vocabulary = relationship(
        "BookVocabulary",
        back_populates="word",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<VocabularyWord(id={self.id}, word='{self.word}', grade={self.grade_level})>"


class StudentVocabulary(Base):
    """
    Student vocabulary profile model representing a student's usage of a vocabulary word.
    
    Dismissal fields:
    - dismissed: Whether the teacher has dismissed this misuse report
    - dismissed_reason: Why it was dismissed ('addressed' or 'ai_error')
    - dismissed_at: When it was dismissed
    """
    __tablename__ = "student_vocabulary"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    word_id = Column(Integer, ForeignKey("vocabulary_words.id", ondelete="CASCADE"), nullable=False, index=True)
    usage_count = Column(Integer, default=0)
    correct_usage_count = Column(Integer, default=0)
    misuse_examples = Column(ARRAY(Text), nullable=True)
    last_analyzed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Dismissal fields
    dismissed = Column(Boolean, default=False, nullable=False)
    dismissed_reason = Column(String(20), nullable=True)  # 'addressed' or 'ai_error'
    dismissed_at = Column(DateTime(timezone=True), nullable=True)

    # Constraints
    __table_args__ = (
        UniqueConstraint("student_id", "word_id", name="uq_student_vocabulary"),
        CheckConstraint(
            "dismissed_reason IN ('addressed', 'ai_error') OR dismissed_reason IS NULL",
            name="ck_dismissed_reason"
        ),
    )

    # Relationships
    student = relationship("Student", back_populates="student_vocabulary")
    word = relationship("VocabularyWord", back_populates="student_vocabulary")

    def __repr__(self):
        return f"<StudentVocabulary(id={self.id}, student_id={self.student_id}, word_id={self.word_id})>"

