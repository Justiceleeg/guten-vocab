#!/usr/bin/env python3
"""
Verify recommendations were stored correctly in database.
"""
import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.database import SessionLocal, init_db
from app.models import StudentRecommendation, ClassRecommendation, Student, Book

def verify_recommendations():
    """Verify recommendations in database."""
    print("=" * 70)
    print("VERIFYING RECOMMENDATIONS")
    print("=" * 70)
    
    init_db()
    db = SessionLocal()
    
    try:
        # Count student recommendations
        student_recs = db.query(StudentRecommendation).count()
        print(f"\n📊 Student Recommendations: {student_recs} (expected: 75)")
        if student_recs == 75:
            print("   ✅ Count matches expected")
        else:
            print(f"   ⚠️  Count differs from expected")
        
        # Count class recommendations
        class_recs = db.query(ClassRecommendation).count()
        print(f"\n📚 Class Recommendations: {class_recs} (expected: 2)")
        if class_recs == 2:
            print("   ✅ Count matches expected")
        else:
            print(f"   ⚠️  Count differs from expected")
        
        # Check sample student recommendation
        sample = db.query(StudentRecommendation).first()
        if sample:
            student = db.query(Student).filter(Student.id == sample.student_id).first()
            book = db.query(Book).filter(Book.id == sample.book_id).first()
            print(f"\n📝 Sample Student Recommendation:")
            print(f"   Student: {student.name}")
            print(f"   Book: {book.title[:60]}")
            print(f"   Match Score: {sample.match_score:.3f} (range: 0-1)")
            print(f"   Known Words %: {sample.known_words_percent:.1%}")
            print(f"   New Words: {sample.new_words_count}")
            
            # Verify score is in valid range
            if 0 <= sample.match_score <= 1:
                print("   ✅ Match score in valid range")
            else:
                print("   ❌ Match score out of range")
        
        # Check class recommendations
        class_recs_list = db.query(ClassRecommendation).order_by(
            ClassRecommendation.students_recommended_count.desc()
        ).all()
        print(f"\n📖 Class-Wide Recommendations:")
        for i, rec in enumerate(class_recs_list, 1):
            book = db.query(Book).filter(Book.id == rec.book_id).first()
            print(f"   {i}. {book.title[:60]}")
            print(f"      Recommended to: {rec.students_recommended_count} students")
            print(f"      Average match score: {rec.match_score:.3f}")
        
        # Check for duplicate recommendations per student
        print(f"\n🔍 Checking for duplicate recommendations per student...")
        students = db.query(Student).all()
        duplicates_found = False
        for student in students:
            recs = db.query(StudentRecommendation).filter(
                StudentRecommendation.student_id == student.id
            ).all()
            book_ids = [rec.book_id for rec in recs]
            if len(book_ids) != len(set(book_ids)):
                print(f"   ⚠️  Student {student.name} has duplicate book recommendations")
                duplicates_found = True
        
        if not duplicates_found:
            print("   ✅ No duplicate recommendations per student")
        
        # Verify all students have 3 recommendations
        print(f"\n👥 Checking student recommendation counts...")
        students_with_3 = 0
        students_with_less = []
        for student in students:
            rec_count = db.query(StudentRecommendation).filter(
                StudentRecommendation.student_id == student.id
            ).count()
            if rec_count == 3:
                students_with_3 += 1
            else:
                students_with_less.append((student.name, rec_count))
        
        print(f"   Students with 3 recommendations: {students_with_3}/{len(students)}")
        if students_with_less:
            print(f"   ⚠️  Students with fewer than 3:")
            for name, count in students_with_less:
                print(f"      - {name}: {count} recommendations")
        else:
            print("   ✅ All students have 3 recommendations")
        
        print("\n" + "=" * 70)
        print("✅ VERIFICATION COMPLETE")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error verifying recommendations: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    if verify_recommendations():
        sys.exit(0)
    else:
        sys.exit(1)

