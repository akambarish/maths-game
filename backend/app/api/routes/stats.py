from __future__ import annotations

from fastapi import APIRouter

from backend.app.core.dependencies import get_scoring

router = APIRouter(prefix="/api", tags=["stats"])


@router.get("/stats")
def get_stats():
    scoring = get_scoring()
    return scoring.get_stats()


