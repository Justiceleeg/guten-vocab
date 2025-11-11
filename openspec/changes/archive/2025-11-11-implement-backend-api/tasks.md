## 1. Setup API Structure
- [x] 1.1 Create `backend/app/schemas/` directory and `__init__.py`
- [x] 1.2 Create `backend/app/api/routes/` directory structure
- [x] 1.3 Create `backend/app/api/routes/__init__.py`
- [x] 1.4 Create `backend/app/api/routes/students.py` for student endpoints
- [x] 1.5 Create `backend/app/api/routes/class.py` for class endpoints
- [x] 1.6 Create `backend/app/api/routes/books.py` for books endpoint (optional)

## 2. Create Pydantic Schemas
- [x] 2.1 Create `backend/app/schemas/student.py` with:
  - `StudentListResponse` schema (id, name, reading_level, assigned_grade, vocab_mastery_percent)
  - `StudentDetailResponse` schema (full student profile with nested vocab_mastery, missing_words, misused_words, book_recommendations)
  - `VocabMasteryResponse` schema (total_grade_level_words, words_mastered, mastery_percent)
  - `MisusedWordResponse` schema (word, correct_count, incorrect_count, example)
  - `BookRecommendationResponse` schema (book_id, title, author, reading_level, match_score, known_words_percent, new_words_count)
- [x] 2.2 Create `backend/app/schemas/class.py` with:
  - `ClassStatsResponse` schema (total_students, avg_vocab_mastery_percent, reading_level_distribution, top_missing_words, commonly_misused_words)
  - `TopMissingWordResponse` schema (word, students_missing)
  - `CommonlyMisusedWordResponse` schema (word, misuse_count)
  - `ClassRecommendationResponse` schema (book_id, title, author, reading_level, students_recommended_count, avg_match_score)
- [x] 2.3 Create `backend/app/schemas/book.py` with:
  - `BookListResponse` schema (id, title, author, reading_level, total_words)

## 3. Create Service Layer
- [x] 3.1 Create `backend/app/services/student_service.py` with:
  - `get_all_students(db)` - Query all students, calculate vocab_mastery_percent for each
  - `get_student_by_id(db, student_id)` - Query student with related data, calculate detailed vocab mastery, get missing words, get misused words, get book recommendations
  - `calculate_vocab_mastery_percent(student)` - Calculate percentage of grade-level words mastered
  - `get_missing_words(student)` - Get list of vocabulary words student hasn't used correctly
  - `get_misused_words(student)` - Get list of words with misuse examples
- [x] 3.2 Create `backend/app/services/class_service.py` with:
  - `get_class_stats(db)` - Aggregate class-wide statistics (total students, avg mastery, reading level distribution, top missing words, commonly misused words)
  - `get_class_recommendations(db)` - Query top 2 class recommendations with book details
- [x] 3.3 Create `backend/app/services/recommendation_service.py` with:
  - `get_student_recommendations(db, student_id)` - Query student recommendations with book details
- [x] 3.4 Create `backend/app/services/__init__.py` to export services

## 4. Implement Student Endpoints
- [x] 4.1 Implement `GET /api/students` in `backend/app/api/routes/students.py`:
  - Use `get_all_students` service
  - Return list of `StudentListResponse` schemas
  - Handle database errors
- [x] 4.2 Implement `GET /api/students/{id}` in `backend/app/api/routes/students.py`:
  - Use `get_student_by_id` service
  - Return `StudentDetailResponse` schema
  - Return 404 if student not found
  - Handle database errors

## 5. Implement Class Endpoints
- [x] 5.1 Implement `GET /api/class/stats` in `backend/app/api/routes/class.py`:
  - Use `get_class_stats` service
  - Return `ClassStatsResponse` schema
  - Handle database errors
- [x] 5.2 Implement `GET /api/class/recommendations` in `backend/app/api/routes/class.py`:
  - Use `get_class_recommendations` service
  - Return list of `ClassRecommendationResponse` schemas
  - Handle database errors

## 6. Implement Books Endpoint (Optional)
- [x] 6.1 Implement `GET /api/books` in `backend/app/api/routes/books.py`:
  - Query all books from database
  - Support optional query parameters: `reading_level_min`, `reading_level_max`
  - Return list of `BookListResponse` schemas
  - Handle database errors

## 7. Register Routes in Main App
- [x] 7.1 Import route routers in `backend/app/main.py`
- [x] 7.2 Register student routes with `app.include_router(students_router, prefix="/api/students", tags=["students"])`
- [x] 7.3 Register class routes with `app.include_router(class_router, prefix="/api/class", tags=["class"])`
- [x] 7.4 Register books routes with `app.include_router(books_router, prefix="/api/books", tags=["books"])` (if implemented)

## 8. Error Handling and Validation
- [x] 8.1 Add 404 error handler for missing students in student endpoints
- [x] 8.2 Add 500 error handler for database/server errors
- [x] 8.3 Validate student_id is integer in path parameters
- [x] 8.4 Verify CORS configuration in `main.py` allows frontend origin

## 9. Testing and Documentation
- [x] 9.1 Test `GET /api/students` with curl or Postman:
  - Verify returns list of all students
  - Verify vocab_mastery_percent is calculated correctly
  - ✅ Tested with test script - all 25 students returned correctly
- [x] 9.2 Test `GET /api/students/{id}` with curl or Postman:
  - Verify returns detailed student profile
  - Verify 404 for non-existent student
  - Verify vocab_mastery, missing_words, misused_words, book_recommendations are correct
  - ✅ Tested with test script - detailed profile correct, 404 works
- [x] 9.3 Test `GET /api/class/stats` with curl or Postman:
  - Verify returns class-wide statistics
  - Verify calculations are correct
  - ✅ Tested with test script - class stats returned correctly
- [x] 9.4 Test `GET /api/class/recommendations` with curl or Postman:
  - Verify returns top 2 class recommendations
  - Verify book details are included
  - ✅ Tested with test script - 2 recommendations returned with book details
- [x] 9.5 Test `GET /api/books` (if implemented) with curl or Postman:
  - Verify returns list of books
  - Test filtering by reading_level_min/max
  - ✅ Tested with test script - books returned, filtering works
- [x] 9.6 Verify FastAPI automatic docs available at `/docs`
  - ✅ Verified - docs accessible at /docs and /redoc
- [x] 9.7 Verify all endpoints return correct JSON structure matching schemas
  - ✅ Verified - all endpoints return correct JSON matching Pydantic schemas

## 10. Validation
- [x] 10.1 Run `openspec validate implement-backend-api --strict` and fix any issues
  - ✅ Validated - no issues found
- [x] 10.2 Verify all tasks are complete before marking change as ready
  - ✅ All tasks complete - ready for archive

