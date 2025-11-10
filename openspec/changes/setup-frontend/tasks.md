## 1. Frontend Setup

### 1.1 Initialize Next.js Project
- [ ] Navigate to `frontend/` directory
- [ ] Run `npx create-next-app@latest . --typescript --tailwind --app --no-src-dir` (or adjust for src/ structure)
- [ ] Verify TypeScript configuration is set up correctly
- [ ] Verify Next.js app runs: `npm run dev`

### 1.2 Install Dependencies
- [ ] Install tailwindcss (if not included in create-next-app)
- [ ] Install axios: `npm install axios`
- [ ] Install recharts: `npm install recharts`
- [ ] Verify all dependencies in `package.json`

### 1.3 Configure Tailwind CSS
- [ ] Verify `tailwind.config.js` or `tailwind.config.ts` exists
- [ ] Configure content paths to include all component files
- [ ] Add any custom theme configurations if needed
- [ ] Verify Tailwind CSS is working in a test component

### 1.4 Set Up shadcn/ui Component Library
- [ ] Initialize shadcn/ui: `npx shadcn-ui@latest init`
- [ ] Configure shadcn/ui (choose TypeScript, Tailwind, etc.)
- [ ] Install base components as needed (Card, Button, Table, etc.)
- [ ] Verify components are accessible in `src/components/ui/`

### 1.5 Create Basic Layout
- [ ] Create `src/app/layout.tsx` with root layout
- [ ] Create navigation component in `src/components/nav/Navigation.tsx`
- [ ] Add navigation links (Class Overview, Students)
- [ ] Add navigation to root layout
- [ ] Style navigation with Tailwind CSS

### 1.6 Set Up API Client Utilities
- [ ] Create `src/lib/api.ts` for API client
- [ ] Configure axios instance with base URL from environment variable
- [ ] Add error handling utilities
- [ ] Create `src/lib/types.ts` for TypeScript types/interfaces
- [ ] Add `.env.example` with `NEXT_PUBLIC_API_URL` variable
- [ ] Document API client usage

**Acceptance Criteria:**
- ✅ Next.js project initialized with TypeScript
- ✅ All dependencies installed
- ✅ Tailwind CSS configured and working
- ✅ shadcn/ui components accessible
- ✅ Basic layout with navigation displays correctly
- ✅ API client utilities set up
- ✅ Application runs without errors

