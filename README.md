# Flourish Schools - Personalized Vocabulary Recommendation Engine

An AI-powered system that analyzes middle school student language use (classroom transcripts and essays) to identify vocabulary gaps and generate personalized book recommendations from Project Gutenberg.

## Project Overview

This system helps teachers:
- **Track Student Vocabulary**: Identify which grade-level vocabulary words students use and understand
- **Generate Book Recommendations**: Recommend Project Gutenberg books with optimal vocabulary challenge (~50% known, 50% new)
- **Provide Insights**: Class-wide and individual student insights on vocabulary mastery
- **Detect Misuse**: Identify commonly misused words across the class

## Tech Stack

### Frontend
- **Framework**: Next.js 14 (React 18)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Component Library**: shadcn/ui
- **Data Fetching**: Axios
- **Charts**: Recharts
- **Deployment**: Vercel

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **ORM**: SQLAlchemy
- **Database Driver**: psycopg2-binary
- **Validation**: Pydantic
- **Deployment**: Railway

### Database
- **RDBMS**: PostgreSQL 14+
- **Hosting**: Railway

### AI/NLP
- **LLM**: OpenAI GPT-4 (via API)
- **NLP Library**: spaCy (en_core_web_sm model)
- **Reading Level**: textstat library

## Project Structure

```
/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── models/       # SQLAlchemy models
│   │   ├── api/          # API routes
│   │   ├── services/     # Business logic
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/             # Next.js application
│   ├── app/              # Next.js app router pages
│   ├── components/       # React components
│   ├── lib/              # Utilities (API client, types)
│   ├── package.json
│   └── .env.example
├── scripts/              # Data generation & seeding scripts
│   ├── generate_vocab_lists.py
│   ├── generate_mock_data.py
│   ├── seed_books.py
│   ├── analyze_students.py
│   └── run_all.py
├── data/                 # Static data files
│   ├── vocab/            # Grade-level vocabulary JSON files
│   └── mock/             # Generated mock data
│       ├── classroom_transcript.txt
│       └── student_essays/
├── docs/                 # Documentation
│   ├── ARCHITECTURE.md
│   ├── ALL_TASKS.md
│   └── PRD.md
├── openspec/             # OpenSpec specifications
│   ├── project.md
│   ├── AGENTS.md
│   ├── specs/
│   └── changes/
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.9+ installed
- Node.js 18+ installed
- PostgreSQL 14+ installed (or Docker)
- OpenAI API key with credits
- Git repository initialized

### Setup Instructions

1. **Clone the repository** (if applicable)
   ```bash
   git clone <repository-url>
   cd guten-vocab
   ```

2. **Set up Backend**
   ```bash
   cd backend
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your DATABASE_URL and OPENAI_API_KEY
   ```

   **For Cursor/VS Code users:**
   - The workspace is configured to automatically use the virtual environment
   - Cursor terminals should auto-activate the venv (check for `(venv)` in prompt)
   - If venv doesn't activate automatically, use: `source backend/activate.sh`
   - Or manually activate: `source backend/venv/bin/activate`

3. **Set up Frontend**
   ```bash
   cd frontend
   pnpm install
   cp .env.example .env.local
   # Edit .env.local with your NEXT_PUBLIC_API_URL
   ```

4. **Set up Database**
   ```bash
   # Create PostgreSQL database
   createdb vocab_engine
   # Or use Docker
   docker run --name vocab-db -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:14
   ```

5. **Run Development Servers**
   ```bash
   # Backend (in backend/ directory)
   uvicorn app.main:app --reload

   # Frontend (in frontend/ directory)
   pnpm dev
   ```

## Environment Variables

### Backend Environment Variables

Create a `.env` file in the `backend/` directory (copy from `backend/.env.example`):

```bash
cp backend/.env.example backend/.env
```

**Required Variables:**

- **`DATABASE_URL`** (required)
  - PostgreSQL connection string
  - Format: `postgresql://username:password@host:port/database_name`
  - Example: `postgresql://postgres:password@localhost:5432/vocab_engine`
  - Used for: Database connection in FastAPI application

- **`OPENAI_API_KEY`** (required)
  - OpenAI API key for GPT-4 access
  - Get from: https://platform.openai.com/api-keys
  - Used for: Generating mock student data and analyzing vocabulary usage correctness
  - Note: Only used during offline data generation, not at runtime

**Example `.env` file:**
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/vocab_engine
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Frontend Environment Variables

Create a `.env.local` file in the `frontend/` directory:

**Required Variables:**

- **`NEXT_PUBLIC_API_URL`** (required)
  - Backend API URL
  - Format: `http://localhost:8000` (local) or `https://your-backend.railway.app` (production)
  - Used for: API client to connect to FastAPI backend
  - Note: `NEXT_PUBLIC_` prefix makes it available in the browser

**Example `.env.local` file:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Security Notes

- **Never commit `.env` or `.env.local` files** - they are in `.gitignore`
- Use `.env.example` files as templates
- For production, set environment variables in your deployment platform (Railway, Vercel)
- Keep API keys secure and rotate them regularly

## Key Constraints

- **Scale**: MVP designed for 1 classroom, 20-25 students (architecture supports 1000+)
- **Data**: Mock data only (no real student data)
- **Auth**: None (demo application - no authentication required)
- **Processing**: Batch/overnight (not real-time) - all analysis done before deployment

## Documentation

- [Architecture Documentation](docs/ARCHITECTURE.md) - System architecture and technical decisions
- [Task List](docs/ALL_TASKS.md) - Complete implementation task breakdown
- [Product Requirements](docs/PRD.md) - Product requirements and specifications

## Development

This project uses OpenSpec for spec-driven development. See `openspec/AGENTS.md` for instructions on creating and managing change proposals.

## License

[Add license information]

## Contributing

[Add contributing guidelines]

