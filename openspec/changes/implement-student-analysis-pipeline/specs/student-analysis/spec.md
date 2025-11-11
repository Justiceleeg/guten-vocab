## MODIFIED Requirements

### Requirement: Analysis Pipeline Execution
The system SHALL provide a script that executes the complete analysis pipeline.

#### Scenario: Run complete analysis pipeline
- **WHEN** `python scripts/analyze_students.py` is executed
- **THEN** the script processes all 25 students from mock data
- **AND** loads and parses classroom transcript from `/data/mock/classroom_transcript.txt`
- **AND** loads student essays from `/data/mock/student_essays/`
- **AND** processes text with spaCy for vocabulary extraction
- **AND** analyzes vocabulary usage correctness using OpenAI API
- **AND** builds vocabulary profiles for each student
- **AND** calculates class-wide statistics
- **AND** stores all results in database
- **AND** monitors progress and handles errors gracefully
- **AND** verifies output in database:
  - 25 students in `students` table
  - Thousands of records in `student_vocabulary` table
  - Student with highest/lowest vocabulary mastery can be queried
  - "through" appears in commonly misused words

