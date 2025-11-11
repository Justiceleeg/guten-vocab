#!/usr/bin/env python3
"""
Quick verification script to check if database has necessary data.
"""
import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.database import SessionLocal, init_db
from app.models import (
    Student,
    Book,
    VocabularyWord,
    StudentVocabulary,
    BookVocabulary,
)

def verify_prerequisites():
    """Check if database has necessary data for recommendations."""
    print("=" * 70)
    print("VERIFYING PREREQUISITES")
    print("=" * 70)
    
    init_db()
    db = SessionLocal()
    
    try:
        # Check vocabulary words
        vocab_count = db.query(VocabularyWord).count()
        print(f"\n📚 Vocabulary Words: {vocab_count}")
        if vocab_count == 0:
            print("   ❌ No vocabulary words found. Run: python scripts/seed_vocabulary.py")
            return False
        else:
            print("   ✅ Vocabulary words loaded")
        
        # Check books
        books_count = db.query(Book).count()
        print(f"\n📖 Books: {books_count}")
        if books_count == 0:
            print("   ❌ No books found. Run: python scripts/seed_books.py")
            return False
        else:
            print("   ✅ Books loaded")
        
        # Check book vocabulary
        book_vocab_count = db.query(BookVocabulary).count()
        print(f"\n📝 Book Vocabulary Records: {book_vocab_count}")
        if book_vocab_count == 0:
            print("   ❌ No book vocabulary found. Run: python scripts/seed_books.py")
            return False
        else:
            print("   ✅ Book vocabulary loaded")
        
        # Check students
        students_count = db.query(Student).count()
        print(f"\n👥 Students: {students_count}")
        if students_count == 0:
            print("   ❌ No students found. Run: python scripts/analyze_students.py")
            return False
        else:
            print("   ✅ Students loaded")
        
        # Check student vocabulary
        student_vocab_count = db.query(StudentVocabulary).filter(
            StudentVocabulary.correct_usage_count > 0
        ).count()
        print(f"\n📊 Student Vocabulary (known words): {student_vocab_count}")
        if student_vocab_count == 0:
            print("   ❌ No student vocabulary profiles found. Run: python scripts/analyze_students.py")
            return False
        else:
            print("   ✅ Student vocabulary profiles loaded")
        
        print("\n" + "=" * 70)
        print("✅ ALL PREREQUISITES MET")
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"\n❌ Error checking prerequisites: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    if verify_prerequisites():
        sys.exit(0)
    else:
        sys.exit(1)

