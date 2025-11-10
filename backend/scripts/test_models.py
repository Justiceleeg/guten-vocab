#!/usr/bin/env python3
"""
Test SQLAlchemy models and relationships.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models import (
    Student,
    VocabularyWord,
    StudentVocabulary,
    Book,
    BookVocabulary,
    StudentRecommendation,
    ClassRecommendation,
)

def test_models():
    """Test creating and querying models."""
    print("Testing SQLAlchemy models...")
    
    # Initialize database (create tables if they don't exist)
    print("\n1. Initializing database...")
    init_db()
    print("   ✓ Database initialized")
    
    # Create a session
    db: Session = SessionLocal()
    
    try:
        # Test creating a student
        print("\n2. Creating test student...")
        student = Student(
            name="Test Student",
            actual_reading_level=6.5,
            assigned_grade=6,
        )
        db.add(student)
        db.commit()
        db.refresh(student)
        print(f"   ✓ Created student: {student}")
        
        # Test creating a vocabulary word
        print("\n3. Creating test vocabulary word...")
        word = VocabularyWord(
            word="test",
            grade_level=6,
        )
        db.add(word)
        db.commit()
        db.refresh(word)
        print(f"   ✓ Created vocabulary word: {word}")
        
        # Test creating student vocabulary relationship
        print("\n4. Creating student vocabulary relationship...")
        student_vocab = StudentVocabulary(
            student_id=student.id,
            word_id=word.id,
            usage_count=5,
            correct_usage_count=4,
        )
        db.add(student_vocab)
        db.commit()
        db.refresh(student_vocab)
        print(f"   ✓ Created student vocabulary: {student_vocab}")
        
        # Test relationship access
        print("\n5. Testing relationships...")
        student = db.query(Student).filter(Student.id == student.id).first()
        print(f"   ✓ Student has {len(student.student_vocabulary)} vocabulary entries")
        print(f"   ✓ First vocabulary word: {student.student_vocabulary[0].word.word}")
        
        word = db.query(VocabularyWord).filter(VocabularyWord.id == word.id).first()
        print(f"   ✓ Vocabulary word has {len(word.student_vocabulary)} student entries")
        
        # Test creating a book
        print("\n6. Creating test book...")
        book = Book(
            title="Test Book",
            author="Test Author",
            reading_level=6.0,
            total_words=1000,
        )
        db.add(book)
        db.commit()
        db.refresh(book)
        print(f"   ✓ Created book: {book}")
        
        # Test creating book vocabulary
        print("\n7. Creating book vocabulary...")
        book_vocab = BookVocabulary(
            book_id=book.id,
            word_id=word.id,
            occurrence_count=10,
        )
        db.add(book_vocab)
        db.commit()
        db.refresh(book_vocab)
        print(f"   ✓ Created book vocabulary: {book_vocab}")
        
        # Test book relationships
        print("\n8. Testing book relationships...")
        book = db.query(Book).filter(Book.id == book.id).first()
        print(f"   ✓ Book has {len(book.book_vocabulary)} vocabulary entries")
        
        # Test creating a recommendation
        print("\n9. Creating test recommendation...")
        recommendation = StudentRecommendation(
            student_id=student.id,
            book_id=book.id,
            match_score=0.85,
            known_words_percent=0.75,
            new_words_count=25,
        )
        db.add(recommendation)
        db.commit()
        db.refresh(recommendation)
        print(f"   ✓ Created recommendation: {recommendation}")
        
        # Test recommendation relationships
        print("\n10. Testing recommendation relationships...")
        student = db.query(Student).filter(Student.id == student.id).first()
        print(f"   ✓ Student has {len(student.recommendations)} recommendations")
        
        book = db.query(Book).filter(Book.id == book.id).first()
        print(f"   ✓ Book has {len(book.student_recommendations)} student recommendations")
        
        # Test class recommendation
        print("\n11. Creating class recommendation...")
        class_rec = ClassRecommendation(
            book_id=book.id,
            match_score=0.80,
            students_recommended_count=5,
        )
        db.add(class_rec)
        db.commit()
        db.refresh(class_rec)
        print(f"   ✓ Created class recommendation: {class_rec}")
        
        # Clean up test data
        print("\n12. Cleaning up test data...")
        db.delete(class_rec)
        db.delete(recommendation)
        db.delete(book_vocab)
        db.delete(book)
        db.delete(student_vocab)
        db.delete(word)
        db.delete(student)
        db.commit()
        print("   ✓ Test data cleaned up")
        
        print("\n✅ All model tests passed!")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    test_models()

