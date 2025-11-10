# Change: Seed Books and Extract Vocabulary

## Why
Populate the database with middle-grade appropriate books from Project Gutenberg and extract vocabulary matches. This involves filtering books by category and reading level, selecting the top 100 books, and extracting vocabulary word counts that match our master vocabulary list.

## What Changes
- Create `scripts/seed_books.py` script with two phases:
  - **Phase 1: Book Filtering & Selection**
    - Load pgcorpus metadata CSV
    - Filter books by category ("Children's Literature" OR "Children's Fiction")
    - Filter by language (English)
    - Filter by availability (has counts file available)
    - Calculate reading level using textstat (Flesch-Kincaid)
    - Filter to reading level 5.0-9.0
    - Sort by download count (popularity)
    - Select top 100 books
    - Save list to `/data/books/selected_books.json`
  - **Phase 2: Book Vocabulary Extraction**
    - For each selected book:
      - Load pre-computed counts file from pgcorpus
      - Apply spaCy lemmatization to each word in counts
      - Filter to only words in our vocabulary_words table (525 words)
      - Calculate total word count of book
      - Insert into `books` table
      - Insert word counts into `book_vocabulary` table
    - Add progress tracking
    - Handle errors gracefully (skip books that fail)
    - Print summary statistics

## Impact
- Affected specs: None (data seeding)
- Affected code: `scripts/seed_books.py`, `data/books/` directory

