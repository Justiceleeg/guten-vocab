## 1. Setup and Infrastructure
- [x] 1.1 Install shadcn/ui Dialog component (`npx shadcn@latest add dialog`)
- [x] 1.2 Add Open Library API client utilities to `frontend/lib/api.ts`
- [x] 1.3 Add DictionaryAPI.dev client utilities to `frontend/lib/api.ts`
- [x] 1.4 Add TypeScript types for book details (cover URL, summary, page count) to `frontend/lib/types.ts`
- [x] 1.5 Add TypeScript types for word details (definition, usage, origin) to `frontend/lib/types.ts`

## 2. Book Recommendations Enhancement
- [x] 2.1 Create book detail modal component with Dialog
- [x] 2.2 Add book cover image display to book recommendation cards (student view)
- [x] 2.3 Add book cover image display to book recommendation cards (class view)
- [x] 2.4 Implement book cover fetching from Open Library API (with fallback placeholder)
- [x] 2.5 Add click handler to book recommendation cards to open modal
- [x] 2.6 Implement book detail modal content:
  - Book cover image
  - Title and author
  - Page count (from Open Library API)
  - Summary/description (from Open Library API)
  - Reading level
  - Match score and vocabulary stats
- [x] 2.7 Add loading state for book detail modal while fetching data
- [x] 2.8 Add error handling for failed API calls (show error message or hide modal)
- [x] 2.9 Ensure modal is dismissible by clicking outside and ESC key

## 3. Sortable Student Table
- [x] 3.1 Add sort state management to `/students` page (default: descending by mastery %)
- [x] 3.2 Add click handler to "Grade Mastery %" table header
- [x] 3.3 Implement sort toggle logic (ascending ↔ descending)
- [x] 3.4 Add visual sort indicator (arrow icon) showing current sort direction
- [x] 3.5 Update table rendering to use sorted data

## 4. Word Detail Modals
- [x] 4.1 Create word detail modal component with Dialog
- [x] 4.2 Add click handler to vocabulary gap table rows (`/class` page)
- [x] 4.3 Add click handler to common mistakes table rows (`/class` page)
- [x] 4.4 Implement word detail modal content:
  - Word definition (from DictionaryAPI.dev)
  - Usage examples
  - Word origin/etymology
- [x] 4.5 Add loading state for word detail modal while fetching data
- [x] 4.6 Add error handling for failed API calls
- [x] 4.7 Ensure modal is dismissible by clicking outside and ESC key

## 5. Component Unification
- [x] 5.1 Create reusable `VocabularyTableCard` component
- [x] 5.2 Extract common structure from vocabulary gaps and common mistakes cards
- [x] 5.3 Update vocabulary gaps section to use `VocabularyTableCard`
- [x] 5.4 Update common mistakes section to use `VocabularyTableCard`
- [x] 5.5 Ensure both cards look and behave identically

## 6. Testing and Verification
- [x] 6.1 Test book detail modals open and close correctly
- [x] 6.2 Test book cover images load (with fallback for missing covers)
- [x] 6.3 Test sortable table functionality (click header, verify sort direction)
- [x] 6.4 Test word detail modals open from both vocabulary gaps and common mistakes tables
- [x] 6.5 Test modal dismissible behavior (click outside, ESC key)
- [x] 6.6 Test loading and error states for all modals
- [x] 6.7 Verify component unification (both vocabulary cards look identical)
- [x] 6.8 Test responsive design on mobile, tablet, and desktop

