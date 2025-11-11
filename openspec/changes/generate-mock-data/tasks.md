## 1. Mock Data Generation

### 1.1 Student Personas Generation
- [ ] Create `scripts/generate_mock_data.py` script structure
- [ ] Define 25 student personas with:
  - [ ] Names (diverse, realistic)
  - [ ] Reading proficiency levels:
    - [ ] 2 students at 5th grade level
    - [ ] 6 students at 6th grade level
    - [ ] 13 students at 7th grade level (majority)
    - [ ] 4 students at 8th grade level
  - [ ] Personality traits (to make transcript realistic)
- [ ] Save personas to `/data/mock/student_personas.json`:
  - [ ] Create directory if needed
  - [ ] Format as JSON array with student objects
  - [ ] Include: name, reading_level, personality_traits, assigned_grade

### 1.2 Classroom Transcript Generation
- [ ] Implement OpenAI API integration:
  - [ ] Load OpenAI API key from environment
  - [ ] Set up GPT-4 client
  - [ ] Handle rate limits and errors gracefully
- [ ] Create transcript generation prompt:
  - [ ] Include student personas with reading levels
  - [ ] Specify full-day structure (~40,000 words)
  - [ ] Define subjects: Reading, Math, Science, Social Studies
  - [ ] Request natural dialogue with teacher calling students by name
  - [ ] Request timestamps format: `[09:15 AM]`
  - [ ] Request speaker labels: `Teacher:`, `Student_Sarah:`, etc.
  - [ ] Request "through" misuse in 15-20 students' speech
  - [ ] Request natural speech patterns ("um", pauses, etc.)
- [ ] Generate transcript:
  - [ ] Call OpenAI API with prompt
  - [ ] Handle long responses (may need streaming or chunking)
  - [ ] Save raw response
- [ ] Save transcript to `/data/mock/classroom_transcript.txt`:
  - [ ] Create directory if needed
  - [ ] Write transcript with proper formatting
- [ ] Verify transcript output:
  - [ ] Check word count (~40,000 words)
  - [ ] Verify speaker distribution (all 25 students appear)
  - [ ] Check timestamps are present
  - [ ] Verify "through" misuse appears naturally

### 1.3 Student Essay Generation
- [ ] Extend `generate_mock_data.py` to generate essays:
  - [ ] Load student personas
  - [ ] For each student (25 total):
    - [ ] Generate essay topic (varied: book analysis, personal narrative)
    - [ ] Create prompt per student:
      - [ ] Include student name and reading level
      - [ ] Specify ~300 words
      - [ ] Request vocabulary/sentence complexity matches reading level
      - [ ] For ~10 students: Request "through" misuse
      - [ ] Request authentic student writing with minor imperfections
    - [ ] Call OpenAI API for each essay
    - [ ] Handle rate limits (may need delays between requests)
    - [ ] Parse response
- [ ] Save essays to `/data/mock/student_essays/`:
  - [ ] Create directory if needed
  - [ ] Save as JSON files: `student_1_sarah.json`, etc.
  - [ ] Format: `{"student_name": "...", "reading_level": 7, "essay": "...", "word_count": 305}`
  - [ ] Verify word count for each essay (~300 words)

### 1.4 Verify Mock Data Quality
- [ ] Review transcript sample for realism:
  - [ ] Check dialogue sounds natural
  - [ ] Verify teacher-student interactions are realistic
  - [ ] Check vocabulary usage matches proficiency levels
- [ ] Check vocabulary distribution:
  - [ ] Verify lower-level students use simpler vocabulary
  - [ ] Verify higher-level students use more complex vocabulary
- [ ] Verify "through/thorough" misuses:
  - [ ] Check misuses are subtle and realistic
  - [ ] Verify they appear in transcript (15-20 students)
  - [ ] Verify they appear in essays (~10 students)
- [ ] Confirm file sizes:
  - [ ] Check total size is appropriate for Git (~300 KB)
  - [ ] Verify individual files are reasonable
- [ ] Add progress tracking and error handling:
  - [ ] Display progress during generation
  - [ ] Handle API errors gracefully
  - [ ] Log any issues encountered
  - [ ] Provide summary statistics at end

**Acceptance Criteria:**
- ✅ 25 student personas created with varied proficiency levels
- ✅ 40,000-word classroom transcript generated and saved
- ✅ 25 student essays generated (300 words each)
- ✅ Misused word "through" appears naturally in transcript and essays
- ✅ All mock data files saved to `/data/mock/` directory
- ✅ Script handles errors gracefully and provides progress feedback

