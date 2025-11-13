## Context
The frontend currently uses client-side React components that fetch data using Axios on every page load. The data is mostly static (pre-computed student profiles, vocabulary analysis, book recommendations) that changes infrequently. Converting to Next.js Server Components with fetch caching will improve performance without requiring backend changes.

## Goals / Non-Goals

**Goals:**
- Improve initial page load performance (server-side rendering)
- Reduce API calls through Next.js fetch caching
- Reduce client-side JavaScript bundle size
- Maintain all existing functionality and user experience
- Keep interactive features working (modals, sorting, dismiss buttons)

**Non-Goals:**
- Backend caching (this is frontend-only optimization)
- Real-time data updates (data is static, caching is appropriate)
- Complex cache invalidation (time-based revalidation is sufficient)
- Breaking existing API contracts

## Decisions

**Decision: Server Components over React Query**
- **Rationale**: Data is mostly static, Server Components provide better performance (SSR, smaller bundles), and Next.js fetch caching is simpler than managing React Query cache.
- **Alternatives considered**: 
  - React Query: Would still require client-side fetching, larger bundle, more complex setup
  - SWR: Similar to React Query, doesn't provide SSR benefits

**Decision: Extract interactive features to small client components**
- **Rationale**: Server Components can't use hooks or event handlers. Extracting only the interactive parts keeps most of the page as Server Component (better performance).
- **Alternatives considered**: 
  - Keep entire pages as client components: Would lose SSR and caching benefits
  - Use Server Actions for all interactions: Overkill for simple UI interactions

**Decision: Time-based revalidation (no manual invalidation)**
- **Rationale**: Data is static and changes infrequently. Time-based revalidation (5-15 minutes) is sufficient and simpler than manual cache invalidation.
- **Alternatives considered**: 
  - Manual cache invalidation: Would require more complex setup, not needed for static data
  - Longer cache times (30+ minutes): Could serve stale data, current times are conservative

**Decision: Keep external API calls (book covers, word definitions) client-side**
- **Rationale**: These are external APIs (Open Library, DictionaryAPI.dev) that can't be easily cached server-side and require client-side interaction anyway.
- **Alternatives considered**: 
  - Server-side fetching: Would require API routes, adds complexity, external APIs may have rate limits

**Decision: Use native `fetch()` instead of Axios**
- **Rationale**: Next.js fetch caching only works with native `fetch()`, not Axios. Native fetch is sufficient for our needs.
- **Alternatives considered**: 
  - Keep Axios: Would lose Next.js caching benefits
  - Create wrapper: Unnecessary complexity, native fetch is fine

## Risks / Trade-offs

**Risk: Breaking interactive features during conversion**
- **Mitigation**: Extract interactive features to client components carefully, test thoroughly

**Risk: Cache serving stale data**
- **Mitigation**: Use conservative revalidation times (5-15 minutes), data is relatively static anyway

**Risk: External API calls still client-side (no caching benefit)**
- **Mitigation**: Acceptable trade-off, these are external APIs that can't be easily cached server-side

**Trade-off: Server Components vs. Client Components**
- **Chosen**: Server Components for data fetching, small client components for interactivity
- **Reason**: Best performance (SSR + caching) while maintaining all interactive features

**Trade-off: Simplicity vs. Performance**
- **Chosen**: Simple time-based revalidation over complex cache invalidation
- **Reason**: Data is static, time-based is sufficient and much simpler

## Migration Plan

1. **Convert pages one at a time**: Start with students list, then detail, then class page
2. **Test each conversion**: Verify functionality and caching before moving to next page
3. **Extract client components incrementally**: Create client components as needed during conversion
4. **No rollback needed**: Changes are additive (can keep old code if needed), but should remove unused code

**Rollback Strategy**: 
- If issues occur, can revert individual page files
- Client components are separate, won't break if Server Components have issues
- No database or API changes, so backend remains stable

## Open Questions
None - straightforward conversion with clear patterns.

