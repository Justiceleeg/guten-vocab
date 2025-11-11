#!/usr/bin/env python3
"""
Verify selected books and cleanup pgcorpus dataset.

This script:
1. Verifies that all 100 selected books have counts files available
2. Removes unneeded pgcorpus data (keeps only what we need)
3. Reports disk space savings

Usage:
    python scripts/cleanup_pgcorpus.py [path_to_gutenberg] [path_to_selected_books]
    
    Defaults:
    - gutenberg: ./gutenberg
    - selected_books: ./data/books/selected_books.json
"""

import json
import os
import shutil
import sys
from pathlib import Path
from typing import List, Dict, Set


def load_selected_books(selected_books_path: Path) -> List[Dict]:
    """Load the selected books JSON file."""
    if not selected_books_path.exists():
        print(f"❌ Error: Selected books file not found: {selected_books_path}")
        sys.exit(1)
    
    with open(selected_books_path, 'r') as f:
        books = json.load(f)
    
    print(f"✅ Loaded {len(books)} selected books from {selected_books_path}")
    return books


def find_counts_file(gutenberg_path: Path, gutenberg_id: int) -> Path:
    """Find the counts file for a given Gutenberg ID."""
    # Try Zenodo structure first (counts/ directly in dataset path)
    counts_dir = gutenberg_path / "counts"
    
    # Try pgcorpus structure (data/counts/)
    if not counts_dir.exists():
        counts_dir = gutenberg_path / "data" / "counts"
    
    if not counts_dir.exists():
        return None
    
    # Try common naming patterns (Zenodo uses PG{id}_counts.txt)
    patterns = [
        f"PG{gutenberg_id}_counts.txt",  # Zenodo format (most common)
        f"{gutenberg_id}_counts.txt",
        f"{gutenberg_id}.txt",
        f"gutenberg_{gutenberg_id}.txt",
    ]
    
    for pattern in patterns:
        file_path = counts_dir / pattern
        if file_path.exists():
            return file_path
    
    # Try to find any file starting with the ID
    for file in counts_dir.glob(f"{gutenberg_id}*"):
        if file.is_file():
            return file
    
    return None


def verify_books(gutenberg_path: Path, books: List[Dict]) -> Dict[str, List]:
    """Verify that all selected books have counts files."""
    print("\n📚 Verifying selected books...")
    
    verified = []
    missing = []
    
    for book in books:
        gutenberg_id = book.get('gutenberg_id')
        title = book.get('title', 'Unknown')
        
        if not gutenberg_id:
            missing.append({
                'book': book,
                'reason': 'No gutenberg_id in book data'
            })
            continue
        
        counts_file = find_counts_file(gutenberg_path, gutenberg_id)
        
        if counts_file:
            verified.append({
                'gutenberg_id': gutenberg_id,
                'title': title,
                'counts_file': counts_file
            })
            print(f"  ✅ {gutenberg_id}: {title[:50]}")
        else:
            missing.append({
                'gutenberg_id': gutenberg_id,
                'title': title,
                'reason': 'Counts file not found'
            })
            print(f"  ❌ {gutenberg_id}: {title[:50]} - COUNTS FILE NOT FOUND")
    
    print(f"\n📊 Verification Summary:")
    print(f"  ✅ Verified: {len(verified)}/{len(books)} books")
    print(f"  ❌ Missing: {len(missing)}/{len(books)} books")
    
    if missing:
        print(f"\n⚠️  Warning: {len(missing)} books are missing counts files:")
        for item in missing[:10]:  # Show first 10
            print(f"    - {item.get('gutenberg_id')}: {item.get('title', 'Unknown')}")
        if len(missing) > 10:
            print(f"    ... and {len(missing) - 10} more")
    
    return {
        'verified': verified,
        'missing': missing
    }


def get_directory_size(path: Path) -> int:
    """Get total size of directory in bytes."""
    total = 0
    try:
        for entry in path.rglob('*'):
            if entry.is_file():
                total += entry.stat().st_size
    except Exception as e:
        print(f"  ⚠️  Warning: Could not calculate size for {path}: {e}")
    return total


def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def cleanup_unneeded_data(gutenberg_path: Path, verified_books: List[Dict], dry_run: bool = False) -> Dict:
    """Remove unneeded pgcorpus data, keeping only selected books."""
    print("\n🧹 Cleaning up unneeded data...")
    
    if dry_run:
        print("  🔍 DRY RUN MODE - No files will be deleted")
    
    # Get Gutenberg IDs we need to keep
    keep_ids: Set[int] = {book['gutenberg_id'] for book in verified_books}
    
    # Try Zenodo structure first (counts/ directly in dataset path)
    counts_dir = gutenberg_path / "counts"
    data_dir = gutenberg_path / "data"
    
    # Try pgcorpus structure (data/counts/)
    if not counts_dir.exists():
        counts_dir = data_dir / "counts"
    
    cleanup_stats = {
        'counts_removed': 0,
        'counts_kept': 0,
        'raw_removed': 0,
        'tokens_removed': 0,
        'text_removed': 0,
        'mirror_removed': False,
        'space_freed': 0
    }
    
    # 1. Clean up counts folder - keep only selected books
    if counts_dir.exists():
        print(f"\n  📝 Cleaning counts folder...")
        all_counts_files = list(counts_dir.glob("*"))
        all_counts_files = [f for f in all_counts_files if f.is_file() and not f.name.startswith('.')]
        
        for counts_file in all_counts_files:
            # Try to extract Gutenberg ID from filename
            file_id = None
            filename = counts_file.stem  # filename without extension
            
            # Try to extract number from filename
            import re
            match = re.search(r'(\d+)', filename)
            if match:
                file_id = int(match.group(1))
            
            if file_id in keep_ids:
                cleanup_stats['counts_kept'] += 1
                if not dry_run:
                    print(f"    ✅ Keeping: {counts_file.name}")
            else:
                cleanup_stats['counts_removed'] += 1
                file_size = counts_file.stat().st_size
                cleanup_stats['space_freed'] += file_size
                if not dry_run:
                    counts_file.unlink()
                    print(f"    🗑️  Removing: {counts_file.name} ({format_size(file_size)})")
                else:
                    print(f"    🗑️  Would remove: {counts_file.name} ({format_size(file_size)})")
    
    # 2. Remove raw books folder (we only need counts)
    raw_dir = data_dir / "raw"
    if raw_dir.exists():
        print(f"\n  📄 Removing raw books folder...")
        size = get_directory_size(raw_dir)
        cleanup_stats['raw_removed'] = size
        cleanup_stats['space_freed'] += size
        if not dry_run:
            shutil.rmtree(raw_dir)
            print(f"    🗑️  Removed: {format_size(size)}")
        else:
            print(f"    🗑️  Would remove: {format_size(size)}")
    
    # 3. Remove tokens folder (we only need counts)
    tokens_dir = data_dir / "tokens"
    if tokens_dir.exists():
        print(f"\n  🔤 Removing tokens folder...")
        size = get_directory_size(tokens_dir)
        cleanup_stats['tokens_removed'] = size
        cleanup_stats['space_freed'] += size
        if not dry_run:
            shutil.rmtree(tokens_dir)
            print(f"    🗑️  Removed: {format_size(size)}")
        else:
            print(f"    🗑️  Would remove: {format_size(size)}")
    
    # 4. Remove text folder (we only need counts)
    text_dir = data_dir / "text"
    if text_dir.exists():
        print(f"\n  📖 Removing text folder...")
        size = get_directory_size(text_dir)
        cleanup_stats['text_removed'] = size
        cleanup_stats['space_freed'] += size
        if not dry_run:
            shutil.rmtree(text_dir)
            print(f"    🗑️  Removed: {format_size(size)}")
        else:
            print(f"    🗑️  Would remove: {format_size(size)}")
    
    # 5. Remove .mirror folder (raw downloaded books)
    mirror_dir = data_dir / ".mirror"
    if mirror_dir.exists():
        print(f"\n  📦 Removing .mirror folder (raw downloads)...")
        size = get_directory_size(mirror_dir)
        cleanup_stats['mirror_removed'] = True
        cleanup_stats['space_freed'] += size
        if not dry_run:
            shutil.rmtree(mirror_dir)
            print(f"    🗑️  Removed: {format_size(size)}")
        else:
            print(f"    🗑️  Would remove: {format_size(size)}")
    
    return cleanup_stats


def main():
    """Main cleanup script."""
    print("=" * 70)
    print("pgcorpus Cleanup and Verification Script")
    print("=" * 70)
    
    # Parse arguments
    gutenberg_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("gutenberg")
    selected_books_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("data/books/selected_books.json")
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    
    if not gutenberg_path.exists():
        print(f"\n❌ Error: Gutenberg directory not found: {gutenberg_path}")
        print(f"\nUsage: python {sys.argv[0]} [gutenberg_path] [selected_books_path] [--dry-run]")
        sys.exit(1)
    
    print(f"\n📁 Gutenberg path: {gutenberg_path.absolute()}")
    print(f"📚 Selected books: {selected_books_path.absolute()}")
    if dry_run:
        print(f"🔍 Mode: DRY RUN (no files will be deleted)")
    
    # Load selected books
    books = load_selected_books(selected_books_path)
    
    if len(books) == 0:
        print("❌ Error: No books found in selected_books.json")
        sys.exit(1)
    
    # Verify books
    verification = verify_books(gutenberg_path, books)
    
    if len(verification['missing']) > 0:
        print(f"\n⚠️  Warning: {len(verification['missing'])} books are missing counts files.")
        response = input("\nContinue with cleanup anyway? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Cleanup cancelled.")
            sys.exit(1)
    
    # Cleanup
    cleanup_stats = cleanup_unneeded_data(
        gutenberg_path,
        verification['verified'],
        dry_run=dry_run
    )
    
    # Summary
    print("\n" + "=" * 70)
    print("Cleanup Summary")
    print("=" * 70)
    print(f"✅ Counts files kept: {cleanup_stats['counts_kept']}")
    print(f"🗑️  Counts files removed: {cleanup_stats['counts_removed']}")
    print(f"🗑️  Raw books removed: {format_size(cleanup_stats['raw_removed'])}")
    print(f"🗑️  Tokens removed: {format_size(cleanup_stats['tokens_removed'])}")
    print(f"🗑️  Text removed: {format_size(cleanup_stats['text_removed'])}")
    if cleanup_stats['mirror_removed']:
        print(f"🗑️  Mirror folder removed")
    print(f"\n💾 Total space freed: {format_size(cleanup_stats['space_freed'])}")
    
    if dry_run:
        print("\n🔍 This was a dry run. Run without --dry-run to actually delete files.")
    else:
        print("\n✅ Cleanup complete!")
        print("\n📋 What's kept:")
        print("  - Selected books' counts files")
        print("  - Metadata CSV")
        print("  - Repository scripts (get_data.py, process_data.py, etc.)")
        print("\n📋 What's removed:")
        print("  - All other counts files")
        print("  - Raw book text files")
        print("  - Tokenized text files")
        print("  - Processed text files")
        print("  - Downloaded mirror folder")


if __name__ == "__main__":
    main()

