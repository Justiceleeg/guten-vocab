#!/usr/bin/env python3
"""
Check the status of pgcorpus download/processing.

This script helps you monitor:
- Whether get_data.py or process_data.py is running
- Progress of downloads (file counts, sizes)
- Network/disk activity
- Estimated time remaining

Usage:
    python scripts/check_pgcorpus_status.py [path_to_gutenberg]
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime


def check_processes():
    """Check if pgcorpus processes are running."""
    print("🔍 Checking for running processes...")
    
    processes = []
    try:
        result = subprocess.run(
            ['ps', 'aux'],
            capture_output=True,
            text=True
        )
        
        lines = result.stdout.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['get_data', 'process_data', 'rsync']):
                if 'grep' not in line:
                    processes.append(line)
    except Exception as e:
        print(f"  ⚠️  Could not check processes: {e}")
        return []
    
    if processes:
        print(f"  ✅ Found {len(processes)} related process(es):")
        for proc in processes:
            # Extract key info
            parts = proc.split()
            if len(parts) > 10:
                pid = parts[1]
                cpu = parts[2]
                mem = parts[3]
                cmd = ' '.join(parts[10:])
                print(f"    - PID {pid}: {cmd[:60]}... (CPU: {cpu}%, MEM: {mem}%)")
    else:
        print("  ❌ No pgcorpus processes found running")
    
    return processes


def check_directory_status(gutenberg_path: Path):
    """Check status of gutenberg directories."""
    print("\n📁 Checking directory status...")
    
    data_dir = gutenberg_path / "data"
    
    # Check .mirror folder (downloads)
    mirror_dir = data_dir / ".mirror"
    if mirror_dir.exists():
        files = list(mirror_dir.rglob("*"))
        files = [f for f in files if f.is_file()]
        total_size = sum(f.stat().st_size for f in files if f.exists())
        
        print(f"  📦 .mirror folder:")
        print(f"    - Files: {len(files):,}")
        print(f"    - Size: {format_size(total_size)}")
        
        # Check if recently modified
        if files:
            latest = max(f.stat().st_mtime for f in files if f.exists())
            latest_time = datetime.fromtimestamp(latest)
            age = time.time() - latest
            if age < 300:  # Modified in last 5 minutes
                print(f"    - ✅ Recently active (last file: {latest_time.strftime('%H:%M:%S')})")
            else:
                print(f"    - ⚠️  Last modified: {latest_time.strftime('%Y-%m-%d %H:%M:%S')} ({int(age/60)} min ago)")
    else:
        print(f"  📦 .mirror folder: Not found (download may not have started)")
    
    # Check raw folder
    raw_dir = data_dir / "raw"
    if raw_dir.exists():
        files = list(raw_dir.glob("*"))
        files = [f for f in files if f.is_file()]
        print(f"  📄 data/raw folder: {len(files):,} files")
    else:
        print(f"  📄 data/raw folder: Not found")
    
    # Check counts folder
    counts_dir = data_dir / "counts"
    if counts_dir.exists():
        files = list(counts_dir.glob("*"))
        files = [f for f in files if f.is_file() and not f.name.startswith('.')]
        total_size = sum(f.stat().st_size for f in files if f.exists())
        print(f"  📝 data/counts folder: {len(files):,} files ({format_size(total_size)})")
        
        if files:
            latest = max(f.stat().st_mtime for f in files if f.exists())
            latest_time = datetime.fromtimestamp(latest)
            age = time.time() - latest
            if age < 300:
                print(f"    - ✅ Recently active (last file: {latest_time.strftime('%H:%M:%S')})")
    else:
        print(f"  📝 data/counts folder: Not found")
    
    # Check metadata
    metadata_dir = gutenberg_path / "metadata"
    csv_files = list(metadata_dir.glob("*.csv")) if metadata_dir.exists() else []
    if csv_files:
        print(f"  📊 Metadata CSV: Found ({len(csv_files)} file(s))")
    else:
        print(f"  📊 Metadata CSV: Not found")


def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def check_network_activity():
    """Check if there's network activity (rsync/download)."""
    print("\n🌐 Checking network activity...")
    
    try:
        # Check for rsync processes
        result = subprocess.run(
            ['pgrep', '-f', 'rsync'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            print(f"  ✅ rsync process(es) running (PIDs: {', '.join(pids)})")
            return True
        else:
            print(f"  ❌ No rsync processes found")
            return False
    except Exception as e:
        print(f"  ⚠️  Could not check network activity: {e}")
        return False


def estimate_progress(gutenberg_path: Path):
    """Estimate progress based on file counts."""
    print("\n📊 Progress Estimate...")
    
    # Typical numbers (as of 2025)
    total_books_expected = 75000
    
    data_dir = gutenberg_path / "data"
    mirror_dir = data_dir / ".mirror"
    
    if mirror_dir.exists():
        # Count downloaded books (rough estimate)
        files = list(mirror_dir.rglob("*.txt"))
        files = [f for f in files if f.is_file()]
        
        # Rough estimate: each book might have multiple files, but let's count unique IDs
        book_ids = set()
        for f in files:
            # Try to extract book ID from path
            parts = f.parts
            for part in parts:
                if part.isdigit() and len(part) >= 4:
                    book_ids.add(int(part))
        
        if book_ids:
            downloaded = len(book_ids)
            percent = (downloaded / total_books_expected) * 100
            print(f"  📚 Estimated books downloaded: ~{downloaded:,} / ~{total_books_expected:,} ({percent:.1f}%)")
        else:
            print(f"  📚 Files found: {len(files):,} (estimating progress...)")
    
    counts_dir = data_dir / "counts"
    if counts_dir.exists():
        count_files = list(counts_dir.glob("*"))
        count_files = [f for f in count_files if f.is_file() and not f.name.startswith('.')]
        if count_files:
            processed = len(count_files)
            percent = (processed / total_books_expected) * 100
            print(f"  ⚙️  Estimated books processed: ~{processed:,} / ~{total_books_expected:,} ({percent:.1f}%)")


def main():
    """Main status check."""
    print("=" * 70)
    print("pgcorpus Download/Processing Status Check")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get gutenberg path
    gutenberg_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("gutenberg")
    
    if not gutenberg_path.exists():
        print(f"\n❌ Error: Gutenberg directory not found: {gutenberg_path}")
        print(f"\nUsage: python {sys.argv[0]} [gutenberg_path]")
        sys.exit(1)
    
    print(f"\n📁 Checking: {gutenberg_path.absolute()}\n")
    
    # Check processes
    processes = check_processes()
    
    # Check network activity
    has_network = check_network_activity()
    
    # Check directory status
    check_directory_status(gutenberg_path)
    
    # Estimate progress
    estimate_progress(gutenberg_path)
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    
    if processes:
        print("✅ Process is RUNNING")
        if has_network:
            print("✅ Network activity detected (downloading)")
        else:
            print("⚠️  No network activity (may be processing)")
    else:
        print("❌ No process found - may have completed or not started")
    
    print("\n💡 Tips:")
    print("  - Run this script periodically to monitor progress")
    print("  - Check file counts in .mirror/ to see download progress")
    print("  - Check file counts in data/counts/ to see processing progress")
    print("  - If no activity for >10 minutes, process may have completed or errored")


if __name__ == "__main__":
    main()

