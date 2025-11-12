## 1. Railway Setup - Database
- [x] 1.1 Create Railway account
- [x] 1.2 Create new PostgreSQL database service on Railway
- [x] 1.3 Note database connection string from Railway dashboard
- [x] 1.4 Update backend `.env` with Railway database URL (for local seeding)

## 2. Railway Setup - Backend
- [x] 2.1 Create Railway project for backend service
- [x] 2.2 Configure build settings:
  - Root directory: `backend/`
  - Build command: `pip install -r requirements.txt`
  - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [x] 2.3 Set environment variables in Railway:
  - `DATABASE_URL` (from Railway PostgreSQL service)
  - `OPENAI_API_KEY` (for future use, though not needed at runtime)
  - `FRONTEND_URL` (set to `guten-vocab.vercel.app` for CORS)
- [x] 2.4 Connect Railway project to GitHub repository
- [x] 2.5 Deploy backend and verify health endpoint works
  - Backend URL: `https://backend-production-82d4.up.railway.app`
  - Health endpoint verified

## 3. Seed Railway Database
- [x] 3.1 Update local `.env` with Railway DATABASE_URL
- [x] 3.2 Run seed scripts: `python scripts/run_all.py`
- [x] 3.3 Verify data in Railway PostgreSQL dashboard:
  - Check vocabulary_words count (should be 525) ✅
  - Check books count (should be 100) ✅
  - Check students count (should be 25) ✅
  - Check student_recommendations count (should be 75) ✅
  - Check class_recommendations count (should be 2) ✅
- [x] 3.4 Alternative: Export local database and import to Railway (if direct seeding fails) - Not needed, direct seeding succeeded

## 4. Vercel Setup - Frontend
- [x] 4.1 Create Vercel account
- [x] 4.2 Connect GitHub repository to Vercel
- [x] 4.3 Configure build settings:
  - Root directory: `frontend/`
  - Build command: `pnpm build`
  - Output directory: `.next`
  - Framework preset: Next.js
- [x] 4.4 Set environment variable in Vercel:
  - `NEXT_PUBLIC_API_URL` (Railway backend URL) ✅ Set to `https://backend-production-82d4.up.railway.app`
- [x] 4.5 Deploy frontend and verify it loads
  - Frontend URL: `https://guten-vocab.vercel.app`
  - Fixed missing `frontend/lib/utils.ts` file (was ignored by `.gitignore`)

## 5. Integration Testing
- [x] 5.1 Test deployed frontend → backend connection ✅ Verified working
- [x] 5.2 Verify all pages load correctly:
  - `/` (home/class overview) ✅
  - `/students` (student list) ✅
  - `/students/[id]` (student detail) ✅
  - `/class` (class overview) ✅
- [x] 5.3 Test API calls are working:
  - `GET /api/students` ✅
  - `GET /api/students/[id]` ✅
  - `GET /api/class/stats` ✅
  - `GET /api/class/recommendations` ✅
- [x] 5.4 Verify data displays correctly:
  - Student list shows all 25 students ✅
  - Student detail pages show vocabulary mastery, recommendations, misused words ✅
  - Class view shows statistics, recommendations, vocabulary gaps, common mistakes ✅
- [x] 5.5 Test on different devices/browsers (desktop, tablet, mobile) ✅ Verified deployment looks good

## 6. Documentation - README
- [x] 6.1 Enhance README.md with:
  - Project overview and goals ✅
  - Tech stack description ✅
  - Architecture diagram (text/ASCII or reference to ARCHITECTURE.md) ✅
  - Comprehensive setup instructions:
    - Prerequisites (Node, Python, PostgreSQL) ✅
    - Installation steps ✅
    - Environment variables (with examples) ✅
    - Database setup ✅
    - Running locally ✅
  - Deployment instructions (Railway + Vercel) ✅
  - Data generation process explanation ✅
  - API documentation (link to FastAPI /docs) ✅
  - Known limitations ✅
  - Future enhancements ✅

## 7. Documentation - Scripts
- [x] 7.1 Create `scripts/README.md` with:
  - Purpose of each script ✅
  - Order of execution (dependencies) ✅
  - Prerequisites and dependencies ✅
  - Expected outputs ✅
  - Troubleshooting common issues ✅
  - Examples of running each script ✅

## 8. Code Cleanup
- [x] 8.1 Remove unused code/files ✅ No unused code found - all files are used
- [x] 8.2 Add comments to complex logic (especially in services and algorithms) ✅ Code is well-documented with docstrings and comments
- [x] 8.3 Ensure consistent code formatting (run formatters if available) ✅ Code is consistently formatted (no formatters configured, but style is consistent)
- [x] 8.4 Verify no hardcoded values (use environment variables) ✅ All hardcoded values are development defaults with proper fallbacks; production uses environment variables
- [x] 8.5 Verify .gitignore files are complete:
  - Root `.gitignore` (Python, Node, env files, etc.) ✅
  - `frontend/.gitignore` (Next.js defaults) ✅
  - Ensure sensitive files are ignored ✅
  - Fixed: Added exception `!frontend/lib/` to `.gitignore` to allow frontend utilities

## 9. Demo Materials (Optional)
- [ ] 9.1 Take screenshots of key features:
  - Class overview page
  - Student detail view with book recommendations
  - Vocabulary gaps and common mistakes sections
- [ ] 9.2 Record short demo video showing:
  - Navigation through app
  - Key insights (vocabulary gaps, recommendations)
  - Highlighting "through" misuse feature
  - Book detail modals and word detail modals

