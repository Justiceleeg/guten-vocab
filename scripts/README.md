# Scripts Documentation

This directory contains scripts for data generation, database seeding, and verification. These scripts run **offline** before deployment to populate the database with vocabulary words, books, students, and recommendations.

## Table of Contents

1. [Main Pipeline Scripts](#main-pipeline-scripts)
2. [Utility Scripts](#utility-scripts)
3. [Prerequisites](#prerequisites)
4. [Quick Start](#quick-start)
5. [Script Details](#script-details)
6. [Troubleshooting](#troubleshooting)

---

## Main Pipeline Scripts

These scripts form the core data generation pipeline and should be run in order:

1. **`seed_vocabulary.py`** - Load vocabulary words from grade-level JSON files
2. **`seed_books.py`** - Load books and extract vocabulary from Project Gutenberg corpus
3. **`analyze_students.py`** - Analyze student transcripts and essays to build vocabulary profiles
4. **`generate_recommendations.py`** - Generate personalized book recommendations

### Master Script

**`run_all.py`** - Orchestrates all four scripts in the correct order with progress tracking.

---

## Quick Start

### Run Complete Pipeline

```bash
# From project root
cd backend
source venv/bin/activate
python ../scripts/run_all.py
```

This will:
1. Seed 525 vocabulary words (grades 5-8)
2. Load 100 books from Project Gutenberg
3. Analyze 25 students from mock data
4. Generate 75 student recommendations + 2 class recommendations

### Run Individual Scripts

```bash
# Seed vocabulary only
python scripts/seed_vocabulary.py

# Seed books only
python scripts/seed_books.py

# Analyze students only
python scripts/analyze_students.py

# Generate recommendations only
python scripts/generate_recommendations.py
```

### Skip or Run Specific Scripts

```bash
# Skip books seeding (if already done)
python scripts/run_all.py --skip books

# Run only vocabulary and recommendations
python scripts/run_all.py --only vocab,recommendations
```

---

## Prerequisites

### Required Dependencies

- **Python 3.9+**
- **PostgreSQL database** (local or remote)
- **spaCy English model**: `python -m spacy download en_core_web_sm`
- **Environment variables** set in `backend/.env`:
  - `DATABASE_URL` - PostgreSQL connection string
  - `OPENAI_API_KEY` - Required for `analyze_students.py`

### Python Packages

All required packages are in `backend/requirements.txt`. Install with:

```bash
cd backend
pip install -r requirements.txt
```

Key dependencies:
- `sqlalchemy` - Database ORM
- `psycopg2-binary` - PostgreSQL driver
- `spacy` - NLP processing
- `openai` - GPT-4 API (for student analysis)
- `pandas` - Data processing (for book seeding)
- `textstat` - Reading level calculation (optional, for book seeding)

### Data Files

The scripts expect the following data structure:

```
data/
├── vocab/
│   ├── 5th_grade.json
│   ├── 6th_grade.json
│   ├── 7th_grade.json
│   └── 8th_grade.json
├── mock/
│   ├── classroom_transcript.txt
│   └── student_essays/
│       └── [student_name].json
└── pgcorpus-2018/  (optional, for book seeding)
    ├── metadata.csv
    └── [book_id].txt files
```

---

## Script Details

### 1. `seed_vocabulary.py`

**Purpose**: Loads vocabulary words from grade-level JSON files into the database.

**What it does**:
- Reads JSON files from `data/vocab/` (5th-8th grade)
- Handles duplicates (keeps highest grade level)
- Applies spaCy lemmatization for word normalization
- Inserts words into `vocabulary_words` table

**Expected Output**:
- 525 unique vocabulary words inserted
- Words categorized by grade level (5-8)
- Each word includes: word, grade_level, definition, part_of_speech

**Example**:
```bash
python scripts/seed_vocabulary.py
```

**Output**:
```
Loading vocabulary files...
  Loaded 150 words from 5th_grade.json
  Loaded 125 words from 6th_grade.json
  Loaded 125 words from 7th_grade.json
  Loaded 125 words from 8th_grade.json

Total unique words: 525
Words inserted: 525
✅ Loaded 525 words across grades 5-8
```

**Dependencies**: None (must run first)

---

### 2. `seed_books.py`

**Purpose**: Loads books from Project Gutenberg corpus and extracts vocabulary matches.

**What it does**:
- Loads book metadata from `data/pgcorpus-2018/metadata.csv`
- Filters books: Children's Literature, English language, available text files
- Selects top 100 books by popularity (download count)
- Processes book text with spaCy to find vocabulary matches
- Inserts books and book-vocabulary associations

**Expected Output**:
- 100 books inserted into `books` table
- Book-vocabulary associations in `book_vocabulary` table
- Average ~109 vocabulary matches per book

**Example**:
```bash
python scripts/seed_books.py
```

**Output**:
```
📁 Using dataset: data/pgcorpus-2018
📊 Loading metadata from: data/pgcorpus-2018/metadata.csv
   ✅ Loaded 57,713 books

🔍 Filtering books...
   ✅ Selected top 100 books

📚 Processing 100 books...
   [1/100] Processing: The Wonderful Wizard of Oz
      ✅ Found 36 vocabulary matches
   ...
✅ Phase 2 Complete!
   ✅ Books processed successfully: 100
   📚 Average vocabulary matches per book: 109.1
```

**Dependencies**: Requires `seed_vocabulary.py` to run first (needs vocabulary words in database)

**Options**:
- `--dataset-path PATH` - Specify path to pgcorpus/Zenodo dataset
- `--phase PHASE` - Run specific phase: 'select', 'extract', or 'all' (default)

---

### 3. `analyze_students.py`

**Purpose**: Analyzes student transcripts and essays to build vocabulary profiles.

**What it does**:
- Parses classroom transcript (`data/mock/classroom_transcript.txt`)
- Loads student essays from `data/mock/student_essays/`
- Uses spaCy for text preprocessing and vocabulary detection
- Uses OpenAI GPT-4 to analyze vocabulary usage correctness
- Detects misused words (e.g., "through" vs "threw")
- Creates student profiles with vocabulary mastery percentages
- Stores results in `students` and `student_vocabulary` tables

**Expected Output**:
- 25 students inserted into `students` table
- Student vocabulary records in `student_vocabulary` table
- Class-wide statistics calculated

**Example**:
```bash
python scripts/analyze_students.py
```

**Output**:
```
📖 Parsing transcript from data/mock/classroom_transcript.txt...
✅ Parsed transcript: Found dialogue for 6 students

📝 Loading essays from data/mock/student_essays...
✅ Loaded 25 essays

[1/25] Processing Amy Jones...
  ✅ Found 3 vocab words
     Analyzed 3, Skipped 0
...

✅ Processed 25 students
📊 Database Verification:
   Students in database: 25
   Student vocabulary records: 38
```

**Dependencies**: 
- Requires `seed_vocabulary.py` (needs vocabulary words)
- Requires `OPENAI_API_KEY` environment variable

**Note**: This script makes API calls to OpenAI GPT-4, which may take several minutes and incur API costs.

---

### 4. `generate_recommendations.py`

**Purpose**: Generates personalized book recommendations for students.

**What it does**:
- Calculates vocabulary overlap between students and books
- Matches students to books with optimal challenge (~50% known, ~50% new vocabulary)
- Considers reading level appropriateness
- Stores top 3 recommendations per student
- Aggregates class-wide recommendations (top 2 books)

**Expected Output**:
- 75 student recommendations (3 per student × 25 students)
- 2 class-wide recommendations
- All stored in `student_recommendations` and `class_recommendations` tables

**Example**:
```bash
python scripts/generate_recommendations.py
```

**Output**:
```
📚 Processing 25 students against 100 books...

[1/25] Processing Amy Jones...
  ✅ Top 3 recommendations:
     1. The Turn of the Screw: score=0.900, known=74.5%, new_words=38
     2. North and South: score=0.900, known=72.9%, new_words=70
     3. Little Dorrit: score=0.900, known=74.4%, new_words=88

...

✅ Stored recommendations for 25 students
   Inserted: 75 recommendations

✅ Stored class-wide recommendations
   Inserted: 2 recommendations
```

**Dependencies**: 
- Requires `seed_vocabulary.py` (vocabulary words)
- Requires `seed_books.py` (books)
- Requires `analyze_students.py` (students)

---

### 5. `run_all.py`

**Purpose**: Master script that orchestrates all seeding scripts in the correct order.

**What it does**:
- Runs scripts sequentially: vocab → books → students → recommendations
- Tracks progress and statistics
- Provides summary output
- Supports `--skip` and `--only` flags for selective execution

**Example**:
```bash
# Run all scripts
python scripts/run_all.py

# Skip books (if already seeded)
python scripts/run_all.py --skip books

# Run only vocabulary and recommendations
python scripts/run_all.py --only vocab,recommendations
```

**Output**:
```
======================================================================
DATABASE SEEDING PIPELINE
======================================================================
Started at: 2025-11-12 15:46:31

Scripts to run (4):
  - Seed Vocabulary: Load vocabulary words from grade-level JSON files
  - Seed Books: Load books and vocabulary from pgcorpus/Zenodo
  - Analyze Students: Analyze student transcripts and essays to build vocabulary profiles
  - Generate Recommendations: Generate personalized book recommendations for students

======================================================================
Running: Seed Vocabulary
Script: seed_vocabulary.py
======================================================================

✅ Seed Vocabulary completed successfully

...

======================================================================
SEEDING PIPELINE SUMMARY
======================================================================

📊 Execution Summary:
   Total scripts: 4
   ✅ Successful: 4
   ❌ Failed: 0

✅ All scripts completed successfully!
```

---

## Utility Scripts

### Data Generation

- **`generate_mock_data.py`** - Generates mock classroom transcript and student essays using OpenAI GPT-4
  - Creates `data/mock/classroom_transcript.txt`
  - Creates `data/mock/student_essays/*.json` files
  - Requires `OPENAI_API_KEY`

### Verification

- **`verify_prerequisites.py`** - Checks that all required dependencies are installed
- **`verify_recommendations.py`** - Verifies recommendation data quality
- **`verify_class_view.py`** - Verifies API endpoints and database structure for class view
- **`test_recommendation_algorithm.py`** - Unit tests for recommendation matching algorithm

### Database Management

- **`reset_students.py`** - Clears all student data and re-runs analysis and recommendations
- **`cleanup_essays.py`** - Removes essay files that don't match student personas

### Dataset Management

- **`setup_zenodo.py`** - Downloads and sets up Zenodo 2018 dataset
- **`verify_pgcorpus.py`** - Verifies pgcorpus dataset integrity
- **`check_pgcorpus_status.py`** - Checks pgcorpus dataset status
- **`cleanup_pgcorpus.py`** - Cleans up pgcorpus dataset files

---

## Troubleshooting

### Common Issues

#### 1. "spaCy English model not found"

**Error**:
```
Error: spaCy English model not found. Run: python -m spacy download en_core_web_sm
```

**Solution**:
```bash
python -m spacy download en_core_web_sm
```

#### 2. "Database connection failed"

**Error**:
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution**:
- Verify `DATABASE_URL` is set correctly in `backend/.env`
- Check PostgreSQL is running: `pg_isready` or `docker ps`
- For Railway: Use `DATABASE_PUBLIC_URL` for external connections

#### 3. "OpenAI API key not found"

**Error**:
```
openai.AuthenticationError: Invalid API key
```

**Solution**:
- Set `OPENAI_API_KEY` in `backend/.env`
- Get API key from https://platform.openai.com/api-keys
- Ensure you have API credits available

#### 4. "Vocabulary files not found"

**Error**:
```
FileNotFoundError: data/vocab/5th_grade.json
```

**Solution**:
- Verify vocabulary JSON files exist in `data/vocab/`
- Check file names match: `5th_grade.json`, `6th_grade.json`, `7th_grade.json`, `8th_grade.json`

#### 5. "Books dataset not found"

**Error**:
```
FileNotFoundError: data/pgcorpus-2018/metadata.csv
```

**Solution**:
- Download Zenodo 2018 dataset or use pgcorpus repository
- Run `python scripts/setup_zenodo.py` to download dataset
- Or specify custom path: `python scripts/seed_books.py --dataset-path /path/to/dataset`

#### 6. "Duplicate key error" (vocabulary/books already seeded)

**Error**:
```
sqlalchemy.exc.IntegrityError: duplicate key value violates unique constraint
```

**Solution**:
- Scripts handle duplicates gracefully (update existing records)
- If you want to start fresh, drop and recreate database tables
- Or skip already-seeded scripts: `python scripts/run_all.py --skip vocab,books`

#### 7. "Student personas not found"

**Error**:
```
FileNotFoundError: data/mock/student_personas.json
```

**Solution**:
- Run `python scripts/generate_mock_data.py` first to generate personas
- Or ensure `data/mock/student_personas.json` exists

### Performance Tips

- **Book seeding is slow**: Processing 100 books can take 10-20 minutes. Be patient.
- **Student analysis uses OpenAI API**: May take 5-10 minutes and incur API costs (~$0.50-1.00)
- **Run scripts in order**: Each script depends on previous ones completing successfully

### Verification

After running scripts, verify data:

```bash
# Check database counts
psql $DATABASE_URL -c "SELECT COUNT(*) FROM vocabulary_words;"  # Should be 525
psql $DATABASE_URL -c "SELECT COUNT(*) FROM books;"  # Should be 100
psql $DATABASE_URL -c "SELECT COUNT(*) FROM students;"  # Should be 25
psql $DATABASE_URL -c "SELECT COUNT(*) FROM student_recommendations;"  # Should be 75
psql $DATABASE_URL -c "SELECT COUNT(*) FROM class_recommendations;"  # Should be 2
```

Or use verification scripts:

```bash
python scripts/verify_recommendations.py
python scripts/verify_class_view.py
```

---

## Expected Output Summary

After running the complete pipeline (`run_all.py`), you should have:

| Table | Expected Count | Description |
|-------|---------------|-------------|
| `vocabulary_words` | 525 | Grade-level vocabulary words (5-8) |
| `books` | 100 | Project Gutenberg books |
| `book_vocabulary` | ~10,914 | Book-vocabulary associations |
| `students` | 25 | Student profiles |
| `student_vocabulary` | ~38 | Student vocabulary mastery records |
| `student_recommendations` | 75 | Personalized recommendations (3 per student) |
| `class_recommendations` | 2 | Class-wide recommendations |

---

## Script Execution Order

```
1. seed_vocabulary.py
   ↓ (provides vocabulary_words)
2. seed_books.py
   ↓ (provides books, book_vocabulary)
3. analyze_students.py
   ↓ (provides students, student_vocabulary)
4. generate_recommendations.py
   ↓ (provides student_recommendations, class_recommendations)
```

**Note**: Each script can be run independently if prerequisites are met, but `run_all.py` ensures correct order and dependencies.

---

## Additional Resources

- [Main README](../README.md) - Project overview and setup
- [Architecture Documentation](../docs/ARCHITECTURE.md) - System architecture
- [API Documentation](https://backend-production-82d4.up.railway.app/docs) - Interactive API docs

