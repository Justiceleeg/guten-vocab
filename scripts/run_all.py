#!/usr/bin/env python3
"""
Master script to run all seeding scripts in order.

This script orchestrates the complete database seeding pipeline:
1. seed_vocabulary.py - Load vocabulary words
2. seed_books.py - Load books and vocabulary
3. analyze_students.py - Analyze student vocabulary profiles
4. generate_recommendations.py - Generate book recommendations

Usage:
    python scripts/run_all.py [--skip SKIP] [--only ONLY]
    
    --skip: Skip specific scripts (comma-separated: vocab,books,students,recommendations)
    --only: Run only specific scripts (comma-separated)
"""
import argparse
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


# Script definitions
SCRIPTS = {
    "vocab": {
        "name": "Seed Vocabulary",
        "script": "seed_vocabulary.py",
        "description": "Load vocabulary words from grade-level JSON files"
    },
    "books": {
        "name": "Seed Books",
        "script": "seed_books.py",
        "description": "Load books and vocabulary from pgcorpus/Zenodo"
    },
    "students": {
        "name": "Analyze Students",
        "script": "analyze_students.py",
        "description": "Analyze student transcripts and essays to build vocabulary profiles"
    },
    "recommendations": {
        "name": "Generate Recommendations",
        "script": "generate_recommendations.py",
        "description": "Generate personalized book recommendations for students"
    }
}

# Statistics tracking
stats = {
    "vocab": {"words_loaded": 0, "status": "not_run"},
    "books": {"books_processed": 0, "status": "not_run"},
    "students": {"students_analyzed": 0, "status": "not_run"},
    "recommendations": {"recommendations_generated": 0, "status": "not_run"}
}


def run_script(script_key: str, script_info: Dict) -> bool:
    """
    Run a single seeding script.
    
    Args:
        script_key: Key in SCRIPTS dict
        script_info: Script information dict
        
    Returns:
        True if successful, False otherwise
    """
    script_name = script_info["name"]
    script_file = script_info["script"]
    
    print("\n" + "=" * 70)
    print(f"Running: {script_name}")
    print(f"Script: {script_file}")
    print("=" * 70)
    
    # Get script path
    script_path = Path(__file__).parent / script_file
    
    if not script_path.exists():
        print(f"❌ Error: Script not found: {script_path}")
        stats[script_key]["status"] = "error"
        return False
    
    # Run script as subprocess
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=False,  # Let output stream to console
            text=True,
            check=False  # Don't raise exception on non-zero exit
        )
        
        if result.returncode == 0:
            print(f"\n✅ {script_name} completed successfully")
            stats[script_key]["status"] = "success"
            return True
        else:
            print(f"\n❌ {script_name} failed with exit code {result.returncode}")
            stats[script_key]["status"] = "error"
            return False
            
    except Exception as e:
        print(f"\n❌ Error running {script_name}: {e}")
        stats[script_key]["status"] = "error"
        import traceback
        traceback.print_exc()
        return False


def parse_script_list(arg_value: Optional[str]) -> List[str]:
    """
    Parse comma-separated script list.
    
    Args:
        arg_value: Comma-separated string like "vocab,books"
        
    Returns:
        List of script keys
    """
    if not arg_value:
        return []
    
    return [key.strip() for key in arg_value.split(",") if key.strip()]


def determine_scripts_to_run(skip: Optional[str], only: Optional[str]) -> List[str]:
    """
    Determine which scripts to run based on skip/only arguments.
    
    Args:
        skip: Comma-separated list of scripts to skip
        only: Comma-separated list of scripts to run (only these)
        
    Returns:
        List of script keys to run in order
    """
    all_scripts = list(SCRIPTS.keys())
    
    if only:
        # Run only specified scripts
        only_list = parse_script_list(only)
        # Validate script keys
        invalid = [s for s in only_list if s not in all_scripts]
        if invalid:
            print(f"❌ Error: Invalid script keys: {invalid}")
            print(f"   Valid keys: {', '.join(all_scripts)}")
            sys.exit(1)
        return only_list
    
    if skip:
        # Skip specified scripts
        skip_list = parse_script_list(skip)
        # Validate script keys
        invalid = [s for s in skip_list if s not in all_scripts]
        if invalid:
            print(f"❌ Error: Invalid script keys: {invalid}")
            print(f"   Valid keys: {', '.join(all_scripts)}")
            sys.exit(1)
        return [s for s in all_scripts if s not in skip_list]
    
    # Run all scripts
    return all_scripts


def print_summary():
    """Print final summary with statistics."""
    print("\n" + "=" * 70)
    print("SEEDING PIPELINE SUMMARY")
    print("=" * 70)
    
    total_scripts = len(SCRIPTS)
    successful = sum(1 for s in stats.values() if s["status"] == "success")
    failed = sum(1 for s in stats.values() if s["status"] == "error")
    not_run = sum(1 for s in stats.values() if s["status"] == "not_run")
    
    print(f"\n📊 Execution Summary:")
    print(f"   Total scripts: {total_scripts}")
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"   ⏭️  Not run: {not_run}")
    
    print(f"\n📋 Script Details:")
    for key, script_info in SCRIPTS.items():
        status = stats[key]["status"]
        if status == "success":
            status_icon = "✅"
        elif status == "error":
            status_icon = "❌"
        else:
            status_icon = "⏭️"
        
        print(f"   {status_icon} {script_info['name']}: {status}")
    
    # Print statistics (if we had a way to capture them)
    print(f"\n📈 Statistics:")
    print(f"   Vocabulary words: {stats['vocab'].get('words_loaded', 'N/A')}")
    print(f"   Books processed: {stats['books'].get('books_processed', 'N/A')}")
    print(f"   Students analyzed: {stats['students'].get('students_analyzed', 'N/A')}")
    print(f"   Recommendations generated: {stats['recommendations'].get('recommendations_generated', 'N/A')}")
    
    print("\n" + "=" * 70)
    
    if failed > 0:
        print("⚠️  Some scripts failed. Check output above for details.")
        sys.exit(1)
    else:
        print("✅ All scripts completed successfully!")
        sys.exit(0)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Master script to run all database seeding scripts in order",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all scripts
  python scripts/run_all.py
  
  # Skip books seeding
  python scripts/run_all.py --skip books
  
  # Run only vocabulary and recommendations
  python scripts/run_all.py --only vocab,recommendations
        """
    )
    
    parser.add_argument(
        "--skip",
        type=str,
        help="Comma-separated list of scripts to skip (vocab,books,students,recommendations)"
    )
    
    parser.add_argument(
        "--only",
        type=str,
        help="Comma-separated list of scripts to run (only these scripts)"
    )
    
    args = parser.parse_args()
    
    # Validate that skip and only are not both specified
    if args.skip and args.only:
        print("❌ Error: Cannot specify both --skip and --only")
        sys.exit(1)
    
    # Determine scripts to run
    scripts_to_run = determine_scripts_to_run(args.skip, args.only)
    
    if not scripts_to_run:
        print("❌ Error: No scripts to run")
        sys.exit(1)
    
    # Print header
    print("=" * 70)
    print("DATABASE SEEDING PIPELINE")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nScripts to run ({len(scripts_to_run)}):")
    for key in scripts_to_run:
        print(f"  - {SCRIPTS[key]['name']}: {SCRIPTS[key]['description']}")
    
    # Run scripts in order
    for script_key in scripts_to_run:
        script_info = SCRIPTS[script_key]
        success = run_script(script_key, script_info)
        
        if not success:
            print(f"\n⚠️  {script_info['name']} failed. Continuing with remaining scripts...")
            # Continue with next script instead of stopping
    
    # Print summary
    print_summary()


if __name__ == "__main__":
    main()
