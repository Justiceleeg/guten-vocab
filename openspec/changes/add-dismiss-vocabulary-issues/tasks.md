## 1. Database Schema Changes
- [ ] 1.1 Create migration to add columns to `student_vocabulary` table:
  - `dismissed` BOOLEAN DEFAULT FALSE
  - `dismissed_reason` VARCHAR(20) CHECK (dismissed_reason IN ('addressed', 'ai_error'))
  - `dismissed_at` TIMESTAMP
- [ ] 1.2 Add indexes for efficient filtering:
  - Index on `(student_id, dismissed)` for quick filtering
- [ ] 1.3 Update SQLAlchemy model in `app/models/vocabulary.py`:
  - Add `dismissed`, `dismissed_reason`, `dismissed_at` fields
  - Add validation for dismissed_reason enum

## 2. Backend API Implementation
- [ ] 2.1 Create dismiss endpoint in `app/api/routes/students.py`:
  - Route: `POST /api/students/{student_id}/vocabulary/{word_id}/dismiss`
  - Request body: `{ "reason": "addressed" | "ai_error" }`
  - Response: `{ "success": true, "dismissed_at": timestamp }`
  - Validate student_id and word_id exist
  - Validate reason is one of allowed values
  - Return 404 if student or word not found
  - Return 400 if reason is invalid
- [ ] 2.2 Update `get_misused_words()` in `app/services/student_service.py`:
  - Add filter: `StudentVocabulary.dismissed == False` (or IS NULL for backwards compatibility)
  - Ensure only non-dismissed words are returned
  - Add optional parameter to include dismissed words for teacher review (future)

## 3. Frontend UI Implementation
- [ ] 3.1 Update misused word cards in `app/students/[id]/page.tsx`:
  - Add state management: `dismissingWordId` to track which card is showing action buttons
  - Add X button in top-right of each card (visible on hover or always visible)
  - Style X button with hover effect
- [ ] 3.2 Implement inline dismissal flow:
  - Click X → fade out X, fade/slide in two action buttons
  - "Addressed" button (blue/primary color)
  - "AI Error" button (orange/warning color)
  - Position buttons in top-right where X was
  - Make buttons small/pill-shaped to fit
- [ ] 3.3 Add dismissal logic:
  - Call `POST /api/students/{id}/vocabulary/{word_id}/dismiss` with reason
  - On success: fade out entire card with smooth animation
  - On error: show error message, restore X button
  - Handle loading state during API call (disable buttons)
- [ ] 3.4 Implement cancel behavior:
  - Click outside card OR click another card's X → cancel current dismissal
  - Fade out action buttons, fade in X button
  - Restore original state
- [ ] 3.5 Add CSS transitions:
  - Smooth fade for X button (200ms)
  - Smooth slide/fade for action buttons (200ms)
  - Card fade-out on dismiss (300ms)

## 4. Testing & Validation
- [ ] 4.1 Test backend endpoint:
  - Verify dismiss with "addressed" reason works
  - Verify dismiss with "ai_error" reason works
  - Verify invalid reason returns 400
  - Verify non-existent student/word returns 404
  - Verify dismissed words are filtered from API response
- [ ] 4.2 Test frontend UI:
  - Verify X button appears and is clickable
  - Verify clicking X shows action buttons
  - Verify clicking "Addressed" dismisses word
  - Verify clicking "AI Error" dismisses word
  - Verify card fades out after dismissal
  - Verify cancel behavior (click outside) works
  - Verify multiple cards can be dismissed in sequence
  - Test on students with multiple misused words
- [ ] 4.3 Test edge cases:
  - Rapid clicks on X button
  - Network errors during dismiss
  - Refreshing page after dismiss (should stay dismissed)
  - Multiple browser tabs (one dismisses, other should update on refresh)

## 5. Polish & UX
- [ ] 5.1 Add confirmation for successful dismissal:
  - Optional: Brief toast notification "Word dismissed"
  - Or rely on card fade-out as confirmation
- [ ] 5.2 Update empty state text:
  - Change "No misused words found. Great job! 🎉" to account for dismissed words
  - Could say "No vocabulary issues to review" to be more neutral
- [ ] 5.3 Consider adding "Show dismissed" toggle (future enhancement):
  - Allow teachers to review what they've dismissed
  - Show dismissed words with strikethrough or different styling
  - Include dismiss reason and timestamp

## 6. Documentation
- [ ] 6.1 Update API documentation (if exists) with new endpoint
- [ ] 6.2 Add comments in code explaining dismissal logic
- [ ] 6.3 Document dismiss reasons in schema comments
