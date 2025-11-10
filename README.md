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
│   ├── src/
│   │   ├── app/          # Next.js app router pages
│   │   ├── components/   # React components
│   │   └── lib/          # Utilities (API client, types)
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
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   cp .env.example .env
   # Edit .env with your DATABASE_URL and OPENAI_API_KEY
   ```

3. **Set up Frontend**
   ```bash
   cd frontend
   npm install
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
   npm run dev
   ```

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

