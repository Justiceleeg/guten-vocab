## 1. Implementation

### 1.1 Student-Book Matching Algorithm
- [ ] Create `scripts/generate_recommendations.py` script structure
- [ ] Implement matching logic:
  - [ ] For each student:
    - [ ] Get their vocabulary profile (known words from student_vocabulary where correct_usage_count > 0)
    - [ ] Get their reading level from students table
    - [ ] For each book:
      - [ ] Calculate vocabulary overlap:
        - [ ] Known words: words student has used correctly (in student_vocabulary with correct_usage_count > 0)
        - [ ] New words: words in book but not in student's profile
        - [ ] Overlap percentage: known_words / total_vocab_words_in_book
      - [ ] Filter books by reading level:
        - [ ] Prefer books at student's level ± 1 grade
        - [ ] Allow higher if vocabulary fit is exceptional
      - [ ] Calculate match score using algorithm:
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
      - [ ] Sort books by match score (descending)
      - [ ] Store top 3 books per student

### 1.2 Store Student Recommendations
- [ ] For each student:
  - [ ] Insert top 3 recommendations into `student_recommendations` table:
    - [ ] student_id
    - [ ] book_id  
    - [ ] match_score
    - [ ] known_words_percent
    - [ ] new_words_count
  - [ ] Handle duplicate recommendations (idempotent - update if exists)
- [ ] Add progress tracking (processing student X of 25)
- [ ] Verify recommendations make sense (spot check a few students)
  - [ ] Check that high proficiency students get appropriately challenging books
  - [ ] Check that low proficiency students get appropriately accessible books
  - [ ] Verify match scores are reasonable (0-1 range)

### 1.3 Class-Wide Recommendations
- [ ] Aggregate student recommendations:
  - [ ] Count how many students have each book in their top 3
  - [ ] Calculate average match score per book across all students who have it recommended
  - [ ] Select top 2 books that appear most frequently in individual recommendations
  - [ ] Store in `class_recommendations` table:
    - [ ] book_id
    - [ ] match_score (average across students)
    - [ ] students_recommended_count
- [ ] Handle duplicates (idempotent - update if exists)

### 1.4 Run Recommendation Engine
- [ ] Execute `python scripts/generate_recommendations.py`
- [ ] Monitor progress and handle any errors
- [ ] Verify output in database:
  - [ ] Query: `SELECT COUNT(*) FROM student_recommendations;` (should be 75 = 25 students × 3)
  - [ ] Query: `SELECT COUNT(*) FROM class_recommendations;` (should be 2)
  - [ ] Query student with highest/lowest vocabulary mastery and verify their recommendations
  - [ ] Spot check: Do recommendations make sense for high/low proficiency students?
  - [ ] Verify match scores are in valid range [0, 1]

### 1.5 Master Seed Script
- [ ] Create `scripts/run_all.py`:
  - [ ] Runs all scripts in order:
    1. seed_vocabulary.py
    2. seed_books.py
    3. analyze_students.py (assumes mock data exists)
    4. generate_recommendations.py
  - [ ] Add error handling and logging
  - [ ] Print summary at end with all statistics:
    - [ ] Vocabulary words loaded
    - [ ] Books processed
    - [ ] Students analyzed
    - [ ] Recommendations generated
  - [ ] Add command-line arguments for selective execution (optional)

## 2. Testing & Verification

### 2.1 Algorithm Verification
- [ ] Test match score calculation with known inputs
- [ ] Verify penalty logic works correctly (too easy/hard books get penalized)
- [ ] Verify reading level bonus is applied correctly
- [ ] Test edge cases:
  - [ ] Student with 0% vocabulary mastery
  - [ ] Student with 100% vocabulary mastery
  - [ ] Book with very low vocabulary coverage
  - [ ] Book with very high vocabulary coverage

### 2.2 Data Quality Checks
- [ ] Verify all 25 students have 3 recommendations
- [ ] Verify no duplicate book recommendations per student
- [ ] Verify match scores are in valid range [0, 1]
- [ ] Verify known_words_percent + new_words_count logic is correct
- [ ] Verify class recommendations are sensible (top 2 books make sense for class)

### 2.3 Database Verification
- [ ] Verify `student_recommendations` records created correctly
- [ ] Verify `class_recommendations` records created correctly
- [ ] Verify foreign key constraints work (student_id, book_id)
- [ ] Verify data integrity (no orphaned records)

**Acceptance Criteria:**
- ✅ Matching algorithm correctly calculates vocabulary overlap
- ✅ Book recommendations prioritize ~50% known / 50% new vocabulary
- ✅ Reading level considered in recommendations
- ✅ Each student has 3 book recommendations stored
- ✅ Class-wide top 2 books identified
- ✅ Master script can seed entire database from scratch
- ✅ Recommendations are sensible for students at different proficiency levels

