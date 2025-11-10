-- Database Schema for Vocabulary Recommendation Engine
-- Run this script to create all tables and indexes

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    actual_reading_level FLOAT NOT NULL,
    assigned_grade INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vocabulary words (master list, 5th-8th grade)
CREATE TABLE IF NOT EXISTS vocabulary_words (
    id SERIAL PRIMARY KEY,
    word VARCHAR(100) NOT NULL UNIQUE,
    grade_level INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_vocab_word ON vocabulary_words(word);
CREATE INDEX IF NOT EXISTS idx_vocab_grade ON vocabulary_words(grade_level);

-- Student vocabulary profiles
CREATE TABLE IF NOT EXISTS student_vocabulary (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    word_id INTEGER REFERENCES vocabulary_words(id) ON DELETE CASCADE,
    usage_count INTEGER DEFAULT 0,
    correct_usage_count INTEGER DEFAULT 0,
    misuse_examples TEXT[],
    last_analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, word_id)
);
CREATE INDEX IF NOT EXISTS idx_student_vocab_student ON student_vocabulary(student_id);
CREATE INDEX IF NOT EXISTS idx_student_vocab_word ON student_vocabulary(word_id);

-- Books
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    author VARCHAR(255),
    gutenberg_id INTEGER UNIQUE,
    reading_level FLOAT,
    total_words INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_books_reading_level ON books(reading_level);

-- Book vocabulary (only words in our master vocab list)
CREATE TABLE IF NOT EXISTS book_vocabulary (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    word_id INTEGER REFERENCES vocabulary_words(id) ON DELETE CASCADE,
    occurrence_count INTEGER NOT NULL,
    UNIQUE(book_id, word_id)
);
CREATE INDEX IF NOT EXISTS idx_book_vocab_book ON book_vocabulary(book_id);
CREATE INDEX IF NOT EXISTS idx_book_vocab_word ON book_vocabulary(word_id);

-- Student book recommendations
CREATE TABLE IF NOT EXISTS student_recommendations (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    match_score FLOAT NOT NULL,
    known_words_percent FLOAT NOT NULL,
    new_words_count INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_student_recs_student ON student_recommendations(student_id);
CREATE INDEX IF NOT EXISTS idx_student_recs_book ON student_recommendations(book_id);

-- Class-wide book recommendations
CREATE TABLE IF NOT EXISTS class_recommendations (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    match_score FLOAT NOT NULL,
    students_recommended_count INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_class_recs_score ON class_recommendations(match_score DESC);

