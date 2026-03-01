# Med-Agents

AI-powered multi-agent system for medical advertorial generation. The platform uses specialized agents to automate the creation of compliant, high-converting advertorial content with AI-generated images.

## Features

- **Copy Injection Agent**: Parses raw advertorial copy and injects it into HTML templates
- **AI Image Generation**: Uses Gemini 2.5 Flash for photorealistic image generation (headline, body, product images)
- **Template System**: HTML templates with placeholders for dynamic content injection
- **Multi-Agent Architecture**: Extensible base agent class for adding new specialized agents

## Project Structure

```
med-agents/
├── backend/
│   ├── app/
│   │   ├── api/v1/routers/        # API endpoints
│   │   │   ├── auth.py            # Authentication routes
│   │   │   ├── copy_injection.py  # Copy injection agent routes
│   │   │   ├── health.py          # Health check routes
│   │   │   └── user.py            # User management routes
│   │   ├── core/                  # Config, security, logging
│   │   ├── db/                    # Database session, base
│   │   ├── middleware/            # Request timing middleware
│   │   ├── models/                # SQLAlchemy models
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── services/
│   │   │   ├── agents/            # AI Agent implementations
│   │   │   │   ├── base.py        # Abstract base agent class
│   │   │   │   ├── llm_client.py  # Gemini LLM client
│   │   │   │   ├── image_client.py # Gemini image generation
│   │   │   │   └── copy_injection/ # Agent 1: Copy Injection
│   │   │   │       ├── agent.py           # Main orchestrator
│   │   │   │       ├── copy_parser.py     # LLM-based copy parsing
│   │   │   │       ├── image_generator.py # Image generation
│   │   │   │       ├── placeholder_filler.py # Template filling
│   │   │   │       ├── template_service.py   # Template loading
│   │   │   │       └── schemas.py         # Data models
│   │   │   ├── auth.py
│   │   │   ├── health.py
│   │   │   └── user.py
│   │   ├── static/
│   │   │   ├── generated/         # Generated advertorial output
│   │   │   └── new_templates/     # HTML templates
│   │   └── utils/
│   ├── alembic/                   # Database migrations
│   └── tests/                     # pytest tests
├── frontend/
│   └── src/
│       ├── api/
│       │   └── agents/            # Agent API clients
│       │       └── copyInjection.ts
│       ├── components/
│       │   ├── features/          # Feature-specific components
│       │   └── layout/            # Layout components
│       ├── layouts/
│       │   └── DefaultLayout.vue
│       ├── pages/
│       │   ├── HomePage.vue
│       │   ├── CopyInjectionPage.vue
│       │   ├── CompliancePage.vue
│       │   ├── OptimizationPage.vue
│       │   ├── ResearchPage.vue
│       │   └── TranslationPage.vue
│       ├── router/
│       ├── stores/
│       └── types/
│           └── agent.ts           # Agent type definitions
├── docs/                          # Documentation
│   └── AGENT_1_COPY_INJECTION.md  # Agent 1 full documentation
├── docker/                        # Docker configuration
├── scripts/                       # Utility scripts
└── .github/                       # GitHub workflows & Copilot instructions
```

## Tech Stack

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy (async) + PostgreSQL
- Alembic migrations
- Google Gemini API (LLM + Image Generation)
- Pydantic v2
- pytest + pytest-asyncio

### Frontend
- Vue 3 (Composition API, `<script setup>`)
- TypeScript
- Vite
- Pinia
- Vue Router 4
- Tailwind CSS

### Infrastructure
- Docker + Docker Compose

## Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- Docker & Docker Compose
- Google Gemini API key

### Create & activate virtual environment (backend)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

### Install frontend dependencies
```powershell
cd frontend
npm install
```

### Environment configuration
Copy `backend/.env.example` to `backend/.env` and configure:
```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/backend_db
GEMINI_API_KEY=your-gemini-api-key
SECRET_KEY=your-secret-key
```

For Docker, use `DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/backend_db`.

### Run Docker services
First time:
```powershell
docker compose -f docker/docker-compose.yml up -d --build
```
Subsequent runs:
```powershell
docker compose -f docker/docker-compose.yml up -d
```

### Apply database migrations
```powershell
cd docker
docker compose exec backend /bin/bash
alembic upgrade head
exit
```

### Run locally (development)
```powershell
# Backend
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm run dev
```

## Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health/

## API Endpoints

### Health
- `GET /api/v1/health/` – Service heartbeat

### Authentication
- `POST /api/v1/auth/register` – Register user & receive JWT
- `POST /api/v1/auth/token` – Obtain JWT via credentials

### Users
- `POST /api/v1/user/` – Create user
- `GET /api/v1/user/` – List users

### Agents
- `POST /api/v1/copy-injection/process` – Process copy injection
- `GET /api/v1/copy-injection/templates` – List available templates

## Agents

### Agent 1: Copy & Image Injection

> 📖 **Full Documentation:** [docs/AGENT_1_COPY_INJECTION.md](docs/AGENT_1_COPY_INJECTION.md)
>
> 🧪 **Testing Ground:** [CheckoutChamp Funnel Builder](https://app.checkoutchamp.com/editfunnel/b263cdf6-2082-4fec-9565-77578efc1772)

Automatically generates complete landing pages from HTML templates and raw advertorial copy.

**Pipeline:**
1. Load HTML template with placeholders
2. Parse raw copy using Gemini 2.5 Flash LLM (structured output)
3. Fill repeatable sections (body, reviews, social proof)
4. Fill simple placeholders (headline, hook, product, offer)
5. Generate AI images using Gemini 2.5 Flash Image
6. Return complete HTML ready to publish

**Key Features:**
- Template-aware content placement
- Dynamic section cloning (adapts to content length)
- AI-powered copy parsing (extracts structure from raw text)
- Context-aware image generation (embedded as base64)
- Automatic cleanup of empty optional sections

### Image Generation Guidelines

Three types of images are generated following strict advertorial guidelines:

| Type | Goal | Style |
|------|------|-------|
| **Headline** | Create extreme curiosity | Editorial, candid, NO product |
| **Body** | Explain concepts simply | Educational, clear focus |
| **Product** | Demonstrate mechanism | Trustworthy, clinical-but-human |

## Running Tests

```powershell
# All tests
pytest

# Specific directory
pytest tests/services

# With coverage
pytest --cov=app tests/
```

## Git Hooks

Pre-commit hooks are configured for code quality:
```powershell
# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

Hooks include: Black, isort, Ruff, and selective pytest for changed files.

## Environment Modes

```powershell
# Development (default)
docker compose -f docker/docker-compose.yml up -d

# Staging
APP_ENV=staging docker compose -f docker/docker-compose.yml up -d --build

# Production
APP_ENV=production docker compose -f docker/docker-compose.yml up -d --build
```
