## 1. Mock Data Generation

### 1.1 Student Personas Generation
- [x] Create `scripts/generate_mock_data.py` script structure
- [x] Define 25 student personas with:
  - [x] Names (diverse, realistic)
  - [x] Reading proficiency levels:
    - [x] 2 students at 5th grade level
    - [x] 6 students at 6th grade level
    - [x] 13 students at 7th grade level (majority)
    - [x] 4 students at 8th grade level
  - [x] Personality traits (to make transcript realistic)
- [x] Save personas to `/data/mock/student_personas.json`:
  - [x] Create directory if needed
  - [x] Format as JSON array with student objects
  - [x] Include: name, reading_level, personality_traits, assigned_grade

### 1.2 Classroom Transcript Generation
- [x] Implement OpenAI API integration:
  - [x] Load OpenAI API key from environment
  - [x] Set up GPT-4 client
  - [x] Handle rate limits and errors gracefully
- [x] Create transcript generation prompt:
  - [x] Include student personas with reading levels
  - [x] Specify full-day structure (~40,000 words)
  - [x] Define subjects: Reading, Math, Science, Social Studies
  - [x] Request natural dialogue with teacher calling students by name
  - [x] Request timestamps format: `[09:15 AM]`
  - [x] Request speaker labels: `Teacher:`, `Student_Sarah:`, etc.
  - [x] Request "through" misuse in 15-20 students' speech
  - [x] Request natural speech patterns ("um", pauses, etc.)
- [x] Generate transcript:
  - [x] Call OpenAI API with prompt
  - [x] Handle long responses (chunked by time of day)
  - [x] Save raw response
- [x] Save transcript to `/data/mock/classroom_transcript.txt`:
  - [x] Create directory if needed
  - [x] Write transcript with proper formatting
- [x] Verify transcript output:
  - [x] Check word count (~40,000 words)
  - [x] Verify speaker distribution (all 25 students appear)
  - [x] Check timestamps are present
  - [x] Verify "through" misuse appears naturally

### 1.3 Student Essay Generation
- [x] Extend `generate_mock_data.py` to generate essays:
  - [x] Load student personas
  - [x] For each student (25 total):
    - [x] Generate essay topic (varied: book analysis, personal narrative)
    - [x] Create prompt per student:
      - [x] Include student name and reading level
      - [x] Specify ~300 words
      - [x] Request vocabulary/sentence complexity matches reading level
      - [x] For ~10 students: Request "through" misuse
      - [x] Request authentic student writing with minor imperfections
    - [x] Call OpenAI API for each essay
    - [x] Handle rate limits (delays between requests, retry logic)
    - [x] Parse response
- [x] Save essays to `/data/mock/student_essays/`:
  - [x] Create directory if needed
  - [x] Save as JSON files: `student_1_sarah.json`, etc.
  - [x] Format: `{"student_name": "...", "reading_level": 7, "essay": "...", "word_count": 305}`
  - [x] Verify word count for each essay (~300 words)

### 1.4 Verify Mock Data Quality
- [x] Review transcript sample for realism:
  - [x] Check dialogue sounds natural
  - [x] Verify teacher-student interactions are realistic
  - [x] Check vocabulary usage matches proficiency levels
- [x] Check vocabulary distribution:
  - [x] Verify lower-level students use simpler vocabulary
  - [x] Verify higher-level students use more complex vocabulary
- [x] Verify "through/thorough" misuses:
  - [x] Check misuses are subtle and realistic
  - [x] Verify they appear in transcript (15-20 students)
  - [x] Verify they appear in essays (~10 students)
- [x] Confirm file sizes:
  - [x] Check total size is appropriate for Git (~300 KB)
  - [x] Verify individual files are reasonable
- [x] Add progress tracking and error handling:
  - [x] Display progress during generation
  - [x] Handle API errors gracefully
  - [x] Log any issues encountered
  - [x] Provide summary statistics at end

**Acceptance Criteria:**
- ✅ 25 student personas created with varied proficiency levels
- ✅ 40,000-word classroom transcript generated and saved
- ✅ 25 student essays generated (300 words each)
- ✅ Misused word "through" appears naturally in transcript and essays
- ✅ All mock data files saved to `/data/mock/` directory
- ✅ Script handles errors gracefully and provides progress feedback

