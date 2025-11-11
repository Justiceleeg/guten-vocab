# Change: Generate Mock Data

## Why
Generate realistic classroom transcript and student essays using LLMs to create mock data for testing and demonstration. This mock data will be used to build student vocabulary profiles and test the recommendation system without requiring real student data.

## What Changes
- Create `scripts/generate_mock_data.py` script with three phases:
  - **Phase 1: Student Personas Generation**
    - Generate 25 diverse student personas with names, reading proficiency levels (2 at 5th, 6 at 6th, 13 at 7th, 4 at 8th), and personality traits
    - Save to `/data/mock/student_personas.json`
  - **Phase 2: Classroom Transcript Generation**
    - Use OpenAI GPT-4 API to generate full-day classroom transcript (~40,000 words)
    - Include multiple subjects (Reading, Math, Science, Social Studies)
    - Natural dialogue with teacher and students at appropriate proficiency levels
    - Pre-labeled speakers with timestamps
    - Plant misused word "through" (instead of "thorough") in 15-20 students' speech
    - Save to `/data/mock/classroom_transcript.txt`
  - **Phase 3: Student Essay Generation**
    - Generate 25 essays (one per student, ~300 words each)
    - Topics vary (book analysis, personal narrative)
    - Writing quality matches each student's reading level
    - Include "through" misuse in ~10 essays
    - Save to `/data/mock/student_essays/` as JSON files
- Add verification and quality checks:
  - Verify word counts and speaker distribution
  - Check vocabulary distribution matches proficiency levels
  - Verify "through/thorough" misuses are realistic
  - Confirm file sizes are appropriate for Git

## Impact
- Affected specs: None (data generation only)
- Affected code: `scripts/generate_mock_data.py`, `data/mock/` directory
- External dependencies: OpenAI GPT-4 API (requires API key)

