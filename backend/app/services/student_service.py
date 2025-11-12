"""
Student service for querying student data and calculating vocabulary metrics.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

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


def _get_baseline_mastery_percent(reading_level: int) -> float:
    """
    Get baseline mastery percentage based on reading level.
    
    Baseline assumptions for 7th grade vocabulary:
    - Reading level 5 (struggling): ~40% baseline mastery
    - Reading level 6 (below grade): ~55% baseline mastery
    - Reading level 7 (at grade): ~75% baseline mastery
    - Reading level 8 (above grade): ~85% baseline mastery
    
    Args:
        reading_level: Student's reading level (integer)
        
    Returns:
        Baseline mastery percentage (0.0-1.0)
    """
    baseline_percentages = {
        5: 0.40,
        6: 0.55,
        7: 0.75,
        8: 0.85,
    }
    return baseline_percentages.get(reading_level, 0.60)


def _calculate_baseline_words_known(
    student_id: int,
    grade_words: List[VocabularyWord],
    baseline_percent: float
) -> set:
    """
    Calculate baseline words known using deterministic hash.
    
    Args:
        student_id: Student ID
        grade_words: List of vocabulary words for the grade
        baseline_percent: Baseline mastery percentage (0.0-1.0)
        
    Returns:
        Set of word IDs that student knows at baseline
    """
    baseline_words_known = set()
    for word in grade_words:
        word_hash = hash(f"{student_id}_{word.id}") % 100
        if word_hash < (baseline_percent * 100):
            baseline_words_known.add(word.id)
    return baseline_words_known


def calculate_vocab_mastery_percent(student: Student, db: Session) -> float:
    """
    Calculate vocabulary mastery percentage for a student.
    
    This function assumes students have baseline knowledge based on their reading level
    relative to their assigned grade, and the transcript/essay data is additive
    (shows additional words they know beyond baseline).
    
    Baseline assumptions for 7th grade vocabulary:
    - Reading level 5 (struggling): ~40% baseline mastery of 7th grade words
    - Reading level 6 (below grade): ~55% baseline mastery of 7th grade words
    - Reading level 7 (at grade): ~75% baseline mastery of 7th grade words
    - Reading level 8 (above grade): ~85% baseline mastery of 7th grade words
    
    The transcript/essay data adds to this baseline, showing words they've demonstrated
    knowledge of beyond what we'd expect from their reading level alone.
    
    Args:
        student: Student model instance
        db: Database session
        
    Returns:
        Percentage of grade-level vocabulary mastered (0-100)
    """
    # Get all vocabulary words for the student's assigned grade level
    grade_words = db.query(VocabularyWord).filter(
        VocabularyWord.grade_level == student.assigned_grade
    ).all()
    
    total_words = len(grade_words)
    if total_words == 0:
        return 0.0
    
    # Get student's reading level (round to nearest integer)
    reading_level = int(round(student.actual_reading_level))
    
    # Get baseline percentage for student's reading level
    baseline_percent = _get_baseline_mastery_percent(reading_level)
    
    # Get words student has used correctly in transcript/essay
    student_vocab = db.query(StudentVocabulary).filter(
        StudentVocabulary.student_id == student.id,
        StudentVocabulary.correct_usage_count > 0
    ).all()
    
    used_word_ids = {sv.word_id for sv in student_vocab}
    
    # Calculate baseline words known (based on reading level)
    baseline_words_known = _calculate_baseline_words_known(
        student.id, grade_words, baseline_percent
    )
    
    # Combine baseline knowledge with words used in transcript/essay
    # Words from transcript/essay are additive (show knowledge beyond baseline)
    all_known_words = baseline_words_known | used_word_ids
    
    # Calculate mastery percentage
    words_mastered = len(all_known_words)
    mastery_percent = (words_mastered / total_words) * 100.0
    
    # Cap at 100% (shouldn't happen, but safety check)
    return min(100.0, mastery_percent)


def get_missing_words(student: Student, db: Session) -> List[str]:
    """
    Get list of vocabulary words student hasn't mastered.
    
    This uses the same baseline logic as calculate_vocab_mastery_percent:
    - Assumes baseline knowledge based on reading level
    - Adds words used correctly in transcript/essay
    - Missing words are those not in either set
    
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
    
    # Get student's reading level (round to nearest integer)
    reading_level = int(round(student.actual_reading_level))
    
    # Get baseline percentage for student's reading level
    baseline_percent = _get_baseline_mastery_percent(reading_level)
    
    # Get words student has used correctly in transcript/essay
    student_vocab = db.query(StudentVocabulary).filter(
        StudentVocabulary.student_id == student.id,
        StudentVocabulary.correct_usage_count > 0
    ).all()
    
    used_word_ids = {sv.word_id for sv in student_vocab}
    
    # Calculate baseline words known (same logic as calculate_vocab_mastery_percent)
    baseline_words_known = _calculate_baseline_words_known(
        student.id, grade_words, baseline_percent
    )
    
    # Combine baseline with words from transcript/essay
    all_known_word_ids = baseline_words_known | used_word_ids
    
    # Find missing words (not in baseline or transcript/essay)
    missing_words = [
        word.word for word in grade_words
        if word.id not in all_known_word_ids
    ]
    
    return missing_words


def get_misused_words(student: Student, db: Session) -> List[MisusedWordResponse]:
    """
    Get list of words with misuse examples (excluding dismissed words).
    
    Args:
        student: Student model instance
        db: Database session
        
    Returns:
        List of misused word responses (non-dismissed only)
    """
    # Get student vocabulary with misuse examples (exclude dismissed)
    student_vocab = db.query(StudentVocabulary).filter(
        StudentVocabulary.student_id == student.id,
        StudentVocabulary.misuse_examples.isnot(None),
        StudentVocabulary.dismissed == False  # Filter out dismissed words
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
                    word_id=sv.word_id,
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
    
    # Calculate vocabulary mastery using the updated function
    mastery_percent = calculate_vocab_mastery_percent(student, db)
    
    # Get total words and words mastered for response
    total_words = db.query(VocabularyWord).filter(
        VocabularyWord.grade_level == student.assigned_grade
    ).count()
    
    # Calculate words mastered (baseline + transcript/essay)
    # This matches the logic in calculate_vocab_mastery_percent
    reading_level = int(round(student.actual_reading_level))
    baseline_percent = _get_baseline_mastery_percent(reading_level)
    
    grade_words = db.query(VocabularyWord).filter(
        VocabularyWord.grade_level == student.assigned_grade
    ).all()
    
    student_vocab = db.query(StudentVocabulary).filter(
        StudentVocabulary.student_id == student.id,
        StudentVocabulary.correct_usage_count > 0
    ).all()
    used_word_ids = {sv.word_id for sv in student_vocab}
    
    baseline_words_known = _calculate_baseline_words_known(
        student.id, grade_words, baseline_percent
    )
    
    all_known_words = baseline_words_known | used_word_ids
    words_mastered = len(all_known_words)
    
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


def dismiss_vocabulary_issue(
    db: Session,
    student_id: int,
    word_id: int,
    reason: str
) -> Optional[datetime]:
    """
    Dismiss a vocabulary issue for a student.
    
    Args:
        db: Database session
        student_id: Student ID
        word_id: Vocabulary word ID
        reason: Dismissal reason ('addressed' or 'ai_error')
        
    Returns:
        Dismissal timestamp if successful, None if record not found
    """
    # Find the student vocabulary record
    student_vocab = db.query(StudentVocabulary).filter(
        StudentVocabulary.student_id == student_id,
        StudentVocabulary.word_id == word_id
    ).first()
    
    if not student_vocab:
        return None
    
    # Update dismissal fields
    dismissed_at = datetime.now()
    student_vocab.dismissed = True
    student_vocab.dismissed_reason = reason
    student_vocab.dismissed_at = dismissed_at
    
    db.commit()
    
    return dismissed_at

