from app.middleware.request_timing import RequestTimingMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def register_middlewares(app: FastAPI) -> None:
    # CORS middleware - allow frontend requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict to specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if not any(m.cls is RequestTimingMiddleware for m in app.user_middleware):
        app.add_middleware(RequestTimingMiddleware)
