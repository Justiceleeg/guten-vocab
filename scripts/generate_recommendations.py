#!/usr/bin/env python3
"""
Generate personalized book recommendations for students.

This script:
- Calculates vocabulary overlap between students and books
- Matches students to books with optimal challenge (~50% known, ~50% new)
- Considers reading level appropriateness
- Stores top 3 recommendations per student
- Aggregates class-wide recommendations
"""
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Add backend directory to path to import app modules
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import SessionLocal, init_db
from app.models import (
    Student,
    Book,
    VocabularyWord,
    StudentVocabulary,
    BookVocabulary,
    StudentRecommendation,
    ClassRecommendation,
)


# ============================================================================
# TASK 1.1: Student-Book Matching Algorithm
# ============================================================================

def get_student_vocabulary_profile(db: Session, student_id: int) -> Dict[int, int]:
    """
    Get student's vocabulary profile (known words).
    
    This includes:
    - Words used correctly in transcript/essay (correct_usage_count > 0)
    - Baseline words based on reading level (assumed knowledge)
    - Prerequisite grade levels: Students know ~95% of words from grades below their assigned grade
    
    For a 7th grader:
    - ~95% of 5th grade words (prerequisite)
    - ~95% of 6th grade words (prerequisite)
    - ~75% of 7th grade words (current grade, based on reading level)
    - ~0% of 8th grade words (future grade, unless advanced)
    
    Args:
        db: Database session
        student_id: Student ID
        
    Returns:
        Dictionary mapping word_id -> usage_count (1 for baseline words, actual count for used words)
    """
    # Get student info
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return {}
    
    # Get words used correctly in transcript/essay
    student_vocab = db.query(StudentVocabulary).filter(
        StudentVocabulary.student_id == student_id,
        StudentVocabulary.correct_usage_count > 0
    ).all()
    
    used_words = {sv.word_id: sv.correct_usage_count for sv in student_vocab}
    
    # Get baseline words based on reading level
    reading_level = int(round(student.actual_reading_level))
    assigned_grade = student.assigned_grade
    
    # Baseline percentages for current grade based on reading level
    current_grade_baseline_percentages = {
        5: 0.40,
        6: 0.55,
        7: 0.75,
        8: 0.85,
    }
    current_grade_baseline = current_grade_baseline_percentages.get(reading_level, 0.60)
    
    # Prerequisite grade baseline (students should know most/all prerequisite words)
    prerequisite_baseline = 0.95  # 95% of prerequisite grade words
    
    # Get all vocabulary words for prerequisite grades and current grade
    # For a 7th grader, this includes 5th, 6th, and 7th grade words
    all_grade_words = db.query(VocabularyWord).filter(
        VocabularyWord.grade_level <= assigned_grade
    ).all()
    
    # Calculate baseline words known
    baseline_words = {}
    for word in all_grade_words:
        word_grade = word.grade_level
        
        # Prerequisite grades: assume high baseline knowledge
        if word_grade < assigned_grade:
            word_hash = hash(f"{student_id}_{word.id}") % 100
            if word_hash < (prerequisite_baseline * 100):
                baseline_words[word.id] = 1
        
        # Current grade: baseline varies by reading level
        elif word_grade == assigned_grade:
            word_hash = hash(f"{student_id}_{word.id}") % 100
            if word_hash < (current_grade_baseline * 100):
                baseline_words[word.id] = 1
    
    # Combine baseline words with words from transcript/essay
    # Words from transcript/essay take precedence (use actual count)
    all_known_words = {**baseline_words, **used_words}
    
    return all_known_words


def get_book_vocabulary(db: Session, book_id: int) -> Dict[int, int]:
    """
    Get vocabulary words in a book.
    
    Args:
        db: Database session
        book_id: Book ID
        
    Returns:
        Dictionary mapping word_id -> occurrence_count
    """
    book_vocab = db.query(BookVocabulary).filter(
        BookVocabulary.book_id == book_id
    ).all()
    
    return {bv.word_id: bv.occurrence_count for bv in book_vocab}


def calculate_vocabulary_overlap(
    student_vocab: Dict[int, int],
    book_vocab: Dict[int, int]
) -> Tuple[set, set, float]:
    """
    Calculate vocabulary overlap between student and book.
    
    Args:
        student_vocab: Dictionary of word_id -> correct_usage_count (known words)
        book_vocab: Dictionary of word_id -> occurrence_count (words in book)
        
    Returns:
        Tuple of:
        - known_words: set of word_ids that student knows and are in book
        - new_words: set of word_ids in book but not known by student
        - overlap_percent: percentage of book vocab that student knows
    """
    book_word_ids = set(book_vocab.keys())
    student_known_word_ids = set(student_vocab.keys())
    
    known_words = book_word_ids & student_known_word_ids
    new_words = book_word_ids - student_known_word_ids
    
    total_vocab_words = len(book_word_ids)
    if total_vocab_words == 0:
        overlap_percent = 0.0
    else:
        overlap_percent = len(known_words) / total_vocab_words
    
    return known_words, new_words, overlap_percent


def calculate_match_score(
    known_percent: float,
    new_words_count: int,
    book_reading_level: Optional[float],
    student_reading_level: float
) -> float:
    """
    Calculate match score for a book-student pair.
    
    Strategy: Optimize for both high percentage of known words AND high count of new words.
    This ensures students can comprehend the book (high % known) while learning new vocabulary (high count of new words).
    
    Algorithm:
    - Reward higher percentage of known words (for comprehension/confidence)
    - Reward higher count of new words (for vocabulary expansion)
    - Penalize if too easy (>85% known) or too hard (<40% known)
    - Apply reading level bonus (prefers books at student's level ± 1 grade)
    
    Args:
        known_percent: Percentage of book vocabulary that student knows (0-1)
        new_words_count: Number of new vocabulary words in the book
        book_reading_level: Book's reading level (grade level)
        student_reading_level: Student's reading level (grade level)
        
    Returns:
        Match score between 0 and 1
    """
    known_percent = max(0.0, min(1.0, known_percent))  # Clamp to [0, 1]
    
    # Penalize if too easy (>85% known) or too hard (<40% known)
    if known_percent > 0.85:
        # Too easy - heavy penalty
        penalty = (known_percent - 0.85) * 3
    elif known_percent < 0.40:
        # Too hard - heavy penalty
        penalty = (0.40 - known_percent) * 3
    else:
        penalty = 0
    
    # Reward higher percentage of known words (for comprehension)
    # Optimal range: 50-75% known, with more granular scoring
    # Use a continuous function to create more differentiation
    if 0.50 <= known_percent <= 0.75:
        # Optimal range: score based on how close to 62.5% (middle of optimal range)
        optimal_target = 0.625
        distance_from_optimal = abs(known_percent - optimal_target)
        # Score decreases as we move away from optimal, but stays high in range
        known_score = 1.0 - (distance_from_optimal / 0.125) * 0.15  # Scale from 1.0 to 0.85
    elif known_percent < 0.50:
        # Below optimal, but still acceptable (40-50%)
        known_score = 0.7 + (known_percent - 0.40) / 0.10 * 0.15  # Scale from 0.7 to 0.85
    else:
        # Above optimal but acceptable (75-85%)
        known_score = 1.0 - ((known_percent - 0.75) / 0.10) * 0.2  # Scale from 1.0 to 0.8
    
    # Reward higher count of new words (for vocabulary expansion)
    # Use a more gradual scaling to create differentiation
    # Optimal: 20-40 new words, with diminishing returns beyond 40
    if new_words_count >= 40:
        new_words_score = 1.0
    elif new_words_count >= 20:
        # Scale from 0.85 to 1.0 for 20-40 new words
        new_words_score = 0.85 + (new_words_count - 20) / 20 * 0.15
    elif new_words_count >= 10:
        new_words_score = 0.7 + (new_words_count - 10) / 10 * 0.15  # Scale from 0.7 to 0.85
    elif new_words_count >= 5:
        new_words_score = 0.4 + (new_words_count - 5) / 5 * 0.3  # Scale from 0.4 to 0.7
    else:
        new_words_score = new_words_count / 5 * 0.4  # Scale from 0 to 0.4
    
    # Reading level match bonus
    if book_reading_level is not None:
        reading_level_diff = abs(book_reading_level - student_reading_level)
        reading_level_score = max(0, 1 - (reading_level_diff / 2))
    else:
        # If book has no reading level, give neutral score
        reading_level_score = 0.5
    
    # Combine factors with weights:
    # - 40% weight on known words percentage (comprehension)
    # - 40% weight on new words count (vocabulary expansion)
    # - 20% weight on reading level match
    match_score = (known_score * 0.4) + (new_words_score * 0.4) + (reading_level_score * 0.2) - penalty
    match_score = max(0, min(1, match_score))  # Clamp to [0, 1]
    
    return match_score


def match_student_to_books(
    db: Session,
    student: Student,
    all_books: List[Book]
) -> List[Tuple[Book, float, float, int]]:
    """
    Match a student to all books and return sorted results.
    
    Args:
        db: Database session
        student: Student object
        all_books: List of all Book objects
        
    Returns:
        List of tuples: (book, match_score, known_words_percent, new_words_count)
        Sorted by match_score (descending)
    """
    # Get student's vocabulary profile
    student_vocab = get_student_vocabulary_profile(db, student.id)
    
    # Get student's reading level
    student_reading_level = student.actual_reading_level
    
    matches = []
    
    for book in all_books:
        # Get book vocabulary
        book_vocab = get_book_vocabulary(db, book.id)
        
        if not book_vocab:
            # Skip books with no vocabulary data
            continue
        
        # Calculate vocabulary overlap
        known_words, new_words, overlap_percent = calculate_vocabulary_overlap(
            student_vocab, book_vocab
        )
        
        # Filter by reading level (prefer books at student's level ± 1 grade)
        # Allow higher if vocabulary fit is exceptional (handled by match score)
        book_reading_level = book.reading_level
        
        # Store match information
        known_words_percent = overlap_percent
        new_words_count = len(new_words)
        
        # Calculate match score (now includes new_words_count)
        match_score = calculate_match_score(
            known_words_percent,
            new_words_count,
            book_reading_level,
            student_reading_level
        )
        
        matches.append((book, match_score, known_words_percent, new_words_count))
    
    # Sort by match score (descending)
    matches.sort(key=lambda x: x[1], reverse=True)
    
    return matches


def generate_student_recommendations(db: Session) -> Dict:
    """
    Generate recommendations for all students.
    
    Returns:
        Dictionary with statistics
    """
    print("\n" + "=" * 70)
    print("PHASE 1: Student-Book Matching")
    print("=" * 70)
    
    # Get all students
    students = db.query(Student).all()
    total_students = len(students)
    
    if total_students == 0:
        print("❌ No students found in database")
        return {"error": "No students found"}
    
    # Get all books
    books = db.query(Book).all()
    total_books = len(books)
    
    if total_books == 0:
        print("❌ No books found in database")
        return {"error": "No books found"}
    
    print(f"📚 Processing {total_students} students against {total_books} books...")
    
    all_matches = {}
    processed = 0
    
    for student in students:
        processed += 1
        print(f"\n[{processed}/{total_students}] Processing {student.name}...")
        
        # Match student to books
        matches = match_student_to_books(db, student, books)
        
        if not matches:
            print(f"  ⚠️  No matches found for {student.name}")
            continue
        
        # Store top 3 matches
        top_3 = matches[:3]
        all_matches[student.id] = top_3
        
        print(f"  ✅ Top 3 recommendations:")
        for i, (book, score, known_pct, new_count) in enumerate(top_3, 1):
            print(f"     {i}. {book.title[:50]}: score={score:.3f}, "
                  f"known={known_pct:.1%}, new_words={new_count}")
    
    return {
        "students_processed": processed,
        "total_students": total_students,
        "total_books": total_books,
        "matches": all_matches
    }


# ============================================================================
# TASK 1.2: Store Student Recommendations
# ============================================================================

def store_student_recommendations(
    db: Session,
    matches: Dict[int, List[Tuple[Book, float, float, int]]]
) -> Dict:
    """
    Store top 3 recommendations for each student in database.
    
    Args:
        db: Database session
        matches: Dictionary mapping student_id -> list of (book, score, known_pct, new_count) tuples
        
    Returns:
        Dictionary with statistics
    """
    print("\n" + "=" * 70)
    print("PHASE 2: Store Student Recommendations")
    print("=" * 70)
    
    total_inserted = 0
    total_updated = 0
    students_with_recommendations = 0
    
    for student_id, top_3 in matches.items():
        if not top_3:
            continue
        
        students_with_recommendations += 1
        
        for rank, (book, match_score, known_words_percent, new_words_count) in enumerate(top_3, 1):
            # Check if recommendation already exists
            existing = db.query(StudentRecommendation).filter(
                StudentRecommendation.student_id == student_id,
                StudentRecommendation.book_id == book.id
            ).first()
            
            if existing:
                # Update existing recommendation
                existing.match_score = match_score
                existing.known_words_percent = known_words_percent
                existing.new_words_count = new_words_count
                total_updated += 1
            else:
                # Insert new recommendation
                recommendation = StudentRecommendation(
                    student_id=student_id,
                    book_id=book.id,
                    match_score=match_score,
                    known_words_percent=known_words_percent,
                    new_words_count=new_words_count
                )
                db.add(recommendation)
                total_inserted += 1
        
        # Commit after each student to handle errors gracefully
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            print(f"  ⚠️  Error storing recommendations for student {student_id}: {e}")
            continue
    
    print(f"\n✅ Stored recommendations for {students_with_recommendations} students")
    print(f"   Inserted: {total_inserted} recommendations")
    print(f"   Updated: {total_updated} recommendations")
    
    return {
        "students_with_recommendations": students_with_recommendations,
        "total_inserted": total_inserted,
        "total_updated": total_updated
    }


def verify_student_recommendations(db: Session) -> Dict:
    """
    Verify student recommendations make sense.
    
    Returns:
        Dictionary with verification results
    """
    print("\n" + "=" * 70)
    print("VERIFICATION: Student Recommendations")
    print("=" * 70)
    
    # Get all students
    students = db.query(Student).all()
    
    # Find student with highest vocabulary mastery
    highest_mastery = None
    highest_mastery_count = 0
    
    # Find student with lowest vocabulary mastery
    lowest_mastery = None
    lowest_mastery_count = float('inf')
    
    for student in students:
        student_vocab = db.query(StudentVocabulary).filter(
            StudentVocabulary.student_id == student.id,
            StudentVocabulary.correct_usage_count > 0
        ).count()
        
        if student_vocab > highest_mastery_count:
            highest_mastery_count = student_vocab
            highest_mastery = student
        
        if student_vocab < lowest_mastery_count:
            lowest_mastery_count = student_vocab
            lowest_mastery = student
    
    verification_results = {
        "total_students": len(students),
        "students_with_recommendations": 0,
        "recommendations_count": 0,
        "high_proficiency_check": {},
        "low_proficiency_check": {},
        "score_range_check": {"min": 1.0, "max": 0.0, "all_valid": True}
    }
    
    # Count recommendations
    all_recommendations = db.query(StudentRecommendation).all()
    verification_results["recommendations_count"] = len(all_recommendations)
    verification_results["students_with_recommendations"] = len(
        set(rec.student_id for rec in all_recommendations)
    )
    
    # Check score ranges
    for rec in all_recommendations:
        if rec.match_score < verification_results["score_range_check"]["min"]:
            verification_results["score_range_check"]["min"] = rec.match_score
        if rec.match_score > verification_results["score_range_check"]["max"]:
            verification_results["score_range_check"]["max"] = rec.match_score
        if not (0 <= rec.match_score <= 1):
            verification_results["score_range_check"]["all_valid"] = False
    
    # Check high proficiency student
    if highest_mastery:
        high_recs = db.query(StudentRecommendation).filter(
            StudentRecommendation.student_id == highest_mastery.id
        ).order_by(StudentRecommendation.match_score.desc()).all()
        
        if high_recs:
            verification_results["high_proficiency_check"] = {
                "student": highest_mastery.name,
                "vocab_mastery": highest_mastery_count,
                "recommendations": [
                    {
                        "book": rec.book.title,
                        "score": rec.match_score,
                        "known_pct": rec.known_words_percent,
                        "new_words": rec.new_words_count
                    }
                    for rec in high_recs[:3]
                ]
            }
    
    # Check low proficiency student
    if lowest_mastery:
        low_recs = db.query(StudentRecommendation).filter(
            StudentRecommendation.student_id == lowest_mastery.id
        ).order_by(StudentRecommendation.match_score.desc()).all()
        
        if low_recs:
            verification_results["low_proficiency_check"] = {
                "student": lowest_mastery.name,
                "vocab_mastery": lowest_mastery_count,
                "recommendations": [
                    {
                        "book": rec.book.title,
                        "score": rec.match_score,
                        "known_pct": rec.known_words_percent,
                        "new_words": rec.new_words_count
                    }
                    for rec in low_recs[:3]
                ]
            }
    
    # Print verification results
    print(f"\n📊 Verification Results:")
    print(f"   Total students: {verification_results['total_students']}")
    print(f"   Students with recommendations: {verification_results['students_with_recommendations']}")
    print(f"   Total recommendations: {verification_results['recommendations_count']}")
    print(f"   Expected: {verification_results['total_students'] * 3}")
    
    print(f"\n📈 Score Range:")
    print(f"   Min: {verification_results['score_range_check']['min']:.3f}")
    print(f"   Max: {verification_results['score_range_check']['max']:.3f}")
    print(f"   All in [0, 1]: {'✅' if verification_results['score_range_check']['all_valid'] else '❌'}")
    
    if verification_results["high_proficiency_check"]:
        check = verification_results["high_proficiency_check"]
        print(f"\n🎓 High Proficiency Student: {check['student']}")
        print(f"   Vocabulary mastery: {check['vocab_mastery']} words")
        print(f"   Top recommendations:")
        for i, rec in enumerate(check['recommendations'], 1):
            print(f"     {i}. {rec['book'][:50]}: score={rec['score']:.3f}, "
                  f"known={rec['known_pct']:.1%}, new_words={rec['new_words']}")
    
    if verification_results["low_proficiency_check"]:
        check = verification_results["low_proficiency_check"]
        print(f"\n📚 Low Proficiency Student: {check['student']}")
        print(f"   Vocabulary mastery: {check['vocab_mastery']} words")
        print(f"   Top recommendations:")
        for i, rec in enumerate(check['recommendations'], 1):
            print(f"     {i}. {rec['book'][:50]}: score={rec['score']:.3f}, "
                  f"known={rec['known_pct']:.1%}, new_words={rec['new_words']}")
    
    return verification_results


# ============================================================================
# TASK 1.3: Class-Wide Recommendations
# ============================================================================

def generate_class_recommendations(db: Session) -> Dict:
    """
    Aggregate individual recommendations to identify top 2 books for class-wide reading.
    
    Returns:
        Dictionary with statistics
    """
    print("\n" + "=" * 70)
    print("PHASE 3: Class-Wide Recommendations")
    print("=" * 70)
    
    # Get all student recommendations
    all_recommendations = db.query(StudentRecommendation).all()
    
    if not all_recommendations:
        print("❌ No student recommendations found")
        return {"error": "No student recommendations found"}
    
    # Aggregate by book
    book_stats = {}  # book_id -> {count, total_score, students}
    
    for rec in all_recommendations:
        book_id = rec.book_id
        
        if book_id not in book_stats:
            book_stats[book_id] = {
                "count": 0,
                "total_score": 0.0,
                "students": set()
            }
        
        book_stats[book_id]["count"] += 1
        book_stats[book_id]["total_score"] += rec.match_score
        book_stats[book_id]["students"].add(rec.student_id)
    
    # Calculate average scores and prepare for sorting
    book_aggregates = []
    for book_id, stats in book_stats.items():
        avg_score = stats["total_score"] / stats["count"]
        students_count = len(stats["students"])
        
        book_aggregates.append({
            "book_id": book_id,
            "students_recommended_count": students_count,
            "average_match_score": avg_score,
            "total_recommendations": stats["count"]
        })
    
    # Sort by students_recommended_count (descending), then by average_match_score (descending)
    book_aggregates.sort(
        key=lambda x: (x["students_recommended_count"], x["average_match_score"]),
        reverse=True
    )
    
    # Select top 2
    top_2 = book_aggregates[:2]
    
    print(f"\n📚 Top 2 class-wide recommendations:")
    for i, book_info in enumerate(top_2, 1):
        book = db.query(Book).filter(Book.id == book_info["book_id"]).first()
        if book:
            print(f"   {i}. {book.title[:60]}")
            print(f"      Recommended to {book_info['students_recommended_count']} students")
            print(f"      Average match score: {book_info['average_match_score']:.3f}")
    
    return {
        "top_2_books": top_2,
        "total_books_recommended": len(book_stats)
    }


def store_class_recommendations(db: Session, top_2: List[Dict]) -> Dict:
    """
    Store top 2 class-wide recommendations in database.
    
    Args:
        db: Database session
        top_2: List of book aggregate dictionaries
        
    Returns:
        Dictionary with statistics
    """
    print("\n" + "=" * 70)
    print("PHASE 4: Store Class Recommendations")
    print("=" * 70)
    
    total_inserted = 0
    total_updated = 0
    
    for book_info in top_2:
        book_id = book_info["book_id"]
        
        # Check if class recommendation already exists
        existing = db.query(ClassRecommendation).filter(
            ClassRecommendation.book_id == book_id
        ).first()
        
        if existing:
            # Update existing recommendation
            existing.match_score = book_info["average_match_score"]
            existing.students_recommended_count = book_info["students_recommended_count"]
            total_updated += 1
        else:
            # Insert new recommendation
            recommendation = ClassRecommendation(
                book_id=book_id,
                match_score=book_info["average_match_score"],
                students_recommended_count=book_info["students_recommended_count"]
            )
            db.add(recommendation)
            total_inserted += 1
    
    try:
        db.commit()
        print(f"\n✅ Stored class-wide recommendations")
        print(f"   Inserted: {total_inserted} recommendations")
        print(f"   Updated: {total_updated} recommendations")
    except IntegrityError as e:
        db.rollback()
        print(f"  ❌ Error storing class recommendations: {e}")
        return {"error": str(e)}
    
    return {
        "total_inserted": total_inserted,
        "total_updated": total_updated
    }


def run_recommendation_engine():
    """
    Run the complete recommendation engine pipeline.
    """
    print("=" * 70)
    print("Book Recommendation Engine")
    print("=" * 70)
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # Phase 1: Generate student recommendations
        result = generate_student_recommendations(db)
        
        if "error" in result:
            print(f"\n❌ Error: {result['error']}")
            sys.exit(1)
        
        # Phase 2: Store student recommendations
        store_result = store_student_recommendations(db, result["matches"])
        
        if "error" in store_result:
            print(f"\n❌ Error storing recommendations: {store_result['error']}")
            sys.exit(1)
        
        # Verification: Check student recommendations
        verify_result = verify_student_recommendations(db)
        
        # Phase 3: Generate class-wide recommendations
        class_result = generate_class_recommendations(db)
        
        if "error" in class_result:
            print(f"\n❌ Error: {class_result['error']}")
            sys.exit(1)
        
        # Phase 4: Store class recommendations
        class_store_result = store_class_recommendations(db, class_result["top_2_books"])
        
        if "error" in class_store_result:
            print(f"\n❌ Error storing class recommendations: {class_store_result['error']}")
            sys.exit(1)
        
        # Final verification
        print("\n" + "=" * 70)
        print("FINAL VERIFICATION")
        print("=" * 70)
        
        # Count student recommendations
        student_rec_count = db.query(StudentRecommendation).count()
        expected_student_rec = result["total_students"] * 3
        print(f"\n📊 Student Recommendations:")
        print(f"   Expected: {expected_student_rec} (25 students × 3)")
        print(f"   Actual: {student_rec_count}")
        if student_rec_count == expected_student_rec:
            print(f"   ✅ Count matches expected")
        else:
            print(f"   ⚠️  Count differs from expected (some students may have fewer than 3 matches)")
        
        # Count class recommendations
        class_rec_count = db.query(ClassRecommendation).count()
        print(f"\n📚 Class Recommendations:")
        print(f"   Expected: 2")
        print(f"   Actual: {class_rec_count}")
        if class_rec_count == 2:
            print(f"   ✅ Count matches expected")
        else:
            print(f"   ⚠️  Count differs from expected")
        
        # Final summary
        print("\n" + "=" * 70)
        print("✅ RECOMMENDATION ENGINE COMPLETE!")
        print("=" * 70)
        print(f"\n📊 Final Summary:")
        print(f"   Students processed: {result['students_processed']}")
        print(f"   Total books: {result['total_books']}")
        print(f"   Student recommendations stored: {student_rec_count}")
        print(f"   Class recommendations stored: {class_rec_count}")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    run_recommendation_engine()

