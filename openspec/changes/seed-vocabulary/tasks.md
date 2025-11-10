## 1. Vocabulary Data Seeding

### 1.1 Vocabulary Lists Setup
- [ ] Create `data/vocab/` directory if it doesn't exist
- [ ] Copy vocabulary JSON files to `/data/vocab/`:
  - [ ] 5th_grade.json (150 words)
  - [ ] 6th_grade.json (125 words)
  - [ ] 7th_grade.json (125 words)
  - [ ] 8th_grade.json (125 words)
- [ ] Verify JSON files are valid and contain expected word lists
- [ ] Document source of vocabulary lists

### 1.2 Create Vocabulary Seed Script
- [ ] Create `scripts/seed_vocabulary.py`
- [ ] Load all 4 JSON files from `data/vocab/`
- [ ] Parse JSON structure and extract words with grade levels
- [ ] Handle duplicates:
  - [ ] Detect words that appear in multiple grade files
  - [ ] Keep highest grade level for duplicate words
  - [ ] Log duplicate handling decisions
- [ ] Insert words into `vocabulary_words` table:
  - [ ] Use SQLAlchemy models
  - [ ] Handle database connection errors
  - [ ] Use batch inserts for performance
- [ ] Print summary statistics:
  - [ ] Total words loaded
  - [ ] Words per grade level
  - [ ] Duplicates handled
  - [ ] "Loaded X words across grades 5-8"

### 1.3 Test Vocabulary Seeding
- [ ] Run `python scripts/seed_vocabulary.py`
- [ ] Verify data in database:
  - [ ] Query: `SELECT COUNT(*) FROM vocabulary_words;` (should be ~525)
  - [ ] Query words by grade level distribution
  - [ ] Verify no duplicate words (same word, different grade)
- [ ] Handle errors gracefully
- [ ] Add idempotency (can run multiple times safely)

**Acceptance Criteria:**
- ✅ All 4 vocabulary JSON files in `data/vocab/`
- ✅ Vocabulary seed script created and working
- ✅ ~525 unique vocabulary words loaded into database
- ✅ Words properly associated with grade levels
- ✅ Script is idempotent (can run multiple times)

