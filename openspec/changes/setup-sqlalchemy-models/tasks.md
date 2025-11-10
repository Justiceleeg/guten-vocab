## 1. SQLAlchemy Models

### 1.1 Create Base Model
- [x] Create `backend/app/models/__init__.py` - Created with Base import and all model exports
- [x] Set up SQLAlchemy Base class - Base imported from app.database
- [x] Configure declarative base - Base configured in database.py
- [x] Export Base for use in other model files - All models exported in __init__.py

### 1.2 Create Student Model
- [x] Create `backend/app/models/student.py` - Created with Student class
- [x] Define `Student` class inheriting from Base - Student class defined
- [x] Add columns: id, name, actual_reading_level, assigned_grade, created_at - All columns added
- [x] Add relationships:
  - `student_vocabulary` (one-to-many with StudentVocabulary) - Relationship added
  - `recommendations` (one-to-many with StudentRecommendation) - Relationship added
- [x] Add `__repr__` method for debugging - __repr__ method added

### 1.3 Create VocabularyWord Model
- [x] Create `backend/app/models/vocabulary.py` - Created with VocabularyWord and StudentVocabulary classes
- [x] Define `VocabularyWord` class inheriting from Base - VocabularyWord class defined
- [x] Add columns: id, word, grade_level, created_at - All columns added with indexes
- [x] Add relationships:
  - `student_vocabulary` (one-to-many with StudentVocabulary) - Relationship added
  - `book_vocabulary` (one-to-many with BookVocabulary) - Relationship added
- [x] Add `__repr__` method - __repr__ method added

### 1.4 Create StudentVocabulary Model
- [x] Add `StudentVocabulary` class to `backend/app/models/vocabulary.py` - Created in vocabulary.py
- [x] Define columns: id, student_id, word_id, usage_count, correct_usage_count, misuse_examples, last_analyzed_at - All columns added
- [x] Add foreign key relationships:
  - `student` (many-to-one with Student) - Relationship added with back_populates
  - `word` (many-to-one with VocabularyWord) - Relationship added with back_populates
- [x] Add unique constraint on (student_id, word_id) - UniqueConstraint added
- [x] Add `__repr__` method - __repr__ method added

### 1.5 Create Book Model
- [x] Create `backend/app/models/book.py` - Created with Book and BookVocabulary classes
- [x] Define `Book` class inheriting from Base - Book class defined
- [x] Add columns: id, title, author, gutenberg_id, reading_level, total_words, created_at - All columns added
- [x] Add relationships:
  - `book_vocabulary` (one-to-many with BookVocabulary) - Relationship added
  - `student_recommendations` (one-to-many with StudentRecommendation) - Relationship added
  - `class_recommendations` (one-to-many with ClassRecommendation) - Relationship added
- [x] Add `__repr__` method - __repr__ method added

### 1.6 Create BookVocabulary Model
- [x] Add `BookVocabulary` class to `backend/app/models/book.py` - Created in book.py
- [x] Define columns: id, book_id, word_id, occurrence_count - All columns added
- [x] Add foreign key relationships:
  - `book` (many-to-one with Book) - Relationship added with back_populates
  - `word` (many-to-one with VocabularyWord) - Relationship added with back_populates
- [x] Add unique constraint on (book_id, word_id) - UniqueConstraint added
- [x] Add `__repr__` method - __repr__ method added

### 1.7 Create StudentRecommendation Model
- [x] Create `backend/app/models/recommendation.py` - Created with StudentRecommendation and ClassRecommendation classes
- [x] Define `StudentRecommendation` class inheriting from Base - StudentRecommendation class defined
- [x] Add columns: id, student_id, book_id, match_score, known_words_percent, new_words_count, created_at - All columns added
- [x] Add foreign key relationships:
  - `student` (many-to-one with Student) - Relationship added with back_populates
  - `book` (many-to-one with Book) - Relationship added with back_populates
- [x] Add `__repr__` method - __repr__ method added

### 1.8 Create ClassRecommendation Model
- [x] Add `ClassRecommendation` class to `backend/app/models/recommendation.py` - Created in recommendation.py
- [x] Define columns: id, book_id, match_score, students_recommended_count, created_at - All columns added
- [x] Add foreign key relationship:
  - `book` (many-to-one with Book) - Relationship added with back_populates
- [x] Add `__repr__` method - __repr__ method added

### 1.9 Create Database Initialization Script
- [x] Create `backend/app/database.py` (if not already created) - Already exists, updated
- [x] Import Base and all models - Models imported in init_db function
- [x] Create function to initialize database (create_all) - init_db function updated
- [x] Add function to get database session - get_db function exists
- [x] Add dependency function for FastAPI routes - get_db function exists
- [x] Test database initialization - Tested successfully

### 1.10 Verify Models
- [x] Import all models in a test script - test_models.py created
- [x] Verify relationships are correctly defined - All relationships verified
- [x] Test creating instances of each model - All models tested
- [x] Test saving to database and querying back - Save and query tested
- [x] Verify foreign key constraints work - Foreign keys verified
- [x] Test relationship access (e.g., student.student_vocabulary) - Relationship access tested successfully

**Acceptance Criteria:**
- ✅ All 7 SQLAlchemy models created
- ✅ All models match database schema exactly
- ✅ Relationships correctly defined (one-to-many, many-to-one)
- ✅ Foreign keys and constraints match database schema
- ✅ Database initialization script works
- ✅ Can create, query, and relate model instances
- ✅ All models importable and usable in FastAPI routes

