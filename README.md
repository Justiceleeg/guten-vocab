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

## Architecture

For detailed architecture documentation, see [ARCHITECTURE.md](docs/ARCHITECTURE.md).

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Vercel)                         │
│                  Next.js + React + TypeScript                │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │ Class View   │  │ Student List │  │ Student Detail  │ │
│  └──────────────┘  └──────────────┘  └─────────────────┘ │
└───────────────────────────────┬──────────────────────────────┘
                                │ HTTPS
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend (Railway)                         │
│                    FastAPI + Python                         │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Endpoints                                       │  │
│  │  - GET /api/students                                 │  │
│  │  - GET /api/students/{id}                          │  │
│  │  - GET /api/class/stats                             │  │
│  │  - GET /api/class/recommendations                   │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────────┬──────────────────────────────┘
                                │ PostgreSQL
                                ▼
┌─────────────────────────────────────────────────────────────┐
│              Database (Railway PostgreSQL)                   │
│                                                              │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ students │  │ vocabulary_  │  │    books     │        │
│  │          │  │    words     │  │              │        │
│  └──────────┘  └──────────────┘  └──────────────┘        │
│  ┌──────────────────┐  ┌──────────────────────────────┐  │
│  │ student_vocab    │  │ student_recommendations       │  │
│  └──────────────────┘  └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

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
│   ├── railway.json      # Railway deployment config
│   └── .env.example
├── frontend/             # Next.js application
│   ├── app/              # Next.js app router pages
│   ├── components/       # React components
│   ├── lib/              # Utilities (API client, types)
│   ├── package.json
│   └── .env.example
├── scripts/              # Data generation & seeding scripts
│   ├── seed_vocabulary.py
│   ├── seed_books.py
│   ├── analyze_students.py
│   ├── generate_recommendations.py
│   └── run_all.py        # Master script to run all seeds
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

## Deployment Instructions

### Railway (Backend + Database)

1. **Create Railway Account**
   - Sign up at https://railway.app
   - Connect your GitHub account

2. **Deploy PostgreSQL Database**
   - Create a new project in Railway
   - Add a PostgreSQL service
   - Note the connection string from the service variables

3. **Deploy Backend Service**
   - Add a new service to your Railway project
   - Connect to your GitHub repository
   - Configure build settings:
     - Root directory: `backend/`
     - Build command: `pip install -r requirements.txt`
     - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Set environment variables:
     - `DATABASE_URL`: Copy from PostgreSQL service (Railway auto-provides this)
     - `FRONTEND_URL`: Your Vercel domain (e.g., `guten-vocab.vercel.app`)
     - `OPENAI_API_KEY`: (Optional, only needed for seed scripts)

4. **Seed the Database**
   - Update your local `backend/.env` with the Railway `DATABASE_PUBLIC_URL`
   - Run seed scripts locally: `python scripts/run_all.py`
   - This will populate vocabulary words, books, students, and recommendations

### Vercel (Frontend)

1. **Create Vercel Account**
   - Sign up at https://vercel.com
   - Connect your GitHub account

2. **Deploy Frontend**
   - Import your GitHub repository
   - Configure build settings:
     - Root directory: `frontend/`
     - Build command: `pnpm build` (or `npm run build`)
     - Output directory: `.next` (auto-detected)
     - Framework preset: Next.js
   - Set environment variable:
     - `NEXT_PUBLIC_API_URL`: Your Railway backend URL (e.g., `https://backend-production-82d4.up.railway.app`)

3. **Update Backend CORS**
   - The backend automatically configures CORS based on the `FRONTEND_URL` environment variable
   - Ensure `FRONTEND_URL` is set in Railway backend service

### Production URLs

- **Frontend**: `https://guten-vocab.vercel.app`
- **Backend**: `https://backend-production-82d4.up.railway.app`
- **API Docs**: `https://backend-production-82d4.up.railway.app/docs`

## Data Generation Process

The system uses a multi-stage data generation pipeline that runs **offline** before deployment:

### 1. Vocabulary Words (`scripts/seed_vocabulary.py`)
- Loads grade-level vocabulary from JSON files (`data/vocab/`)
- Inserts 525 unique words across grades 5-8 into the database
- Each word includes: word, grade level, definition, part of speech

### 2. Books (`scripts/seed_books.py`)
- Selects 100 books from Project Gutenberg corpus
- Filters by: Children's Literature category, English language, availability
- Extracts vocabulary matches from book text using spaCy NLP
- Creates book-vocabulary associations in the database

### 3. Student Analysis (`scripts/analyze_students.py`)
- Processes mock classroom transcript and student essays
- Uses OpenAI GPT-4 to analyze vocabulary usage:
  - Identifies which vocabulary words students use correctly
  - Detects misused words (e.g., "through" vs "threw")
  - Calculates mastery percentages
- Creates 25 student profiles with vocabulary assessments

### 4. Recommendations (`scripts/generate_recommendations.py`)
- Matches students to books based on vocabulary overlap
- Scoring algorithm:
  - Target: ~50% known vocabulary, ~50% new vocabulary
  - Considers book difficulty and student proficiency
- Generates:
  - 3 personalized recommendations per student (75 total)
  - 2 class-wide recommendations (most beneficial for the class)

### Running the Pipeline

```bash
# From project root
cd backend
source venv/bin/activate
python ../scripts/run_all.py
```

This master script runs all four stages in sequence and provides progress output.

## API Documentation

Interactive API documentation is available at:

- **Swagger UI**: `https://backend-production-82d4.up.railway.app/docs`
- **ReDoc**: `https://backend-production-82d4.up.railway.app/redoc`

### Key Endpoints

- `GET /api/students` - List all students
- `GET /api/students/{id}` - Get student details with recommendations
- `GET /api/class/stats` - Get class-wide statistics
- `GET /api/class/recommendations` - Get class-wide book recommendations
- `GET /api/books` - List all books
- `GET /health` - Health check endpoint

See the interactive docs for request/response schemas and examples.

## Known Limitations

- **Scale**: MVP designed for 1 classroom, 20-25 students (architecture supports 1000+)
- **Data**: Mock data only (no real student data)
- **Authentication**: None (demo application - no authentication required)
- **Processing**: Batch/overnight (not real-time) - all analysis done before deployment
- **Book Selection**: Limited to 100 books from Project Gutenberg corpus
- **Vocabulary Scope**: Focuses on grades 5-8 vocabulary (525 words)
- **NLP Accuracy**: Vocabulary detection relies on exact word matching (no stemming/lemmatization)
- **Recommendations**: Algorithm is rule-based, not ML-trained
- **No User Accounts**: Single teacher view, no multi-user support

## Future Enhancements

- **Real-time Analysis**: Process student work as it's submitted
- **Expanded Vocabulary**: Include more grade levels and subject-specific vocabulary
- **Machine Learning**: Train recommendation model on student reading outcomes
- **User Authentication**: Multi-teacher support with secure login
- **Student Portal**: Allow students to view their own recommendations
- **Reading Progress Tracking**: Track which books students read and vocabulary gains
- **Parent Reports**: Generate reports for parents on student vocabulary progress
- **Integration**: Connect with LMS systems (Google Classroom, Canvas, etc.)
- **Mobile App**: Native mobile app for teachers and students
- **Advanced Analytics**: Predictive analytics for vocabulary acquisition
- **Custom Vocabulary Lists**: Allow teachers to add custom vocabulary words
- **Book Preview**: Show sample pages from recommended books
- **Audiobook Integration**: Link to audiobook versions for accessibility

## Additional Documentation

- [Architecture Documentation](docs/ARCHITECTURE.md) - Detailed system architecture and technical decisions
- [Task List](docs/ALL_TASKS.md) - Complete implementation task breakdown
- [Product Requirements](docs/PRD.md) - Product requirements and specifications
- [Scripts Documentation](scripts/README.md) - Guide to data generation and seeding scripts

## Development

This project uses OpenSpec for spec-driven development. See `openspec/AGENTS.md` for instructions on creating and managing change proposals.

## License

[Add license information]

## Contributing

[Add contributing guidelines]

