# Project Context

## Purpose
Flourish Schools - Personalized Vocabulary Recommendation Engine

An AI-powered system that analyzes middle school student language use (classroom transcripts and essays) to:
- Identify vocabulary gaps per student
- Generate personalized book recommendations from Project Gutenberg
- Provide teachers with actionable insights on student vocabulary mastery
- Detect commonly misused words across the class

**Key Features:**
- Student Vocabulary Profiling: Track which grade-level vocabulary words students use and understand
- Intelligent Book Matching: Recommend books with optimal vocabulary challenge (~50% known, 50% new)
- Teacher Dashboard: Class-wide and individual student insights
- Misuse Detection: Identify commonly misused words (e.g., "through" vs "thorough")

**Target Users:** Middle school teachers (7th grade classroom, 20-25 students)

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

### Data Sources
- **Vocabulary Lists**: Vocabulary.com (525 words, grades 5-8)
- **Books**: Project Gutenberg via pgcorpus/gutenberg
  - Pre-computed word counts
  - Metadata (title, author, etc.)

### Development Tools
- **Version Control**: Git
- **Package Management**: 
  - Python: pip (requirements.txt)
  - Node: npm (package.json)
- **Environment Variables**: python-dotenv

## Project Conventions

### Code Style

**Python (Backend):**
- Follow PEP 8 style guide
- Use type hints for function parameters and return types
- Use Pydantic models for data validation
- SQLAlchemy models for database entities
- Async/await for I/O operations where appropriate

**TypeScript (Frontend):**
- Use TypeScript strict mode
- Define types/interfaces for all API responses
- Use functional components with hooks
- Prefer named exports over default exports
- Use shadcn/ui components for UI primitives

**Naming Conventions:**
- Files: kebab-case (e.g., `student-service.py`, `student-table.tsx`)
- Classes: PascalCase (e.g., `StudentService`, `StudentTable`)
- Functions/variables: snake_case (Python), camelCase (TypeScript)
- Constants: UPPER_SNAKE_CASE
- Database tables: snake_case (e.g., `student_vocabulary`)

### Architecture Patterns

**Backend Structure:**
```
backend/app/
├── models/          # SQLAlchemy models (database entities)
├── schemas/         # Pydantic schemas (API request/response)
├── api/             # FastAPI route handlers
├── services/        # Business logic layer
└── main.py          # FastAPI app entry point
```

**Frontend Structure:**
```
frontend/src/
├── app/             # Next.js app router pages
├── components/      # React components
│   ├── ui/          # shadcn/ui base components
│   ├── class/       # Class view components
│   └── students/     # Student view components
└── lib/             # Utilities (API client, types)
```

**Key Patterns:**
- **Separation of Concerns**: API routes delegate to services, services use models
- **Data Validation**: Pydantic schemas for all API boundaries
- **Error Handling**: Standard HTTP status codes, JSON error responses
- **Database**: SQLAlchemy ORM with explicit relationships
- **API Design**: RESTful endpoints, JSON request/response bodies

### Testing Strategy

**Current State (MVP/Demo):**
- Manual testing during development
- No automated tests yet (future enhancement)

**Future Testing Approach:**
- **Unit Tests**: pytest for backend services, Jest + React Testing Library for frontend components
- **Integration Tests**: API integration tests (full request/response cycle)
- **End-to-End Tests**: Playwright or Cypress for user flows
- **Data Quality Tests**: Validate mock data generation and recommendation algorithm correctness

### Git Workflow

**Branching Strategy:**
- `main` branch: Production-ready code
- Feature branches: `feature/description` for new features
- Use descriptive commit messages

**Commit Conventions:**
- Use present tense, imperative mood: "Add student detail endpoint"
- Prefix with scope when helpful: "backend: Add student service", "frontend: Fix table styling"
- Reference issues/PRs when applicable

## Domain Context

### Educational Context
- **Target Grade**: 7th grade (middle school)
- **Class Size**: 20-25 students
- **Vocabulary Focus**: Grade-level appropriate vocabulary (5th-8th grade words)
- **Reading Levels**: Students range from 5.0 to 8.0 (Flesch-Kincaid grade level)

### Vocabulary Analysis
- **Master Vocabulary List**: 525 words across grades 5-8
- **Vocabulary Mastery**: Based on correct usage in context (not just word recognition)
- **Optimal Challenge**: Books should have ~50% known vocabulary, ~50% new vocabulary
- **Common Misuses**: System detects when words are used incorrectly (e.g., "through" instead of "thorough")

### Book Recommendations
- **Source**: Project Gutenberg (public domain books)
- **Selection Criteria**: 
  - Children's literature or children's fiction
  - Reading level 5.0-9.0
  - Top 100 by popularity
- **Matching Algorithm**: Considers vocabulary overlap, reading level, and optimal challenge ratio

### Data Processing Pipeline
1. **Offline Processing** (before deployment):
   - Generate mock student data (transcripts, essays)
   - Analyze student vocabulary usage with spaCy + OpenAI
   - Generate book recommendations
   - Seed database with all processed data
2. **Runtime** (after deployment):
   - Read-only API serving pre-computed data
   - No real-time analysis or data generation

## Important Constraints

### Technical Constraints
- **Scale**: MVP designed for 1 classroom, 20-25 students (architecture supports 1000+)
- **Data**: Mock data only (no real student data)
- **Auth**: None (demo application - no authentication required)
- **Processing**: Batch/overnight (not real-time) - all analysis done before deployment
- **Database**: Pre-seeded with all student profiles and recommendations

### Business Constraints
- **MVP/Demo**: Focus on core functionality, polish for demonstration
- **No Real Student Data**: All data is generated/mock to avoid privacy concerns
- **Single Classroom**: Designed for one teacher, one class (can scale later)

### Performance Constraints
- **API Response Time**: Should be fast (<500ms) since data is pre-computed
- **Database Queries**: Optimized with indexes on frequently queried fields
- **Frontend**: Should load quickly, use Next.js optimizations

### Security Constraints (Current MVP)
- No authentication (intentional for demo)
- No real student data (mock only)
- Read-only API (no writes from frontend)
- HTTPS via Vercel/Railway

## External Dependencies

### APIs
- **OpenAI API (GPT-4)**: 
  - Used for generating mock student data (transcripts, essays)
  - Used for analyzing vocabulary usage correctness
  - API key stored in backend environment variables
  - Called during offline data generation only (not at runtime)

### Data Sources
- **pgcorpus/gutenberg**: 
  - Pre-computed word counts for Project Gutenberg books
  - Metadata CSV with book information
  - Used during book seeding process
  - Repository: https://github.com/pgcorpus/gutenberg

- **Vocabulary.com**: 
  - Vocabulary word lists for grades 5-8
  - 525 words total
  - Stored as JSON files in `/data/vocab/`

### Deployment Platforms
- **Vercel**: 
  - Frontend hosting and deployment
  - Automatic deployments from GitHub
  - Environment variable: `NEXT_PUBLIC_API_URL`

- **Railway**: 
  - Backend API hosting
  - PostgreSQL database hosting
  - Environment variables: `DATABASE_URL`, `OPENAI_API_KEY`
  - Automatic deployments from GitHub

### Python Libraries
- **spaCy**: NLP processing for lemmatization and text analysis
- **textstat**: Reading level calculation (Flesch-Kincaid)
- **openai**: OpenAI API client
- **SQLAlchemy**: ORM for database operations
- **FastAPI**: Web framework
- **Pydantic**: Data validation

### Node.js Libraries
- **Next.js**: React framework with SSR
- **React**: UI library
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Component library built on Radix UI
- **Axios**: HTTP client
- **Recharts**: Charting library
