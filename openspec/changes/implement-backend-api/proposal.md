# Change: Implement Backend REST API

## Why
The frontend needs a REST API to fetch student data, vocabulary profiles, book recommendations, and class-wide statistics. Currently, the backend has database models and data seeding scripts, but no API endpoints to serve this data to the frontend application. Building the REST API will enable the frontend to display student dashboards, vocabulary insights, and book recommendations.

## What Changes
- Create FastAPI route handlers for student endpoints:
  - `GET /api/students` - Returns list of all students with basic info (id, name, reading_level, assigned_grade, vocab_mastery_percent)
  - `GET /api/students/{id}` - Returns detailed student profile including vocabulary mastery, missing words, misused words, and book recommendations
- Create FastAPI route handlers for class endpoints:
  - `GET /api/class/stats` - Returns class-wide statistics (total students, avg vocab mastery, reading level distribution, top missing words, commonly misused words)
  - `GET /api/class/recommendations` - Returns top 2 class-wide book recommendations
- Create optional `GET /api/books` endpoint for listing all books (useful for debugging/exploration)
- Create Pydantic schemas for request/response validation:
  - Student list response schema
  - Student detail response schema
  - Class stats response schema
  - Class recommendations response schema
  - Book list response schema
- Create service layer functions to handle business logic:
  - Student service for querying student data and calculating vocabulary mastery
  - Class service for aggregating class-wide statistics
  - Recommendation service for fetching book recommendations
- Add error handling:
  - 404 for missing students
  - 500 for server errors
  - Proper HTTP status codes
- Configure CORS for frontend integration (already exists in main.py, verify configuration)
- Enable FastAPI automatic documentation at `/docs`

## Impact
- Affected specs: `rest-api` (new capability)
- Affected code:
  - `backend/app/api/` - New route handlers
  - `backend/app/schemas/` - New Pydantic schemas (create directory)
  - `backend/app/services/` - New service functions
  - `backend/app/main.py` - Register API routes
- External dependencies: None (uses existing database and models)

