# rest-api Specification

## Purpose
TBD - created by archiving change implement-backend-api. Update Purpose after archive.
## Requirements
### Requirement: Student List Endpoint
The system SHALL provide a REST API endpoint that returns a list of all students with basic information including vocabulary mastery percentage.

#### Scenario: Get list of all students
- **WHEN** a client sends a GET request to `/api/students`
- **THEN** the system queries all students from the database
- **AND** calculates vocabulary mastery percentage for each student (words mastered / total grade-level words)
- **AND** returns a JSON array of student objects with:
  - `id`: student ID
  - `name`: student name
  - `reading_level`: student reading level (float)
  - `assigned_grade`: assigned grade level (integer)
  - `vocab_mastery_percent`: percentage of grade-level vocabulary mastered (float)
- **AND** returns HTTP 200 status code

### Requirement: Student Detail Endpoint
The system SHALL provide a REST API endpoint that returns detailed student profile information including vocabulary mastery, missing words, misused words, and book recommendations.

#### Scenario: Get detailed student profile
- **WHEN** a client sends a GET request to `/api/students/{id}` with a valid student ID
- **THEN** the system queries the student from the database
- **AND** calculates detailed vocabulary mastery metrics:
  - `total_grade_level_words`: total number of grade-level vocabulary words
  - `words_mastered`: number of words used correctly at least once
  - `mastery_percent`: percentage of grade-level vocabulary mastered
- **AND** retrieves missing words (vocabulary words student hasn't used correctly)
- **AND** retrieves misused words with examples:
  - `word`: vocabulary word
  - `correct_count`: number of correct usages
  - `incorrect_count`: number of incorrect usages
  - `example`: example sentence with misuse
- **AND** retrieves book recommendations for the student:
  - `book_id`: book ID
  - `title`: book title
  - `author`: book author
  - `reading_level`: book reading level
  - `match_score`: recommendation match score (0-1)
  - `known_words_percent`: percentage of vocabulary words student knows
  - `new_words_count`: number of new vocabulary words in book
- **AND** returns a JSON object with all student profile data
- **AND** returns HTTP 200 status code

#### Scenario: Handle missing student
- **WHEN** a client sends a GET request to `/api/students/{id}` with a non-existent student ID
- **THEN** the system returns HTTP 404 status code
- **AND** returns an error message indicating student not found

### Requirement: Class Statistics Endpoint
The system SHALL provide a REST API endpoint that returns class-wide statistics including total students, average vocabulary mastery, reading level distribution, top missing words, and commonly misused words.

#### Scenario: Get class-wide statistics
- **WHEN** a client sends a GET request to `/api/class/stats`
- **THEN** the system queries all students from the database
- **AND** calculates class-wide statistics:
  - `total_students`: total number of students in class
  - `avg_vocab_mastery_percent`: average vocabulary mastery percentage across all students
  - `reading_level_distribution`: count of students by reading level (e.g., {"5": 2, "6": 6, "7": 13, "8": 4})
  - `top_missing_words`: top 10 vocabulary words most students are missing (word, students_missing count)
  - `commonly_misused_words`: top 10 words most commonly misused across the class (word, misuse_count)
- **AND** returns a JSON object with all class statistics
- **AND** returns HTTP 200 status code

### Requirement: Class Book Recommendations Endpoint
The system SHALL provide a REST API endpoint that returns the top 2 class-wide book recommendations.

#### Scenario: Get class-wide book recommendations
- **WHEN** a client sends a GET request to `/api/class/recommendations`
- **THEN** the system queries the top 2 class recommendations from the database
- **AND** retrieves book details for each recommendation:
  - `book_id`: book ID
  - `title`: book title
  - `author`: book author
  - `reading_level`: book reading level
  - `students_recommended_count`: number of students who have this book recommended
  - `avg_match_score`: average match score across all students
- **AND** returns a JSON array of recommendation objects (max 2)
- **AND** returns HTTP 200 status code

### Requirement: Books List Endpoint
The system SHALL provide an optional REST API endpoint that returns a list of all books in the database with optional filtering by reading level.

#### Scenario: Get list of all books
- **WHEN** a client sends a GET request to `/api/books`
- **THEN** the system queries all books from the database
- **AND** returns a JSON array of book objects with:
  - `id`: book ID
  - `title`: book title
  - `author`: book author
  - `reading_level`: book reading level (float, nullable)
  - `total_words`: total word count (integer, nullable)
- **AND** returns HTTP 200 status code

#### Scenario: Filter books by reading level
- **WHEN** a client sends a GET request to `/api/books` with query parameters `reading_level_min` and/or `reading_level_max`
- **THEN** the system filters books by reading level range
- **AND** returns only books within the specified range
- **AND** returns HTTP 200 status code

### Requirement: API Error Handling
The system SHALL handle API errors gracefully and return appropriate HTTP status codes.

#### Scenario: Handle server errors
- **WHEN** a database error or server error occurs during an API request
- **THEN** the system returns HTTP 500 status code
- **AND** returns an error message indicating server error
- **AND** logs the error for debugging

#### Scenario: Handle invalid request parameters
- **WHEN** a client sends a request with invalid parameters (e.g., non-integer student ID)
- **THEN** the system returns HTTP 422 status code (Unprocessable Entity)
- **AND** returns validation error details

### Requirement: API Documentation
The system SHALL provide automatic API documentation accessible via FastAPI's built-in documentation endpoints.

#### Scenario: Access API documentation
- **WHEN** a client navigates to `/docs` endpoint
- **THEN** the system serves FastAPI's automatic interactive API documentation (Swagger UI)
- **AND** all API endpoints are documented with request/response schemas
- **AND** clients can test endpoints directly from the documentation interface

### Requirement: CORS Configuration
The system SHALL configure CORS to allow frontend requests from the Next.js application.

#### Scenario: Allow frontend requests
- **WHEN** the frontend application sends API requests from `http://localhost:3000` (or configured frontend origin)
- **THEN** the system allows the requests via CORS middleware
- **AND** includes appropriate CORS headers in responses
- **AND** allows credentials if needed

