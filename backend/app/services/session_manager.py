"""In-memory session manager for multi-user game sessions.

For production, this can be swapped with Redis or another shared store.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class GameSession:
    game_id: str
    created_at: float
    last_access_at: float
    secret_number: int
    max_guesses: int
    guess_attempts: int = 0
    won: bool = False
    game_over: bool = False
    stats_recorded: bool = False
    engine: object = field(default=None)


class SessionManager:
    def __init__(self, ttl_seconds: int = 60 * 60):
        self._ttl_seconds = ttl_seconds
        self._sessions: Dict[str, GameSession] = {}

    def create_session(self, *, engine: object, secret_number: int, max_guesses: int) -> GameSession:
        now = time.time()
        game_id = str(uuid.uuid4())
        session = GameSession(
            game_id=game_id,
            created_at=now,
            last_access_at=now,
            secret_number=secret_number,
            max_guesses=max_guesses,
            engine=engine,
        )
        self._sessions[game_id] = session
        return session

    def get_session(self, game_id: str) -> Optional[GameSession]:
        self._cleanup_expired()
        session = self._sessions.get(game_id)
        if session:
            session.last_access_at = time.time()
        return session

    def delete_session(self, game_id: str) -> None:
        self._sessions.pop(game_id, None)

    def _cleanup_expired(self) -> None:
        now = time.time()
        expired = [gid for gid, s in self._sessions.items() if (now - s.last_access_at) > self._ttl_seconds]
        for gid in expired:
            self._sessions.pop(gid, None)


