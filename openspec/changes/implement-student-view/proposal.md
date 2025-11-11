# Change: Implement Student View Frontend

## Why
Teachers need a user interface to view individual student data, vocabulary profiles, and book recommendations. Currently, the backend API provides all necessary endpoints, but the frontend only has placeholder pages. Building the student view will enable teachers to access student insights, track vocabulary mastery, and view personalized book recommendations through an intuitive dashboard interface.

## What Changes
- Create student list page (`/students`) that displays all students in a table/grid:
  - Show student name, reading level, and vocabulary mastery percentage
  - Add visual indicators (color coding) for proficiency levels
  - Make rows clickable to navigate to student detail pages
- Create student detail page (`/students/[id]`) with four sections:
  - **Section 1: Student Overview** - Name, reading level, assigned grade, vocabulary mastery gauge/chart
  - **Section 2: Book Recommendations** - Display 3 recommended books as cards with match scores, known/new word percentages, and explanations
  - **Section 3: Vocabulary Progress** - Grade-level vocabulary stats with progress bar, expandable missing words list
  - **Section 4: Vocabulary Issues** - Misused words with correct/incorrect usage counts and example sentences
- Update TypeScript types to match backend API response schemas:
  - Student list response types
  - Student detail response types
  - Book recommendation types
  - Vocabulary mastery types
- Implement API client methods for student endpoints:
  - `getStudents()` - Fetch all students
  - `getStudentById(id)` - Fetch detailed student profile
- Add UI components using shadcn/ui:
  - Table component for student list
  - Card components for book recommendations
  - Progress bars for vocabulary mastery
  - Expandable/collapsible sections for missing words
- Add loading states, error handling, and empty states
- Make pages responsive (tablet/desktop)
- Add navigation breadcrumbs

## Impact
- Affected specs: `teacher-dashboard` (new capability)
- Affected code:
  - `frontend/app/students/page.tsx` - Student list page
  - `frontend/app/students/[id]/page.tsx` - Student detail page (new)
  - `frontend/lib/types.ts` - TypeScript type definitions
  - `frontend/lib/api.ts` - API client methods
  - `frontend/components/` - New UI components (if needed)
- External dependencies: None (uses existing shadcn/ui components and backend API)

