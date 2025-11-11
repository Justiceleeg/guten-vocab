"""
Student service for querying student data and calculating vocabulary metrics.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.student import Student
from app.models.vocabulary import VocabularyWord, StudentVocabulary
from app.models.recommendation import StudentRecommendation
from app.schemas.student import (
    StudentListResponse,
    StudentDetailResponse,
    VocabMasteryResponse,
    MisusedWordResponse,
    BookRecommendationResponse,
)


def calculate_vocab_mastery_percent(student: Student, db: Session) -> float:
    """
    Calculate vocabulary mastery percentage for a student.
    
    Args:
        student: Student model instance
        db: Database session
        
    Returns:
        Percentage of grade-level vocabulary mastered (0-100)
    """
    # Get all vocabulary words for the student's grade level
    total_words = db.query(VocabularyWord).filter(
        VocabularyWord.grade_level == student.assigned_grade
    ).count()
    
    if total_words == 0:
        return 0.0
    
    # Count words mastered (used correctly at least once)
    words_mastered = db.query(StudentVocabulary).filter(
        StudentVocabulary.student_id == student.id,
        StudentVocabulary.correct_usage_count > 0
    ).count()
    
    return (words_mastered / total_words) * 100.0


def get_missing_words(student: Student, db: Session) -> List[str]:
    """
    Get list of vocabulary words student hasn't used correctly.
    
    Args:
        student: Student model instance
        db: Database session
        
    Returns:
        List of missing vocabulary words
    """
    # Get all vocabulary words for the student's grade level
    grade_words = db.query(VocabularyWord).filter(
        VocabularyWord.grade_level == student.assigned_grade
    ).all()
    
    # Get words student has used correctly
    student_vocab = db.query(StudentVocabulary).filter(
        StudentVocabulary.student_id == student.id,
        StudentVocabulary.correct_usage_count > 0
    ).all()
    
    known_word_ids = {sv.word_id for sv in student_vocab}
    
    # Find missing words
    missing_words = [
        word.word for word in grade_words
        if word.id not in known_word_ids
    ]
    
    return missing_words


def get_misused_words(student: Student, db: Session) -> List[MisusedWordResponse]:
    """
    Get list of words with misuse examples.
    
    Args:
        student: Student model instance
        db: Database session
        
    Returns:
        List of misused word responses
    """
    # Get student vocabulary with misuse examples
    student_vocab = db.query(StudentVocabulary).filter(
        StudentVocabulary.student_id == student.id,
        StudentVocabulary.misuse_examples.isnot(None)
    ).all()
    
    misused_words = []
    for sv in student_vocab:
        if sv.misuse_examples and len(sv.misuse_examples) > 0:
            # Get word details
            word = db.query(VocabularyWord).filter(
                VocabularyWord.id == sv.word_id
            ).first()
            
            if word:
                misused_words.append(MisusedWordResponse(
                    word=word.word,
                    correct_count=sv.correct_usage_count,
                    incorrect_count=sv.usage_count - sv.correct_usage_count,
                    example=sv.misuse_examples[0] if sv.misuse_examples else None
                ))
    
    return misused_words


def get_all_students(db: Session) -> List[StudentListResponse]:
    """
    Get all students with basic information including vocabulary mastery.
    
    Args:
        db: Database session
        
    Returns:
        List of student list responses
    """
    students = db.query(Student).all()
    
    result = []
    for student in students:
        vocab_mastery_percent = calculate_vocab_mastery_percent(student, db)
        
        result.append(StudentListResponse(
            id=student.id,
            name=student.name,
            reading_level=student.actual_reading_level,
            assigned_grade=student.assigned_grade,
            vocab_mastery_percent=vocab_mastery_percent
        ))
    
    return result


def get_student_by_id(db: Session, student_id: int) -> Optional[StudentDetailResponse]:
    """
    Get detailed student profile including vocabulary mastery, missing words, misused words, and book recommendations.
    
    Args:
        db: Database session
        student_id: Student ID
        
    Returns:
        Student detail response or None if student not found
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        return None
    
    # Calculate vocabulary mastery
    total_words = db.query(VocabularyWord).filter(
        VocabularyWord.grade_level == student.assigned_grade
    ).count()
    
    words_mastered = db.query(StudentVocabulary).filter(
        StudentVocabulary.student_id == student.id,
        StudentVocabulary.correct_usage_count > 0
    ).count()
    
    mastery_percent = (words_mastered / total_words * 100.0) if total_words > 0 else 0.0
    
    vocab_mastery = VocabMasteryResponse(
        total_grade_level_words=total_words,
        words_mastered=words_mastered,
        mastery_percent=mastery_percent
    )
    
    # Get missing words
    missing_words = get_missing_words(student, db)
    
    # Get misused words
    misused_words = get_misused_words(student, db)
    
    # Get book recommendations
    recommendations = db.query(StudentRecommendation).filter(
        StudentRecommendation.student_id == student.id
    ).order_by(StudentRecommendation.match_score.desc()).limit(3).all()
    
    book_recommendations = []
    for rec in recommendations:
        book = rec.book
        book_recommendations.append(BookRecommendationResponse(
            book_id=book.id,
            title=book.title,
            author=book.author,
            reading_level=book.reading_level,
            match_score=rec.match_score,
            known_words_percent=rec.known_words_percent,
            new_words_count=rec.new_words_count
        ))
    
    return StudentDetailResponse(
        id=student.id,
        name=student.name,
        reading_level=student.actual_reading_level,
        assigned_grade=student.assigned_grade,
        vocab_mastery=vocab_mastery,
        missing_words=missing_words,
        misused_words=misused_words,
        book_recommendations=book_recommendations
    )

