# Implementation Tasks

## 1. TypeScript Types & API Client
- [ ] 1.1 Add class response types to `frontend/lib/types.ts`:
  - [ ] `TopMissingWordResponse` (word, students_missing)
  - [ ] `CommonlyMisusedWordResponse` (word, misuse_count)
  - [ ] `ClassRecommendationResponse` (book_id, title, author, reading_level, students_recommended_count, avg_match_score)
  - [ ] `ClassStatsResponse` (total_students, avg_vocab_mastery_percent, reading_level_distribution, top_missing_words, commonly_misused_words)
- [ ] 1.2 Add API client methods to `frontend/lib/api.ts`:
  - [ ] `getClassStats()` - GET /api/class/stats
  - [ ] `getClassRecommendations()` - GET /api/class/recommendations

## 2. Class Statistics Section
- [ ] 2.1 Fetch class stats data on page load
- [ ] 2.2 Display total students count
- [ ] 2.3 Display average vocabulary mastery percentage with visual indicator
- [ ] 2.4 Create reading level distribution bar chart using recharts:
  - [ ] X-axis: Grade levels (5, 6, 7, 8)
  - [ ] Y-axis: Number of students
  - [ ] Color-coded bars
  - [ ] Responsive chart sizing

## 3. Class-Wide Book Recommendations Section
- [ ] 3.1 Fetch class recommendations data
- [ ] 3.2 Display top 2 books as prominent cards:
  - [ ] Book title and author
  - [ ] "Recommended for X of Y students" text
  - [ ] Average match score (as percentage or visual indicator)
  - [ ] Brief explanation of why book is good for the class
  - [ ] Placeholder image or book icon
- [ ] 3.3 Style cards prominently (larger than student detail page cards)
- [ ] 3.4 Handle empty state (no recommendations)

## 4. Vocabulary Gaps Section
- [ ] 4.1 Display "Top 10 Words Students Need to Learn" header
- [ ] 4.2 Create table/list showing:
  - [ ] Word column
  - [ ] Students Missing column (with count)
  - [ ] Grade Level column (optional - can be added later)
- [ ] 4.3 Make table sortable by students missing count (descending by default)
- [ ] 4.4 Style with alternating row colors or card layout
- [ ] 4.5 Handle empty state (no missing words - unlikely but possible)

## 5. Common Mistakes Section
- [ ] 5.1 Display "Words Frequently Used Incorrectly" header
- [ ] 5.2 Create table/list showing:
  - [ ] Word column (prominently displayed)
  - [ ] Total Misuses column (count)
  - [ ] Students Affected column (count)
- [ ] 5.3 Highlight "through" if it appears (should be top misused word)
- [ ] 5.4 Add example sentence of common misuse (optional enhancement - can show one example on expand)
- [ ] 5.5 Style with alert or warning styling to emphasize issues
- [ ] 5.6 Handle empty state (no misused words)

## 6. Navigation & Layout
- [ ] 6.1 Add "Class Overview" link to main navigation
- [ ] 6.2 Add "Students" link to main navigation (if not present)
- [ ] 6.3 Add navigation breadcrumbs or header showing current page
- [ ] 6.4 Update home page (`/`) to redirect to class view or show both options
- [ ] 6.5 Ensure navigation is accessible via keyboard and screen readers

## 7. Loading & Error States
- [ ] 7.1 Add loading spinner/skeleton for class stats
- [ ] 7.2 Add loading spinner/skeleton for class recommendations
- [ ] 7.3 Add error handling for API failures:
  - [ ] User-friendly error messages
  - [ ] Retry button
  - [ ] Graceful degradation
- [ ] 7.4 Add empty states for all sections

## 8. Styling & Responsiveness
- [ ] 8.1 Apply consistent design system (shadcn/ui + Tailwind)
- [ ] 8.2 Ensure responsive layout:
  - [ ] Mobile: Stack sections vertically
  - [ ] Tablet: 2-column layout where appropriate
  - [ ] Desktop: Optimal 2-3 column layout
- [ ] 8.3 Use shadcn/ui components (Card, Table, Alert, etc.)
- [ ] 8.4 Add helpful tooltips for complex metrics
- [ ] 8.5 Ensure consistent spacing and typography with student view

## 9. Testing & Verification
- [ ] 9.1 Test class stats display with real data from backend
- [ ] 9.2 Verify reading level distribution chart renders correctly
- [ ] 9.3 Verify class recommendations show correct book data
- [ ] 9.4 Check vocabulary gaps table shows top missing words
- [ ] 9.5 Verify "through" appears in commonly misused words
- [ ] 9.6 Test navigation between class and student views
- [ ] 9.7 Test responsive design on tablet and desktop
- [ ] 9.8 Test loading and error states
- [ ] 9.9 Verify no console errors or linting issues

## 10. Polish & Finalization
- [ ] 10.1 Add helpful explanations for teachers (e.g., what "match score" means)
- [ ] 10.2 Optimize chart performance if needed
- [ ] 10.3 Add accessibility attributes (ARIA labels, alt text)
- [ ] 10.4 Review with ALL_TASKS.md requirements to ensure all items completed
- [ ] 10.5 Update documentation or README if needed

