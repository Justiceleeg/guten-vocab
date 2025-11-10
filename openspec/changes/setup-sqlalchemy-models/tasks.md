## 1. SQLAlchemy Models

### 1.1 Create Base Model
- [ ] Create `backend/app/models/__init__.py`
- [ ] Set up SQLAlchemy Base class
- [ ] Configure declarative base
- [ ] Export Base for use in other model files

### 1.2 Create Student Model
- [ ] Create `backend/app/models/student.py`
- [ ] Define `Student` class inheriting from Base
- [ ] Add columns: id, name, actual_reading_level, assigned_grade, created_at
- [ ] Add relationships:
  - `student_vocabulary` (one-to-many with StudentVocabulary)
  - `recommendations` (one-to-many with StudentRecommendation)
- [ ] Add `__repr__` method for debugging

### 1.3 Create VocabularyWord Model
- [ ] Create `backend/app/models/vocabulary.py`
- [ ] Define `VocabularyWord` class inheriting from Base
- [ ] Add columns: id, word, grade_level, created_at
- [ ] Add relationships:
  - `student_vocabulary` (one-to-many with StudentVocabulary)
  - `book_vocabulary` (one-to-many with BookVocabulary)
- [ ] Add `__repr__` method

### 1.4 Create StudentVocabulary Model
- [ ] Add `StudentVocabulary` class to `backend/app/models/vocabulary.py` (or separate file)
- [ ] Define columns: id, student_id, word_id, usage_count, correct_usage_count, misuse_examples, last_analyzed_at
- [ ] Add foreign key relationships:
  - `student` (many-to-one with Student)
  - `word` (many-to-one with VocabularyWord)
- [ ] Add unique constraint on (student_id, word_id)
- [ ] Add `__repr__` method

### 1.5 Create Book Model
- [ ] Create `backend/app/models/book.py`
- [ ] Define `Book` class inheriting from Base
- [ ] Add columns: id, title, author, gutenberg_id, reading_level, total_words, created_at
- [ ] Add relationships:
  - `book_vocabulary` (one-to-many with BookVocabulary)
  - `student_recommendations` (one-to-many with StudentRecommendation)
  - `class_recommendations` (one-to-many with ClassRecommendation)
- [ ] Add `__repr__` method

### 1.6 Create BookVocabulary Model
- [ ] Add `BookVocabulary` class to `backend/app/models/book.py` (or separate file)
- [ ] Define columns: id, book_id, word_id, occurrence_count
- [ ] Add foreign key relationships:
  - `book` (many-to-one with Book)
  - `word` (many-to-one with VocabularyWord)
- [ ] Add unique constraint on (book_id, word_id)
- [ ] Add `__repr__` method

### 1.7 Create StudentRecommendation Model
- [ ] Create `backend/app/models/recommendation.py`
- [ ] Define `StudentRecommendation` class inheriting from Base
- [ ] Add columns: id, student_id, book_id, match_score, known_words_percent, new_words_count, created_at
- [ ] Add foreign key relationships:
  - `student` (many-to-one with Student)
  - `book` (many-to-one with Book)
- [ ] Add `__repr__` method

### 1.8 Create ClassRecommendation Model
- [ ] Add `ClassRecommendation` class to `backend/app/models/recommendation.py`
- [ ] Define columns: id, book_id, match_score, students_recommended_count, created_at
- [ ] Add foreign key relationship:
  - `book` (many-to-one with Book)
- [ ] Add `__repr__` method

### 1.9 Create Database Initialization Script
- [ ] Create `backend/app/database.py` (if not already created)
- [ ] Import Base and all models
- [ ] Create function to initialize database (create_all)
- [ ] Add function to get database session
- [ ] Add dependency function for FastAPI routes
- [ ] Test database initialization

### 1.10 Verify Models
- [ ] Import all models in a test script
- [ ] Verify relationships are correctly defined
- [ ] Test creating instances of each model
- [ ] Test saving to database and querying back
- [ ] Verify foreign key constraints work
- [ ] Test relationship access (e.g., student.student_vocabulary)

**Acceptance Criteria:**
- ✅ All 7 SQLAlchemy models created
- ✅ All models match database schema exactly
- ✅ Relationships correctly defined (one-to-many, many-to-one)
- ✅ Foreign keys and constraints match database schema
- ✅ Database initialization script works
- ✅ Can create, query, and relate model instances
- ✅ All models importable and usable in FastAPI routes

