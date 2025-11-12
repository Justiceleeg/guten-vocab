#!/usr/bin/env python3
"""
Reset database to contain only the original 25 students from mock data.

This script:
1. Loads the 25 student personas from student_personas.json
2. Clears all existing student data from the database
3. Inserts the 25 original students
4. Provides option to re-run analysis and recommendations

Usage:
    python scripts/reset_students.py
    python scripts/reset_students.py --run-analysis
"""
import argparse
import json
import sys
from pathlib import Path

# Add backend to Python path
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.student import Student
from app.models.vocabulary import StudentVocabulary
from app.models.recommendation import StudentRecommendation

# Paths
STUDENT_PERSONAS_PATH = PROJECT_ROOT / "data" / "mock" / "student_personas.json"


def load_student_personas():
    """Load the 25 original student personas from JSON."""
    if not STUDENT_PERSONAS_PATH.exists():
        print(f"❌ Error: Student personas file not found at {STUDENT_PERSONAS_PATH}")
        print(f"   Please run 'python scripts/generate_mock_data.py --phase personas' first")
        sys.exit(1)
    
    with open(STUDENT_PERSONAS_PATH, 'r') as f:
        personas = json.load(f)
    
    print(f"✅ Loaded {len(personas)} student personas from {STUDENT_PERSONAS_PATH}")
    return personas


def clear_all_students(db: Session):
    """Clear all students and related data from the database."""
    print("\n" + "=" * 70)
    print("Clearing Database")
    print("=" * 70)
    
    # Count before deletion
    student_count = db.query(Student).count()
    vocab_count = db.query(StudentVocabulary).count()
    rec_count = db.query(StudentRecommendation).count()
    
    print(f"\nCurrent database contents:")
    print(f"  Students: {student_count}")
    print(f"  Student vocabulary entries: {vocab_count}")
    print(f"  Student recommendations: {rec_count}")
    
    # Delete all (cascade will handle related records)
    print(f"\n🗑️  Deleting all students and related data...")
    db.query(Student).delete()
    db.commit()
    
    # Verify deletion
    remaining = db.query(Student).count()
    print(f"✅ Deleted {student_count} students")
    print(f"   Remaining students: {remaining}")


def insert_students(db: Session, personas: list):
    """Insert the 25 original students into the database."""
    print("\n" + "=" * 70)
    print("Inserting Students")
    print("=" * 70)
    
    inserted_count = 0
    
    for persona in personas:
        student = Student(
            id=persona["id"],
            name=persona["name"],
            actual_reading_level=float(persona["reading_level"]),
            assigned_grade=persona["assigned_grade"]
        )
        db.add(student)
        inserted_count += 1
        print(f"  Added: {student.name} (ID: {student.id}, Reading Level: {student.actual_reading_level})")
    
    db.commit()
    print(f"\n✅ Inserted {inserted_count} students")
    
    # Verify insertion
    total = db.query(Student).count()
    print(f"   Total students in database: {total}")
    
    # Show distribution
    print(f"\n📊 Reading level distribution:")
    for level in [5, 6, 7, 8]:
        count = db.query(Student).filter(Student.actual_reading_level == level).count()
        print(f"   Grade {level}: {count} students")


def reset_sequence(db: Session):
    """Reset the auto-increment sequence for the students table."""
    print("\n🔄 Resetting ID sequence...")
    
    # PostgreSQL sequence reset
    try:
        db.execute("SELECT setval('students_id_seq', (SELECT MAX(id) FROM students));")
        db.commit()
        print("✅ Sequence reset successfully")
    except Exception as e:
        print(f"⚠️  Could not reset sequence: {e}")
        print("   This is normal if using SQLite or if sequence doesn't exist")


def verify_database(db: Session):
    """Verify the database state after reset."""
    print("\n" + "=" * 70)
    print("Verification")
    print("=" * 70)
    
    student_count = db.query(Student).count()
    vocab_count = db.query(StudentVocabulary).count()
    rec_count = db.query(StudentRecommendation).count()
    
    print(f"\nFinal database state:")
    print(f"  ✓ Students: {student_count} (expected: 25)")
    print(f"  ✓ Student vocabulary entries: {vocab_count} (expected: 0 - will be populated by analysis)")
    print(f"  ✓ Student recommendations: {rec_count} (expected: 0 - will be populated by recommendations)")
    
    if student_count == 25:
        print(f"\n✅ Database successfully reset to 25 students!")
    else:
        print(f"\n⚠️  Warning: Expected 25 students but found {student_count}")
    
    # Show first few students
    print(f"\nFirst 5 students:")
    students = db.query(Student).order_by(Student.id).limit(5).all()
    for s in students:
        print(f"  ID {s.id}: {s.name} (Reading Level: {s.actual_reading_level})")


def run_analysis():
    """Run the student analysis script."""
    print("\n" + "=" * 70)
    print("Running Student Analysis")
    print("=" * 70)
    print("\nExecuting: python scripts/analyze_students.py")
    
    import subprocess
    result = subprocess.run(
        ["python", str(SCRIPT_DIR / "analyze_students.py")],
        cwd=PROJECT_ROOT,
        capture_output=False
    )
    
    if result.returncode == 0:
        print("\n✅ Student analysis completed successfully")
    else:
        print(f"\n❌ Student analysis failed with exit code {result.returncode}")
        return False
    
    return True


def run_recommendations():
    """Run the recommendation generation script."""
    print("\n" + "=" * 70)
    print("Generating Recommendations")
    print("=" * 70)
    print("\nExecuting: python scripts/generate_recommendations.py")
    
    import subprocess
    result = subprocess.run(
        ["python", str(SCRIPT_DIR / "generate_recommendations.py")],
        cwd=PROJECT_ROOT,
        capture_output=False
    )
    
    if result.returncode == 0:
        print("\n✅ Recommendations generated successfully")
    else:
        print(f"\n❌ Recommendation generation failed with exit code {result.returncode}")
        return False
    
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Reset database to contain only the 25 original students from mock data"
    )
    parser.add_argument(
        "--run-analysis",
        action="store_true",
        help="Automatically run analysis and recommendation generation after reset"
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Skip confirmation prompt"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Database Reset Script")
    print("=" * 70)
    print("\nThis script will:")
    print("  1. Load the 25 student personas from student_personas.json")
    print("  2. DELETE ALL existing students and related data")
    print("  3. Insert the 25 original students")
    
    if args.run_analysis:
        print("  4. Run student analysis (analyze_students.py)")
        print("  5. Generate recommendations (generate_recommendations.py)")
    
    if not args.yes:
        print("\n⚠️  WARNING: This will DELETE ALL existing student data!")
        response = input("\nDo you want to continue? (yes/no): ")
        if response.lower() not in ["yes", "y"]:
            print("❌ Aborted")
            sys.exit(0)
    
    # Load personas
    personas = load_student_personas()
    
    # Database operations
    db = SessionLocal()
    try:
        # Clear existing data
        clear_all_students(db)
        
        # Insert new students
        insert_students(db, personas)
        
        # Reset sequence
        reset_sequence(db)
        
        # Verify
        verify_database(db)
        
    finally:
        db.close()
    
    # Optionally run analysis and recommendations
    if args.run_analysis:
        print("\n" + "=" * 70)
        print("Running Post-Reset Scripts")
        print("=" * 70)
        
        if not run_analysis():
            print("\n⚠️  Analysis failed. Skipping recommendations.")
            sys.exit(1)
        
        if not run_recommendations():
            print("\n⚠️  Recommendation generation failed.")
            sys.exit(1)
        
        print("\n" + "=" * 70)
        print("✅ Database Reset Complete!")
        print("=" * 70)
        print("\nThe database now contains:")
        print("  - 25 students from mock data")
        print("  - Student vocabulary analysis")
        print("  - Book recommendations")
    else:
        print("\n" + "=" * 70)
        print("✅ Database Reset Complete!")
        print("=" * 70)
        print("\nNext steps:")
        print("  1. Run: python scripts/analyze_students.py")
        print("  2. Run: python scripts/generate_recommendations.py")
        print("\nOr run this script with --run-analysis to do both automatically:")
        print("  python scripts/reset_students.py --run-analysis")


if __name__ == "__main__":
    main()

