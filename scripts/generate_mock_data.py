#!/usr/bin/env python3
"""
Generate mock classroom transcript and student essays using OpenAI API.

This script generates:
- 25 student personas with varied reading proficiency levels
- Classroom transcript (~40,000 words)
- Student essays (25 essays, ~300 words each)

Usage:
    python scripts/generate_mock_data.py [--phase PHASE] [--skip-personas]
    
    --phase: 'personas', 'transcript', 'essays', or 'all' (default: all)
    --skip-personas: Skip persona generation if file already exists
"""

import argparse
import json
import os
import random
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

try:
    from openai import OpenAI
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install openai python-dotenv")
    sys.exit(1)

# Load environment variables
load_dotenv(Path(__file__).parent.parent / "backend" / ".env")

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_MOCK_DIR = PROJECT_ROOT / "data" / "mock"
STUDENT_PERSONAS_PATH = DATA_MOCK_DIR / "student_personas.json"
TRANSCRIPT_PATH = DATA_MOCK_DIR / "classroom_transcript.txt"
STUDENT_ESSAYS_DIR = DATA_MOCK_DIR / "student_essays"


def get_openai_client() -> OpenAI:
    """Initialize OpenAI client with API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment")
        print("   Set it in backend/.env or export OPENAI_API_KEY=your_key_here")
        sys.exit(1)
    return OpenAI(api_key=api_key)


def generate_student_personas() -> List[Dict]:
    """
    Phase 1: Generate 25 diverse student personas.
    
    Distribution:
    - 2 students at 5th grade level
    - 6 students at 6th grade level
    - 13 students at 7th grade level (majority)
    - 4 students at 8th grade level
    """
    print("=" * 70)
    print("Phase 1: Student Personas Generation")
    print("=" * 70)
    
    # Define reading level distribution
    reading_levels = (
        [5] * 2 +      # 2 students at 5th grade
        [6] * 6 +      # 6 students at 6th grade
        [7] * 13 +     # 13 students at 7th grade
        [8] * 4        # 4 students at 8th grade
    )
    random.shuffle(reading_levels)
    
    # Generate diverse names (mix of common names)
    first_names = [
        "Sarah", "Michael", "Emily", "David", "Jessica", "James", "Ashley",
        "Daniel", "Amanda", "Christopher", "Melissa", "Matthew", "Nicole",
        "Andrew", "Michelle", "Joshua", "Kimberly", "Ryan", "Amy", "Kevin",
        "Angela", "Brian", "Stephanie", "Jonathan", "Rebecca"
    ]
    
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson",
        "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee",
        "Thompson", "White", "Harris", "Clark", "Lewis"
    ]
    
    # Personality traits for realistic dialogue
    personality_traits = [
        ["curious", "outgoing", "confident"],
        ["shy", "thoughtful", "observant"],
        ["enthusiastic", "talkative", "creative"],
        ["analytical", "quiet", "focused"],
        ["friendly", "helpful", "cooperative"],
        ["independent", "determined", "ambitious"],
        ["playful", "energetic", "social"],
        ["serious", "mature", "responsible"],
        ["imaginative", "artistic", "expressive"],
        ["logical", "precise", "detail-oriented"],
        ["adventurous", "bold", "risk-taking"],
        ["cautious", "careful", "methodical"],
        ["optimistic", "cheerful", "positive"],
        ["skeptical", "questioning", "critical"],
        ["empathetic", "caring", "supportive"],
        ["competitive", "driven", "goal-oriented"],
        ["collaborative", "team-oriented", "inclusive"],
        ["introspective", "reflective", "philosophical"],
        ["practical", "down-to-earth", "realistic"],
        ["idealistic", "visionary", "inspiring"],
        ["humorous", "witty", "lighthearted"],
        ["diligent", "hardworking", "persistent"],
        ["flexible", "adaptable", "open-minded"],
        ["organized", "structured", "systematic"],
        ["spontaneous", "unpredictable", "dynamic"]
    ]
    
    personas = []
    used_names = set()
    
    for i, reading_level in enumerate(reading_levels):
        # Generate unique name
        while True:
            first = random.choice(first_names)
            last = random.choice(last_names)
            full_name = f"{first} {last}"
            if full_name not in used_names:
                used_names.add(full_name)
                break
        
        # Assign personality traits
        traits = personality_traits[i % len(personality_traits)]
        
        persona = {
            "id": i + 1,
            "name": full_name,
            "first_name": first,
            "last_name": last,
            "reading_level": reading_level,
            "assigned_grade": 7,  # All students are in 7th grade class
            "personality_traits": traits
        }
        personas.append(persona)
    
    # Save to file
    DATA_MOCK_DIR.mkdir(parents=True, exist_ok=True)
    with open(STUDENT_PERSONAS_PATH, 'w') as f:
        json.dump(personas, f, indent=2)
    
    print(f"\n✅ Generated {len(personas)} student personas")
    print(f"   Distribution:")
    level_counts = {}
    for p in personas:
        level = p["reading_level"]
        level_counts[level] = level_counts.get(level, 0) + 1
    for level in sorted(level_counts.keys()):
        print(f"      Grade {level}: {level_counts[level]} students")
    print(f"\n💾 Saved to: {STUDENT_PERSONAS_PATH}")
    
    return personas


def load_student_personas() -> List[Dict]:
    """Load student personas from file."""
    if not STUDENT_PERSONAS_PATH.exists():
        print("❌ Error: Student personas file not found")
        print("   Run Phase 1 first: python scripts/generate_mock_data.py --phase personas")
        sys.exit(1)
    
    with open(STUDENT_PERSONAS_PATH) as f:
        return json.load(f)


def generate_classroom_transcript(client: OpenAI, personas: List[Dict]) -> str:
    """
    Phase 2: Generate full-day classroom transcript (~40,000 words).
    
    Includes:
    - Multiple subjects (Reading, Math, Science, Social Studies)
    - Natural dialogue with teacher and students
    - Pre-labeled speakers with timestamps
    - "through" misuse in 15-20 students' speech
    """
    print("\n" + "=" * 70)
    print("Phase 2: Classroom Transcript Generation")
    print("=" * 70)
    
    # Select 15-20 students who will misuse "through"
    students_to_misuse = random.sample(personas, random.randint(15, 20))
    misuse_student_names = [p["name"] for p in students_to_misuse]
    
    # Build prompt
    personas_text = "\n".join([
        f"- {p['name']} (Grade {p['reading_level']} reading level, traits: {', '.join(p['personality_traits'])})"
        for p in personas
    ])
    
    misuse_text = ", ".join(misuse_student_names[:5])  # Show first 5 as examples
    
    print("\n📝 Generating transcript (this may take several minutes)...")
    print("   Target: ~40,000 words")
    print("   Generating in chunks: Morning → Mid-morning → Afternoon → Late afternoon")
    
    try:
        # Generate transcript in chunks (by time of day) for better control
        # Using smaller chunks to fit within token limits
        chunks = [
            {
                "name": "Morning (Reading/Language Arts)",
                "time_range": "08:30 AM - 10:00 AM",
                "target_words": 10000,
                "subject": "Reading/Language Arts - discussing a book, vocabulary exercises"
            },
            {
                "name": "Mid-morning (Math)",
                "time_range": "10:15 AM - 11:45 AM",
                "target_words": 10000,
                "subject": "Math - problem-solving, group work, equations"
            },
            {
                "name": "Afternoon (Science)",
                "time_range": "12:30 PM - 2:00 PM",
                "target_words": 10000,
                "subject": "Science - experiment discussion, observations, hypotheses"
            },
            {
                "name": "Late afternoon (Social Studies)",
                "time_range": "2:15 PM - 3:45 PM",
                "target_words": 10000,
                "subject": "Social Studies - history discussion, current events, geography"
            }
        ]
        
        transcript_parts = []
        total_words = 0
        
        # Use gpt-4o or gpt-4-turbo which have larger context windows (128k tokens)
        # Try gpt-4o first, fall back to gpt-4-turbo if needed
        model = "gpt-4o"
        try:
            # Test if model is available
            test_response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1,
            )
        except Exception as model_error:
            if "model" in str(model_error).lower() or "not found" in str(model_error).lower():
                print(f"   ⚠️  {model} not available, using gpt-4-turbo...")
                model = "gpt-4-turbo"
            else:
                raise
        
        for i, chunk in enumerate(chunks, 1):
            print(f"\n   [{i}/{len(chunks)}] Generating {chunk['name']}...")
            
            # Generate multiple sub-chunks to reach target word count
            # Each API call generates ~4500 words, so we need ~2-3 calls per 10k word chunk
            sub_chunks = []
            chunk_words = 0
            sub_chunk_num = 1
            
            while chunk_words < chunk['target_words'] * 0.9:  # Generate until we're close to target
                is_continuation = sub_chunk_num > 1
                time_marker = chunk['time_range'].split(' - ')[0] if not is_continuation else None
                
                if is_continuation:
                    # Continue from previous sub-chunk
                    continuation_context = "\n\n".join(sub_chunks[-1].split('\n')[-10:]) if sub_chunks else ""
                    chunk_prompt = f"""Continue the classroom transcript segment. This is part {sub_chunk_num} of the {chunk['name']} period.

PREVIOUS CONTEXT (last few lines):
{continuation_context}

CONTINUE with more dialogue for this same time period and subject ({chunk['subject']}).
- Keep the same format with timestamps and speaker labels
- Continue the natural dialogue and discussions
- Include more "through" misuses if applicable
- Generate approximately 4000-5000 more words
- Make it flow naturally from the previous content"""
                else:
                    # First sub-chunk
                    chunk_prompt = f"""Generate a realistic classroom transcript segment for a 7th grade class.

STUDENTS (25 total):
{personas_text}

SEGMENT DETAILS:
- Time: {chunk['time_range']}
- Subject: {chunk['subject']}
- Target length: ~4000-5000 words (this is part 1 of the {chunk['name']} period)

REQUIREMENTS:
1. Format: Use timestamps like [09:15 AM] and speaker labels like "Teacher:" or "Student_[Name]:"
2. Natural dialogue:
   - Teacher calls students by name
   - Students respond at their reading level (vocabulary complexity matches their grade level)
   - Include natural speech patterns: "um", "like", pauses, interruptions
   - Students with lower reading levels use simpler vocabulary
   - Students with higher reading levels use more complex vocabulary
3. Word misuse: Some students should naturally misuse "through" instead of "thorough":
   Examples: {misuse_text}
   - Use it in contexts like "I need to be more through with my work" (should be "thorough")
   - Make it sound natural, not forced
   - Include it 2-4 times in this segment
4. Realism: Include classroom management moments, side conversations, questions, answers

OUTPUT FORMAT:
[{time_marker}]
Teacher: [Opening for this subject]...

Continue with realistic dialogue for this time period and subject."""

                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant that generates realistic classroom transcripts."},
                            {"role": "user", "content": chunk_prompt}
                        ],
                        temperature=0.8,
                        max_tokens=6000,  # ~4500 words per call
                    )
                    
                    sub_chunk_text = response.choices[0].message.content.strip()
                    sub_chunk_words = len(sub_chunk_text.split())
                    sub_chunks.append(sub_chunk_text)
                    chunk_words += sub_chunk_words
                    
                    print(f"      Part {sub_chunk_num}: {sub_chunk_words:,} words (total: {chunk_words:,})")
                    
                    # If we haven't reached target, continue
                    if chunk_words < chunk['target_words'] * 0.9:
                        sub_chunk_num += 1
                        time.sleep(2)  # Small delay between sub-chunks
                    else:
                        break
                        
                except Exception as e:
                    print(f"      ❌ Error in sub-chunk {sub_chunk_num}: {e}")
                    if sub_chunks:
                        # Use what we have so far
                        break
                    else:
                        raise
            
            # Combine sub-chunks for this time period
            chunk_text = "\n\n".join(sub_chunks)
            transcript_parts.append(chunk_text)
            total_words += chunk_words
            
            print(f"      ✅ {chunk['name']} complete: {chunk_words:,} words")
            
            # Small delay between major chunks to avoid rate limits
            if i < len(chunks):
                time.sleep(2)
        
        # Combine all chunks
        transcript = "\n\n".join(transcript_parts)
        word_count = len(transcript.split())
        print(f"\n   ✅ Total transcript: {word_count:,} words")
        
        # Save transcript
        DATA_MOCK_DIR.mkdir(parents=True, exist_ok=True)
        with open(TRANSCRIPT_PATH, 'w', encoding='utf-8') as f:
            f.write(transcript)
        
        print(f"\n💾 Saved to: {TRANSCRIPT_PATH}")
        
        # Verify transcript
        verify_transcript(transcript, personas, misuse_student_names)
        
        return transcript
        
    except Exception as e:
        print(f"\n❌ Error generating transcript: {e}")
        if "rate_limit" in str(e).lower():
            print("   ⚠️  Rate limit hit. Please wait and try again.")
        raise


def verify_transcript(transcript: str, personas: List[Dict], misuse_students: List[str]):
    """Verify transcript quality and requirements."""
    print("\n🔍 Verifying transcript...")
    
    # Word count
    word_count = len(transcript.split())
    print(f"   Word count: {word_count:,} words")
    if word_count < 35000:
        print("   ⚠️  Warning: Below target of 40,000 words")
    elif word_count > 50000:
        print("   ⚠️  Warning: Above target, may be too large for Git")
    else:
        print("   ✅ Word count is appropriate")
    
    # Check speaker distribution
    student_names = [p["name"] for p in personas]
    found_students = []
    for name in student_names:
        # Check for various formats: Student_Name, Student_Name:, etc.
        if f"Student_{name}" in transcript or f"{name}:" in transcript:
            found_students.append(name)
    
    print(f"   Students appearing in transcript: {len(found_students)}/{len(student_names)}")
    if len(found_students) < len(student_names) * 0.8:  # At least 80%
        print("   ⚠️  Warning: Some students may not appear in transcript")
    else:
        print("   ✅ Good speaker distribution")
    
    # Check timestamps
    timestamp_pattern = r'\[\d{1,2}:\d{2}\s+(AM|PM)\]'
    timestamps = re.findall(timestamp_pattern, transcript)
    print(f"   Timestamps found: {len(timestamps)}")
    if len(timestamps) < 10:
        print("   ⚠️  Warning: Few timestamps found")
    else:
        print("   ✅ Timestamps present")
    
    # Check "through" misuse
    # Look for patterns like "more through", "be through", "very through" (should be "thorough")
    misuse_patterns = [
        r'\bmore through\b',
        r'\bvery through\b',
        r'\bbe through\b',
        r'\bso through\b',
        r'\bquite through\b',
        r'\bmost through\b',
    ]
    misuse_count = sum(len(re.findall(pattern, transcript, re.IGNORECASE)) for pattern in misuse_patterns)
    print(f"   'through' misuses found: {misuse_count}")
    if misuse_count < 15:
        print("   ⚠️  Warning: Fewer misuses than expected (target: 15-20)")
    else:
        print("   ✅ Misuses present")


def generate_student_essays(client: OpenAI, personas: List[Dict]) -> List[Dict]:
    """
    Phase 3: Generate 25 student essays (~300 words each).
    
    Each essay:
    - Matches student's reading level
    - Has varied topics (book analysis, personal narrative)
    - Includes "through" misuse in ~10 essays
    """
    print("\n" + "=" * 70)
    print("Phase 3: Student Essay Generation")
    print("=" * 70)
    
    # Select ~10 students who will misuse "through" in their essays
    students_to_misuse = random.sample(personas, random.randint(8, 12))
    misuse_student_ids = {p["id"] for p in students_to_misuse}
    
    # Essay topics
    topics = [
        "book analysis",
        "personal narrative",
        "persuasive essay",
        "descriptive writing",
        "compare and contrast",
        "cause and effect",
        "narrative story",
        "expository essay",
    ]
    
    essays = []
    STUDENT_ESSAYS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Determine which model to use (same as transcript generation)
    model = "gpt-4o"
    try:
        test_response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=1,
        )
    except Exception as model_error:
        if "model" in str(model_error).lower() or "not found" in str(model_error).lower():
            model = "gpt-4-turbo"
    
    print(f"\n📝 Generating {len(personas)} essays...")
    
    for i, persona in enumerate(personas, 1):
        print(f"\n   [{i}/{len(personas)}] Generating essay for {persona['name']} (Grade {persona['reading_level']} level)...")
        
        # Select topic
        topic = random.choice(topics)
        
        # Determine if this student should misuse "through"
        should_misuse = persona["id"] in misuse_student_ids
        misuse_instruction = ""
        if should_misuse:
            misuse_instruction = ' Include a natural misuse of "through" instead of "thorough" (e.g., "I need to be more through in my analysis").'
        
        prompt = f"""Write a realistic 7th grade student essay (~300 words).

STUDENT INFORMATION:
- Name: {persona['name']}
- Reading Level: Grade {persona['reading_level']}
- Personality: {', '.join(persona['personality_traits'])}

REQUIREMENTS:
1. Topic: {topic}
2. Length: Approximately 300 words
3. Writing Quality: Match a Grade {persona['reading_level']} reading level student:
   - Vocabulary complexity appropriate for this level
   - Sentence structure matches reading level
   - Include minor imperfections (realistic student writing)
   - Some spelling/grammar errors are okay if they match the level
4. Authenticity: Sound like a real student wrote this, not a professional writer
{misuse_instruction}

OUTPUT: Just the essay text, no labels or metadata."""

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates realistic student essays."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=500,
            )
            
            essay_text = response.choices[0].message.content.strip()
            word_count = len(essay_text.split())
            
            # Save as JSON
            essay_data = {
                "student_id": persona["id"],
                "student_name": persona["name"],
                "reading_level": persona["reading_level"],
                "essay": essay_text,
                "word_count": word_count,
                "topic": topic,
                "has_misuse": should_misuse
            }
            
            # Sanitize filename
            safe_name = persona["name"].replace(" ", "_").lower()
            essay_filename = f"student_{persona['id']}_{safe_name}.json"
            essay_path = STUDENT_ESSAYS_DIR / essay_filename
            
            with open(essay_path, 'w', encoding='utf-8') as f:
                json.dump(essay_data, f, indent=2)
            
            essays.append(essay_data)
            print(f"      ✅ Generated {word_count} words")
            print(f"      💾 Saved to: {essay_path.name}")
            
            # Rate limiting - add small delay between requests
            if i < len(personas):
                time.sleep(1)  # 1 second delay to avoid rate limits
                
        except Exception as e:
            print(f"      ❌ Error generating essay: {e}")
            if "rate_limit" in str(e).lower():
                print("      ⚠️  Rate limit hit. Waiting 60 seconds...")
                time.sleep(60)
                # Retry once
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant that generates realistic student essays."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.9,
                        max_tokens=500,
                    )
                    essay_text = response.choices[0].message.content.strip()
                    word_count = len(essay_text.split())
                    essay_data = {
                        "student_id": persona["id"],
                        "student_name": persona["name"],
                        "reading_level": persona["reading_level"],
                        "essay": essay_text,
                        "word_count": word_count,
                        "topic": topic,
                        "has_misuse": should_misuse
                    }
                    safe_name = persona["name"].replace(" ", "_").lower()
                    essay_filename = f"student_{persona['id']}_{safe_name}.json"
                    essay_path = STUDENT_ESSAYS_DIR / essay_filename
                    with open(essay_path, 'w', encoding='utf-8') as f:
                        json.dump(essay_data, f, indent=2)
                    essays.append(essay_data)
                    print(f"      ✅ Retry successful: {word_count} words")
                except Exception as retry_error:
                    print(f"      ❌ Retry failed: {retry_error}")
            continue
    
    print(f"\n✅ Generated {len(essays)} essays")
    print(f"💾 Saved to: {STUDENT_ESSAYS_DIR}")
    
    # Verify essays
    verify_essays(essays)
    
    return essays


def verify_essays(essays: List[Dict]):
    """Verify essay quality and requirements."""
    print("\n🔍 Verifying essays...")
    
    if not essays:
        print("   ❌ No essays generated")
        return
    
    # Word counts
    word_counts = [e["word_count"] for e in essays]
    avg_words = sum(word_counts) / len(word_counts)
    min_words = min(word_counts)
    max_words = max(word_counts)
    
    print(f"   Word counts: avg={avg_words:.0f}, min={min_words}, max={max_words}")
    if avg_words < 250 or avg_words > 350:
        print("   ⚠️  Warning: Average word count outside target range (250-350)")
    else:
        print("   ✅ Word counts are appropriate")
    
    # Check misuses
    essays_with_misuse = [e for e in essays if e.get("has_misuse")]
    print(f"   Essays with 'through' misuse: {len(essays_with_misuse)}")
    if len(essays_with_misuse) < 8:
        print("   ⚠️  Warning: Fewer misuses than expected (target: ~10)")
    else:
        print("   ✅ Misuses present")
    
    # Check reading level distribution
    level_dist = {}
    for e in essays:
        level = e["reading_level"]
        level_dist[level] = level_dist.get(level, 0) + 1
    print(f"   Reading level distribution: {level_dist}")


def verify_all_data():
    """Final verification of all generated data."""
    print("\n" + "=" * 70)
    print("Final Verification")
    print("=" * 70)
    
    # Check file sizes
    total_size = 0
    
    if STUDENT_PERSONAS_PATH.exists():
        size = STUDENT_PERSONAS_PATH.stat().st_size
        total_size += size
        print(f"   student_personas.json: {size:,} bytes")
    
    if TRANSCRIPT_PATH.exists():
        size = TRANSCRIPT_PATH.stat().st_size
        total_size += size
        print(f"   classroom_transcript.txt: {size:,} bytes ({size/1024:.1f} KB)")
    
    if STUDENT_ESSAYS_DIR.exists():
        essay_files = list(STUDENT_ESSAYS_DIR.glob("*.json"))
        essay_size = sum(f.stat().st_size for f in essay_files)
        total_size += essay_size
        print(f"   student_essays/ ({len(essay_files)} files): {essay_size:,} bytes ({essay_size/1024:.1f} KB)")
    
    print(f"\n   Total size: {total_size:,} bytes ({total_size/1024:.1f} KB)")
    if total_size > 500 * 1024:  # 500 KB
        print("   ⚠️  Warning: Total size exceeds 500 KB (may be large for Git)")
    else:
        print("   ✅ File sizes are appropriate for Git")
    
    print("\n✅ Mock data generation complete!")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate mock classroom transcript and student essays"
    )
    parser.add_argument(
        "--phase",
        choices=["personas", "transcript", "essays", "all"],
        default="all",
        help="Which phase to run (default: all)",
    )
    parser.add_argument(
        "--skip-personas",
        action="store_true",
        help="Skip persona generation if file already exists",
    )
    
    args = parser.parse_args()
    
    personas = None
    client = None
    
    # Phase 1: Generate personas
    if args.phase in ["personas", "all"]:
        if args.skip_personas and STUDENT_PERSONAS_PATH.exists():
            print("⏭️  Skipping persona generation (file exists)")
            personas = load_student_personas()
        else:
            personas = generate_student_personas()
    
    # Load personas if needed for other phases
    if args.phase in ["transcript", "essays"] and personas is None:
        personas = load_student_personas()
    
    # Phase 2: Generate transcript
    if args.phase in ["transcript", "all"]:
        if not client:
            client = get_openai_client()
        generate_classroom_transcript(client, personas)
    
    # Phase 3: Generate essays
    if args.phase in ["essays", "all"]:
        if not client:
            client = get_openai_client()
        generate_student_essays(client, personas)
    
    # Final verification
    if args.phase == "all":
        verify_all_data()


if __name__ == "__main__":
    main()
