#!/usr/bin/env python3
"""
Seed the database with Project Gutenberg books.

This script:
- Loads pgcorpus/Zenodo metadata
- Filters to children's literature
- Calculates reading levels
- Extracts vocabulary counts
- Inserts books and vocabulary into database

Supports both:
- pgcorpus/gutenberg repository (full download)
- Zenodo 2018 dataset (pre-processed)

Usage:
    python scripts/seed_books.py [--dataset-path PATH] [--phase PHASE]
    
    --dataset-path: Path to pgcorpus or Zenodo dataset (auto-detected if not provided)
    --phase: 'select' (Phase 1) or 'extract' (Phase 2) or 'all' (default: all)
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

try:
    import pandas as pd
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install pandas")
    sys.exit(1)

# Optional imports (only needed for Phase 2)
try:
    import spacy
except ImportError:
    spacy = None

try:
    from textstat import flesch_kincaid_grade
except ImportError:
    flesch_kincaid_grade = None

# Database imports (only needed for Phase 2)
try:
    from app.database import SessionLocal
    from app.models.book import Book, BookVocabulary
    from app.models.vocabulary import VocabularyWord
except ImportError:
    SessionLocal = None
    Book = None
    BookVocabulary = None
    VocabularyWord = None


def find_dataset_path() -> Optional[Path]:
    """Auto-detect dataset path (Zenodo or pgcorpus)."""
    project_root = Path(__file__).parent.parent
    
    # Check for Zenodo config
    config_path = project_root / "data" / "pgcorpus_config.json"
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
            if config.get("dataset_type") == "zenodo_2018":
                return Path(config["dataset_path"])
    
    # Check project directory first (preferred location)
    project_zenodo = project_root / "data" / "pgcorpus-2018"
    if project_zenodo.exists() and (project_zenodo / "counts").exists():
        return project_zenodo
    
    # Check common Zenodo locations
    zenodo_paths = [
        project_root / "datasets" / "pgcorpus-2018",
        Path.home() / "datasets" / "pgcorpus-2018",
        Path("~/datasets/pgcorpus-2018").expanduser(),
    ]
    for path in zenodo_paths:
        if path.exists() and (path / "counts").exists():
            return path
    
    # Check for pgcorpus repository
    pgcorpus_paths = [
        project_root / "gutenberg",
        Path("gutenberg"),
        Path("../gutenberg"),
    ]
    for path in pgcorpus_paths:
        if path.exists() and (path / "data" / "counts").exists():
            return path
    
    return None


def find_metadata_csv(dataset_path: Path) -> Optional[Path]:
    """Find metadata CSV file."""
    # Check common locations (including Zenodo naming)
    locations = [
        dataset_path / "metadata" / "metadata.csv",
        dataset_path / "metadata.csv",
        dataset_path / "data" / "metadata.csv",
        dataset_path / "SPGC-metadata-2018-07-18.csv",  # Zenodo default name
    ]
    
    # Also check for any CSV file in the directory
    for csv_file in dataset_path.glob("*.csv"):
        if "metadata" in csv_file.name.lower():
            return csv_file
    
    for loc in locations:
        if loc.exists():
            return loc
    
    return None


def find_counts_file(dataset_path: Path, gutenberg_id: int) -> Optional[Path]:
    """Find counts file for a Gutenberg ID."""
    # Try Zenodo structure first
    counts_dir = dataset_path / "counts"
    if not counts_dir.exists():
        # Try pgcorpus structure
        counts_dir = dataset_path / "data" / "counts"
    
    if not counts_dir.exists():
        return None
    
    # Try common naming patterns
    patterns = [
        f"{gutenberg_id}.txt",
        f"{gutenberg_id}_counts.txt",
        f"gutenberg_{gutenberg_id}.txt",
        f"PG{gutenberg_id}_counts.txt",
        f"{gutenberg_id}",
    ]
    
    for pattern in patterns:
        file_path = counts_dir / pattern
        if file_path.exists() and file_path.is_file():
            return file_path
    
    # Try to find any file starting with the ID
    for file in counts_dir.glob(f"{gutenberg_id}*"):
        if file.is_file():
            return file
    
    return None


def load_metadata(metadata_path: Path) -> pd.DataFrame:
    """Load and parse metadata CSV."""
    print(f"📊 Loading metadata from: {metadata_path}")
    
    try:
        df = pd.read_csv(metadata_path, low_memory=False)
        print(f"   ✅ Loaded {len(df):,} books")
        return df
    except Exception as e:
        print(f"   ❌ Error loading metadata: {e}")
        raise


def filter_books(df: pd.DataFrame, counts_dir: Path) -> pd.DataFrame:
    """Filter books by category, language, and availability."""
    print("\n🔍 Filtering books...")
    initial_count = len(df)
    
    # Filter by category/subjects (check multiple possible column names)
    category_col = None
    if "category" in df.columns:
        category_col = "category"
    elif "bookshelf" in df.columns:
        category_col = "bookshelf"
    elif "subjects" in df.columns:
        category_col = "subjects"
    
    if category_col:
        # Check for children's literature in the column
        children_mask = df[category_col].astype(str).str.contains(
            "Children|children|Juvenile|juvenile", case=False, na=False
        )
        df = df[children_mask]
        print(f"   Category filter: {len(df):,} books (Children's Literature/Fiction)")
    else:
        print("   ⚠️  No category/subjects column found, skipping category filter")
    
    # Filter by language
    if "language" in df.columns:
        df = df[df["language"].str.contains("en|English", case=False, na=False)]
        print(f"   Language filter: {len(df):,} books (English)")
    else:
        print("   ⚠️  No language column found, skipping language filter")
    
    # Filter by availability (has counts file)
    print("   Checking counts file availability...")
    available_books = []
    for idx, row in df.iterrows():
        gutenberg_id = row.get("gutenberg_id") or row.get("id") or row.get("PG")
        if pd.isna(gutenberg_id):
            continue
        
        try:
            # Handle "PG1" format - extract numeric part
            id_str = str(gutenberg_id).strip()
            if id_str.startswith("PG"):
                gutenberg_id = int(id_str[2:])
            else:
                gutenberg_id = int(id_str)
            
            counts_file = find_counts_file(counts_dir.parent if "data" in str(counts_dir) else counts_dir, gutenberg_id)
            if counts_file:
                available_books.append(idx)
        except (ValueError, TypeError):
            continue
    
    df = df.loc[available_books]
    print(f"   Availability filter: {len(df):,} books (have counts files)")
    
    print(f"\n   📊 Filtered from {initial_count:,} to {len(df):,} books")
    return df


def calculate_reading_level(text: str) -> Optional[float]:
    """Calculate Flesch-Kincaid reading level."""
    try:
        return flesch_kincaid_grade(text)
    except Exception:
        return None


def phase1_select_books(dataset_path: Path, output_path: Path):
    """Phase 1: Filter and select top 100 books."""
    print("=" * 70)
    print("Phase 1: Book Selection")
    print("=" * 70)
    
    # Find metadata
    metadata_path = find_metadata_csv(dataset_path)
    if not metadata_path:
        print("❌ Error: Metadata CSV not found")
        print("   Expected locations:")
        print(f"     - {dataset_path / 'metadata.csv'}")
        print(f"     - {dataset_path / 'metadata' / 'metadata.csv'}")
        print(f"     - {dataset_path / 'data' / 'metadata.csv'}")
        sys.exit(1)
    
    # Load metadata
    df = load_metadata(metadata_path)
    
    # Determine counts directory
    counts_dir = dataset_path / "counts" if (dataset_path / "counts").exists() else dataset_path / "data" / "counts"
    
    # Filter books
    df = filter_books(df, counts_dir)
    
    if len(df) == 0:
        print("❌ Error: No books found after filtering")
        sys.exit(1)
    
    # Calculate reading levels (simplified - would need book text for accurate calculation)
    print("\n📖 Note: Reading level calculation requires book text.")
    print("   For now, we'll skip this and filter by other criteria.")
    print("   You can add reading level calculation later if needed.")
    
    # Sort by download count if available
    if "download_count" in df.columns or "downloads" in df.columns:
        download_col = "download_count" if "download_count" in df.columns else "downloads"
        df = df.sort_values(download_col, ascending=False, na_position='last')
        print(f"\n   Sorted by download count (popularity)")
    
    # Select top 100
    selected = df.head(100)
    print(f"\n✅ Selected top 100 books")
    
    # Prepare output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    books_list = []
    for _, row in selected.iterrows():
        gutenberg_id = row.get("gutenberg_id") or row.get("id") or row.get("PG")
        
        # Handle "PG1" format - extract numeric part
        gutenberg_id_int = None
        if not pd.isna(gutenberg_id):
            try:
                id_str = str(gutenberg_id).strip()
                if id_str.startswith("PG"):
                    gutenberg_id_int = int(id_str[2:])
                else:
                    gutenberg_id_int = int(id_str)
            except (ValueError, TypeError):
                pass
        
        # Handle download count (may be "downloads" column)
        download_count = None
        if "download_count" in row:
            download_count = row.get("download_count")
        elif "downloads" in row:
            download_count = row.get("downloads")
        
        try:
            download_count = int(download_count) if not pd.isna(download_count) else None
        except (ValueError, TypeError):
            download_count = None
        
        book = {
            "gutenberg_id": gutenberg_id_int,
            "title": str(row.get("title", "Unknown")),
            "author": str(row.get("author", "Unknown")),
            "reading_level": None,  # Would calculate from text
            "download_count": download_count,
        }
        books_list.append(book)
    
    with open(output_path, 'w') as f:
        json.dump(books_list, f, indent=2)
    
    print(f"💾 Saved to: {output_path}")
    print(f"   {len(books_list)} books selected")
    
    return books_list


def parse_counts_file(counts_file: Path) -> Dict[str, int]:
    """Parse counts file (handles different formats)."""
    counts = {}
    
    try:
        with open(counts_file, 'r', encoding='utf-8') as f:
            # Try JSON first
            try:
                content = f.read()
                data = json.loads(content)
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                pass
            
            # Try space/tab separated
            f.seek(0)
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split()
                if len(parts) >= 2:
                    word = parts[0].lower()
                    try:
                        count = int(parts[-1])
                        counts[word] = counts.get(word, 0) + count
                    except ValueError:
                        continue
    except Exception as e:
        print(f"      ⚠️  Error reading counts file: {e}")
    
    return counts


def phase2_extract_vocabulary(dataset_path: Path, selected_books_path: Path):
    """Phase 2: Extract vocabulary counts for selected books."""
    print("\n" + "=" * 70)
    print("Phase 2: Vocabulary Extraction")
    print("=" * 70)
    
    # Check for required dependencies
    if spacy is None:
        print("❌ Error: spaCy is required for Phase 2")
        print("   Install with: pip install spacy")
        print("   Then download model: python -m spacy download en_core_web_sm")
        sys.exit(1)
    
    if SessionLocal is None:
        print("❌ Error: Database modules are required for Phase 2")
        print("   Make sure you're in the project root and backend dependencies are installed")
        print("   Install with: pip install sqlalchemy psycopg2-binary python-dotenv")
        sys.exit(1)
    
    # Load selected books
    with open(selected_books_path) as f:
        books = json.load(f)
    
    print(f"📚 Processing {len(books)} books...")
    
    # Load spaCy model
    print("🔤 Loading spaCy model...")
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("❌ Error: spaCy model not found")
        print("   Install with: python -m spacy download en_core_web_sm")
        sys.exit(1)
    
    # Load vocabulary words from database
    db = SessionLocal()
    try:
        vocab_words = db.query(VocabularyWord).all()
        vocab_dict = {word.word.lower(): word.id for word in vocab_words}
        print(f"   ✅ Loaded {len(vocab_dict)} vocabulary words from database")
    finally:
        db.close()
    
    # Determine counts directory
    counts_dir = dataset_path / "counts" if (dataset_path / "counts").exists() else dataset_path / "data" / "counts"
    
    # Process each book
    db = SessionLocal()
    try:
        for i, book_data in enumerate(books, 1):
            gutenberg_id = book_data.get("gutenberg_id")
            if not gutenberg_id:
                print(f"\n   [{i}/{len(books)}] Skipping book without gutenberg_id")
                continue
            
            print(f"\n   [{i}/{len(books)}] Processing: {book_data.get('title', 'Unknown')} (ID: {gutenberg_id})")
            
            # Find counts file
            counts_file = find_counts_file(counts_dir.parent if "data" in str(counts_dir) else counts_dir, gutenberg_id)
            if not counts_file:
                print(f"      ❌ Counts file not found")
                continue
            
            # Parse counts
            counts = parse_counts_file(counts_file)
            if not counts:
                print(f"      ⚠️  No counts found in file")
                continue
            
            # Lemmatize and match vocabulary
            matched_vocab = {}
            total_words = 0
            
            for word, count in counts.items():
                total_words += count
                # Lemmatize
                doc = nlp(word)
                lemma = doc[0].lemma_.lower() if len(doc) > 0 else word.lower()
                
                # Check if in vocabulary
                if lemma in vocab_dict:
                    word_id = vocab_dict[lemma]
                    matched_vocab[word_id] = matched_vocab.get(word_id, 0) + count
            
            print(f"      ✅ Found {len(matched_vocab)} vocabulary matches out of {total_words:,} total words")
            
            # Insert/update book
            book = db.query(Book).filter(Book.gutenberg_id == gutenberg_id).first()
            if not book:
                book = Book(
                    gutenberg_id=gutenberg_id,
                    title=book_data.get("title", "Unknown"),
                    author=book_data.get("author"),
                    reading_level=book_data.get("reading_level"),
                    total_words=total_words,
                )
                db.add(book)
                db.flush()
            else:
                book.total_words = total_words
                # Clear existing vocabulary
                db.query(BookVocabulary).filter(BookVocabulary.book_id == book.id).delete()
            
            # Insert vocabulary matches
            for word_id, count in matched_vocab.items():
                book_vocab = BookVocabulary(
                    book_id=book.id,
                    word_id=word_id,
                    occurrence_count=count,
                )
                db.add(book_vocab)
            
            db.commit()
            print(f"      💾 Saved to database")
    
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
        raise
    finally:
        db.close()
    
    print("\n" + "=" * 70)
    print("✅ Phase 2 Complete!")
    print("=" * 70)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Seed books and vocabulary from pgcorpus/Zenodo")
    parser.add_argument(
        "--dataset-path",
        type=str,
        help="Path to pgcorpus or Zenodo dataset (auto-detected if not provided)",
    )
    parser.add_argument(
        "--phase",
        choices=["select", "extract", "all"],
        default="all",
        help="Which phase to run (default: all)",
    )
    parser.add_argument(
        "--selected-books",
        type=str,
        default="data/books/selected_books.json",
        help="Path to selected books JSON (default: data/books/selected_books.json)",
    )
    
    args = parser.parse_args()
    
    # Find dataset path
    if args.dataset_path:
        dataset_path = Path(args.dataset_path).expanduser()
    else:
        dataset_path = find_dataset_path()
    
    if not dataset_path or not dataset_path.exists():
        print("❌ Error: Dataset path not found")
        print("\nPlease provide dataset path:")
        print("  --dataset-path /path/to/zenodo-2018")
        print("  --dataset-path /path/to/gutenberg")
        print("\nOr set up Zenodo dataset:")
        print("  python scripts/setup_zenodo.py ~/datasets/pgcorpus-2018")
        sys.exit(1)
    
    print(f"📁 Using dataset: {dataset_path.absolute()}")
    
    selected_books_path = Path(args.selected_books)
    
    # Run phases
    if args.phase in ["select", "all"]:
        phase1_select_books(dataset_path, selected_books_path)
    
    if args.phase in ["extract", "all"]:
        if not selected_books_path.exists():
            print(f"\n❌ Error: Selected books file not found: {selected_books_path}")
            print("   Run Phase 1 first: python scripts/seed_books.py --phase select")
            sys.exit(1)
        phase2_extract_vocabulary(dataset_path, selected_books_path)


if __name__ == "__main__":
    main()
