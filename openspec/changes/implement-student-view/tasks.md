## 1. Update TypeScript Types
- [ ] 1.1 Update `frontend/lib/types.ts` with API response types:
  - `StudentListResponse` interface (id, name, reading_level, assigned_grade, vocab_mastery_percent)
  - `StudentDetailResponse` interface with nested types:
    - `VocabMasteryResponse` (total_grade_level_words, words_mastered, mastery_percent)
    - `MisusedWordResponse` (word, correct_count, incorrect_count, example)
    - `BookRecommendationResponse` (book_id, title, author, reading_level, match_score, known_words_percent, new_words_count)
  - Match types to backend Pydantic schemas exactly

## 2. Implement API Client Methods
- [ ] 2.1 Add `getStudents()` method to `frontend/lib/api.ts`:
  - Call `GET /api/students`
  - Return array of `StudentListResponse`
  - Handle errors appropriately
- [ ] 2.2 Add `getStudentById(id: number)` method to `frontend/lib/api.ts`:
  - Call `GET /api/students/{id}`
  - Return `StudentDetailResponse`
  - Handle 404 errors for non-existent students
  - Handle network errors

## 3. Create Student List Page
- [ ] 3.1 Update `frontend/app/students/page.tsx`:
  - Fetch students using `getStudents()` API method
  - Display students in a table using shadcn/ui Table component
  - Show columns: Name, Reading Level, Vocab Mastery %
  - Add visual indicators (color coding) for proficiency levels:
    - Low mastery (<50%): Red/orange
    - Medium mastery (50-75%): Yellow
    - High mastery (>75%): Green
  - Make table rows clickable to navigate to `/students/[id]`
  - Add loading state while fetching data
  - Add error state if API call fails
  - Add empty state if no students found

## 4. Create Student Detail Page
- [ ] 4.1 Create `frontend/app/students/[id]/page.tsx`:
  - Fetch student data using `getStudentById(id)` API method
  - Handle loading, error, and not found states
  - Add navigation breadcrumbs (Home > Students > [Student Name])

- [ ] 4.2 Implement Section 1: Student Overview:
  - Display student name, reading level, assigned grade
  - Create vocabulary mastery gauge/chart:
    - Use progress bar or circular progress component
    - Show mastery percentage visually
    - Display "X of Y words mastered (Z%)"
  - Use shadcn/ui Card component for layout

- [ ] 4.3 Implement Section 2: Book Recommendations:
  - Display 3 recommended books as cards
  - Each card shows:
    - Book title and author
    - Placeholder image (or book icon)
    - Match score (as percentage or star rating)
    - "Known: X% | New: Y% (Z words)" text
    - Brief explanation: "This book will challenge you with Z new vocabulary words while reinforcing words you already know."
  - Use shadcn/ui Card components
  - Make cards visually appealing with proper spacing

- [ ] 4.4 Implement Section 3: Vocabulary Progress:
  - Display grade-level vocabulary stats:
    - "Mastered X of Y [grade] words (Z%)"
    - Progress bar visualization using shadcn/ui Progress component
  - Create expandable/collapsible section for missing words:
    - Default: Collapsed with count ("X missing words")
    - Expanded: List of missing words (can be long list)
    - Use shadcn/ui Collapsible or Accordion component
  - Use shadcn/ui Card component for layout

- [ ] 4.5 Implement Section 4: Vocabulary Issues:
  - Create "Words Used Incorrectly" section
  - For each misused word, display:
    - Word name (prominent)
    - Correct vs. incorrect usage count (e.g., "Correct: 2 | Incorrect: 3")
    - Example sentence(s) of misuse (1-2 examples)
    - Highlight the misused word in the example sentence
  - Use shadcn/ui Card or Alert component for each misused word
  - Show empty state if no misused words

## 5. Styling & UX Improvements
- [ ] 5.1 Apply consistent design system:
  - Use Tailwind CSS utility classes
  - Use shadcn/ui components consistently
  - Follow existing design patterns from class page
- [ ] 5.2 Add loading states:
  - Skeleton loaders for table rows
  - Skeleton loaders for student detail sections
  - Use shadcn/ui Skeleton component
- [ ] 5.3 Add error handling:
  - Display user-friendly error messages
  - Add retry buttons for failed API calls
  - Use shadcn/ui Alert component for errors
- [ ] 5.4 Add empty states:
  - Empty state for student list (no students)
  - Empty state for missing words (all words mastered)
  - Empty state for misused words (no misused words)
- [ ] 5.5 Make pages responsive:
  - Test on tablet (768px) and desktop (1024px+)
  - Ensure tables are scrollable on mobile
  - Stack cards vertically on smaller screens
- [ ] 5.6 Add navigation breadcrumbs:
  - Use shadcn/ui Breadcrumb component
  - Show: Home > Students > [Student Name] on detail page
  - Make breadcrumb items clickable

## 6. Testing & Validation
- [ ] 6.1 Test student list page:
  - Verify all 25 students display correctly
  - Verify color coding works for proficiency levels
  - Verify clicking rows navigates to detail page
  - Test loading and error states
- [ ] 6.2 Test student detail page:
  - Verify all sections display correctly
  - Verify data matches API responses
  - Test with different students (high/low mastery)
  - Test with students who have misused words
  - Test with students who have no misused words
  - Verify navigation breadcrumbs work
  - Test 404 handling for non-existent students
- [ ] 6.3 Test responsive design:
  - Test on different screen sizes
  - Verify tables and cards adapt properly
- [ ] 6.4 Verify TypeScript types:
  - Ensure no type errors
  - Verify types match backend API exactly

## 7. Code Quality
- [ ] 7.1 Add comments to complex logic
- [ ] 7.2 Ensure consistent code formatting
- [ ] 7.3 Remove any console.log statements
- [ ] 7.4 Verify no linting errors

