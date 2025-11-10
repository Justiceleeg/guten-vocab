## 1. Frontend Setup

### 1.1 Initialize Next.js Project
- [x] Navigate to `frontend/` directory
- [x] Run `npx create-next-app@latest . --typescript --tailwind --app --no-src-dir` (or adjust for src/ structure)
- [x] Verify TypeScript configuration is set up correctly - tsconfig.json configured with strict mode
- [x] Verify Next.js app runs: `pnpm dev` - Build successful, app compiles without errors

### 1.2 Install Dependencies
- [x] Install tailwindcss (if not included in create-next-app) - Tailwind CSS v4 installed
- [x] Install axios: `pnpm add axios` - Installed v1.13.2
- [x] Install recharts: `pnpm add recharts` - Installed v3.4.1
- [x] Verify all dependencies in `package.json` - All dependencies verified

### 1.3 Configure Tailwind CSS
- [x] Verify Tailwind CSS v4 is installed (uses CSS-based configuration, no config file needed)
- [x] Configure content paths in `app/globals.css` (v4 uses @import and @theme directives)
- [x] Add any custom theme configurations if needed (in globals.css) - Theme configured with @theme inline
- [x] Verify Tailwind CSS is working in a test component - Tailwind classes working in page.tsx

### 1.4 Set Up shadcn/ui Component Library
- [x] Initialize shadcn/ui: `npx shadcn-ui@latest init`
- [x] Configure shadcn/ui (choose TypeScript, Tailwind, etc.)
- [x] Install base components as needed (Card, Button, Table, etc.) - Installed button, card, table components
- [x] Verify components are accessible in `components/ui/` - Components verified in components/ui/

### 1.5 Create Basic Layout
- [x] Create `app/layout.tsx` with root layout (or update existing) - Updated with Navigation component and metadata
- [x] Create navigation component in `components/nav/Navigation.tsx` - Created with active link highlighting
- [x] Add navigation links (Class Overview, Students) - Links added to /class and /students
- [x] Add navigation to root layout - Navigation component added to layout
- [x] Style navigation with Tailwind CSS - Styled with Tailwind classes and shadcn/ui theme

### 1.6 Set Up API Client Utilities
- [x] Create `lib/api.ts` for API client - Created with axios instance and interceptors
- [x] Configure axios instance with base URL from environment variable - Uses NEXT_PUBLIC_API_URL with fallback
- [x] Add error handling utilities - Response interceptor with error handling for common status codes
- [x] Create `lib/types.ts` for TypeScript types/interfaces - Created with HealthResponse, Student, VocabularyWord, Book types
- [x] Add `.env.example` with `NEXT_PUBLIC_API_URL` variable - Created with example configuration
- [x] Document API client usage - Inline documentation in api.ts with usage examples

**Acceptance Criteria:**
- ✅ Next.js project initialized with TypeScript
- ✅ All dependencies installed
- ✅ Tailwind CSS configured and working
- ✅ shadcn/ui components accessible
- ✅ Basic layout with navigation displays correctly
- ✅ API client utilities set up
- ✅ Application runs without errors

