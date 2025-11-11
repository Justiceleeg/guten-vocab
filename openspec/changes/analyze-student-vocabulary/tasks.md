## 1. Implementation

### 1.1 Transcript Parsing
- [x] Create `scripts/analyze_students.py` script structure
- [x] Implement transcript parser:
  - [x] Load `/data/mock/classroom_transcript.txt`
  - [x] Parse format: `[TIME] Speaker: dialogue`
  - [x] Extract all dialogue per student
  - [x] Aggregate by student name
  - [x] Output: Dictionary of `{student_name: [all_their_dialogue_combined]}`

### 1.2 Essay Loading
- [x] Implement essay loader:
  - [x] Load all JSON files from `/data/mock/student_essays/`
  - [x] Map to student names
  - [x] Output: Dictionary of `{student_name: essay_text}`

### 1.3 Text Preprocessing with spaCy
- [x] Implement text processing function:
  - [x] Input: Raw text (transcript dialogue OR essay)
  - [x] Use spaCy to:
    - [x] Tokenize text (preserve original sentences for OpenAI analysis)
    - [x] For each token:
      - [x] Lemmatize to get root form (for vocabulary matching)
      - [x] Store mapping: `original_word → lemmatized_word`
      - [x] Filter to only alphabetic tokens (remove punctuation, numbers)
      - [x] Convert to lowercase for matching
    - [x] Preserve original sentences with original word forms
  - [x] Output: 
    - [x] Dictionary of `{vocab_word: count}` (using lemmatized forms for matching)
    - [x] Original sentences indexed by vocabulary word (for OpenAI analysis)
- [x] Create word frequency counter:
  - [x] For each token, lemmatize and check if it matches vocabulary_words table (525 words)
  - [x] Count occurrences of each vocabulary word (using lemmatized matching)
  - [x] Store original word forms and their sentence contexts
  - [x] Output: `{vocab_word: count}` with original sentence examples

### 1.4 OpenAI Analysis - Vocabulary Understanding
- [x] Implement OpenAI API integration for correctness checking:
  - [x] For each student:
    - [x] Combine their transcript dialogue + essay into one text
    - [x] For each vocabulary word they used (identified via lemmatization):
      - [x] Extract 1-2 example sentences with ORIGINAL word forms (not lemmatized)
      - [x] Send to OpenAI with prompt using the base vocabulary word:
        ```
        Analyze if the student correctly uses the word "[WORD]" in these contexts:
        
        1. [sentence]
        2. [sentence]
        
        Respond with JSON:
        {
          "correct_usage_count": X,
          "incorrect_usage_count": Y,
          "misuse_examples": ["sentence if misused"],
          "analysis": "brief explanation"
        }
        ```
      - [x] Parse response and store results
- [x] Handle rate limits and errors gracefully
- [x] Add progress tracking (analyzing student X of 25)

### 1.5 Build Student Vocabulary Profiles
- [x] For each student:
  - [x] Calculate vocabulary mastery:
    - [x] Total grade-level words known (used correctly at least once)
    - [x] Percentage of grade-level vocabulary mastered
    - [x] List of missing vocabulary words
  - [x] Identify misused words with examples
  - [x] Insert/update database:
    - [x] `students` table (name, reading level, assigned grade)
    - [x] `student_vocabulary` table (word usage counts, correctness, examples)

### 1.6 Class-Wide Analysis
- [x] Aggregate class statistics:
  - [x] Top 10 words most students are missing
  - [x] Commonly misused words across class ("through" should appear here)
  - [x] Average vocabulary mastery by grade level
  - [x] Store in database or output to JSON for dashboard

### 1.7 Run Analysis Pipeline
- [x] Execute `python scripts/analyze_students.py`
- [x] Monitor progress and handle any errors
- [x] Verify output in database:
  - [x] Query: `SELECT COUNT(*) FROM students;` (should be 25)
  - [x] Query: `SELECT COUNT(*) FROM student_vocabulary;` (thousands of records)
  - [x] Query student with highest/lowest vocabulary mastery
  - [x] Check that "through" appears in commonly misused words

## 2. Testing & Verification

### 2.1 Data Quality Checks
- [x] Verify transcript parsing extracts all 25 students
- [x] Verify essay loading maps correctly to student names
- [x] Verify spaCy lemmatization correctly matches inflected forms to vocabulary words
- [x] Verify original sentences are preserved for OpenAI analysis
- [x] Verify vocabulary word filtering (only 525 words counted)

### 2.2 OpenAI Integration
- [x] Test OpenAI API calls with sample data
- [x] Verify JSON response parsing
- [x] Test rate limit handling
- [x] Verify error handling for API failures

### 2.3 Database Verification
- [x] Verify all 25 students inserted into `students` table
- [x] Verify `student_vocabulary` records created correctly
- [x] Verify usage counts and correctness counts are accurate
- [x] Verify misuse examples stored correctly

### 2.4 Class-Wide Statistics
- [x] Verify top 10 missing words calculation
- [x] Verify "through" appears in commonly misused words
- [x] Verify average mastery by grade level calculation

**Acceptance Criteria:**
- ✅ Transcript successfully parsed and attributed to students
- ✅ Essays loaded and processed
- ✅ spaCy lemmatization correctly matches inflected forms to vocabulary words
- ✅ Original sentences preserved for OpenAI analysis
- ✅ OpenAI API successfully analyzing vocabulary usage
- ✅ Student vocabulary profiles stored in database
- ✅ Class-wide statistics calculated
- ✅ Can query any student's vocabulary mastery from database

