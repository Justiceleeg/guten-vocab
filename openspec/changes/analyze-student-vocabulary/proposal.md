# Change: Analyze Student Vocabulary

## Why
Build a comprehensive student analysis pipeline that processes mock classroom transcripts and student essays to create detailed vocabulary profiles. This pipeline will identify which grade-level vocabulary words each student uses correctly, detect misused words, and calculate vocabulary mastery metrics. These profiles are essential for generating personalized book recommendations and providing teachers with actionable insights on student vocabulary development.

## What Changes
- Create `scripts/analyze_students.py` script implementing a multi-phase analysis pipeline:
  - **Phase 1: Data Loading**
    - Parse classroom transcript (`/data/mock/classroom_transcript.txt`) with format `[TIME] Speaker: dialogue`
    - Load student essays from JSON files (`/data/mock/student_essays/`)
    - Aggregate dialogue and essays by student name
  - **Phase 2: Text Preprocessing**
    - Use spaCy for tokenization and lemmatization (for vocabulary matching only)
    - Match inflected word forms (e.g., "endured", "prevails") to base vocabulary words (e.g., "endure", "prevail")
    - Preserve original sentences with original word forms for OpenAI analysis
    - Extract vocabulary words (filter to 525 words in vocabulary_words table)
    - Count word frequencies per student
  - **Phase 3: Vocabulary Correctness Analysis**
    - Integrate OpenAI API to analyze vocabulary usage correctness
    - For each vocabulary word used by a student, extract example sentences
    - Send to OpenAI with structured prompt to determine correct vs incorrect usage
    - Parse JSON responses with correctness counts and misuse examples
    - Handle rate limits and errors gracefully
  - **Phase 4: Profile Building**
    - Calculate vocabulary mastery metrics (total words known, mastery percentage)
    - Identify missing vocabulary words per student
    - Store student records in `students` table
    - Store vocabulary usage data in `student_vocabulary` table (usage counts, correctness, misuse examples)
  - **Phase 5: Class-Wide Analysis**
    - Aggregate statistics: top 10 missing words, commonly misused words, average mastery by grade
    - Output class-wide insights for dashboard
- Add progress tracking and error handling throughout pipeline
- Verify analysis results in database (25 students, thousands of student_vocabulary records)

## Impact
- Affected specs: New capability `student-analysis` (ADDED)
- Affected code: 
  - `scripts/analyze_students.py` (new script)
  - Database tables: `students`, `student_vocabulary` (data population)
- External dependencies: 
  - OpenAI GPT-4 API (requires API key for correctness analysis)
  - spaCy NLP library (for text preprocessing)
  - PostgreSQL database (for storing profiles)

