# deployment Specification

## Purpose
Defines requirements for deploying the Vocabulary Recommendation Engine to production environments (Railway for backend/database, Vercel for frontend) and maintaining comprehensive documentation for setup, deployment, and maintenance.
## Requirements
### Requirement: Production Deployment
The system SHALL be deployable to production environments using Railway for backend services and database, and Vercel for frontend services.

#### Scenario: Deploy database to Railway
- **WHEN** deploying the application to production
- **THEN** a PostgreSQL database SHALL be provisioned on Railway
- **AND** the database SHALL be accessible via a connection string
- **AND** the connection string SHALL be stored as an environment variable (`DATABASE_URL`)
- **AND** the database SHALL contain all required schema (tables, indexes, constraints)

#### Scenario: Deploy backend to Railway
- **WHEN** deploying the application to production
- **THEN** the FastAPI backend SHALL be deployed to Railway
- **AND** Railway SHALL be configured with:
  - Root directory: `backend/`
  - Build command: `pip install -r requirements.txt`
  - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **AND** environment variables SHALL be set:
  - `DATABASE_URL` (Railway PostgreSQL connection string)
  - `OPENAI_API_KEY` (for future use)
- **AND** the backend SHALL be accessible via HTTPS
- **AND** the health check endpoint (`/health`) SHALL respond successfully

#### Scenario: Deploy frontend to Vercel
- **WHEN** deploying the application to production
- **THEN** the Next.js frontend SHALL be deployed to Vercel
- **AND** Vercel SHALL be configured with:
  - Root directory: `frontend/`
  - Build command: `pnpm build`
  - Output directory: `.next`
- **AND** environment variable SHALL be set:
  - `NEXT_PUBLIC_API_URL` (Railway backend URL)
- **AND** the frontend SHALL be accessible via HTTPS
- **AND** the frontend SHALL successfully connect to the backend API

#### Scenario: Seed production database
- **WHEN** deploying the application to production
- **THEN** the production database SHALL be seeded with:
  - 525 vocabulary words (grades 5-8)
  - 100 Project Gutenberg books with vocabulary counts
  - 25 student profiles with vocabulary mastery data
  - 75 student book recommendations (3 per student)
  - 2 class-wide book recommendations
- **AND** all data SHALL be verified in the database
- **AND** seed scripts SHALL be idempotent (can be run multiple times safely)

#### Scenario: End-to-end production functionality
- **WHEN** the application is deployed to production
- **THEN** all pages SHALL load correctly:
  - Class overview page (`/class`)
  - Student list page (`/students`)
  - Student detail pages (`/students/[id]`)
- **AND** all API endpoints SHALL respond correctly:
  - `GET /api/students` returns list of all students
  - `GET /api/students/[id]` returns student detail with recommendations
  - `GET /api/class/stats` returns class statistics
  - `GET /api/class/recommendations` returns class recommendations
- **AND** frontend SHALL successfully fetch and display data from backend
- **AND** application SHALL work on desktop, tablet, and mobile devices

### Requirement: Deployment Documentation
The system SHALL include comprehensive documentation for setup, deployment, and maintenance.

#### Scenario: README documentation
- **WHEN** a developer wants to understand or deploy the application
- **THEN** the README.md SHALL contain:
  - Project overview and goals
  - Complete tech stack description
  - Architecture overview (or reference to ARCHITECTURE.md)
  - Prerequisites (Node.js, Python, PostgreSQL versions)
  - Step-by-step setup instructions
  - Environment variable documentation with examples
  - Database setup instructions
  - Local development server instructions
  - Deployment instructions for Railway and Vercel
  - Data generation process explanation
  - Link to API documentation (FastAPI `/docs`)
  - Known limitations
  - Future enhancements

#### Scenario: Scripts documentation
- **WHEN** a developer wants to run data generation or seeding scripts
- **THEN** `scripts/README.md` SHALL exist and contain:
  - Purpose and description of each script
  - Order of execution (dependencies between scripts)
  - Prerequisites and required dependencies
  - Expected outputs for each script
  - Troubleshooting guide for common issues
  - Examples of running each script

#### Scenario: Code documentation
- **WHEN** a developer reviews the codebase
- **THEN** complex logic SHALL have explanatory comments
- **AND** code SHALL follow consistent formatting standards
- **AND** no hardcoded values SHALL exist (environment variables used instead)
- **AND** unused code/files SHALL be removed

### Requirement: Code Quality and Security
The system SHALL maintain code quality standards and security best practices.

#### Scenario: Git ignore configuration
- **WHEN** code is committed to version control
- **THEN** `.gitignore` files SHALL exclude:
  - Python artifacts (`__pycache__/`, `*.pyc`, `venv/`)
  - Node.js artifacts (`node_modules/`, `.next/`)
  - Environment variable files (`.env`, `.env.local`)
  - IDE configuration files (`.vscode/`, `.idea/`)
  - Database files (`*.db`, `*.sqlite`)
  - Log files (`*.log`)
  - Generated mock data files
  - Large external datasets

#### Scenario: Environment variable security
- **WHEN** deploying to production
- **THEN** sensitive values SHALL be stored as environment variables
- **AND** `.env` files SHALL never be committed to version control
- **AND** `.env.example` files SHALL exist as templates
- **AND** production environment variables SHALL be set in deployment platform (Railway/Vercel)

