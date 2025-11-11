#!/usr/bin/env python3
"""
Verification script for pgcorpus/gutenberg setup.

This script checks that the pgcorpus dataset has been properly set up
and is ready for use in the book seeding process.

Usage:
    python scripts/verify_pgcorpus.py [path_to_gutenberg_repo]
    
    If no path provided, assumes: ./gutenberg
"""

import os
import sys
from pathlib import Path


def check_mark(condition, message):
    """Print a checkmark or X based on condition."""
    symbol = "✅" if condition else "❌"
    print(f"{symbol} {message}")
    return condition


def verify_repository_structure(gutenberg_path):
    """Verify the repository has the expected structure."""
    print("\n📁 Verifying Repository Structure...")
    
    required_files = [
        "get_data.py",
        "process_data.py",
        "requirements.txt",
    ]
    
    all_passed = True
    for file in required_files:
        file_path = gutenberg_path / file
        all_passed &= check_mark(
            file_path.exists(),
            f"{file} exists"
        )
    
    return all_passed


def verify_dependencies():
    """Verify required Python packages are installed."""
    print("\n📦 Verifying Dependencies...")
    
    try:
        import pandas
        check_mark(True, "pandas installed")
    except ImportError:
        check_mark(False, "pandas not installed")
        return False
    
    try:
        import numpy
        check_mark(True, "numpy installed")
    except ImportError:
        check_mark(False, "numpy not installed")
        return False
    
    return True


def verify_data_download(gutenberg_path):
    """Verify data has been downloaded."""
    print("\n⬇️  Verifying Data Download...")
    
    mirror_path = gutenberg_path / ".mirror"
    raw_path = gutenberg_path / "data" / "raw"
    
    mirror_exists = mirror_path.exists() and any(mirror_path.iterdir())
    raw_exists = raw_path.exists() and any(raw_path.iterdir())
    
    check_mark(mirror_exists, f".mirror folder exists and has content")
    check_mark(raw_exists, f"data/raw folder exists and has content")
    
    return mirror_exists or raw_exists


def verify_processing(gutenberg_path):
    """Verify data has been processed."""
    print("\n⚙️  Verifying Data Processing...")
    
    counts_path = gutenberg_path / "data" / "counts"
    
    if not counts_path.exists():
        check_mark(False, "data/counts folder does not exist")
        return False
    
    count_files = list(counts_path.glob("*"))
    count_files = [f for f in count_files if f.is_file()]
    
    has_files = len(count_files) > 0
    check_mark(has_files, f"data/counts has {len(count_files)} files")
    
    if has_files:
        # Try to read a sample file
        sample_file = count_files[0]
        try:
            with open(sample_file, 'r') as f:
                first_line = f.readline().strip()
                check_mark(
                    len(first_line) > 0,
                    f"Sample counts file is readable: {sample_file.name}"
                )
        except Exception as e:
            check_mark(False, f"Error reading sample file: {e}")
            return False
    
    return has_files


def verify_metadata(gutenberg_path):
    """Verify metadata CSV exists and is readable."""
    print("\n📊 Verifying Metadata CSV...")
    
    # Try common locations
    possible_paths = [
        gutenberg_path / "data" / "metadata.csv",
        gutenberg_path / "metadata.csv",
        gutenberg_path / "data" / "books.csv",
    ]
    
    metadata_path = None
    for path in possible_paths:
        if path.exists():
            metadata_path = path
            break
    
    if not metadata_path:
        check_mark(False, "Metadata CSV not found in common locations")
        return False
    
    check_mark(True, f"Metadata CSV found: {metadata_path.relative_to(gutenberg_path)}")
    
    # Try to read it
    try:
        import pandas as pd
        df = pd.read_csv(metadata_path)
        check_mark(True, f"Metadata CSV readable: {len(df)} books")
        check_mark(
            "gutenberg_id" in df.columns or "id" in df.columns,
            "Metadata has gutenberg_id column"
        )
        return True
    except Exception as e:
        check_mark(False, f"Error reading metadata CSV: {e}")
        return False


def verify_counts_format(gutenberg_path):
    """Verify counts files have correct format."""
    print("\n📝 Verifying Counts File Format...")
    
    counts_path = gutenberg_path / "data" / "counts"
    
    if not counts_path.exists():
        return False
    
    count_files = [f for f in counts_path.iterdir() if f.is_file()]
    
    if not count_files:
        return False
    
    # Test reading a sample file
    sample_file = count_files[0]
    try:
        with open(sample_file, 'r') as f:
            lines = [f.readline().strip() for _ in range(5)]
            lines = [l for l in lines if l]  # Remove empty lines
            
            if not lines:
                check_mark(False, "Sample counts file appears empty")
                return False
            
            # Check format (space/tab separated or JSON)
            first_line = lines[0]
            is_valid = False
            
            # Check for space/tab separated
            parts = first_line.split()
            if len(parts) >= 2:
                # Try to parse count as number
                try:
                    int(parts[-1])
                    is_valid = True
                except ValueError:
                    pass
            
            # Check for JSON
            if not is_valid and first_line.startswith("{"):
                try:
                    import json
                    json.loads(first_line)
                    is_valid = True
                except:
                    pass
            
            check_mark(is_valid, f"Counts file format appears valid")
            return is_valid
            
    except Exception as e:
        check_mark(False, f"Error reading counts file: {e}")
        return False


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("pgcorpus/gutenberg Setup Verification")
    print("=" * 60)
    
    # Get gutenberg path
    if len(sys.argv) > 1:
        gutenberg_path = Path(sys.argv[1])
    else:
        gutenberg_path = Path("gutenberg")
    
    if not gutenberg_path.exists():
        print(f"\n❌ Error: Gutenberg repository not found at: {gutenberg_path}")
        print(f"\nUsage: python {sys.argv[0]} [path_to_gutenberg_repo]")
        print(f"   or: python {sys.argv[0]}  (assumes ./gutenberg)")
        sys.exit(1)
    
    print(f"\nChecking repository at: {gutenberg_path.absolute()}")
    
    results = []
    
    # Run all checks
    results.append(("Repository Structure", verify_repository_structure(gutenberg_path)))
    results.append(("Dependencies", verify_dependencies()))
    results.append(("Data Download", verify_data_download(gutenberg_path)))
    results.append(("Data Processing", verify_processing(gutenberg_path)))
    results.append(("Metadata CSV", verify_metadata(gutenberg_path)))
    results.append(("Counts Format", verify_counts_format(gutenberg_path)))
    
    # Summary
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All checks passed! Setup is complete and ready to use.")
        sys.exit(0)
    else:
        print("❌ Some checks failed. Please review the errors above.")
        print("\nNext steps:")
        print("1. If repository structure is missing: Clone the repository")
        print("2. If dependencies are missing: Run 'pip install -r requirements.txt'")
        print("3. If data download failed: Run 'python get_data.py'")
        print("4. If processing failed: Run 'python process_data.py'")
        sys.exit(1)


if __name__ == "__main__":
    main()

