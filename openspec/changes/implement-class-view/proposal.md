# Change: Implement Class View Frontend

## Why
Teachers need a class-wide overview to understand overall vocabulary mastery trends, identify common vocabulary gaps, and discover books that work well for most students. Currently, the backend API provides class statistics and recommendations endpoints (`/api/class/stats` and `/api/class/recommendations`), but the frontend only has a placeholder page. Building the class view will enable teachers to gain actionable insights about the entire class, complement the individual student views, and complete the teacher dashboard MVP.

## What Changes
- Create class overview page (`/class`) with four main sections:
  - **Section 1: Class Statistics** - Total students, average vocabulary mastery, reading level distribution chart
  - **Section 2: Class-Wide Book Recommendations** - Top 2 books recommended for the whole class with prominent cards showing student counts and match scores
  - **Section 3: Vocabulary Gaps** - Top 10 words students need to learn, displayed as sortable table
  - **Section 4: Common Mistakes** - Words frequently used incorrectly with misuse counts, highlighting "through" as expected top misused word
- Update TypeScript types to match backend class API response schemas:
  - Class statistics response types
  - Class recommendation response types
  - Top missing words types
  - Commonly misused words types
- Implement API client methods for class endpoints:
  - `getClassStats()` - Fetch class-wide statistics
  - `getClassRecommendations()` - Fetch top 2 class book recommendations
- Add data visualization components using recharts:
  - Reading level distribution bar chart
  - Vocabulary mastery visualization
- Add navigation between class overview and student list
- Add loading states, error handling, and empty states
- Ensure responsive design (tablet/desktop)
- Add helpful tooltips and explanations for teacher clarity

## Impact
- Affected specs: `teacher-dashboard` (adding class view requirements)
- Affected code:
  - `frontend/app/class/page.tsx` - Class overview page (currently placeholder)
  - `frontend/lib/types.ts` - TypeScript type definitions for class API responses
  - `frontend/lib/api.ts` - API client methods for class endpoints
  - `frontend/components/` - New UI components for charts and visualizations
  - Navigation component - Add class overview link
- External dependencies: None (uses existing shadcn/ui components, recharts library already installed, and backend API)

