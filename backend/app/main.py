import logging
from pathlib import Path

from app.api.v1.routers import api_router
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.middleware import register_middlewares
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

settings = get_settings()
setup_logging(getattr(logging, settings.log_level.upper(), logging.INFO))

# Ensure generated images directory exists
GENERATED_DIR = Path(__file__).parent / "static" / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


def create_app() -> FastAPI:
    app_instance = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        docs_url=f"{settings.api_v1_prefix}/docs" if settings.api_v1_prefix else None,
    )
    register_middlewares(app_instance)
    app_instance.include_router(api_router, prefix=settings.api_v1_prefix)

    # Serve generated images at /static/generated/<filename>
    app_instance.mount(
        "/static/generated",
        StaticFiles(directory=str(GENERATED_DIR)),
        name="generated",
    )

    return app_instance


app = create_app()
