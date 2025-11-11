## 1. Implementation

### 1.1 Student-Book Matching Algorithm
- [x] Create `scripts/generate_recommendations.py` script structure
- [x] Implement matching logic:
  - [x] For each student:
    - [x] Get their vocabulary profile (known words from student_vocabulary where correct_usage_count > 0)
    - [x] Get their reading level from students table
    - [x] For each book:
      - [x] Calculate vocabulary overlap:
        - [x] Known words: words student has used correctly (in student_vocabulary with correct_usage_count > 0)
        - [x] New words: words in book but not in student's profile
        - [x] Overlap percentage: known_words / total_vocab_words_in_book
      - [x] Filter books by reading level:
        - [x] Prefer books at student's level ± 1 grade
        - [x] Allow higher if vocabulary fit is exceptional
      - [x] Calculate match score using algorithm:
        ```python
        # Goal: ~50% known, ~50% new for optimal challenge
        target_known_percent = 0.5
        known_percent = len(known_words) / len(book_vocab_words)
        
        # Penalize if too easy (>80% known) or too hard (<30% known)
        if known_percent > 0.8:
            penalty = (known_percent - 0.8) * 2
        elif known_percent < 0.3:
            penalty = (0.3 - known_percent) * 2
        else:
            penalty = 0
        
        # Reward books close to target
        closeness_to_target = 1 - abs(known_percent - target_known_percent)
        
        # Reading level match bonus
        reading_level_diff = abs(book.reading_level - student.reading_level)
        reading_level_score = max(0, 1 - (reading_level_diff / 2))
        
        match_score = (closeness_to_target * 0.6) + (reading_level_score * 0.3) - penalty
        match_score = max(0, min(1, match_score))  # Clamp to [0, 1]
        ```
      - [x] Sort books by match score (descending)
      - [x] Store top 3 books per student

### 1.2 Store Student Recommendations
- [x] For each student:
  - [x] Insert top 3 recommendations into `student_recommendations` table:
    - [x] student_id
    - [x] book_id  
    - [x] match_score
    - [x] known_words_percent
    - [x] new_words_count
  - [x] Handle duplicate recommendations (idempotent - update if exists)
- [x] Add progress tracking (processing student X of 25)
- [x] Verify recommendations make sense (spot check a few students)
  - [x] Check that high proficiency students get appropriately challenging books
  - [x] Check that low proficiency students get appropriately accessible books
  - [x] Verify match scores are reasonable (0-1 range)

### 1.3 Class-Wide Recommendations
- [x] Aggregate student recommendations:
  - [x] Count how many students have each book in their top 3
  - [x] Calculate average match score per book across all students who have it recommended
  - [x] Select top 2 books that appear most frequently in individual recommendations
  - [x] Store in `class_recommendations` table:
    - [x] book_id
    - [x] match_score (average across students)
    - [x] students_recommended_count
- [x] Handle duplicates (idempotent - update if exists)

### 1.4 Run Recommendation Engine
- [x] Execute `python scripts/generate_recommendations.py`
- [x] Monitor progress and handle any errors
- [x] Verify output in database:
  - [x] Query: `SELECT COUNT(*) FROM student_recommendations;` (should be 75 = 25 students × 3)
  - [x] Query: `SELECT COUNT(*) FROM class_recommendations;` (should be 2)
  - [x] Query student with highest/lowest vocabulary mastery and verify their recommendations
  - [x] Spot check: Do recommendations make sense for high/low proficiency students?
  - [x] Verify match scores are in valid range [0, 1]

### 1.5 Master Seed Script
- [x] Create `scripts/run_all.py`:
  - [x] Runs all scripts in order:
    1. seed_vocabulary.py
    2. seed_books.py
    3. analyze_students.py (assumes mock data exists)
    4. generate_recommendations.py
  - [x] Add error handling and logging
  - [x] Print summary at end with all statistics:
    - [x] Vocabulary words loaded
    - [x] Books processed
    - [x] Students analyzed
    - [x] Recommendations generated
  - [x] Add command-line arguments for selective execution (optional)

## 2. Testing & Verification

### 2.1 Algorithm Verification
- [x] Test match score calculation with known inputs
- [x] Verify penalty logic works correctly (too easy/hard books get penalized)
- [x] Verify reading level bonus is applied correctly
- [x] Test edge cases:
  - [x] Student with 0% vocabulary mastery
  - [x] Student with 100% vocabulary mastery
  - [x] Book with very low vocabulary coverage
  - [x] Book with very high vocabulary coverage

### 2.2 Data Quality Checks
- [x] Verify all 25 students have 3 recommendations
- [x] Verify no duplicate book recommendations per student
- [x] Verify match scores are in valid range [0, 1]
- [x] Verify known_words_percent + new_words_count logic is correct
- [x] Verify class recommendations are sensible (top 2 books make sense for class)

### 2.3 Database Verification
- [x] Verify `student_recommendations` records created correctly
- [x] Verify `class_recommendations` records created correctly
- [x] Verify foreign key constraints work (student_id, book_id)
- [x] Verify data integrity (no orphaned records)

**Acceptance Criteria:**
- ✅ Matching algorithm correctly calculates vocabulary overlap
- ✅ Book recommendations prioritize ~50% known / 50% new vocabulary
- ✅ Reading level considered in recommendations
- ✅ Each student has 3 book recommendations stored
- ✅ Class-wide top 2 books identified
- ✅ Master script can seed entire database from scratch
- ✅ Recommendations are sensible for students at different proficiency levels

