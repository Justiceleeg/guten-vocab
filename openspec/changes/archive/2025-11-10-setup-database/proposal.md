# Change: Setup Database Schema

## Why
Create the PostgreSQL database schema with all required tables, indexes, and relationships to support the vocabulary recommendation engine. This establishes the data model for students, vocabulary words, books, and recommendations before any data seeding or application logic.

## What Changes
- Install PostgreSQL locally (or use Docker)
- Create database: `vocab_engine`
- Set up SQLAlchemy with PostgreSQL connection
- Create database schema with all tables:
  - `students` - Student information
  - `vocabulary_words` - Master vocabulary list (grades 5-8)
  - `student_vocabulary` - Student vocabulary profiles
  - `books` - Project Gutenberg books
  - `book_vocabulary` - Book vocabulary counts
  - `student_recommendations` - Individual book recommendations
  - `class_recommendations` - Class-wide book recommendations
- Create indexes on frequently queried fields

## Impact
- Affected specs: None (infrastructure setup)
- Affected code: Database schema, `backend/app/database.py` (connection setup)

