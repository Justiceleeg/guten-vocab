## 1. Database Setup

### 1.1 Install PostgreSQL
- [ ] Install PostgreSQL 14+ locally OR set up Docker container
- [ ] Verify PostgreSQL is running
- [ ] Create database user if needed
- [ ] Document connection details

### 1.2 Create Database
- [ ] Connect to PostgreSQL
- [ ] Create database: `CREATE DATABASE vocab_engine;`
- [ ] Verify database was created
- [ ] Grant necessary permissions to database user

### 1.3 Set Up SQLAlchemy Connection
- [ ] Create `backend/app/database.py` for database connection
- [ ] Configure SQLAlchemy engine with connection string
- [ ] Set up database session factory
- [ ] Add database dependency for FastAPI routes
- [ ] Test database connection from backend

### 1.4 Create Database Schema
- [ ] Create `students` table:
  ```sql
  CREATE TABLE students (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      actual_reading_level FLOAT NOT NULL,
      assigned_grade INTEGER NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```
- [ ] Create `vocabulary_words` table:
  ```sql
  CREATE TABLE vocabulary_words (
      id SERIAL PRIMARY KEY,
      word VARCHAR(100) NOT NULL UNIQUE,
      grade_level INTEGER NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  CREATE INDEX idx_vocab_word ON vocabulary_words(word);
  CREATE INDEX idx_vocab_grade ON vocabulary_words(grade_level);
  ```
- [ ] Create `student_vocabulary` table:
  ```sql
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
  ```
- [ ] Create `books` table:
  ```sql
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
  ```
- [ ] Create `book_vocabulary` table:
  ```sql
  CREATE TABLE book_vocabulary (
      id SERIAL PRIMARY KEY,
      book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
      word_id INTEGER REFERENCES vocabulary_words(id) ON DELETE CASCADE,
      occurrence_count INTEGER NOT NULL,
      UNIQUE(book_id, word_id)
  );
  CREATE INDEX idx_book_vocab_book ON book_vocabulary(book_id);
  CREATE INDEX idx_book_vocab_word ON book_vocabulary(word_id);
  ```
- [ ] Create `student_recommendations` table:
  ```sql
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
  ```
- [ ] Create `class_recommendations` table:
  ```sql
  CREATE TABLE class_recommendations (
      id SERIAL PRIMARY KEY,
      book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
      match_score FLOAT NOT NULL,
      students_recommended_count INTEGER NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  CREATE INDEX idx_class_recs_score ON class_recommendations(match_score DESC);
  ```

### 1.5 Verify Schema
- [ ] List all tables to verify creation
- [ ] Check indexes are created correctly
- [ ] Verify foreign key constraints
- [ ] Test inserting sample data to verify relationships work
- [ ] Document schema in README or separate schema file

**Acceptance Criteria:**
- ✅ PostgreSQL database created and accessible
- ✅ All 7 tables created with correct structure
- ✅ All indexes created on appropriate columns
- ✅ Foreign key relationships working correctly
- ✅ Can connect to database from backend application
- ✅ Schema matches specification exactly

