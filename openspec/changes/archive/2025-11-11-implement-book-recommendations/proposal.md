# Change: Implement Book Recommendation Engine

## Why
Generate personalized book recommendations for each student based on their vocabulary profile and reading level. The recommendation engine will match students with books that provide optimal vocabulary challenge (~50% known words, ~50% new words) while considering reading level appropriateness. This enables teachers to provide targeted reading assignments that help students expand their vocabulary while building on words they already know.

## What Changes
- Create `scripts/generate_recommendations.py` script implementing a multi-phase recommendation pipeline:
  - **Phase 1: Student-Book Matching**
    - For each student, calculate vocabulary overlap with each book
    - Identify known words (words student has used correctly) and new words (words in book but not in student's profile)
    - Calculate match scores using algorithm that:
      - Targets ~50% known / ~50% new vocabulary for optimal challenge
      - Penalizes books that are too easy (>80% known) or too hard (<30% known)
      - Rewards books close to target ratio
      - Considers reading level match (prefer books at student's level ± 1 grade)
    - Select top 3 books per student
  - **Phase 2: Store Student Recommendations**
    - Insert top 3 recommendations per student into `student_recommendations` table
    - Store match scores, known words percentage, and new words count
  - **Phase 3: Class-Wide Recommendations**
    - Aggregate individual recommendations to identify books recommended to most students
    - Calculate average match scores per book
    - Select top 2 books for class-wide reading
    - Store in `class_recommendations` table
  - **Phase 4: Master Seed Script**
    - Create `scripts/run_all.py` to orchestrate all seeding scripts in order
    - Add error handling and progress tracking
- Add verification and testing to ensure recommendations are sensible

## Impact
- Affected specs: `book-recommendations` (new capability)
- Affected code: 
  - `scripts/generate_recommendations.py` (new script)
  - `scripts/run_all.py` (new script)
  - Database tables: `student_recommendations`, `class_recommendations` (data population)
- External dependencies: None (uses existing database and models)

