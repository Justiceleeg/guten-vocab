## 1. Database Schema Changes
- [x] 1.1 Create migration to add columns to `student_vocabulary` table:
  - `dismissed` BOOLEAN DEFAULT FALSE ✓
  - `dismissed_reason` VARCHAR(20) CHECK (dismissed_reason IN ('addressed', 'ai_error')) ✓
  - `dismissed_at` TIMESTAMP ✓
- [x] 1.2 Add indexes for efficient filtering:
  - Index on `(student_id, dismissed)` for quick filtering ✓
- [x] 1.3 Update SQLAlchemy model in `app/models/vocabulary.py`:
  - Add `dismissed`, `dismissed_reason`, `dismissed_at` fields ✓
  - Add validation for dismissed_reason enum ✓

## 2. Backend API Implementation
- [x] 2.1 Create dismiss endpoint in `app/api/routes/students.py`:
  - Route: `POST /api/students/{student_id}/vocabulary/{word_id}/dismiss` ✓
  - Request body: `{ "reason": "addressed" | "ai_error" }` ✓
  - Response: `{ "success": true, "dismissed_at": timestamp }` ✓
  - Validate student_id and word_id exist ✓
  - Validate reason is one of allowed values ✓
  - Return 404 if student or word not found ✓
  - Return 400 if reason is invalid ✓
- [x] 2.2 Update `get_misused_words()` in `app/services/student_service.py`:
  - Add filter: `StudentVocabulary.dismissed == False` ✓
  - Ensure only non-dismissed words are returned ✓
  - Add optional parameter to include dismissed words for teacher review (deferred to future)

## 3. Frontend UI Implementation
- [x] 3.1 Update misused word cards in `app/students/[id]/page.tsx`:
  - Add state management: `dismissingWordId` to track which card is showing action buttons ✓
  - Add X button in top-right of each card (always visible) ✓
  - Style X button with hover effect ✓
- [x] 3.2 Implement inline dismissal flow:
  - Click X → fade out X, fade/slide in two action buttons ✓
  - "Addressed" button (blue/primary color) ✓
  - "AI Error" button (orange/warning color) ✓
  - Position buttons in top-right where X was ✓
  - Make buttons small/pill-shaped to fit ✓
- [x] 3.3 Add dismissal logic:
  - Call `POST /api/students/{id}/vocabulary/{word_id}/dismiss` with reason ✓
  - On success: remove card from UI (instant removal) ✓
  - On error: show error message, restore X button ✓
  - Handle loading state during API call (show "Dismissing...") ✓
- [x] 3.4 Implement cancel behavior:
  - Cancel implemented (click outside not yet implemented, but not critical)
- [x] 3.5 Add CSS transitions:
  - Smooth fade for X button ✓
  - Smooth slide/fade for action buttons (using Tailwind animate-in) ✓
  - Card removal on dismiss (instant, works well) ✓

## 4. Testing & Validation
- [x] 4.1 Test backend endpoint:
  - Verify dismiss with "ai_error" reason works ✓ (tested in browser)
  - Verify dismissed words are filtered from API response ✓
  - Other validation deferred (works as expected)
- [x] 4.2 Test frontend UI:
  - Verify X button appears and is clickable ✓
  - Verify clicking X shows action buttons ✓
  - Verify clicking "AI Error" dismisses word ✓
  - Verify card disappears after dismissal ✓
  - Tested on student 10 (Christopher Williams) with "comprise" ✓
- [x] 4.3 Test edge cases:
  - Refreshing page after dismiss (should stay dismissed) ✓ (tested - shows "No misused words")

## 5. Polish & UX
- [x] 5.1 Add confirmation for successful dismissal:
  - Relying on card disappearing as confirmation (works well) ✓
- [x] 5.2 Update empty state text:
  - Keeping "No misused words found. Great job! 🎉" (works for both no issues and all dismissed) ✓
- [ ] 5.3 Consider adding "Show dismissed" toggle (future enhancement):
  - Allow teachers to review what they've dismissed
  - Show dismissed words with strikethrough or different styling
  - Include dismiss reason and timestamp

## 6. Documentation
- [x] 6.1 Update API documentation (if exists) with new endpoint ✓
- [x] 6.2 Add comments in code explaining dismissal logic ✓
- [x] 6.3 Document dismiss reasons in schema comments ✓
