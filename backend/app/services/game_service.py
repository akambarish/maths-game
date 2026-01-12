"""Service layer that wraps existing game logic for use via HTTP APIs."""

from __future__ import annotations

import random
from typing import Literal

from config import MAX_QUESTIONS, MIN_NUMBER, MAX_NUMBER
from game_engine import GameEngine
from llm_service import LLMService

from backend.app.services.session_manager import GameSession, SessionManager


GameState = Literal["asking", "guess_only", "won", "lost"]


class GameService:
    def __init__(self, session_manager: SessionManager, llm_service: LLMService):
        self._sessions = session_manager
        self._llm = llm_service

    def start_game(self, *, max_guesses: int = 3) -> GameSession:
        secret_number = random.randint(MIN_NUMBER, MAX_NUMBER)
        engine = GameEngine(llm_service=self._llm)
        engine.set_secret_number(secret_number)
        return self._sessions.create_session(engine=engine, secret_number=secret_number, max_guesses=max_guesses)

    def get_state(self, session: GameSession) -> GameState:
        if session.game_over:
            return "won" if session.won else "lost"
        if session.engine.question_count >= MAX_QUESTIONS:
            return "guess_only"
        return "asking"

    def ask_question(self, session: GameSession, question: str) -> str:
        if session.game_over:
            raise ValueError("Game is already over.")
        if session.engine.question_count >= MAX_QUESTIONS:
            raise ValueError("Maximum questions reached; you can only guess now.")

        answer = self._llm.determine_answer_for_number(session.secret_number, question)
        session.engine.record_qa(question, answer)
        return answer

    def make_guess(self, session: GameSession, guess: int) -> bool:
        if session.game_over:
            raise ValueError("Game is already over.")

        session.guess_attempts += 1
        correct = guess == session.secret_number
        if correct:
            session.won = True
            session.game_over = True
            return True

        if session.guess_attempts >= session.max_guesses:
            session.won = False
            session.game_over = True
        return False


