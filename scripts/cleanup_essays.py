#!/usr/bin/env python3
"""
Clean up duplicate student essays, keeping only those matching student personas.

This script:
1. Loads the 25 student personas from student_personas.json
2. Scans all essay files in student_essays/
3. Keeps only essays where student_name matches a persona name
4. Deletes duplicate/extra essays
5. Reports what was kept and deleted

Usage:
    python scripts/cleanup_essays.py
    python scripts/cleanup_essays.py --dry-run
"""
import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_MOCK_DIR = PROJECT_ROOT / "data" / "mock"
STUDENT_PERSONAS_PATH = DATA_MOCK_DIR / "student_personas.json"
ESSAYS_DIR = DATA_MOCK_DIR / "student_essays"


def load_student_personas():
    """Load the 25 original student personas from JSON."""
    if not STUDENT_PERSONAS_PATH.exists():
        print(f"❌ Error: Student personas file not found at {STUDENT_PERSONAS_PATH}")
        print(f"   Please run 'python scripts/generate_mock_data.py --phase personas' first")
        sys.exit(1)
    
    with open(STUDENT_PERSONAS_PATH, 'r') as f:
        personas = json.load(f)
    
    print(f"✅ Loaded {len(personas)} student personas")
    return personas


def scan_essay_files():
    """Scan all essay files and extract metadata."""
    if not ESSAYS_DIR.exists():
        print(f"❌ Error: Essays directory not found at {ESSAYS_DIR}")
        sys.exit(1)
    
    essay_files = list(ESSAYS_DIR.glob("student_*.json"))
    print(f"\n📄 Found {len(essay_files)} essay files")
    
    essays_by_id = defaultdict(list)
    essay_metadata = []
    
    for essay_file in essay_files:
        try:
            with open(essay_file, 'r') as f:
                data = json.load(f)
            
            student_id = data.get("student_id")
            student_name = data.get("student_name")
            reading_level = data.get("reading_level")
            
            if student_id and student_name:
                metadata = {
                    "file_path": essay_file,
                    "file_name": essay_file.name,
                    "student_id": student_id,
                    "student_name": student_name,
                    "reading_level": reading_level
                }
                essay_metadata.append(metadata)
                essays_by_id[student_id].append(metadata)
            else:
                print(f"⚠️  Warning: Missing data in {essay_file.name}")
        
        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Error parsing {essay_file.name}: {e}")
        except Exception as e:
            print(f"⚠️  Warning: Error reading {essay_file.name}: {e}")
    
    return essay_metadata, essays_by_id


def identify_essays_to_keep(personas, essays_by_id):
    """Identify which essays to keep based on persona names and IDs."""
    # Create mappings for lookup
    persona_by_name = {p["name"]: p for p in personas}
    persona_by_id = {p["id"]: p for p in personas}
    persona_names = set(persona_by_name.keys())
    
    print("\n" + "=" * 70)
    print("Analysis")
    print("=" * 70)
    
    essays_to_keep = []
    essays_to_delete = []
    
    # Group by student_id and check for duplicates
    for student_id, essays in sorted(essays_by_id.items()):
        if len(essays) == 1:
            # Only one essay for this ID
            essay = essays[0]
            if essay["student_name"] in persona_names:
                essays_to_keep.append(essay)
                print(f"✓ ID {student_id}: Keeping '{essay['student_name']}' (matches persona)")
            else:
                essays_to_delete.append(essay)
                print(f"✗ ID {student_id}: Deleting '{essay['student_name']}' (no matching persona)")
        else:
            # Multiple essays for this ID
            print(f"\n⚠️  ID {student_id} has {len(essays)} essays:")
            
            # First, try to match by ID AND name (exact match)
            correct_persona = persona_by_id.get(student_id)
            exact_match = None
            
            if correct_persona:
                for essay in essays:
                    if essay["student_name"] == correct_persona["name"]:
                        exact_match = essay
                        break
            
            if exact_match:
                # Found exact match by ID and name
                essays_to_keep.append(exact_match)
                print(f"   ✓ Keeping '{exact_match['student_name']}' (exact match for ID {student_id})")
                
                for essay in essays:
                    if essay != exact_match:
                        essays_to_delete.append(essay)
                        print(f"   ✗ Deleting '{essay['student_name']}' (duplicate/wrong ID)")
            else:
                # No exact match - keep any that match persona names
                matched = False
                for essay in essays:
                    if essay["student_name"] in persona_names:
                        essays_to_keep.append(essay)
                        print(f"   ⚠️  Keeping '{essay['student_name']}' (matches persona but wrong ID)")
                        matched = True
                    else:
                        essays_to_delete.append(essay)
                        print(f"   ✗ Deleting '{essay['student_name']}' (no matching persona)")
                
                if not matched:
                    print(f"   ⚠️  Warning: No essay matches persona for ID {student_id}")
    
    return essays_to_keep, essays_to_delete


def delete_essays(essays_to_delete, dry_run=False):
    """Delete the specified essay files."""
    if not essays_to_delete:
        print("\n✅ No essays to delete")
        return
    
    print("\n" + "=" * 70)
    if dry_run:
        print("DRY RUN - Files that would be deleted:")
    else:
        print("Deleting Essays")
    print("=" * 70)
    
    for essay in essays_to_delete:
        file_path = essay["file_path"]
        print(f"  {'[DRY RUN] ' if dry_run else ''}Deleting: {essay['file_name']}")
        print(f"    Student: {essay['student_name']} (ID: {essay['student_id']})")
        
        if not dry_run:
            try:
                file_path.unlink()
            except Exception as e:
                print(f"    ❌ Error deleting file: {e}")
    
    if not dry_run:
        print(f"\n✅ Deleted {len(essays_to_delete)} essay files")


def verify_cleanup(personas):
    """Verify the cleanup was successful."""
    print("\n" + "=" * 70)
    print("Verification")
    print("=" * 70)
    
    essay_files = list(ESSAYS_DIR.glob("student_*.json"))
    print(f"\n📊 Remaining essay files: {len(essay_files)}")
    
    # Check that we have exactly one essay per persona
    persona_names = {p["name"] for p in personas}
    found_names = set()
    
    for essay_file in essay_files:
        try:
            with open(essay_file, 'r') as f:
                data = json.load(f)
            student_name = data.get("student_name")
            if student_name:
                found_names.add(student_name)
        except:
            pass
    
    missing_names = persona_names - found_names
    extra_names = found_names - persona_names
    
    print(f"\nExpected: {len(personas)} essays (one per persona)")
    print(f"Found: {len(found_names)} essays")
    
    if len(found_names) == len(personas) and not missing_names and not extra_names:
        print("\n✅ SUCCESS! All essay files match student personas exactly")
        print(f"   - {len(found_names)} essays")
        print(f"   - All names match personas")
        print(f"   - No duplicates")
    else:
        print("\n⚠️  Issues found:")
        if missing_names:
            print(f"\n   Missing essays for {len(missing_names)} personas:")
            for name in sorted(missing_names):
                print(f"     - {name}")
        if extra_names:
            print(f"\n   Extra essays not in personas ({len(extra_names)}):")
            for name in sorted(extra_names):
                print(f"     - {name}")
    
    return len(found_names) == len(personas) and not missing_names and not extra_names


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Clean up duplicate student essays, keeping only those matching personas"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without actually deleting"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Essay Cleanup Script")
    print("=" * 70)
    
    if args.dry_run:
        print("\n⚠️  DRY RUN MODE - No files will be deleted")
    
    # Load personas
    personas = load_student_personas()
    
    # Scan essay files
    essay_metadata, essays_by_id = scan_essay_files()
    
    # Identify which essays to keep/delete
    essays_to_keep, essays_to_delete = identify_essays_to_keep(personas, essays_by_id)
    
    # Show summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"  Total essays found: {len(essay_metadata)}")
    print(f"  Essays to keep: {len(essays_to_keep)}")
    print(f"  Essays to delete: {len(essays_to_delete)}")
    
    if not args.dry_run and essays_to_delete:
        response = input("\nDo you want to delete these files? (yes/no): ")
        if response.lower() not in ["yes", "y"]:
            print("❌ Aborted")
            sys.exit(0)
    
    # Delete essays
    delete_essays(essays_to_delete, dry_run=args.dry_run)
    
    # Verify cleanup (skip in dry-run mode)
    if not args.dry_run:
        success = verify_cleanup(personas)
        
        if success:
            print("\n" + "=" * 70)
            print("✅ Cleanup Complete!")
            print("=" * 70)
            print("\nNext steps:")
            print("  1. Run: python scripts/reset_students.py --run-analysis")
            print("\nThis will:")
            print("  - Clear the database")
            print("  - Insert the 25 correct students")
            print("  - Re-run vocabulary analysis")
            print("  - Generate book recommendations")
        else:
            print("\n⚠️  Cleanup completed but some issues remain")
            print("   Review the verification output above")
    else:
        print("\n" + "=" * 70)
        print("Dry run complete - no files were deleted")
        print("=" * 70)
        print("\nTo actually delete the files, run:")
        print("  python scripts/cleanup_essays.py")


if __name__ == "__main__":
    main()

