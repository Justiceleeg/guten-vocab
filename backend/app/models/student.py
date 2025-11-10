"""
Student model for vocabulary recommendation engine.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Student(Base):
    """
    Student model representing a student in the class.
    """
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    actual_reading_level = Column(Float, nullable=False)
    assigned_grade = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    student_vocabulary = relationship(
        "StudentVocabulary",
        back_populates="student",
        cascade="all, delete-orphan",
    )
    recommendations = relationship(
        "StudentRecommendation",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}', grade={self.assigned_grade})>"

