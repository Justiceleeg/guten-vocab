## ADDED Requirements

### Requirement: Student Book Recommendations
The system SHALL generate personalized book recommendations for each student based on their vocabulary profile and reading level. Recommendations SHALL prioritize books that provide optimal vocabulary challenge (~50% known words, ~50% new words) while considering reading level appropriateness.

#### Scenario: Generate recommendations for student
- **WHEN** a student has a vocabulary profile with known words (words used correctly at least once)
- **THEN** the system calculates match scores for all books
- **AND** selects the top 3 books with highest match scores
- **AND** stores recommendations in `student_recommendations` table with match_score, known_words_percent, and new_words_count

#### Scenario: Match score calculation
- **WHEN** calculating match score for a book-student pair
- **THEN** the system calculates vocabulary overlap (known words / total vocab words in book)
- **AND** applies penalty if book is too easy (>80% known) or too hard (<30% known)
- **AND** rewards books close to target ratio (~50% known)
- **AND** applies reading level bonus (prefers books at student's level ± 1 grade)
- **AND** combines factors into final match score (clamped to [0, 1])

#### Scenario: Optimal challenge ratio
- **WHEN** a book has ~50% known vocabulary and ~50% new vocabulary for a student
- **THEN** the book receives highest match score
- **AND** books with >80% known vocabulary receive penalty
- **AND** books with <30% known vocabulary receive penalty

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

