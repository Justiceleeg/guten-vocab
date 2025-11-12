## 1. Setup and Infrastructure
- [ ] 1.1 Install shadcn/ui Dialog component (`npx shadcn@latest add dialog`)
- [ ] 1.2 Add Open Library API client utilities to `frontend/lib/api.ts`
- [ ] 1.3 Add DictionaryAPI.dev client utilities to `frontend/lib/api.ts`
- [ ] 1.4 Add TypeScript types for book details (cover URL, summary, page count) to `frontend/lib/types.ts`
- [ ] 1.5 Add TypeScript types for word details (definition, usage, origin) to `frontend/lib/types.ts`

## 2. Book Recommendations Enhancement
- [ ] 2.1 Create book detail modal component with Dialog
- [ ] 2.2 Add book cover image display to book recommendation cards (student view)
- [ ] 2.3 Add book cover image display to book recommendation cards (class view)
- [ ] 2.4 Implement book cover fetching from Open Library API (with fallback placeholder)
- [ ] 2.5 Add click handler to book recommendation cards to open modal
- [ ] 2.6 Implement book detail modal content:
  - Book cover image
  - Title and author
  - Page count (from Open Library API)
  - Summary/description (from Open Library API)
  - Reading level
  - Match score and vocabulary stats
- [ ] 2.7 Add loading state for book detail modal while fetching data
- [ ] 2.8 Add error handling for failed API calls (show error message or hide modal)
- [ ] 2.9 Ensure modal is dismissible by clicking outside and ESC key

## 3. Sortable Student Table
- [ ] 3.1 Add sort state management to `/students` page (default: descending by mastery %)
- [ ] 3.2 Add click handler to "Grade Mastery %" table header
- [ ] 3.3 Implement sort toggle logic (ascending ↔ descending)
- [ ] 3.4 Add visual sort indicator (arrow icon) showing current sort direction
- [ ] 3.5 Update table rendering to use sorted data

## 4. Word Detail Modals
- [ ] 4.1 Create word detail modal component with Dialog
- [ ] 4.2 Add click handler to vocabulary gap table rows (`/class` page)
- [ ] 4.3 Add click handler to common mistakes table rows (`/class` page)
- [ ] 4.4 Implement word detail modal content:
  - Word definition (from DictionaryAPI.dev)
  - Usage examples
  - Word origin/etymology
- [ ] 4.5 Add loading state for word detail modal while fetching data
- [ ] 4.6 Add error handling for failed API calls
- [ ] 4.7 Ensure modal is dismissible by clicking outside and ESC key

## 5. Component Unification
- [ ] 5.1 Create reusable `VocabularyTableCard` component
- [ ] 5.2 Extract common structure from vocabulary gaps and common mistakes cards
- [ ] 5.3 Update vocabulary gaps section to use `VocabularyTableCard`
- [ ] 5.4 Update common mistakes section to use `VocabularyTableCard`
- [ ] 5.5 Ensure both cards look and behave identically

## 6. Testing and Verification
- [ ] 6.1 Test book detail modals open and close correctly
- [ ] 6.2 Test book cover images load (with fallback for missing covers)
- [ ] 6.3 Test sortable table functionality (click header, verify sort direction)
- [ ] 6.4 Test word detail modals open from both vocabulary gaps and common mistakes tables
- [ ] 6.5 Test modal dismissible behavior (click outside, ESC key)
- [ ] 6.6 Test loading and error states for all modals
- [ ] 6.7 Verify component unification (both vocabulary cards look identical)
- [ ] 6.8 Test responsive design on mobile, tablet, and desktop

