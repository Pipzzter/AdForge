# AdForge

AI-powered content generation platform that transforms raw marketing copy into beautiful, ready-to-publish landing pages. Using advanced LLMs and image generation, AdForge automates the entire process of creating high-converting advertorial content.

## Features

- **Smart Copy Injection**: Parses raw marketing copy and intelligently injects it into HTML templates
- **AI Image Generation**: Automatically generates contextual images using Gemini 2.5 Flash
- **Clean Templates**: Minimal, conversion-focused HTML template with all standard sections
- **Multi-Agent Architecture**: Extensible base agent class for adding new specialized agents

## How It Works

1. **Input**: Paste your raw advertorial copy (headline, hook, body content, testimonials, CTA)
2. **Parse**: AI extracts and categorizes each content section
3. **Generate**: Creates relevant images for each section
4. **Output**: Complete HTML page ready to publish

## Project Structure

```
adforge/
├── backend/
│   ├── app/
│   │   ├── api/v1/routers/        # API endpoints
│   │   ├── core/                  # Config, security, logging
│   │   ├── db/                    # Database session, base
│   │   ├── models/                # SQLAlchemy models
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── services/
│   │   │   └── agents/            # AI Agent implementations
│   │   │       ├── base.py        # Abstract base agent class
│   │   │       ├── llm_client.py  # Gemini LLM client
│   │   │       ├── image_client.py # Gemini image generation
│   │   │       └── copy_injection/ # Copy Injection Agent
│   │   └── static/
│   │       ├── generated/         # Generated output
│   │       └── templates/         # HTML templates
│   ├── alembic/                   # Database migrations
│   └── tests/                     # pytest tests
├── frontend/
│   └── src/
│       ├── api/                   # API clients
│       ├── components/            # Vue components
│       ├── layouts/               # Page layouts
│       ├── pages/                 # Route pages
│       ├── router/                # Vue Router config
│       └── types/                 # TypeScript types
├── docs/                          # Documentation
└── docker/                        # Docker configuration
```

## Tech Stack

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy (async) + PostgreSQL
- Alembic migrations
- Google Gemini API (LLM + Image Generation)
- Pydantic v2
- pytest

### Frontend
- Vue 3 (Composition API)
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
- PostgreSQL
- Google Cloud API key (for Gemini)

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env    # Configure your environment variables
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/adforge
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_secret_key
```

## Template System

AdForge uses a simple HTML template with placeholder markers:

### Placeholders
- Text: `[Headline goes here]`, `[Hook goes here]`, etc.
- Images: `[Headline image goes here]`, `[Author image goes here]`, etc.

### Repeatable Sections
Sections that can repeat multiple times are wrapped with markers:

```html
<!-- REPEAT:body:START -->
<section class="body-section">
  <h2>[Body section title goes here]</h2>
  <img src="[Body section image goes here]">
  <p>[Body section goes here]</p>
</section>
<!-- REPEAT:body:END -->
```

## API Endpoints

### Copy Injection
- `GET /api/v1/copyinjection/templates` - List available templates
- `POST /api/v1/copyinjection/generate` - Generate landing page from copy

## License

MIT
