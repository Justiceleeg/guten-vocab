#!/usr/bin/env python3
"""
Verify vocabulary words in database.
"""
import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import func
from app.database import SessionLocal
from app.models import VocabularyWord

db = SessionLocal()

try:
    # Total count
    total = db.query(func.count(VocabularyWord.id)).scalar()
    print(f"Total vocabulary words: {total}")
    
    # Count by grade
    print("\nWords by grade level:")
    for grade in range(5, 9):
        count = db.query(func.count(VocabularyWord.id)).filter(
            VocabularyWord.grade_level == grade
        ).scalar()
        print(f"  Grade {grade}: {count} words")
    
    # Sample words
    print("\nSample words from each grade:")
    for grade in range(5, 9):
        word = db.query(VocabularyWord).filter(
            VocabularyWord.grade_level == grade
        ).first()
        if word:
            print(f"  Grade {grade}: '{word.word}'")
    
    # Check for duplicates
    duplicates = db.query(
        VocabularyWord.word,
        func.count(VocabularyWord.id).label('count')
    ).group_by(VocabularyWord.word).having(
        func.count(VocabularyWord.id) > 1
    ).all()
    
    if duplicates:
        print(f"\n⚠️  Found {len(duplicates)} duplicate words!")
        for word, count in duplicates[:5]:
            print(f"  '{word}': {count} occurrences")
    else:
        print("\n✅ No duplicate words found")
    
finally:
    db.close()

