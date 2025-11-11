"""
Class service for aggregating class-wide statistics.
"""
from typing import Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import defaultdict

from app.models.student import Student
from app.models.vocabulary import VocabularyWord, StudentVocabulary
from app.models.recommendation import ClassRecommendation
from app.schemas.class_schemas import (
    ClassStatsResponse,
    TopMissingWordResponse,
    CommonlyMisusedWordResponse,
    ClassRecommendationResponse,
)
from app.services.student_service import calculate_vocab_mastery_percent


def get_class_stats(db: Session) -> ClassStatsResponse:
    """
    Aggregate class-wide statistics.
    
    Args:
        db: Database session
        
    Returns:
        Class stats response
    """
    # Get all students
    students = db.query(Student).all()
    total_students = len(students)
    
    if total_students == 0:
        return ClassStatsResponse(
            total_students=0,
            avg_vocab_mastery_percent=0.0,
            reading_level_distribution={},
            top_missing_words=[],
            commonly_misused_words=[]
        )
    
    # Calculate average vocabulary mastery
    total_mastery = 0.0
    reading_level_distribution = defaultdict(int)
    word_missing_count = defaultdict(int)  # word_id -> count of students missing it
    word_misuse_count = defaultdict(int)  # word_id -> count of students misusing it
    
    # Get all vocabulary words
    vocab_words = db.query(VocabularyWord).all()
    
    for student in students:
        # Calculate mastery for each student
        mastery_percent = calculate_vocab_mastery_percent(student, db)
        total_mastery += mastery_percent
        
        # Track reading level distribution
        reading_level_key = str(int(student.actual_reading_level))
        reading_level_distribution[reading_level_key] += 1
        
        # Track missing words
        student_vocab = db.query(StudentVocabulary).filter(
            StudentVocabulary.student_id == student.id
        ).all()
        
        known_word_ids = {sv.word_id for sv in student_vocab if sv.correct_usage_count > 0}
        for word in vocab_words:
            if word.id not in known_word_ids:
                word_missing_count[word.id] += 1
        
        # Track misused words
        for sv in student_vocab:
            if sv.misuse_examples and len(sv.misuse_examples) > 0:
                word_misuse_count[sv.word_id] += 1
    
    avg_mastery = total_mastery / total_students if total_students > 0 else 0.0
    
    # Get top 10 missing words
    top_missing = sorted(word_missing_count.items(), key=lambda x: x[1], reverse=True)[:10]
    top_missing_words = []
    for word_id, count in top_missing:
        word = db.query(VocabularyWord).filter(VocabularyWord.id == word_id).first()
        if word:
            top_missing_words.append(TopMissingWordResponse(
                word=word.word,
                students_missing=count
            ))
    
    # Get top 10 commonly misused words
    top_misused = sorted(word_misuse_count.items(), key=lambda x: x[1], reverse=True)[:10]
    commonly_misused = []
    for word_id, count in top_misused:
        word = db.query(VocabularyWord).filter(VocabularyWord.id == word_id).first()
        if word:
            # Calculate total misuse count across all students
            total_misuse_count = db.query(StudentVocabulary).filter(
                StudentVocabulary.word_id == word_id,
                StudentVocabulary.misuse_examples.isnot(None)
            ).count()
            
            commonly_misused.append(CommonlyMisusedWordResponse(
                word=word.word,
                misuse_count=total_misuse_count
            ))
    
    return ClassStatsResponse(
        total_students=total_students,
        avg_vocab_mastery_percent=avg_mastery,
        reading_level_distribution=dict(reading_level_distribution),
        top_missing_words=top_missing_words,
        commonly_misused_words=commonly_misused
    )


def get_class_recommendations(db: Session) -> List[ClassRecommendationResponse]:
    """
    Get top 2 class-wide book recommendations.
    
    Args:
        db: Database session
        
    Returns:
        List of class recommendation responses (max 2)
    """
    recommendations = db.query(ClassRecommendation).order_by(
        ClassRecommendation.match_score.desc()
    ).limit(2).all()
    
    result = []
    for rec in recommendations:
        book = rec.book
        result.append(ClassRecommendationResponse(
            book_id=book.id,
            title=book.title,
            author=book.author,
            reading_level=book.reading_level,
            students_recommended_count=rec.students_recommended_count,
            avg_match_score=rec.match_score
        ))
    
    return result

