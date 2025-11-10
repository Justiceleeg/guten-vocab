# Architecture Documentation
## Flourish Schools - Personalized Vocabulary Recommendation Engine

---

## Table of Contents
1. [System Overview](#system-overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Technology Stack](#technology-stack)
4. [Data Flow](#data-flow)
5. [Database Schema](#database-schema)
6. [API Design](#api-design)
7. [Component Architecture](#component-architecture)
8. [Deployment Architecture](#deployment-architecture)
9. [Key Technical Decisions](#key-technical-decisions)
10. [Security Considerations](#security-considerations)

---

## System Overview

### Purpose
An AI-powered system that analyzes middle school student language use (classroom transcripts and essays) to:
- Identify vocabulary gaps
- Generate personalized book recommendations
- Provide teachers with actionable insights

### Key Features
- **Student Vocabulary Profiling**: Track which grade-level vocabulary words students use and understand
- **Intelligent Book Matching**: Recommend Project Gutenberg books with optimal vocabulary challenge (~50% known, 50% new)
- **Teacher Dashboard**: Class-wide and individual student insights
- **Misuse Detection**: Identify commonly misused words

### Constraints
- **Scale**: 1 classroom, 20-25 students (MVP/demo)
- **Data**: Mock data only (no real student data)
- **Auth**: None (demo application)
- **Processing**: Batch/overnight (not real-time)

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Teacher (User)                          │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js/React)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ Class View   │  │ Student List │  │ Student Detail     │   │
│  │ - Stats      │  │ - Table      │  │ - Recommendations  │   │
│  │ - Top Books  │  │ - Filter     │  │ - Vocab Progress   │   │
│  │ - Vocab Gaps │  │              │  │ - Misused Words    │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
└───────────────────────────────┬─────────────────────────────────┘
                                │ HTTP/REST
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     API Endpoints                         │  │
│  │  - GET /api/students                                     │  │
│  │  - GET /api/students/{id}                                │  │
│  │  - GET /api/class/stats                                  │  │
│  │  - GET /api/class/recommendations                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Business Logic                          │  │
│  │  - Student queries                                        │  │
│  │  - Aggregation logic                                      │  │
│  │  - Data formatting                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────┘
                                │ SQL
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Database (PostgreSQL)                         │
│  ┌────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│  │  students  │  │ vocabulary_words │  │     books        │   │
│  └────────────┘  └──────────────────┘  └──────────────────┘   │
│  ┌────────────────────┐  ┌──────────────────────────────────┐ │
│  │ student_vocabulary │  │    book_vocabulary                │ │
│  └────────────────────┘  └──────────────────────────────────┘ │
│  ┌────────────────────────┐  ┌──────────────────────────────┐ │
│  │ student_recommendations│  │  class_recommendations       │ │
│  └────────────────────────┘  └──────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    Offline Processing Pipeline                   │
│                     (Run before deployment)                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  1. Generate Mock Data (OpenAI GPT-4)                    │  │
│  │     - Classroom transcript (40k words)                    │  │
│  │     - Student essays (25 × 300 words)                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  2. Seed Vocabulary & Books                               │  │
│  │     - Load 525 vocab words (grades 5-8)                  │  │
│  │     - Process 100 Gutenberg books (pgcorpus)             │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  3. Analyze Students (OpenAI + spaCy)                    │  │
│  │     - Parse transcripts/essays                            │  │
│  │     - Extract vocabulary usage                            │  │
│  │     - Check correctness with OpenAI                       │  │
│  │     - Build vocabulary profiles                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  4. Generate Recommendations                              │  │
│  │     - Match students to books                             │  │
│  │     - Calculate match scores                              │  │
│  │     - Store top 3 per student + class-wide top 2         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

External Dependencies:
┌──────────────┐  ┌───────────────────┐  ┌─────────────────────┐
│  OpenAI API  │  │ pgcorpus/gutenberg│  │ Project Gutenberg   │
│  (GPT-4)     │  │ (pre-computed     │  │ (book source)       │
│              │  │  word counts)     │  │                     │
└──────────────┘  └───────────────────┘  └─────────────────────┘
```

---

## Technology Stack

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

---

## Data Flow

### 1. Data Preparation Flow (Offline)

```
┌─────────────────┐
│ Vocab JSON Files│
│ (5th-8th grade) │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ seed_vocabulary.py      │
│ - Load vocab words      │
│ - Lemmatize with spaCy  │
│ - Insert into DB        │
└────────┬────────────────┘
         │
         ▼
┌───────────────────────────────────────┐
│ vocabulary_words table (525 records)  │
└───────────────────────────────────────┘

┌──────────────────────┐
│ pgcorpus/gutenberg   │
│ - metadata.csv       │
│ - counts/ folder     │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────────┐
│ seed_books.py            │
│ - Filter to children's   │
│ - Calculate reading level│
│ - Extract vocab counts   │
│ - Top 100 by popularity  │
└────────┬─────────────────┘
         │
         ▼
┌────────────────────────────────┐
│ books + book_vocabulary tables │
│ (100 books, ~10k-50k word refs)│
└────────────────────────────────┘

┌─────────────────┐
│ OpenAI GPT-4    │
│ (LLM)           │
└────────┬────────┘
         │
         ▼
┌───────────────────────────┐
│ generate_mock_data.py     │
│ - Generate transcript     │
│ - Generate 25 essays      │
│ - Save to /data/mock/     │
└────────┬──────────────────┘
         │
         ▼
┌────────────────────────────┐
│ Mock Data Files            │
│ - classroom_transcript.txt │
│ - student_essays/*.json    │
└────────┬───────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ analyze_students.py             │
│ 1. Parse transcript/essays      │
│ 2. Extract words (spaCy)        │
│ 3. Count vocab usage            │
│ 4. Check correctness (OpenAI)   │
│ 5. Build student profiles       │
└────────┬────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│ students + student_vocabulary    │
│ (25 students, thousands of refs) │
└────────┬─────────────────────────┘
         │
         ▼
┌───────────────────────────────────┐
│ generate_recommendations.py       │
│ 1. Calculate vocab overlap        │
│ 2. Score book matches             │
│ 3. Select top 3 per student       │
│ 4. Aggregate class-wide top 2     │
└────────┬──────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│ student_recommendations +              │
│ class_recommendations                  │
│ (75 individual + 2 class-wide recs)    │
└────────────────────────────────────────┘
```

### 2. Runtime Request Flow

```
┌─────────┐
│ Teacher │
└────┬────┘
     │ Opens dashboard
     ▼
┌────────────────┐
│ Next.js App    │
│ (Vercel)       │
└────┬───────────┘
     │ HTTP GET /api/class/stats
     ▼
┌─────────────────┐
│ FastAPI Backend │
│ (Railway)       │
└────┬────────────┘
     │ SQL Query
     ▼
┌──────────────────┐
│ PostgreSQL       │
│ (Railway)        │
└────┬─────────────┘
     │ Return data
     ▼
┌─────────────────┐
│ FastAPI Backend │
│ - Format JSON   │
└────┬────────────┘
     │ JSON Response
     ▼
┌────────────────┐
│ Next.js App    │
│ - Render UI    │
└────┬───────────┘
     │ Display to teacher
     ▼
┌─────────┐
│ Teacher │
│ Views   │
└─────────┘
```

### 3. Student Analysis Flow (Detail)

```
┌──────────────────────┐
│ Raw Student Text     │
│ (transcript + essay) │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────┐
│ spaCy Processing             │
│ 1. Tokenize                  │
│ 2. Lemmatize (root forms)    │
│ 3. Filter (alpha only)       │
│ 4. Lowercase                 │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Word Frequency Count         │
│ {word: count} for vocab only │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ For each word used:                  │
│                                       │
│ Extract example sentences → OpenAI   │
│                                       │
│ Prompt: "Is '[word]' used correctly  │
│          in these contexts?"          │
│                                       │
│ Response: {correct_count,             │
│            incorrect_count,           │
│            misuse_examples}           │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│ Student Vocabulary Profile       │
│ - Words used (counts)            │
│ - Correct vs incorrect usage     │
│ - Example misuses                │
│ - Mastery percentage             │
│ - Missing words                  │
└──────────────────────────────────┘
```

---

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────────────┐
│       students          │
├─────────────────────────┤
│ id (PK)                 │
│ name                    │
│ actual_reading_level    │
│ assigned_grade          │
│ created_at              │
└────────┬────────────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────────────────────┐
│    student_vocabulary           │
├─────────────────────────────────┤
│ id (PK)                         │
│ student_id (FK) ────────────────┤
│ word_id (FK)                    │───┐
│ usage_count                     │   │
│ correct_usage_count             │   │
│ misuse_examples[]               │   │
│ last_analyzed_at                │   │
└─────────────────────────────────┘   │
                                      │ N:1
                                      │
                                      ▼
                            ┌──────────────────────┐
                            │  vocabulary_words    │
                            ├──────────────────────┤
                            │ id (PK)              │
                            │ word                 │
                            │ grade_level          │
                            │ created_at           │
                            └──────────┬───────────┘
                                       │
                                       │ 1:N
                                       │
                                       ▼
                            ┌──────────────────────┐
                            │  book_vocabulary     │
                            ├──────────────────────┤
                            │ id (PK)              │
                            │ book_id (FK) ────────┤
                            │ word_id (FK)         │   │
                            │ occurrence_count     │   │
                            └──────────────────────┘   │
                                                       │ N:1
                                                       │
                                                       ▼
                                            ┌─────────────────┐
                                            │     books       │
                                            ├─────────────────┤
                                            │ id (PK)         │
                                            │ title           │
                                            │ author          │
                                            │ gutenberg_id    │
                                            │ reading_level   │
                                            │ total_words     │
                                            │ created_at      │
                                            └────────┬────────┘
                                                     │
                                                     │ 1:N
                                                     │
         ┌───────────────────────────────────────────┼────────────────────┐
         │                                           │                    │
         ▼                                           ▼                    ▼
┌──────────────────────────┐           ┌──────────────────────────┐     │
│ student_recommendations  │           │  class_recommendations   │     │
├──────────────────────────┤           ├──────────────────────────┤     │
│ id (PK)                  │           │ id (PK)                  │     │
│ student_id (FK)          │           │ book_id (FK) ────────────┤─────┘
│ book_id (FK) ────────────┤───────────│ match_score              │
│ match_score              │           │ students_recommended_cnt │
│ known_words_percent      │           │ created_at               │
│ new_words_count          │           └──────────────────────────┘
│ created_at               │
└──────────────────────────┘
```

### Key Relationships
- **Students ↔ Vocabulary**: Many-to-many via `student_vocabulary`
- **Books ↔ Vocabulary**: Many-to-many via `book_vocabulary`
- **Students ↔ Books**: Many-to-many via `student_recommendations`
- **Class ↔ Books**: Many-to-many via `class_recommendations`

### Indexes
- `vocabulary_words.word` (frequent lookups)
- `student_vocabulary.student_id` (student queries)
- `book_vocabulary.book_id` (book queries)
- `student_recommendations.student_id` (recommendation lookups)
- `books.reading_level` (filtering by level)

---

## API Design

### REST API Endpoints

#### 1. Students

**List Students**
```
GET /api/students
Response: 200 OK
[
  {
    "id": 1,
    "name": "Sarah Johnson",
    "reading_level": 7.2,
    "assigned_grade": 7,
    "vocab_mastery_percent": 68.5
  },
  ...
]
```

**Get Student Detail**
```
GET /api/students/{id}
Response: 200 OK
{
  "id": 1,
  "name": "Sarah Johnson",
  "reading_level": 7.2,
  "assigned_grade": 7,
  "vocab_mastery": {
    "total_grade_level_words": 125,
    "words_mastered": 86,
    "mastery_percent": 68.8
  },
  "missing_words": ["abolish", "coherent", ...],
  "misused_words": [
    {
      "word": "through",
      "correct_count": 2,
      "incorrect_count": 3,
      "example": "I did a through analysis..."
    }
  ],
  "book_recommendations": [
    {
      "book_id": 12,
      "title": "Treasure Island",
      "author": "Robert Louis Stevenson",
      "reading_level": 7.5,
      "match_score": 0.82,
      "known_words_percent": 52.0,
      "new_words_count": 18
    }
  ]
}
```

#### 2. Class Statistics

**Get Class Overview**
```
GET /api/class/stats
Response: 200 OK
{
  "total_students": 25,
  "avg_vocab_mastery_percent": 64.2,
  "reading_level_distribution": {
    "5": 2,
    "6": 6,
    "7": 13,
    "8": 4
  },
  "top_missing_words": [
    {"word": "abolish", "students_missing": 18},
    {"word": "coherent", "students_missing": 16},
    ...
  ],
  "commonly_misused_words": [
    {"word": "through", "misuse_count": 47},
    ...
  ]
}
```

**Get Class Book Recommendations**
```
GET /api/class/recommendations
Response: 200 OK
[
  {
    "book_id": 15,
    "title": "Anne of Green Gables",
    "author": "L. M. Montgomery",
    "reading_level": 6.8,
    "students_recommended_count": 18,
    "avg_match_score": 0.76
  },
  ...
]
```

#### 3. Books (Optional)

**List Books**
```
GET /api/books?reading_level_min=6&reading_level_max=8
Response: 200 OK
[
  {
    "id": 1,
    "title": "Treasure Island",
    "author": "Robert Louis Stevenson",
    "gutenberg_id": 120,
    "reading_level": 7.5,
    "total_words": 67000
  },
  ...
]
```

### Error Responses

```
404 Not Found
{
  "detail": "Student not found"
}

500 Internal Server Error
{
  "detail": "Database connection error"
}
```

### API Conventions
- RESTful design
- JSON request/response bodies
- Standard HTTP status codes
- CORS enabled for frontend origin
- No authentication (demo app)

---

## Component Architecture

### Frontend Component Structure

```
src/
├── app/
│   ├── layout.tsx              # Root layout with nav
│   ├── page.tsx                # Home (redirects to /class)
│   ├── class/
│   │   └── page.tsx            # Class overview
│   └── students/
│       ├── page.tsx            # Student list
│       └── [id]/
│           └── page.tsx        # Student detail
├── components/
│   ├── nav/
│   │   └── Navigation.tsx      # Top nav bar
│   ├── class/
│   │   ├── ClassStats.tsx      # Stats cards
│   │   ├── BookRecommendations.tsx
│   │   ├── VocabGaps.tsx       # Top missing words
│   │   └── CommonMistakes.tsx  # Misused words
│   ├── students/
│   │   ├── StudentTable.tsx    # List view
│   │   ├── StudentCard.tsx     # Individual card
│   │   ├── VocabProgress.tsx   # Progress gauge
│   │   ├── BookRecommendationCard.tsx
│   │   └── MisusedWordsList.tsx
│   └── ui/
│       ├── card.tsx            # shadcn/ui Card component
│       ├── button.tsx          # shadcn/ui Button component
│       ├── table.tsx           # shadcn/ui Table component
│       └── ...                 # Other shadcn/ui components as needed
└── lib/
    ├── api.ts                  # API client (axios)
    └── types.ts                # TypeScript types
```

**Note**: The `components/ui/` directory contains shadcn/ui components (Card, Button, Table, etc.) which are built on top of Tailwind CSS and Radix UI primitives.

### Backend Module Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app entry
│   ├── config.py               # Configuration
│   ├── database.py             # DB connection
│   ├── models/
│   │   ├── student.py          # SQLAlchemy models
│   │   ├── vocabulary.py
│   │   ├── book.py
│   │   └── recommendation.py
│   ├── schemas/
│   │   ├── student.py          # Pydantic schemas
│   │   ├── vocabulary.py
│   │   └── book.py
│   ├── api/
│   │   ├── students.py         # Student endpoints
│   │   ├── class_stats.py      # Class endpoints
│   │   └── books.py            # Book endpoints
│   └── services/
│       ├── student_service.py  # Business logic
│       ├── class_service.py
│       └── book_service.py
└── requirements.txt
```

---

## Deployment Architecture

### Production Environment

```
┌─────────────────────────────────────────────────────────────┐
│                        Internet                              │
└────────────────┬────────────────┬───────────────────────────┘
                 │                │
                 │                │
         ┌───────▼──────┐  ┌──────▼────────┐
         │   Vercel     │  │   Railway     │
         │  (Frontend)  │  │  (Backend +   │
         │              │  │   Database)   │
         │  - Next.js   │  │               │
         │  - CDN       │  │  - FastAPI    │
         │  - SSL       │  │  - PostgreSQL │
         │              │  │  - SSL        │
         └──────────────┘  └───────────────┘
              │                    │
              │   API Calls        │
              └────────────────────┘
```

### Deployment Steps

1. **Database (Railway)**
   - Create PostgreSQL instance
   - Run seed scripts to populate data
   - Configure backups (optional)

2. **Backend (Railway)**
   - Connect to GitHub repo
   - Set environment variables (DATABASE_URL, OPENAI_API_KEY)
   - Auto-deploy on push to main

3. **Frontend (Vercel)**
   - Connect to GitHub repo
   - Set environment variable (NEXT_PUBLIC_API_URL)
   - Auto-deploy on push to main

### Environment Variables

**Backend (.env)**
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
OPENAI_API_KEY=sk-...
```

**Frontend (.env.local)**
```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

---

## Key Technical Decisions

### 1. Why FastAPI for Backend?
- **Fast**: Async support, high performance
- **Modern**: Type hints, auto-generated docs
- **Pythonic**: Great for data/AI workflows
- **Ecosystem**: Works well with SQLAlchemy, spaCy, OpenAI SDK

### 2. Why Next.js for Frontend?
- **React**: Component-based, widely known
- **Server-Side Rendering**: Better performance
- **Vercel Integration**: Seamless deployment
- **TypeScript**: Type safety for complex data

### 3. Why PostgreSQL?
- **Relational**: Complex relationships between students, vocab, books
- **Robust**: ACID compliance, data integrity
- **Scalable**: Can handle growth beyond MVP
- **Railway Support**: Easy managed hosting

### 4. Why OpenAI API (not local LLM)?
- **Quality**: GPT-4 produces high-quality mock data and analysis
- **Speed**: No model download/setup time
- **Simplicity**: No GPU requirements or model management
- **MVP Appropriate**: Good for demo/proof-of-concept

### 5. Why pgcorpus Pre-computed Counts?
- **Time Saving**: No need to process 100 books from scratch
- **Standardized**: Well-tested preprocessing pipeline
- **Complete**: Metadata + counts already available
- **Trade-off**: No lemmatization, but acceptable for MVP

### 6. Why No Lemmatization for Books?
- **Complexity**: Would require processing full book texts
- **Performance**: Pre-computed counts are instant
- **Good Enough**: String matching works well for most vocab
- **Future Enhancement**: Can add if needed

### 7. Why Pre-seed Database (not Runtime)?
- **Performance**: No wait time for teachers
- **Reliability**: Analysis already complete and verified
- **Cost**: No API calls at runtime (only during setup)
- **Demo**: Shows polished results immediately

### 8. Why No Authentication?
- **Scope**: MVP/demo application
- **Simplicity**: Focus on core functionality
- **Future**: Easy to add JWT or OAuth later

---

## Security Considerations

### Current State (MVP/Demo)
- ✅ No real student data (mock only)
- ✅ No authentication (intentional for demo)
- ✅ Read-only API (no writes from frontend)
- ✅ HTTPS via Vercel/Railway
- ⚠️ OpenAI API key in backend environment only
- ⚠️ Database credentials in environment variables

### Future Production Considerations
1. **Authentication & Authorization**
   - Add teacher login (OAuth, JWT)
   - Role-based access (admin, teacher, student)
   - Session management

2. **Data Privacy**
   - Encrypt sensitive student data
   - FERPA compliance for real student data
   - Data retention policies
   - Audit logs

3. **API Security**
   - Rate limiting
   - Input validation (already via Pydantic)
   - SQL injection prevention (already via SQLAlchemy ORM)
   - CORS restrictions (production origins only)

4. **Infrastructure**
   - Database backups
   - Secrets management (Vault, AWS Secrets Manager)
   - Monitoring and alerting
   - DDoS protection

---

## Performance Considerations

### Database Optimization
- **Indexes**: On frequently queried fields (student_id, word_id, book_id)
- **Query Efficiency**: Use JOINs instead of N+1 queries
- **Connection Pooling**: SQLAlchemy manages connection pool

### API Optimization
- **Caching**: Can add Redis for frequently accessed data
- **Pagination**: Implemented if student list grows
- **Lazy Loading**: Load detailed data only when needed

### Frontend Optimization
- **Code Splitting**: Next.js automatic code splitting
- **Image Optimization**: Next.js image optimization (for book covers)
- **Static Generation**: Some pages can be statically generated

### Scalability
- **Horizontal Scaling**: FastAPI can run multiple instances
- **Database Scaling**: PostgreSQL can handle 1000s of students
- **Current Limit**: 25 students (MVP), but architecture supports 1000+

---

## Testing Strategy (Future)

### Unit Tests
- Backend: pytest for services and API endpoints
- Frontend: Jest + React Testing Library for components

### Integration Tests
- API integration tests (full request/response cycle)
- Database integration tests

### End-to-End Tests
- Playwright or Cypress for user flows
- Test critical paths (view student, see recommendations)

### Data Quality Tests
- Validate mock data generation
- Verify recommendation algorithm correctness
- Check for edge cases (0% mastery, 100% mastery)

---

## Monitoring & Observability (Future)

### Application Monitoring
- **Logging**: Structured logs (JSON) for errors and key events
- **Metrics**: API response times, database query performance
- **Alerts**: Errors, slow queries, high API usage

### Tools
- Railway built-in logs
- Vercel analytics
- Optional: Sentry for error tracking
- Optional: LogRocket for user session replay

---

## Future Enhancements

### Short-term
1. Add student-facing view (let students see own progress)
2. Export reports as PDF
3. Add more visualization (charts, graphs)
4. Track vocabulary progress over time (multi-day)

### Medium-term
1. Real-time transcript analysis (as class happens)
2. Integration with Google Classroom
3. Support for multiple classes/teachers
4. Mobile app (React Native)

### Long-term
1. AI-powered lesson plan generation based on gaps
2. Collaborative filtering for book recommendations
3. Gamification for students (badges, progress tracking)
4. Multi-language support (Spanish, etc.)

---

## Conclusion

This architecture is designed for:
- **Simplicity**: Easy to understand and maintain
- **Scalability**: Can grow beyond MVP if needed
- **Modularity**: Components can be replaced/upgraded
- **Demo-friendly**: Pre-seeded data, no auth, fast responses

The offline processing pipeline ensures the demo is always ready to show, while the clean separation between frontend, backend, and database allows for independent scaling and development.
