# Change: Add Dismiss Vocabulary Issues Feature

## Why
Enable teachers to dismiss vocabulary misuse reports by indicating whether they've addressed the issue with the student or if it's an AI detection error. This handles false positives elegantly while providing valuable feedback data on AI accuracy. The current system shows all detected misuses without allowing teacher intervention, which can include false positives (e.g., students discussing vocabulary words rather than using them).

## What Changes
- Add database schema to track dismissed vocabulary issues with reason and timestamp
- Create API endpoint to dismiss vocabulary issues with specified reason
- Update student detail page UI with inline dismissal flow:
  - X button in top-right of misused word cards
  - Inline two-button choice when X is clicked (no modal)
  - Options: "Addressed" (corrected student) or "AI Error" (false positive)
  - Smooth animations for state transitions
  - Click outside to cancel and restore X button
- Filter dismissed words from misused_words API response
- Optional: Track dismissal metrics for AI improvement

## Impact
- Affected specs: `student-analysis` (modified - add dismissal capability)
- Affected code:
  - Database: `student_vocabulary` table schema (add columns)
  - Backend: `app/api/routes/students.py` (new dismiss endpoint), `app/services/student_service.py` (filter logic)
  - Frontend: `app/students/[id]/page.tsx` (inline dismissal UI)
