## 1. Backend Setup

### 1.1 Initialize FastAPI Project
- [ ] Navigate to `backend/` directory
- [ ] Create `requirements.txt` file
- [ ] Create `backend/app/` directory structure
- [ ] Create `backend/app/main.py` as entry point

### 1.2 Install Dependencies
- [ ] Add FastAPI to `requirements.txt`
- [ ] Add SQLAlchemy to `requirements.txt`
- [ ] Add psycopg2-binary (PostgreSQL driver) to `requirements.txt`
- [ ] Add python-dotenv to `requirements.txt`
- [ ] Add openai to `requirements.txt`
- [ ] Add spacy to `requirements.txt`
- [ ] Add textstat (for reading level calculation) to `requirements.txt`
- [ ] Add requests to `requirements.txt`
- [ ] Run `pip install -r requirements.txt` to install all dependencies

### 1.3 Download spaCy Model
- [ ] Run `python -m spacy download en_core_web_sm` to download English model
- [ ] Verify model is installed correctly

### 1.4 Environment Configuration
- [ ] Create `.env.example` file in `backend/` directory
- [ ] Add `DATABASE_URL=postgresql://user:password@localhost:5432/vocab_engine` to `.env.example`
- [ ] Add `OPENAI_API_KEY=your_key_here` to `.env.example`
- [ ] Create `.env` file (for local development, not committed to Git)
- [ ] Document environment variables in README

### 1.5 Basic FastAPI Application
- [ ] Create `backend/app/main.py` with FastAPI app instance
- [ ] Add health check endpoint: `GET /health` or `GET /`
- [ ] Add CORS middleware configuration (for frontend integration)
- [ ] Add basic error handling
- [ ] Test that FastAPI app runs: `uvicorn app.main:app --reload`
- [ ] Verify health check endpoint responds correctly

**Acceptance Criteria:**
- ✅ All dependencies installed and working
- ✅ spaCy English model downloaded
- ✅ `.env.example` created with required variables
- ✅ FastAPI app runs with health check endpoint
- ✅ Application structure follows conventions

