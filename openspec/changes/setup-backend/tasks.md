## 1. Backend Setup

### 1.1 Initialize FastAPI Project
- [x] Navigate to `backend/` directory
- [x] Create `requirements.txt` file
- [x] Create `backend/app/` directory structure
- [x] Create `backend/app/main.py` as entry point

### 1.2 Set Up Virtual Environment
- [x] Create Python virtual environment: `python -m venv venv` (or `python3 -m venv venv`)
- [x] Activate virtual environment:
  - macOS/Linux: `source venv/bin/activate`
  - Windows: `venv\Scripts\activate`
- [x] Verify virtual environment is active (prompt should show `(venv)`)
- [x] Update `.gitignore` to exclude `venv/` directory (already done in project structure)

### 1.3 Install Dependencies
- [x] Add FastAPI to `requirements.txt`
- [x] Add SQLAlchemy to `requirements.txt`
- [x] Add psycopg2-binary (PostgreSQL driver) to `requirements.txt`
- [x] Add python-dotenv to `requirements.txt`
- [x] Add openai to `requirements.txt`
- [x] Add spacy to `requirements.txt`
- [x] Add textstat (for reading level calculation) to `requirements.txt`
- [x] Add requests to `requirements.txt`
- [x] Add uvicorn[standard] to `requirements.txt` (for running FastAPI)
- [x] Run `pip install -r requirements.txt` to install all dependencies (with venv activated)

### 1.4 Download spaCy Model
- [x] Run `python -m spacy download en_core_web_sm` to download English model
- [x] Verify model is installed correctly

### 1.5 Environment Configuration
- [x] Create `.env.example` file in `backend/` directory
- [x] Add `DATABASE_URL=postgresql://user:password@localhost:5432/vocab_engine` to `.env.example`
- [x] Add `OPENAI_API_KEY=your_key_here` to `.env.example`
- [ ] Create `.env` file (for local development, not committed to Git)
- [ ] Document environment variables in README

### 1.6 Basic FastAPI Application
- [x] Create `backend/app/main.py` with FastAPI app instance
- [x] Add health check endpoint: `GET /health` or `GET /`
- [x] Add CORS middleware configuration (for frontend integration)
- [x] Add basic error handling
- [ ] Test that FastAPI app runs: `uvicorn app.main:app --reload`
- [ ] Verify health check endpoint responds correctly

**Acceptance Criteria:**
- ✅ Virtual environment created and activated
- ✅ All dependencies installed and working
- ✅ spaCy English model downloaded
- ✅ `.env.example` created with required variables
- ✅ FastAPI app runs with health check endpoint
- ✅ Application structure follows conventions

