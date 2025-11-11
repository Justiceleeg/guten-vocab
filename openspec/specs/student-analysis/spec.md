# student-analysis Specification

## Purpose
TBD - created by archiving change analyze-student-vocabulary. Update Purpose after archive.
## Requirements
### Requirement: Student Data Loading
The system SHALL load and parse student language data from mock classroom transcripts and essays.

#### Scenario: Load classroom transcript
- **WHEN** the analysis pipeline runs
- **THEN** it loads `/data/mock/classroom_transcript.txt`
- **AND** parses the format `[TIME] Speaker: dialogue`
- **AND** extracts all dialogue per student
- **AND** aggregates dialogue by student name into a dictionary

#### Scenario: Load student essays
- **WHEN** the analysis pipeline runs
- **THEN** it loads all JSON files from `/data/mock/student_essays/`
- **AND** maps essays to student names
- **AND** creates a dictionary of `{student_name: essay_text}`

### Requirement: Text Preprocessing
The system SHALL preprocess raw text using spaCy to extract vocabulary words while preserving original context.

#### Scenario: Process text with spaCy for vocabulary matching
- **WHEN** raw text (transcript dialogue or essay) is provided
- **THEN** the system tokenizes the text
- **AND** preserves original sentences with original word forms
- **AND** for each token, lemmatizes to get root form (for vocabulary matching only)
- **AND** filters to only alphabetic tokens (removes punctuation and numbers)
- **AND** converts to lowercase for matching
- **AND** matches inflected forms (e.g., "endured", "prevails") to base vocabulary words (e.g., "endure", "prevail")

#### Scenario: Count vocabulary word frequencies
- **WHEN** tokens are processed with lemmatization
- **THEN** the system matches lemmatized forms to vocabulary_words table (525 words)
- **AND** counts occurrences of each vocabulary word
- **AND** stores original word forms and their sentence contexts for OpenAI analysis
- **AND** returns a dictionary of `{vocab_word: count}` with original sentence examples

### Requirement: Vocabulary Usage Correctness Analysis
The system SHALL analyze vocabulary word usage correctness using OpenAI API.

#### Scenario: Analyze word usage for a student
- **WHEN** a student has used vocabulary words in their dialogue or essay (identified via lemmatization)
- **THEN** for each vocabulary word used, the system extracts 1-2 example sentences with ORIGINAL word forms (not lemmatized)
- **AND** sends the examples to OpenAI API with a structured prompt using the base vocabulary word
- **AND** asks for correctness analysis of the original usage
- **AND** receives a JSON response with:
  - `correct_usage_count`: number of correct usages
  - `incorrect_usage_count`: number of incorrect usages
  - `misuse_examples`: array of sentences where the word was misused
  - `analysis`: brief explanation of the analysis
- **AND** parses and stores the results

#### Scenario: Handle API rate limits
- **WHEN** OpenAI API rate limits are encountered
- **THEN** the system implements exponential backoff retry logic
- **AND** continues processing after the rate limit is cleared

#### Scenario: Handle API errors gracefully
- **WHEN** OpenAI API calls fail
- **THEN** the system logs the error
- **AND** continues processing other students or words
- **AND** provides progress tracking (analyzing student X of 25)

### Requirement: Student Vocabulary Profile Building
The system SHALL build comprehensive vocabulary profiles for each student and store them in the database.

#### Scenario: Calculate vocabulary mastery metrics
- **WHEN** a student's vocabulary usage has been analyzed
- **THEN** the system calculates:
  - Total grade-level words known (used correctly at least once)
  - Percentage of grade-level vocabulary mastered
  - List of missing vocabulary words
- **AND** identifies misused words with examples

#### Scenario: Store student profile in database
- **WHEN** a student's vocabulary profile is complete
- **THEN** the system inserts or updates the `students` table with:
  - Student name
  - Reading level (from student personas)
  - Assigned grade
- **AND** inserts or updates the `student_vocabulary` table with:
  - Word usage counts
  - Correct usage counts
  - Incorrect usage counts
  - Misuse examples (as array of text)

### Requirement: Class-Wide Vocabulary Analysis
The system SHALL aggregate class-wide statistics on vocabulary mastery and misuse.

#### Scenario: Calculate class-wide statistics
- **WHEN** all student profiles have been built
- **THEN** the system calculates:
  - Top 10 words most students are missing
  - Commonly misused words across the class
  - Average vocabulary mastery by grade level
- **AND** stores or outputs these statistics for dashboard use

#### Scenario: Identify commonly misused words
- **WHEN** class-wide analysis runs
- **THEN** the system identifies words that are frequently misused across multiple students
- **AND** "through" (when used instead of "thorough") appears in the commonly misused words list

### Requirement: Analysis Pipeline Execution
The system SHALL provide a script that executes the complete analysis pipeline.

#### Scenario: Run complete analysis pipeline
- **WHEN** `python scripts/analyze_students.py` is executed
- **THEN** the script processes all 25 students
- **AND** monitors progress and handles errors
- **AND** verifies output in database:
  - 25 students in `students` table
  - Thousands of records in `student_vocabulary` table
  - Student with highest/lowest vocabulary mastery can be queried
  - "through" appears in commonly misused words

