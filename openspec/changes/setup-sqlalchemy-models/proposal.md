# Change: Create SQLAlchemy Models

## Why
Create SQLAlchemy ORM models that map to the database schema. This provides type-safe database access, relationship management, and integration with FastAPI for the vocabulary recommendation engine.

## What Changes
- Create SQLAlchemy models matching the database schema:
  - `Student` model
  - `VocabularyWord` model
  - `StudentVocabulary` model
  - `Book` model
  - `BookVocabulary` model
  - `StudentRecommendation` model
  - `ClassRecommendation` model
- Add relationships between models (one-to-many, many-to-many)
- Create database initialization script

## Impact
- Affected specs: None (infrastructure setup)
- Affected code: `backend/app/models/` directory, model files, `backend/app/database.py`

