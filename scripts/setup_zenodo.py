#!/usr/bin/env python3
"""
Setup script for Zenodo 2018 pgcorpus dataset.

This script helps you set up the pre-processed Zenodo dataset as an alternative
to the full pgcorpus download.

Usage:
    python scripts/setup_zenodo.py [path_to_extracted_zenodo_dataset]
    
    Example:
    python scripts/setup_zenodo.py ~/datasets/pgcorpus-2018
"""

import os
import sys
from pathlib import Path


def verify_zenodo_dataset(dataset_path: Path):
    """Verify the Zenodo dataset structure."""
    print("=" * 70)
    print("Zenodo 2018 Dataset Verification")
    print("=" * 70)
    
    if not dataset_path.exists():
        print(f"\n❌ Error: Dataset path not found: {dataset_path}")
        print("\nPlease extract the Zenodo dataset first:")
        print("  1. Download from: https://zenodo.org/records/2422561")
        print("  2. Extract SPGC-counts-2018-07-18.zip")
        print("  3. Run this script with the path to the extracted folder")
        sys.exit(1)
    
    print(f"\n📁 Checking: {dataset_path.absolute()}\n")
    
    # Check for counts folder
    counts_dir = dataset_path / "counts"
    if counts_dir.exists():
        count_files = list(counts_dir.glob("*"))
        count_files = [f for f in count_files if f.is_file()]
        print(f"✅ Counts folder found: {len(count_files):,} files")
        
        if count_files:
            # Check a sample file
            sample = count_files[0]
            size = sample.stat().st_size
            print(f"   Sample file: {sample.name} ({size:,} bytes)")
    else:
        print(f"❌ Counts folder not found: {counts_dir}")
        print(f"   Expected structure: {dataset_path}/counts/")
        return False
    
    # Check for metadata
    metadata_files = list(dataset_path.glob("*.csv"))
    if metadata_files:
        print(f"✅ Metadata CSV found: {metadata_files[0].name}")
    else:
        print(f"⚠️  Metadata CSV not found (optional but recommended)")
        print(f"   You can download it from: https://zenodo.org/records/2422561")
    
    # Check structure
    print(f"\n📊 Dataset Structure:")
    print(f"  {dataset_path}/")
    if counts_dir.exists():
        print(f"    ├── counts/ ({len(count_files):,} files)")
    if metadata_files:
        print(f"    └── {metadata_files[0].name}")
    
    return True


def create_config(dataset_path: Path, config_path: Path = None):
    """Create a config file pointing to the Zenodo dataset."""
    if config_path is None:
        config_path = Path("data/pgcorpus_config.json")
    
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    import json
    config = {
        "dataset_type": "zenodo_2018",
        "dataset_path": str(dataset_path.absolute()),
        "counts_path": str((dataset_path / "counts").absolute()),
        "metadata_path": str((dataset_path / "metadata.csv").absolute()) if (dataset_path / "metadata.csv").exists() else None
    }
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Created config file: {config_path}")
    print(f"   Scripts can now use this dataset location")


def main():
    """Main setup function."""
    if len(sys.argv) < 2:
        # Default to project directory
        project_root = Path(__file__).parent.parent
        default_path = project_root / "data" / "pgcorpus-2018"
        
        print("Usage: python setup_zenodo.py [path_to_extracted_zenodo_dataset]")
        print(f"\nDefault location: {default_path}")
        print("\nExample:")
        print(f"  python setup_zenodo.py {default_path}")
        print("  python setup_zenodo.py  # Uses default if dataset exists")
        print("\nFirst, download and extract:")
        print("  1. Go to: https://zenodo.org/records/2422561")
        print("  2. Download: SPGC-counts-2018-07-18.zip (~1.5 GB)")
        print(f"  3. Extract to: {default_path}")
        print("  4. Run this script")
        
        # Try default path
        if default_path.exists() and (default_path / "counts").exists():
            print(f"\n✅ Found dataset at default location, using: {default_path}")
            dataset_path = default_path
        else:
            sys.exit(1)
    else:
        dataset_path = Path(sys.argv[1]).expanduser()
    
    if verify_zenodo_dataset(dataset_path):
        create_config(dataset_path)
        print("\n" + "=" * 70)
        print("✅ Setup Complete!")
        print("=" * 70)
        print("\nNext steps:")
        print("  1. Update scripts/seed_books.py to use this dataset")
        print("  2. Run: python scripts/seed_books.py")
        print("\nThe dataset is ready to use!")
    else:
        print("\n❌ Setup failed. Please check the dataset structure.")
        sys.exit(1)


if __name__ == "__main__":
    main()

