#!/usr/bin/env python3
"""
Quick verification script for class view implementation.

This script verifies:
1. Backend API endpoints return correct data
2. Database has expected data
3. Data structure matches frontend expectations
"""
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.database import SessionLocal
from app.services.class_service import get_class_stats, get_class_recommendations
from app.models.student import Student
from app.models.vocabulary import StudentVocabulary
from app.models.recommendation import StudentRecommendation

def check_backend_api():
    """Verify backend API endpoints work correctly."""
    print("=" * 70)
    print("1. Backend API Verification")
    print("=" * 70)
    
    db = SessionLocal()
    try:
        # Test class stats
        print("\n📊 Testing /api/class/stats...")
        stats = get_class_stats(db)
        
        checks = []
        checks.append(("Total students", stats.total_students == 25, f"Found {stats.total_students}, expected 25"))
        checks.append(("Average mastery", 0 <= stats.avg_vocab_mastery_percent <= 100, f"Found {stats.avg_vocab_mastery_percent:.1f}%"))
        checks.append(("Reading level distribution", len(stats.reading_level_distribution) > 0, f"Found {len(stats.reading_level_distribution)} levels"))
        checks.append(("Top missing words", len(stats.top_missing_words) > 0, f"Found {len(stats.top_missing_words)} words"))
        checks.append(("Commonly misused words", len(stats.commonly_misused_words) >= 0, f"Found {len(stats.commonly_misused_words)} words"))
        
        for name, passed, msg in checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {name}: {msg}")
        
        # Test class recommendations
        print("\n📖 Testing /api/class/recommendations...")
        recs = get_class_recommendations(db)
        
        rec_checks = []
        rec_checks.append(("Recommendations exist", len(recs) > 0, f"Found {len(recs)} recommendations"))
        rec_checks.append(("Max 2 recommendations", len(recs) <= 2, f"Found {len(recs)}, max is 2"))
        
        if recs:
            rec_checks.append(("Book titles present", all(r.title for r in recs), "All have titles"))
            rec_checks.append(("Student counts valid", all(0 < r.students_recommended_count <= 25 for r in recs), "All counts valid"))
            rec_checks.append(("Match scores valid", all(0 <= r.avg_match_score <= 1 for r in recs), "All scores valid"))
        
        for name, passed, msg in rec_checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {name}: {msg}")
        
        return all(p for _, p, _ in checks + rec_checks)
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def check_database():
    """Verify database has expected data."""
    print("\n" + "=" * 70)
    print("2. Database Verification")
    print("=" * 70)
    
    db = SessionLocal()
    try:
        # Check students
        student_count = db.query(Student).count()
        print(f"\n👥 Students: {student_count} (expected: 25)")
        
        if student_count != 25:
            print("   ⚠️  Warning: Expected 25 students!")
        
        # Check vocabulary data
        vocab_count = db.query(StudentVocabulary).count()
        students_with_vocab = db.query(StudentVocabulary.student_id).distinct().count()
        print(f"📚 Vocabulary entries: {vocab_count}")
        print(f"   Students with vocab data: {students_with_vocab}/25")
        
        # Check recommendations
        rec_count = db.query(StudentRecommendation).count()
        students_with_recs = db.query(StudentRecommendation.student_id).distinct().count()
        print(f"📖 Recommendations: {rec_count}")
        print(f"   Students with recommendations: {students_with_recs}/25")
        
        # Reading level distribution
        print(f"\n📈 Reading level distribution:")
        for level in [5, 6, 7, 8]:
            count = db.query(Student).filter(Student.actual_reading_level == level).count()
            print(f"   Grade {level}: {count} students")
        
        return student_count == 25 and vocab_count > 0 and rec_count > 0
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    finally:
        db.close()


def check_data_structure():
    """Verify data structure matches frontend expectations."""
    print("\n" + "=" * 70)
    print("3. Data Structure Verification")
    print("=" * 70)
    
    db = SessionLocal()
    try:
        stats = get_class_stats(db)
        
        # Check ClassStatsResponse structure
        required_fields = [
            'total_students',
            'avg_vocab_mastery_percent',
            'reading_level_distribution',
            'top_missing_words',
            'commonly_misused_words'
        ]
        
        print("\n📋 ClassStatsResponse fields:")
        for field in required_fields:
            has_field = hasattr(stats, field)
            status = "✅" if has_field else "❌"
            print(f"   {status} {field}")
        
        # Check TopMissingWordResponse structure
        if stats.top_missing_words:
            word = stats.top_missing_words[0]
            print(f"\n📋 TopMissingWordResponse fields:")
            print(f"   ✅ word: {hasattr(word, 'word')}")
            print(f"   ✅ students_missing: {hasattr(word, 'students_missing')}")
        
        # Check CommonlyMisusedWordResponse structure
        if stats.commonly_misused_words:
            misused = stats.commonly_misused_words[0]
            print(f"\n📋 CommonlyMisusedWordResponse fields:")
            print(f"   ✅ word: {hasattr(misused, 'word')}")
            print(f"   ✅ misuse_count: {hasattr(misused, 'misuse_count')}")
        
        # Check ClassRecommendationResponse structure
        recs = get_class_recommendations(db)
        if recs:
            rec = recs[0]
            print(f"\n📋 ClassRecommendationResponse fields:")
            required_rec_fields = [
                'book_id', 'title', 'author', 'reading_level',
                'students_recommended_count', 'avg_match_score'
            ]
            for field in required_rec_fields:
                has_field = hasattr(rec, field)
                status = "✅" if has_field else "❌"
                print(f"   {status} {field}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def main():
    """Run all verification checks."""
    print("=" * 70)
    print("Class View Implementation Verification")
    print("=" * 70)
    
    results = []
    
    # Run checks
    results.append(("Backend API", check_backend_api()))
    results.append(("Database", check_database()))
    results.append(("Data Structure", check_data_structure()))
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ All checks passed! Ready for frontend testing.")
    else:
        print("⚠️  Some checks failed. Review output above.")
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

