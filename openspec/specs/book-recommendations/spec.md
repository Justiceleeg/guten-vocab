# book-recommendations Specification

## Purpose
TBD - created by archiving change implement-book-recommendations. Update Purpose after archive.
## Requirements
### Requirement: Student Book Recommendations
The system SHALL generate personalized book recommendations for each student based on their vocabulary profile and reading level. Recommendations SHALL optimize for both high percentage of known words (50-75% for comprehension) AND high count of new words (10-30+ for vocabulary expansion) while considering reading level appropriateness.

#### Scenario: Generate recommendations for student
- **WHEN** a student has a vocabulary profile with known words (including baseline knowledge based on reading level and prerequisite grade levels)
- **THEN** the system calculates match scores for all books
- **AND** selects the top 3 books with highest match scores
- **AND** stores recommendations in `student_recommendations` table with match_score, known_words_percent, and new_words_count

#### Scenario: Match score calculation
- **WHEN** calculating match score for a book-student pair
- **THEN** the system builds student vocabulary profile including:
  - Words used correctly in transcript/essay
  - Baseline knowledge based on reading level (40-85% of current grade words)
  - Prerequisite grade levels (~95% of words from grades below assigned grade)
- **AND** calculates vocabulary overlap (known words / total vocab words in book)
- **AND** calculates count of new vocabulary words (words student doesn't know)
- **AND** applies penalty if book is too easy (>85% known) or too hard (<40% known)
- **AND** rewards high percentage of known words (50-75% optimal) with 40% weight
- **AND** rewards high count of new words (10-30+ optimal) with 40% weight
- **AND** applies reading level bonus (prefers books at student's level ± 1 grade) with 20% weight
- **AND** combines factors into final match score (clamped to [0, 1])

#### Scenario: Optimal challenge ratio
- **WHEN** a book has 50-75% known vocabulary AND 10-30+ new vocabulary words for a student
- **THEN** the book receives highest match score
- **AND** books with >85% known vocabulary receive penalty (too easy)
- **AND** books with <40% known vocabulary receive penalty (too hard)

### Requirement: Class-Wide Book Recommendations
The system SHALL aggregate individual student recommendations to identify books recommended to the most students, and SHALL select the top 2 books for class-wide reading.

#### Scenario: Aggregate class recommendations
- **WHEN** all students have individual recommendations
- **THEN** the system counts how many students have each book in their top 3
- **AND** calculates average match score per book across all students
- **AND** selects top 2 books that appear most frequently
- **AND** stores in `class_recommendations` table with average match_score and students_recommended_count

### Requirement: Master Seed Script
The system SHALL provide a master script that orchestrates all database seeding operations in the correct order.

#### Scenario: Run complete seed pipeline
- **WHEN** executing the master seed script
- **THEN** the script runs all seeding scripts in order:
  1. seed_vocabulary.py
  2. seed_books.py
  3. analyze_students.py
  4. generate_recommendations.py
- **AND** handles errors gracefully
- **AND** prints summary statistics at completion

