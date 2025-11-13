## 1. Students List Page
- [x] 1.1 Convert `app/students/page.tsx` to Server Component (remove "use client")
- [x] 1.2 Replace `api.getStudents()` with native `fetch()` using `next.revalidate: 300` (5 minutes)
- [x] 1.3 Extract sorting functionality to `<SortableTableHeader>` client component
- [x] 1.4 Extract row click navigation to `<StudentRow>` client component
- [x] 1.5 Extract retry button to `<RetryButton>` client component (if needed)
- [x] 1.6 Test page loads with cached data

## 2. Student Detail Page
- [x] 2.1 Convert `app/students/[id]/page.tsx` to Server Component (remove "use client")
- [x] 2.2 Replace `api.getStudentById()` with native `fetch()` using `next.revalidate: 600` (10 minutes)
- [x] 2.3 Extract dismiss vocabulary functionality to `<DismissVocabularyButton>` client component
- [x] 2.4 Extract book modal state to client component wrapper
- [x] 2.5 Keep book cover fetching as client-side (external API, can't cache easily)
- [x] 2.6 Extract collapsible sections to client component if needed
- [x] 2.7 Test page loads with cached data

## 3. Class Overview Page
- [x] 3.1 Convert `app/class/page.tsx` to Server Component (remove "use client")
- [x] 3.2 Replace `api.getClassStats()` with native `fetch()` using `next.revalidate: 300` (5 minutes)
- [x] 3.3 Replace `api.getClassRecommendations()` with native `fetch()` using `next.revalidate: 900` (15 minutes)
- [x] 3.4 Extract book modal state to client component wrapper
- [x] 3.5 Extract word modal state to client component wrapper
- [x] 3.6 Extract retry buttons to client components
- [x] 3.7 Keep book cover fetching as client-side (external API)
- [x] 3.8 Keep dark mode detection as client-side (if needed)
- [x] 3.9 Test page loads with cached data

## 4. Client Components
- [x] 4.1 Create `components/students/SortableTableHeader.tsx` for sorting functionality
- [x] 4.2 Create `components/students/StudentRow.tsx` for clickable rows
- [x] 4.3 Create `components/students/DismissVocabularyButton.tsx` for dismiss functionality
- [x] 4.4 Create `components/shared/RetryButton.tsx` for error retry (if reusable)
- [x] 4.5 Update existing modal components to work with Server Component data

## 5. Testing and Validation
- [x] 5.1 Verify all pages load correctly as Server Components
- [x] 5.2 Verify caching works (check Network tab, should see cached responses)
- [x] 5.3 Verify interactive features still work (sorting, modals, dismiss)
- [x] 5.4 Verify error states still work correctly
- [x] 5.5 Verify loading states (if any remain)
- [x] 5.6 Test navigation between pages
- [x] 5.7 Verify responsive design still works

## 6. Cleanup
- [x] 6.1 Remove unused `useState` and `useEffect` hooks from converted pages
- [x] 6.2 Remove unused imports (useRouter, etc.) from Server Components
- [x] 6.3 Update any TypeScript types if needed
- [x] 6.4 Verify bundle size reduction (check build output)

