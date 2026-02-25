# Brza Faktura - Copilot Instructions

## Product Context

**Brza Faktura** (Fast Invoice) is a Fintech product for the Macedonian Market. The product follows the Macedonian accounting law changes requiring invoices to be verified by UJP (Управа за јавни приходи - Public Revenue Office).

**Target audience:** SMBs (95% of Macedonian market) that don't use accounting software.

**Key Features:**
- Fast invoice creation and management
- UJP-compliant e-invoicing
- Client and product management
- Multi-organization support
- Team collaboration

---

## Project Structure

```
e-invoices/
├── backend/
│   ├── app/
│   │   ├── api/v1/routers/     # API endpoints
│   │   ├── core/               # Config, security, logging
│   │   ├── db/                 # Database session, base
│   │   ├── middleware/         # Request timing, etc.
│   │   ├── models/             # SQLAlchemy models
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── services/           # Business logic (core + facade)
│   │   └── static/             # Static files
│   ├── alembic/                # Database migrations
│   └── tests/                  # pytest tests
├── frontend/
│   └── src/
│       ├── api/                # API client + modules
│       ├── assets/             # CSS, images
│       ├── components/
│       │   ├── ui/             # Reusable UI components
│       │   ├── layout/         # Layout components
│       │   └── features/       # Feature components
│       ├── composables/
│       │   ├── core/           # Utilities (formatters, cookies)
│       │   ├── ui/             # UI utilities
│       │   └── features/       # Feature composables
│       ├── i18n/               # Translations (mk, en, sq)
│       ├── layouts/            # Page layouts
│       ├── pages/              # Route pages
│       ├── router/             # Vue Router config
│       ├── stores/             # Pinia stores
│       └── types/              # TypeScript interfaces
├── docker/                     # Docker configs
├── docs/                       # Documentation
└── scripts/                    # Utility scripts
```

---

## Tech Stack

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy (async)
- Alembic
- PostgreSQL
- Redis
- Celery + Flower
- Pydantic v2 + pydantic-settings
- python-jose (JWT)
- pwdlib (Argon2)
- fastapi-mail
- Loguru
- SlowAPI
- fastapi-pagination
- pytest + pytest-asyncio

### Frontend
- Vue 3 (Composition API, `<script setup>`)
- TypeScript
- Vite
- Pinia
- Vue Router 4
- Tailwind CSS 4
- vue-i18n
- ESLint + Prettier

### Infrastructure
- Docker
- Caddy (reverse proxy)

---

## Code Guidelines

### Full-Stack Task Order

When implementing a feature that spans backend and frontend:

#### 1. Backend
- **Models** (`app/models/`)
  - Define SQLAlchemy model with columns, relationships, enums
  - Inherit from `Base`, add docstring with Macedonian translation
- **Schemas** (`app/schemas/`)
  - Create `Base`, `Create`, `Update`, `Response` Pydantic schemas
  - Add field validators where needed
- **Services** (`app/services/{feature}/`)
  - `core.py` - raw database CRUD operations
  - `facade.py` - high-level operations with auth/org checks
  - `__init__.py` - exports
- **Routers** (`app/api/v1/routers/`)
  - Define endpoints with proper dependencies
  - Use `Depends(get_user_context)` and `Depends(get_session)`
  - Scope routes under `/organizations/{organization_id}/`
  - **NO business logic in routers** - only HTTP concerns (logging, calling facade, returning response)
  - All business logic (validation, client creation, transactions) goes in facade
- **Migrations** (`alembic/versions/`)
  - Generate with `alembic revision --autogenerate -m "description"`
  - Review and adjust if needed

#### 2. Frontend
- **Types** (`src/types/`)
  - Define TypeScript interfaces matching backend schemas
- **API** (`src/api/v1/`)
  - Add API methods using the shared client
- **Composables** (`src/composables/features/{feature}/`)
  - Business logic, state management, API calls
  - Use `useAsyncAction` for async operations (loading, error handling)
  - Export via barrel file
- **Components** (`src/components/features/{feature}/`)
  - UI components using composables
  - Keep components focused and reusable
- **Pages** (`src/pages/`)
  - Route-level components
- **i18n** (`src/i18n/`)
  - Add translations for mk, en and sq

#### 3. Validation
- Check for TypeScript/Python errors after each edit
- Run tests if they exist for the modified area

---

## Important Rules

- **Reuse existing code** - Always check if functionality already exists before creating new code
- **Check composables** - Review `src/composables/` for existing utilities (formatters, notifications, cookies, etc.)
- **Check components** - Review `src/components/ui/` for existing UI components
- **When unsure** - Check similar files in the same directory for patterns and conventions

---

## Key Conventions

### Backend
- All service methods are `@staticmethod` - no instance state
- Use `selectinload()` for eager loading relationships
- Use `Decimal` for money/prices, never `float`
- Currency is MKD (Macedonian Denar)
- Config uses `get_settings()` with `@lru_cache`
- Logging: use `import logging` + `logger = logging.getLogger(__name__)`
  - Routers: `logger.info("METHOD /path: org_id=%s user_id=%s", org_id, user_id)`
  - Services: `logger.warning/error` for access denied, failures

### Data Structures
- **NEVER use `dataclasses` in this project** - always use Pydantic `BaseModel`
- **NEVER use `Any` type** - always use proper type hints (`Union`, `Optional`, concrete types)
- All data structures (DTOs, response models, API data) go in `app/schemas/`
- Services should import schemas from `app/schemas/`, not define their own data classes
- Keep services focused on business logic, not data structure definitions
- If a service needs to return structured data from an external API, create schemas in:
  - `app/schemas/{feature}.py` for internal data
  - `app/schemas/{external_api}_api.py` for external API response data (e.g., `ujp_api.py`)

### Frontend
- API client (`src/api/client.ts`) handles token refresh automatically
- Use `useFormatters()` for dates, prices, numbers (locale-aware)
- Use `useNotifications()` for toast messages
- Use `useAuthCookies()` for token management
- Two layouts: `PublicLayout` (landing, auth) and `OrganizationLayout` (app)
- Routes use lazy loading: `component: () => import('@/pages/...')`
- i18n has 3 locales: `mk`, `en`, `sq`

### API Pattern
- Frontend API modules in `src/api/v1/{feature}.ts`
- Export object with methods: `featureApi.getItems()`, `featureApi.create()`
- Use shared `api.get/post/put/patch/delete` from client

### Types
- Frontend types mirror backend schemas
- Separate interfaces: `Feature`, `FeatureCreate`, `FeatureResponse`
- Located in `src/types/{feature}.ts`

---

## Git Workflow

See [git-commit-instructions.md](git-commit-instructions.md) for:
- Pre-commit hooks (black, isort, ruff, end-of-file fixer)
- Commit message format (conventional commits)
- Commit frequency guidelines
