#!/usr/bin/env python3
"""
Seed vocabulary words from grade-level JSON files into the database.

This script:
1. Loads vocabulary JSON files from data/vocab/
2. Handles duplicates (keeps highest grade level)
3. Applies spaCy lemmatization
4. Inserts words into vocabulary_words table
"""
import json
import sys
from pathlib import Path
from collections import defaultdict

# Add backend directory to path to import app modules
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import spacy

from app.database import SessionLocal, init_db
from app.models import VocabularyWord

# Load spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Error: spaCy English model not found. Run: python -m spacy download en_core_web_sm")
    sys.exit(1)


def load_vocabulary_files(data_dir: Path) -> dict:
    """
    Load all vocabulary JSON files and return a dictionary mapping words to grade levels.
    Handles duplicates by keeping the highest grade level.
    
    Returns:
        dict: {word: grade_level}
    """
    vocab_dir = data_dir / "vocab"
    grade_files = {
        5: "5th_grade.json",
        6: "6th_grade.json",
        7: "7th_grade.json",
        8: "8th_grade.json",
    }
    
    word_to_grade = {}
    words_by_grade = defaultdict(list)
    duplicates = []
    
    print("Loading vocabulary files...")
    for grade, filename in grade_files.items():
        filepath = vocab_dir / filename
        if not filepath.exists():
            print(f"Warning: {filename} not found, skipping...")
            continue
        
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        words = data.get("words", [])
        print(f"  Loaded {len(words)} words from {filename}")
        
        for word in words:
            word_lower = word.lower().strip()
            if not word_lower:
                continue
            
            # Handle duplicates: keep highest grade
            if word_lower in word_to_grade:
                old_grade = word_to_grade[word_lower]
                if grade > old_grade:
                    duplicates.append({
                        "word": word_lower,
                        "old_grade": old_grade,
                        "new_grade": grade,
                    })
                    word_to_grade[word_lower] = grade
                    # Remove from old grade list
                    words_by_grade[old_grade].remove(word_lower)
                    words_by_grade[grade].append(word_lower)
                # else: keep existing (higher grade)
            else:
                word_to_grade[word_lower] = grade
                words_by_grade[grade].append(word_lower)
    
    print(f"\nTotal unique words: {len(word_to_grade)}")
    if duplicates:
        print(f"Duplicates handled: {len(duplicates)} words upgraded to higher grade")
    
    return word_to_grade, words_by_grade, duplicates


def lemmatize_word(word: str) -> str:
    """
    Lemmatize a word using spaCy.
    
    Args:
        word: The word to lemmatize
        
    Returns:
        str: The lemmatized form of the word
    """
    doc = nlp(word)
    if len(doc) > 0:
        return doc[0].lemma_.lower()
    return word.lower()


def seed_vocabulary(db: Session, word_to_grade: dict, words_by_grade: dict) -> dict:
    """
    Insert vocabulary words into the database.
    
    Args:
        db: Database session
        word_to_grade: Dictionary mapping words to grade levels
        words_by_grade: Dictionary mapping grades to lists of words
        
    Returns:
        dict: Statistics about the seeding process
    """
    stats = {
        "total_words": len(word_to_grade),
        "inserted": 0,
        "updated": 0,
        "errors": 0,
        "by_grade": {grade: 0 for grade in range(5, 9)},
    }
    
    print("\nInserting words into database...")
    
    # Get existing words to check for updates
    existing_words = {
        word.word.lower(): word
        for word in db.query(VocabularyWord).all()
    }
    
    # Process words in batches
    batch_size = 100
    words_list = list(word_to_grade.items())
    
    for i in range(0, len(words_list), batch_size):
        batch = words_list[i:i + batch_size]
        
        for word, grade in batch:
            try:
                word_lower = word.lower()
                lemmatized = lemmatize_word(word)
                
                # Check if word already exists
                if word_lower in existing_words:
                    # Update existing word if grade is higher
                    existing = existing_words[word_lower]
                    if grade > existing.grade_level:
                        existing.grade_level = grade
                        stats["updated"] += 1
                    else:
                        # Word already exists with same or higher grade, skip
                        stats["by_grade"][grade] += 1
                        continue
                else:
                    # Insert new word
                    vocab_word = VocabularyWord(
                        word=word_lower,
                        grade_level=grade,
                    )
                    db.add(vocab_word)
                    existing_words[word_lower] = vocab_word
                    stats["inserted"] += 1
                
                stats["by_grade"][grade] += 1
                
            except Exception as e:
                print(f"Error processing word '{word}': {e}")
                stats["errors"] += 1
                continue
        
        # Commit batch
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            print(f"Error committing batch: {e}")
            stats["errors"] += len(batch)
    
    return stats


def print_summary(stats: dict, words_by_grade: dict, duplicates: list):
    """Print summary statistics."""
    print("\n" + "=" * 60)
    print("VOCABULARY SEEDING SUMMARY")
    print("=" * 60)
    print(f"Total unique words processed: {stats['total_words']}")
    print(f"Words inserted: {stats['inserted']}")
    print(f"Words updated: {stats['updated']}")
    print(f"Errors: {stats['errors']}")
    print("\nWords by grade level:")
    for grade in range(5, 9):
        count = stats["by_grade"][grade]
        print(f"  Grade {grade}: {count} words")
    
    if duplicates:
        print(f"\nDuplicates handled: {len(duplicates)}")
        print("Sample duplicates (upgraded to higher grade):")
        for dup in duplicates[:5]:  # Show first 5
            print(f"  '{dup['word']}': grade {dup['old_grade']} -> {dup['new_grade']}")
    
    print(f"\n✅ Loaded {stats['total_words']} words across grades 5-8")
    print("=" * 60)


def main():
    """Main function to seed vocabulary."""
    # Get project root directory
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    
    # Load vocabulary files
    word_to_grade, words_by_grade, duplicates = load_vocabulary_files(data_dir)
    
    if not word_to_grade:
        print("Error: No vocabulary words found. Check data/vocab/ directory.")
        sys.exit(1)
    
    # Initialize database (ensure tables exist)
    print("\nInitializing database...")
    init_db()
    
    # Create database session
    db: Session = SessionLocal()
    
    try:
        # Seed vocabulary
        stats = seed_vocabulary(db, word_to_grade, words_by_grade)
        
        # Print summary
        print_summary(stats, words_by_grade, duplicates)
        
    except Exception as e:
        db.rollback()
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()

