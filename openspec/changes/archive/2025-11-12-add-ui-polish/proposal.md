# Change: Add UI Polish and Enhanced Interactions

## Why
Before deployment (Slice 9), we want to add UI polish and enhanced interactions to improve the user experience. This includes:
- Adding visual book covers and detailed book information modals
- Making tables sortable for better data exploration
- Adding word detail modals for vocabulary insights
- Unifying component structure for consistency

## What Changes
- **Book Recommendations Enhancement**: Add book cover images (from Open Library API) and detailed book modals showing page count, summary, and full book information
- **Sortable Student Table**: Make the `/students` table sortable by grade mastery percentage (default: highest first, click to toggle)
- **Word Detail Modals**: Add modals for vocabulary words in class view showing dictionary information (definition, usage, origin)
- **Component Unification**: Create reusable `VocabularyTableCard` component for vocabulary gaps and common mistakes tables
- **Modal Infrastructure**: Add shadcn/ui Dialog component for modals with proper dismissible behavior (click outside, ESC key)

## Impact
- **Affected specs**: `teacher-dashboard` (MODIFIED requirements for enhanced UI interactions)
- **Affected code**: 
  - `frontend/app/students/page.tsx` (sortable table)
  - `frontend/app/students/[id]/page.tsx` (book modals)
  - `frontend/app/class/page.tsx` (book modals, word modals, unified components)
  - `frontend/components/ui/dialog.tsx` (new component)
  - `frontend/components/ui/vocabulary-table-card.tsx` (new reusable component)
  - `frontend/lib/api.ts` (new API methods for external APIs)
  - `frontend/lib/types.ts` (new types for book details, word details)

## External Dependencies
- **Open Library API**: Free API for book covers, summaries, and page counts (https://openlibrary.org/developers/api)
- **DictionaryAPI.dev**: Free dictionary API for word definitions, usage, and origin (https://dictionaryapi.dev/)

