## 1. Implementation

### 1.1 Transcript Parsing
- [ ] Create `scripts/analyze_students.py` script structure
- [ ] Implement transcript parser:
  - [ ] Load `/data/mock/classroom_transcript.txt`
  - [ ] Parse format: `[TIME] Speaker: dialogue`
  - [ ] Extract all dialogue per student
  - [ ] Aggregate by student name
  - [ ] Output: Dictionary of `{student_name: [all_their_dialogue_combined]}`

### 1.2 Essay Loading
- [ ] Implement essay loader:
  - [ ] Load all JSON files from `/data/mock/student_essays/`
  - [ ] Map to student names
  - [ ] Output: Dictionary of `{student_name: essay_text}`

### 1.3 Text Preprocessing with spaCy
- [ ] Implement text processing function:
  - [ ] Input: Raw text (transcript dialogue OR essay)
  - [ ] Use spaCy to:
    - [ ] Tokenize text (preserve original sentences for OpenAI analysis)
    - [ ] For each token:
      - [ ] Lemmatize to get root form (for vocabulary matching)
      - [ ] Store mapping: `original_word → lemmatized_word`
      - [ ] Filter to only alphabetic tokens (remove punctuation, numbers)
      - [ ] Convert to lowercase for matching
    - [ ] Preserve original sentences with original word forms
  - [ ] Output: 
    - [ ] Dictionary of `{vocab_word: count}` (using lemmatized forms for matching)
    - [ ] Original sentences indexed by vocabulary word (for OpenAI analysis)
- [ ] Create word frequency counter:
  - [ ] For each token, lemmatize and check if it matches vocabulary_words table (525 words)
  - [ ] Count occurrences of each vocabulary word (using lemmatized matching)
  - [ ] Store original word forms and their sentence contexts
  - [ ] Output: `{vocab_word: count}` with original sentence examples

### 1.4 OpenAI Analysis - Vocabulary Understanding
- [ ] Implement OpenAI API integration for correctness checking:
  - [ ] For each student:
    - [ ] Combine their transcript dialogue + essay into one text
    - [ ] For each vocabulary word they used (identified via lemmatization):
      - [ ] Extract 1-2 example sentences with ORIGINAL word forms (not lemmatized)
      - [ ] Send to OpenAI with prompt using the base vocabulary word:
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
      - [ ] Parse response and store results
- [ ] Handle rate limits and errors gracefully
- [ ] Add progress tracking (analyzing student X of 25)

### 1.5 Build Student Vocabulary Profiles
- [ ] For each student:
  - [ ] Calculate vocabulary mastery:
    - [ ] Total grade-level words known (used correctly at least once)
    - [ ] Percentage of grade-level vocabulary mastered
    - [ ] List of missing vocabulary words
  - [ ] Identify misused words with examples
  - [ ] Insert/update database:
    - [ ] `students` table (name, reading level, assigned grade)
    - [ ] `student_vocabulary` table (word usage counts, correctness, examples)

### 1.6 Class-Wide Analysis
- [ ] Aggregate class statistics:
  - [ ] Top 10 words most students are missing
  - [ ] Commonly misused words across class ("through" should appear here)
  - [ ] Average vocabulary mastery by grade level
  - [ ] Store in database or output to JSON for dashboard

### 1.7 Run Analysis Pipeline
- [ ] Execute `python scripts/analyze_students.py`
- [ ] Monitor progress and handle any errors
- [ ] Verify output in database:
  - [ ] Query: `SELECT COUNT(*) FROM students;` (should be 25)
  - [ ] Query: `SELECT COUNT(*) FROM student_vocabulary;` (thousands of records)
  - [ ] Query student with highest/lowest vocabulary mastery
  - [ ] Check that "through" appears in commonly misused words

## 2. Testing & Verification

### 2.1 Data Quality Checks
- [ ] Verify transcript parsing extracts all 25 students
- [ ] Verify essay loading maps correctly to student names
- [ ] Verify spaCy lemmatization correctly matches inflected forms to vocabulary words
- [ ] Verify original sentences are preserved for OpenAI analysis
- [ ] Verify vocabulary word filtering (only 525 words counted)

### 2.2 OpenAI Integration
- [ ] Test OpenAI API calls with sample data
- [ ] Verify JSON response parsing
- [ ] Test rate limit handling
- [ ] Verify error handling for API failures

### 2.3 Database Verification
- [ ] Verify all 25 students inserted into `students` table
- [ ] Verify `student_vocabulary` records created correctly
- [ ] Verify usage counts and correctness counts are accurate
- [ ] Verify misuse examples stored correctly

### 2.4 Class-Wide Statistics
- [ ] Verify top 10 missing words calculation
- [ ] Verify "through" appears in commonly misused words
- [ ] Verify average mastery by grade level calculation

**Acceptance Criteria:**
- ✅ Transcript successfully parsed and attributed to students
- ✅ Essays loaded and processed
- ✅ spaCy lemmatization correctly matches inflected forms to vocabulary words
- ✅ Original sentences preserved for OpenAI analysis
- ✅ OpenAI API successfully analyzing vocabulary usage
- ✅ Student vocabulary profiles stored in database
- ✅ Class-wide statistics calculated
- ✅ Can query any student's vocabulary mastery from database

