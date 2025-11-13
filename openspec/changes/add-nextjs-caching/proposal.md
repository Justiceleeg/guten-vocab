# Change: Add Next.js Server Components with Fetch Caching

## Why
The frontend currently uses client-side components that fetch data on every page load, resulting in slower initial page loads and unnecessary API calls. Since the data is mostly static (pre-computed student profiles, vocabulary analysis, book recommendations), converting to Server Components with Next.js fetch caching will improve performance by:
- Rendering pages on the server (faster initial load)
- Caching API responses automatically (fewer backend requests)
- Reducing client-side JavaScript bundle size
- Improving SEO and Core Web Vitals

## What Changes
- Convert page components from client components to Server Components
- Replace Axios API calls with native `fetch()` using Next.js `next.revalidate` option
- Extract interactive features (sorting, modals, dismiss buttons) to small client components
- Add fetch caching with appropriate revalidation times (5-15 minutes)
- Maintain all existing functionality and user experience

## Impact
- Affected specs: `teacher-dashboard` (modifies how data is fetched and rendered)
- Affected code:
  - `frontend/app/students/page.tsx` (convert to Server Component)
  - `frontend/app/students/[id]/page.tsx` (convert to Server Component)
  - `frontend/app/class/page.tsx` (convert to Server Component)
  - `frontend/lib/api.ts` (may need updates or can be kept for client-side features)
  - New client components for interactive features (sorting, modals, etc.)
- No backend changes required
- No breaking changes to API contracts

