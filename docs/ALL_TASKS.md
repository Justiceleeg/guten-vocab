# Flourish Schools - Personalized Vocabulary Recommendation Engine
## Task List - Organized by Vertical Slices

---

## Project Overview
Build an AI-powered vocabulary recommendation system for middle school students that:
- Analyzes classroom transcripts and student essays
- Identifies vocabulary gaps per student
- Recommends books from Project Gutenberg based on vocabulary fit
- Provides teacher dashboard with student and class-wide insights

**Tech Stack:**
- Frontend: Next.js (React)
- Backend: FastAPI (Python)
- Database: PostgreSQL
- AI: OpenAI API
- NLP: spaCy (for lemmatization)
- Deployment: Vercel (frontend), Railway (backend + database)

**Key Constraints:**
- 1 classroom, 20-25 students (7th grade)
- Mock data only (no real student data)
- No authentication (MVP/demo)
- Pre-seeded database (analysis runs before deployment)

---

## VERTICAL SLICE 1: Project Setup & Infrastructure
**Goal:** Set up the foundational project structure, database, and development environment.

### Tasks:

#### 1.1 Repository & Project Structure
- [ ] Initialize Git repository
- [ ] Create project structure:
  ```
  /
  ├── backend/              # FastAPI application
  │   ├── app/
  │   │   ├── models/       # SQLAlchemy models
  │   │   ├── api/          # API routes
  │   │   ├── services/     # Business logic
  │   │   └── main.py
  │   ├── requirements.txt
  │   └── .env.example
  ├── frontend/             # Next.js application
  │   ├── app/              # Next.js app router pages
  │   ├── components/       # React components
  │   ├── lib/              # Utilities (API client, types)
  │   ├── package.json
  │   └── .env.example
  ├── scripts/              # Data generation & seeding scripts
  │   ├── generate_vocab_lists.py
  │   ├── generate_mock_data.py
  │   ├── seed_books.py
  │   ├── analyze_students.py
  │   └── run_all.py
  ├── data/                 # Static data files
  │   ├── vocab/            # Grade-level vocabulary JSON files
  │   └── mock/             # Generated mock data
  │       ├── classroom_transcript.txt
  │       └── student_essays/
  └── README.md
  ```

#### 1.2 Backend Setup
- [ ] Initialize FastAPI project
- [ ] Install dependencies:
  - FastAPI
  - SQLAlchemy
  - psycopg2-binary (PostgreSQL driver)
  - python-dotenv
  - openai
  - spacy
  - textstat (for reading level calculation)
  - requests
- [ ] Download spaCy English model: `python -m spacy download en_core_web_sm`
- [ ] Create `.env.example` with required variables:
  ```
  DATABASE_URL=postgresql://user:password@localhost:5432/vocab_engine
  OPENAI_API_KEY=your_key_here
  ```
- [ ] Set up basic FastAPI app structure with health check endpoint

#### 1.3 Frontend Setup
- [ ] Initialize Next.js project with TypeScript
- [ ] Install dependencies:
  - tailwindcss
  - axios (for API calls)
  - recharts (for visualizations)
- [ ] Configure Tailwind CSS
- [ ] Set up shadcn/ui component library
- [ ] Create basic layout with navigation
- [ ] Set up API client utilities

#### 1.4 Database Setup
- [ ] Install PostgreSQL locally (or use Docker)
- [ ] Create database: `vocab_engine`
- [ ] Set up SQLAlchemy with PostgreSQL connection
- [ ] Create initial database schema:

```sql
-- Students table
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    actual_reading_level FLOAT NOT NULL,
    assigned_grade INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vocabulary words (master list, 5th-8th grade)
CREATE TABLE vocabulary_words (
    id SERIAL PRIMARY KEY,
    word VARCHAR(100) NOT NULL UNIQUE,
    grade_level INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_vocab_word ON vocabulary_words(word);
CREATE INDEX idx_vocab_grade ON vocabulary_words(grade_level);

-- Student vocabulary profiles
CREATE TABLE student_vocabulary (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    word_id INTEGER REFERENCES vocabulary_words(id) ON DELETE CASCADE,
    usage_count INTEGER DEFAULT 0,
    correct_usage_count INTEGER DEFAULT 0,
    misuse_examples TEXT[],
    last_analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, word_id)
);
CREATE INDEX idx_student_vocab_student ON student_vocabulary(student_id);
CREATE INDEX idx_student_vocab_word ON student_vocabulary(word_id);

-- Books
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    author VARCHAR(255),
    gutenberg_id INTEGER UNIQUE,
    reading_level FLOAT,
    total_words INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_books_reading_level ON books(reading_level);

-- Book vocabulary (only words in our master vocab list)
CREATE TABLE book_vocabulary (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    word_id INTEGER REFERENCES vocabulary_words(id) ON DELETE CASCADE,
    occurrence_count INTEGER NOT NULL,
    UNIQUE(book_id, word_id)
);
CREATE INDEX idx_book_vocab_book ON book_vocabulary(book_id);
CREATE INDEX idx_book_vocab_word ON book_vocabulary(word_id);

-- Student book recommendations
CREATE TABLE student_recommendations (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    match_score FLOAT NOT NULL,
    known_words_percent FLOAT NOT NULL,
    new_words_count INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_student_recs_student ON student_recommendations(student_id);
CREATE INDEX idx_student_recs_book ON student_recommendations(book_id);

-- Class-wide book recommendations
CREATE TABLE class_recommendations (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    match_score FLOAT NOT NULL,
    students_recommended_count INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_class_recs_score ON class_recommendations(match_score DESC);
```

#### 1.5 SQLAlchemy Models
- [ ] Create SQLAlchemy models matching the schema above
- [ ] Add relationships between models
- [ ] Create database initialization script

**Acceptance Criteria:**
- ✅ Repository structure is set up
- ✅ Backend runs with health check endpoint
- ✅ Frontend runs and displays basic layout
- ✅ PostgreSQL database is created with all tables
- ✅ Can connect to database from backend

---

## VERTICAL SLICE 2: Vocabulary Data & Book Dataset
**Goal:** Populate the database with vocabulary words and Project Gutenberg books.

### Tasks:

#### 2.1 Vocabulary Lists Setup
- [x] Copy vocabulary JSON files to `/data/vocab/`:
  - 5th_grade.json (150 words)
  - 6th_grade.json (125 words)
  - 7th_grade.json (125 words)
  - 8th_grade.json (125 words)
  - Source: https://www.vocabulary.com/lists/lists-by-grade

#### 2.2 Vocabulary Seed Script
- [x] Create `scripts/seed_vocabulary.py`:
  - Load all 4 JSON files
  - Insert words into `vocabulary_words` table with grade levels
  - Handle duplicates (some words may appear in multiple grades - keep highest grade)
  - Print summary: "Loaded X words across grades 5-8"
  - ✅ Tested: 525 words loaded successfully

#### 2.3 Book Dataset - pgcorpus Setup
- [ ] Research and document pgcorpus/gutenberg setup:
  - Clone repo: `git clone https://github.com/pgcorpus/gutenberg.git`
  - Install dependencies: `pip install -r requirements.txt`
  - Run `python get_data.py` (downloads books - may take hours)
  - Run `python process_data.py` (processes books into counts)
  - Document location of `counts/` folder and metadata CSV

#### 2.4 Book Filtering & Selection Script
- [ ] Create `scripts/seed_books.py`:
  - Load pgcorpus metadata CSV
  - Filter books by:
    - Category: "Children's Literature" OR "Children's Fiction"
    - Language: English
    - Has counts file available
  - Calculate reading level using textstat library (Flesch-Kincaid)
  - Filter to reading level 5.0-9.0
  - Sort by download count (popularity)
  - Select top 100 books
  - Save list to `/data/books/selected_books.json` with:
    ```json
    [
      {
        "gutenberg_id": 76,
        "title": "Adventures of Huckleberry Finn",
        "author": "Mark Twain",
        "reading_level": 7.2,
        "download_count": 50000
      }
    ]
    ```

#### 2.5 Book Vocabulary Extraction
- [ ] Extend `scripts/seed_books.py` to:
  - For each selected book:
    - Load pre-computed counts file from pgcorpus
    - Apply spaCy lemmatization to each word in counts
    - Filter to only words in our vocabulary_words table (525 words)
    - Calculate total word count of book
    - Insert into `books` table
    - Insert word counts into `book_vocabulary` table
  - Add progress tracking (processing book X of 100)
  - Handle errors gracefully (skip books that fail)
  - Print summary statistics:
    - Total books processed
    - Average vocabulary coverage per book
    - Books with highest/lowest coverage

#### 2.6 Run Vocabulary & Book Seeding
- [ ] Execute `python scripts/seed_vocabulary.py`
- [ ] Execute `python scripts/seed_books.py`
- [ ] Verify data in database:
  - Query: `SELECT COUNT(*) FROM vocabulary_words;` (should be ~525)
  - Query: `SELECT COUNT(*) FROM books;` (should be ~100)
  - Query: `SELECT COUNT(*) FROM book_vocabulary;` (should be ~10,000-50,000)
  - Query top 10 books by vocab coverage

**Acceptance Criteria:**
- ✅ 525 vocabulary words loaded into database
- ✅ 100 middle-grade appropriate books selected and documented
- ✅ Book vocabulary counts extracted for all 100 books
- ✅ All data verified in PostgreSQL
- ✅ Script outputs saved for reference

---

## VERTICAL SLICE 3: Mock Data Generation
**Goal:** Generate realistic classroom transcript and student essays using LLMs.

### Tasks:

#### 3.1 Student Personas Generation
- [ ] Create `scripts/generate_mock_data.py`
- [ ] Define 25 student personas with:
  - Names (diverse, realistic)
  - Reading proficiency levels:
    - 2 students at 5th grade level
    - 6 students at 6th grade level
    - 13 students at 7th grade level (majority)
    - 4 students at 8th grade level
  - Personality traits (to make transcript realistic)
- [ ] Save personas to `/data/mock/student_personas.json`

#### 3.2 Classroom Transcript Generation
- [ ] Use OpenAI API (GPT-4) to generate full-day transcript:
  - Total: ~40,000 words
  - Covers multiple subjects: Reading, Math, Science, Social Studies
  - Natural classroom dialogue:
    - Teacher asks questions, calls on students by name
    - Students respond at their proficiency level
    - Group discussions, presentations
    - Casual conversations (lunch, transitions)
  - Pre-labeled speakers: `Teacher:`, `Student_Sarah:`, etc.
  - Include timestamps: `[09:15 AM]`, `[10:30 AM]`, etc.
  - Plant the misused word "through" (used instead of "thorough") in ~15-20 students' speech
- [ ] Prompt engineering:
  ```
  Generate a full school day classroom transcript for a 7th grade class of 25 students.
  The day should be ~40,000 words and include:
  - Morning: English/Reading lesson discussing a novel
  - Mid-morning: Math lesson on algebra
  - Before lunch: Science lesson on ecosystems  
  - Afternoon: Social Studies on American history
  - Include natural transitions, questions, discussions
  
  Students have varying reading levels (5th-8th grade). Match their vocabulary usage to their level:
  [Include student personas with reading levels]
  
  Important: 
  - Most students (15-20) should occasionally misuse "through" when they mean "thorough"
  - Teacher always addresses students by name
  - Format as: [TIME] Speaker: dialogue
  - Make it realistic with "um", natural speech patterns, etc.
  ```
- [ ] Save to `/data/mock/classroom_transcript.txt`
- [ ] Verify output: Check word count, speaker distribution, timestamps

#### 3.3 Student Essay Generation  
- [ ] Extend `generate_mock_data.py` to generate essays:
  - 1 essay per student (25 total)
  - Length: ~300 words each
  - Topic: Analysis of a book or personal narrative (varied)
  - Writing quality matches student's reading level
  - Include the misused word "through" in ~10 student essays
- [ ] Prompt per student:
  ```
  Write a 300-word essay written by a 7th grade student named [NAME] with a [GRADE] reading level.
  The student is writing about [TOPIC].
  
  Match vocabulary and sentence complexity to a [GRADE] reading level.
  [If flagged]: Occasionally use "through" when you mean "thorough" (this is a common mistake).
  
  Make it sound like authentic student writing with minor imperfections.
  ```
- [ ] Save essays to `/data/mock/student_essays/`:
  - `student_1_sarah.json`:
    ```json
    {
      "student_name": "Sarah Johnson",
      "reading_level": 7,
      "essay": "Essay content here...",
      "word_count": 305
    }
    ```

#### 3.4 Verify Mock Data Quality
- [ ] Review transcript sample for realism
- [ ] Check vocabulary distribution matches proficiency levels
- [ ] Verify "through/thorough" misuses are subtle and realistic
- [ ] Confirm file sizes are appropriate for Git (~300 KB total)
- [ ] Commit all mock data files to repository

**Acceptance Criteria:**
- ✅ 25 student personas created with varied proficiency levels
- ✅ 40,000-word classroom transcript generated and saved
- ✅ 25 student essays generated (300 words each)
- ✅ Misused word "through" appears naturally in transcript and essays
- ✅ All mock data committed to repository

---

## VERTICAL SLICE 4: Student Analysis Pipeline
**Goal:** Analyze mock data to build student vocabulary profiles.

### Tasks:

#### 4.1 Transcript Parsing
- [ ] Create `scripts/analyze_students.py`
- [ ] Implement transcript parser:
  - Load `/data/mock/classroom_transcript.txt`
  - Parse format: `[TIME] Speaker: dialogue`
  - Extract all dialogue per student
  - Aggregate by student name
  - Output: Dictionary of `{student_name: [all_their_dialogue_combined]}`

#### 4.2 Essay Loading
- [ ] Implement essay loader:
  - Load all JSON files from `/data/mock/student_essays/`
  - Map to student names
  - Output: Dictionary of `{student_name: essay_text}`

#### 4.3 Text Preprocessing with spaCy
- [ ] Implement text processing function:
  - Input: Raw text (transcript dialogue OR essay)
  - Use spaCy to:
    - Tokenize
    - Lemmatize (get root form of each word)
    - Filter to only alphabetic tokens (remove punctuation, numbers)
    - Convert to lowercase
  - Output: List of lemmatized words
- [ ] Create word frequency counter:
  - Count occurrences of each lemmatized word
  - Filter to only words in our vocabulary_words table (525 words)
  - Output: `{word: count}` for vocabulary words only

#### 4.4 OpenAI Analysis - Vocabulary Understanding
- [ ] Implement OpenAI API integration for correctness checking:
  - For each student:
    - Combine their transcript dialogue + essay into one text
    - For each vocabulary word they used:
      - Extract 1-2 example sentences where they used the word
      - Send to OpenAI with prompt:
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
      - Parse response and store results
- [ ] Handle rate limits and errors gracefully
- [ ] Add progress tracking (analyzing student X of 25)

#### 4.5 Build Student Vocabulary Profiles
- [ ] For each student:
  - Calculate vocabulary mastery:
    - Total grade-level words known (used correctly at least once)
    - Percentage of grade-level vocabulary mastered
    - List of missing vocabulary words
  - Identify misused words with examples
  - Insert/update database:
    - `students` table (name, reading level, assigned grade)
    - `student_vocabulary` table (word usage counts, correctness, examples)

#### 4.6 Class-Wide Analysis
- [ ] Aggregate class statistics:
  - Top 10 words most students are missing
  - Commonly misused words across class ("through" should appear here)
  - Average vocabulary mastery by grade level
  - Store in database or output to JSON for dashboard

#### 4.7 Run Analysis Pipeline
- [ ] Execute `python scripts/analyze_students.py`
- [ ] Monitor progress and handle any errors
- [ ] Verify output in database:
  - Query: `SELECT COUNT(*) FROM students;` (should be 25)
  - Query: `SELECT COUNT(*) FROM student_vocabulary;` (thousands of records)
  - Query student with highest/lowest vocabulary mastery
  - Check that "through" appears in commonly misused words

**Acceptance Criteria:**
- ✅ Transcript successfully parsed and attributed to students
- ✅ Essays loaded and processed
- ✅ spaCy lemmatization working correctly
- ✅ OpenAI API successfully analyzing vocabulary usage
- ✅ Student vocabulary profiles stored in database
- ✅ Class-wide statistics calculated
- ✅ Can query any student's vocabulary mastery from database

---

## VERTICAL SLICE 5: Book Recommendation Engine
**Goal:** Generate personalized and class-wide book recommendations.

### Tasks:

#### 5.1 Student-Book Matching Algorithm
- [ ] Create `scripts/generate_recommendations.py`
- [ ] Implement matching logic:
  - For each student:
    - Get their vocabulary profile (known words from student_vocabulary)
    - Get their reading level
    - For each book:
      - Calculate vocabulary overlap:
        - Known words: words student has used correctly
        - New words: words in book but not in student's profile
        - Overlap percentage: known_words / total_vocab_words_in_book
      - Filter books by reading level:
        - Prefer books at student's level ± 1 grade
        - Allow higher if vocabulary fit is exceptional
      - Calculate match score:
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
      - Store top 3 books per student

#### 5.2 Store Student Recommendations
- [ ] For each student:
  - Insert top 3 recommendations into `student_recommendations` table:
    - student_id
    - book_id  
    - match_score
    - known_words_percent
    - new_words_count
- [ ] Verify recommendations make sense (spot check a few students)

#### 5.3 Class-Wide Recommendations
- [ ] Aggregate student recommendations:
  - Count how many students have each book in their top 3
  - Calculate average match score per book across all students
  - Select top 2 books that appear most frequently in individual recommendations
  - Store in `class_recommendations` table:
    - book_id
    - match_score (average across students)
    - students_recommended_count

#### 5.4 Run Recommendation Engine
- [ ] Execute `python scripts/generate_recommendations.py`
- [ ] Verify output:
  - Query: `SELECT COUNT(*) FROM student_recommendations;` (should be 75 = 25 students × 3)
  - Query: `SELECT COUNT(*) FROM class_recommendations;` (should be 2)
  - Spot check: Do recommendations make sense for high/low proficiency students?

#### 5.5 Master Seed Script
- [ ] Create `scripts/run_all.py`:
  - Runs all scripts in order:
    1. seed_vocabulary.py
    2. seed_books.py
    3. analyze_students.py (assumes mock data exists)
    4. generate_recommendations.py
  - Add error handling and logging
  - Print summary at end with all statistics

**Acceptance Criteria:**
- ✅ Matching algorithm correctly calculates vocabulary overlap
- ✅ Book recommendations prioritize ~50% known / 50% new vocabulary
- ✅ Reading level considered in recommendations
- ✅ Each student has 3 book recommendations stored
- ✅ Class-wide top 2 books identified
- ✅ Master script can seed entire database from scratch

---

## VERTICAL SLICE 6: Backend API
**Goal:** Build REST API to serve data to frontend.

### Tasks:

#### 6.1 Student List Endpoint
- [ ] Create `GET /api/students`
  - Returns list of all students with basic info:
    ```json
    [
      {
        "id": 1,
        "name": "Sarah Johnson",
        "reading_level": 7.2,
        "assigned_grade": 7,
        "vocab_mastery_percent": 68.5
      }
    ]
    ```
- [ ] Add pagination if needed (probably not for 25 students)

#### 6.2 Student Detail Endpoint
- [ ] Create `GET /api/students/{id}`
  - Returns detailed student profile:
    ```json
    {
      "id": 1,
      "name": "Sarah Johnson",
      "reading_level": 7.2,
      "assigned_grade": 7,
      "vocab_mastery": {
        "total_grade_level_words": 125,
        "words_mastered": 86,
        "mastery_percent": 68.8
      },
      "missing_words": ["abolish", "coherent", "comprise", ...],
      "misused_words": [
        {
          "word": "through",
          "correct_count": 2,
          "incorrect_count": 3,
          "example": "I did a through analysis of the book."
        }
      ],
      "book_recommendations": [
        {
          "book_id": 12,
          "title": "Treasure Island",
          "author": "Robert Louis Stevenson",
          "reading_level": 7.5,
          "match_score": 0.82,
          "known_words_percent": 52.0,
          "new_words_count": 18
        }
      ]
    }
    ```

#### 6.3 Class Statistics Endpoint
- [ ] Create `GET /api/class/stats`
  - Returns class-wide statistics:
    ```json
    {
      "total_students": 25,
      "avg_vocab_mastery_percent": 64.2,
      "reading_level_distribution": {
        "5": 2,
        "6": 6,
        "7": 13,
        "8": 4
      },
      "top_missing_words": [
        {"word": "abolish", "students_missing": 18},
        {"word": "coherent", "students_missing": 16}
      ],
      "commonly_misused_words": [
        {"word": "through", "misuse_count": 47}
      ]
    }
    ```

#### 6.4 Class Book Recommendations Endpoint
- [ ] Create `GET /api/class/recommendations`
  - Returns top 2 class-wide book recommendations:
    ```json
    [
      {
        "book_id": 15,
        "title": "Anne of Green Gables",
        "author": "L. M. Montgomery",
        "reading_level": 6.8,
        "students_recommended_count": 18,
        "avg_match_score": 0.76
      }
    ]
    ```

#### 6.5 Books List Endpoint (Optional)
- [ ] Create `GET /api/books`
  - Returns list of all books in database
  - Add filters: reading_level_min, reading_level_max
  - Useful for debugging/exploration

#### 6.6 API Testing
- [ ] Test all endpoints with curl or Postman
- [ ] Verify data matches database queries
- [ ] Add error handling (404 for missing students, 500 for server errors)
- [ ] Add CORS configuration for frontend

#### 6.7 API Documentation
- [ ] Add FastAPI automatic docs (available at `/docs`)
- [ ] Document expected response formats in README

**Acceptance Criteria:**
- ✅ All API endpoints return correct data
- ✅ Endpoints tested and working
- ✅ CORS configured for frontend
- ✅ API docs accessible at `/docs`

---

## VERTICAL SLICE 7: Teacher Dashboard - Student View
**Goal:** Build frontend UI for viewing individual student data.

### Tasks:

#### 7.1 Student List Page
- [ ] Create `/students` page:
  - Display table/grid of all 25 students
  - Show: Name, Reading Level, Vocab Mastery %
  - Add visual indicator (color coding) for proficiency level
  - Make rows clickable to navigate to student detail

#### 7.2 Student Detail Page
- [ ] Create `/students/[id]` page with sections:
  
  **Section 1: Student Overview**
  - Name, reading level, assigned grade
  - Vocabulary mastery gauge/chart showing % mastered
  
  **Section 2: Book Recommendations**
  - Display 3 recommended books as cards:
    - Book title, author, cover (placeholder image)
    - Match score (as star rating or percentage)
    - "Known: 52% | New: 48% (18 words)"
    - Brief explanation: "This book will challenge you with 18 new vocabulary words while reinforcing words you already know."
  
  **Section 3: Vocabulary Progress**
  - Show grade-level vocabulary stats:
    - "Mastered 86 of 125 7th grade words (68.8%)"
    - Progress bar visualization
  - List missing words (expandable/collapsible)
  
  **Section 4: Vocabulary Issues**
  - "Words Used Incorrectly" section
  - Display each misused word with:
    - Word name
    - Correct vs. incorrect usage count
    - Example sentence (1-2) of misuse
    - Highlighted word in context

#### 7.3 Styling & UX
- [ ] Apply consistent design system (shadcn/ui + Tailwind)
- [ ] Use shadcn/ui components for UI elements (cards, buttons, tables, etc.)
- [ ] Add loading states while fetching data
- [ ] Add empty states if no data
- [ ] Make it responsive (works on tablet/desktop)
- [ ] Add navigation breadcrumbs

#### 7.4 Data Fetching
- [ ] Implement API calls using axios
- [ ] Add error handling and user-friendly error messages
- [ ] Add loading spinners/skeletons

**Acceptance Criteria:**
- ✅ Can view list of all students
- ✅ Can click into any student to see detailed view
- ✅ Student detail page shows all required information
- ✅ Book recommendations are clear and actionable
- ✅ Misused words are displayed with examples
- ✅ UI is clean, readable, and responsive

---

## VERTICAL SLICE 8: Teacher Dashboard - Class View
**Goal:** Build frontend UI for class-wide insights.

### Tasks:

#### 8.1 Class Overview Page
- [ ] Create `/class` page with sections:
  
  **Section 1: Class Statistics**
  - Total students: 25
  - Average vocabulary mastery: 64.2%
  - Reading level distribution chart (bar chart or pie chart)
  
  **Section 2: Class-Wide Book Recommendations**
  - Display top 2 books recommended for whole class
  - Show as prominent cards with:
    - Book title, author
    - "Recommended for 18 of 25 students"
    - Average match score
    - Brief explanation of why this book is good for the class
  
  **Section 3: Vocabulary Gaps**
  - "Top 10 Words Students Need to Learn"
  - Display as table or list:
    - Word | Students Missing | Grade Level
  - Sortable by number of students missing
  
  **Section 4: Common Mistakes**
  - "Words Frequently Used Incorrectly"
  - Display: Word | Total Misuses | Students Affected
  - Highlight "through" (should be top misused word)
  - Add example sentence of common misuse

#### 8.2 Data Visualization
- [ ] Implement charts using recharts:
  - Reading level distribution (bar chart)
  - Vocabulary mastery distribution (histogram)
  - Optional: Vocabulary coverage heatmap

#### 8.3 Navigation
- [ ] Add top navigation bar with links:
  - "Class Overview" → `/class`
  - "Students" → `/students`
- [ ] Add home page (landing) that redirects to class view

#### 8.4 Polish & Refinement
- [ ] Ensure consistent styling with student view
- [ ] Add helpful tooltips/explanations
- [ ] Test with real data from database
- [ ] Add print-friendly version (optional)

**Acceptance Criteria:**
- ✅ Class overview page displays all statistics correctly
- ✅ Top 2 class-wide book recommendations shown
- ✅ Top 10 missing words displayed with student counts
- ✅ Commonly misused words section shows "through" prominently
- ✅ Data visualizations are clear and informative
- ✅ Navigation between class and student views works smoothly

---

## VERTICAL SLICE 9: Deployment & Documentation
**Goal:** Deploy the application and create comprehensive documentation.

### Tasks:

#### 9.1 Railway Setup - Database
- [ ] Create Railway account
- [ ] Create new PostgreSQL database on Railway
- [ ] Note connection string
- [ ] Update backend `.env` with Railway database URL

#### 9.2 Railway Setup - Backend
- [ ] Create Railway project for backend
- [ ] Configure build settings:
  - Root directory: `backend/`
  - Build command: `pip install -r requirements.txt`
  - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Set environment variables:
  - `DATABASE_URL` (Railway PostgreSQL)
  - `OPENAI_API_KEY`
- [ ] Deploy backend

#### 9.3 Seed Railway Database
- [ ] Run seed scripts locally pointing to Railway database:
  - Update DATABASE_URL in `.env`
  - Run: `python scripts/run_all.py`
- [ ] Verify data in Railway PostgreSQL dashboard
- [ ] Alternative: Export local database and import to Railway

#### 9.4 Vercel Setup - Frontend
- [ ] Create Vercel account
- [ ] Connect GitHub repository
- [ ] Configure build settings:
  - Root directory: `frontend/`
  - Build command: `pnpm build`
  - Output directory: `.next`
- [ ] Set environment variable:
  - `NEXT_PUBLIC_API_URL` (Railway backend URL)
- [ ] Deploy frontend

#### 9.5 Integration Testing
- [ ] Test deployed frontend → backend connection
- [ ] Verify all pages load correctly
- [ ] Test API calls are working
- [ ] Check student and class views with real data
- [ ] Test on different devices/browsers

#### 9.6 Documentation - README
- [ ] Create comprehensive README.md:
  - Project overview and goals
  - Tech stack description
  - Architecture diagram (simple text/ASCII or draw.io)
  - Setup instructions:
    - Prerequisites (Node, Python, PostgreSQL)
    - Installation steps
    - Environment variables
    - Database setup
    - Running locally
  - Deployment instructions
  - Data generation process explanation
  - API documentation (link to FastAPI /docs)
  - Known limitations
  - Future enhancements

#### 9.7 Documentation - Scripts
- [ ] Add README in `/scripts/` folder:
  - Explain purpose of each script
  - Order of execution
  - Dependencies
  - Expected outputs
  - Troubleshooting common issues

#### 9.8 Code Cleanup
- [ ] Remove unused code/files
- [ ] Add comments to complex logic
- [ ] Ensure consistent code formatting
- [ ] Remove hardcoded values, use environment variables
- [ ] Add .gitignore files (node_modules, .env, __pycache__, etc.)

#### 9.9 Demo Video/Screenshots (Optional)
- [ ] Take screenshots of key features:
  - Class overview
  - Student detail view
  - Book recommendations
- [ ] Record short demo video showing:
  - Navigation through app
  - Key insights (vocabulary gaps, recommendations)
  - Highlighting "through" misuse feature

**Acceptance Criteria:**
- ✅ Backend deployed on Railway and accessible
- ✅ Database deployed on Railway with all data seeded
- ✅ Frontend deployed on Vercel
- ✅ Full application works end-to-end in production
- ✅ README is comprehensive and clear
- ✅ All code is clean and well-documented
- ✅ Demo materials created (screenshots/video)

---

## VERTICAL SLICE 10: Testing & Refinement (Optional)
**Goal:** Polish the application and fix any remaining issues.

### Tasks:

#### 10.1 Data Quality Review
- [ ] Review generated transcript for realism
- [ ] Check essay quality across proficiency levels
- [ ] Verify "through" misuse appears naturally
- [ ] Spot check student vocabulary profiles for accuracy

#### 10.2 Recommendation Quality Review
- [ ] Manually verify book recommendations for 5 students:
  - Do recommendations make sense for their level?
  - Is vocabulary overlap reasonable (~50/50)?
  - Are recommended books age-appropriate?
- [ ] Review class-wide recommendations:
  - Do the top 2 books make sense for most students?

#### 10.3 UI/UX Improvements
- [ ] Get feedback from a teacher (if possible) or peer
- [ ] Improve any confusing UI elements
- [ ] Add helpful tooltips or explanations
- [ ] Improve mobile responsiveness
- [ ] Add loading states where missing

#### 10.4 Performance Optimization
- [ ] Check API response times
- [ ] Add database indexes if queries are slow
- [ ] Optimize frontend bundle size
- [ ] Add caching where appropriate

#### 10.5 Edge Case Handling
- [ ] Test with edge cases:
  - Student with 0% vocabulary mastery
  - Student with 100% vocabulary mastery
  - Books with very low/high vocabulary coverage
- [ ] Add graceful degradation for missing data

#### 10.6 Bug Fixes
- [ ] Create issue tracker for any bugs found
- [ ] Prioritize and fix critical bugs
- [ ] Test fixes thoroughly

**Acceptance Criteria:**
- ✅ Data quality is high and realistic
- ✅ Recommendations are sensible and useful
- ✅ UI is polished and easy to use
- ✅ No major bugs or performance issues
- ✅ Application is demo-ready

---

## Estimated Timeline

- **Slice 1 (Setup):** 1-2 days
- **Slice 2 (Vocab & Books):** 1-2 days (plus pgcorpus download time)
- **Slice 3 (Mock Data):** 1 day (mostly LLM generation wait time)
- **Slice 4 (Analysis):** 2-3 days
- **Slice 5 (Recommendations):** 1-2 days
- **Slice 6 (API):** 1 day
- **Slice 7 (Student View):** 2-3 days
- **Slice 8 (Class View):** 1-2 days
- **Slice 9 (Deployment):** 1 day
- **Slice 10 (Polish):** 1-2 days

**Total: ~14-20 days** (with buffer for debugging and refinement)

---

## Notes & Considerations

### Key Technical Decisions Made:
- Using OpenAI API instead of running models locally (faster for MVP)
- Using pgcorpus pre-computed counts instead of processing books ourselves (simpler)
- No lemmatization for books, only for student analysis (good enough for MVP)
- Pre-seeding database before deployment (no runtime data generation)
- No authentication (demo only)

### Potential Future Enhancements:
- Real-time transcript analysis (as class happens)
- Track vocabulary progress over time (multiple days)
- Student-facing interface (let students see their own progress)
- Integration with real classroom tools (Google Classroom, etc.)
- More sophisticated recommendation algorithm (collaborative filtering)
- Support for multiple classes/teachers
- Export reports as PDF

### Important Reminders:
- Commit vocab JSON files before starting
- Document which 100 books were selected
- Keep mock data realistic but not perfect (students make mistakes)
- Test with edge cases (very high/low proficiency students)
- The "through" vs "thorough" misuse should be subtle but detectable

---

## Quick Start Checklist

Before you begin, ensure you have:
- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] PostgreSQL 14+ installed (or Docker)
- [ ] OpenAI API key with credits
- [ ] Git repository initialized
- [ ] Vocabulary JSON files in `/data/vocab/`

Good luck building! 🚀
