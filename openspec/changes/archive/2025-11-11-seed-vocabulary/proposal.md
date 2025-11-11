# Change: Seed Vocabulary Data

## Why
Populate the database with vocabulary words from grade-level vocabulary lists (grades 5-8). This establishes the master vocabulary list that will be used for matching student vocabulary and book vocabulary throughout the recommendation engine.

## What Changes
- Copy vocabulary JSON files to `/data/vocab/` directory:
  - 5th_grade.json (150 words)
  - 6th_grade.json (125 words)
  - 7th_grade.json (125 words)
  - 8th_grade.json (125 words)
- Create `scripts/seed_vocabulary.py` script to:
  - Load all 4 JSON files
  - Insert words into `vocabulary_words` table with grade levels
  - Handle duplicates (some words may appear in multiple grades - keep highest grade)
  - Print summary: "Loaded X words across grades 5-8"

## Impact
- Affected specs: None (data seeding)
- Affected code: `scripts/seed_vocabulary.py`, `data/vocab/` directory

