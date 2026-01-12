"""Lightweight dependency singletons for the backend app."""

from __future__ import annotations

from functools import lru_cache

from llm_service import LLMService
from scoring import Scoring

from backend.app.services.game_service import GameService
from backend.app.services.session_manager import SessionManager


@lru_cache(maxsize=1)
def get_session_manager() -> SessionManager:
    return SessionManager(ttl_seconds=60 * 60)


@lru_cache(maxsize=1)
def get_llm_service() -> LLMService:
    return LLMService()


@lru_cache(maxsize=1)
def get_game_service() -> GameService:
    return GameService(get_session_manager(), get_llm_service())


@lru_cache(maxsize=1)
def get_scoring() -> Scoring:
    return Scoring()


