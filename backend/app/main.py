from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes.game import router as game_router
from backend.app.api.routes.stats import router as stats_router


def create_app() -> FastAPI:
    app = FastAPI(title="Math Guessing Game API", version="0.1.0")

    # Dev-friendly CORS; tighten for production.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(game_router)
    app.include_router(stats_router)

    @app.get("/api/health")
    def health():
        return {"ok": True}

    return app


app = create_app()


