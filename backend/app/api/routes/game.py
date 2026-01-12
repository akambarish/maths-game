from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.api.models import (
    AskQuestionRequest,
    AskQuestionResponse,
    EndGameResponse,
    GameStatusResponse,
    MakeGuessRequest,
    MakeGuessResponse,
    StartGameResponse,
)
from backend.app.core.dependencies import get_game_service, get_scoring, get_session_manager

from config import MAX_QUESTIONS

router = APIRouter(prefix="/api/game", tags=["game"])


@router.post("/start", response_model=StartGameResponse)
def start_game():
    game_service = get_game_service()
    session = game_service.start_game(max_guesses=3)
    return StartGameResponse(
        game_id=session.game_id,
        secret_number_set=True,
        possible_count=session.engine.get_possible_count(),
        max_questions=MAX_QUESTIONS,
        max_guesses=session.max_guesses,
    )


@router.get("/{game_id}/status", response_model=GameStatusResponse)
def get_status(game_id: str):
    sessions = get_session_manager()
    session = sessions.get_session(game_id)
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found.")

    game_service = get_game_service()
    game_state = game_service.get_state(session)
    remaining_questions = max(0, MAX_QUESTIONS - session.engine.question_count)
    remaining_guesses = max(0, session.max_guesses - session.guess_attempts)

    return GameStatusResponse(
        game_id=session.game_id,
        question_count=session.engine.question_count,
        remaining_questions=remaining_questions,
        possible_count=session.engine.get_possible_count(),
        guess_attempts=session.guess_attempts,
        remaining_guesses=remaining_guesses,
        game_state=game_state,
        won=session.won,
        game_over=session.game_over,
    )


@router.post("/{game_id}/question", response_model=AskQuestionResponse)
def ask_question(game_id: str, payload: AskQuestionRequest):
    sessions = get_session_manager()
    session = sessions.get_session(game_id)
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found.")

    game_service = get_game_service()
    try:
        answer = game_service.ask_question(session, payload.question)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to determine answer: {e}") from e

    game_state = game_service.get_state(session)
    remaining_questions = max(0, MAX_QUESTIONS - session.engine.question_count)
    return AskQuestionResponse(
        answer=answer,
        possible_count=session.engine.get_possible_count(),
        question_count=session.engine.question_count,
        remaining_questions=remaining_questions,
        game_state=game_state,
    )


@router.post("/{game_id}/guess", response_model=MakeGuessResponse)
def make_guess(game_id: str, payload: MakeGuessRequest):
    sessions = get_session_manager()
    session = sessions.get_session(game_id)
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found.")

    # Validate range early
    from config import MIN_NUMBER, MAX_NUMBER

    if payload.guess < MIN_NUMBER or payload.guess > MAX_NUMBER:
        raise HTTPException(status_code=400, detail=f"Guess must be between {MIN_NUMBER} and {MAX_NUMBER}.")

    game_service = get_game_service()
    try:
        correct = game_service.make_guess(session, payload.guess)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    remaining_guesses = max(0, session.max_guesses - session.guess_attempts)
    return MakeGuessResponse(
        correct=correct,
        game_over=session.game_over,
        won=session.won,
        secret_number=session.secret_number if session.game_over else None,
        remaining_guesses=remaining_guesses,
    )


@router.post("/{game_id}/end", response_model=EndGameResponse)
def end_game(game_id: str):
    sessions = get_session_manager()
    session = sessions.get_session(game_id)
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found.")

    # Record stats once
    scoring = get_scoring()
    if not session.stats_recorded:
        scoring.record_game(session.won, session.engine.question_count, mode=2)
        session.stats_recorded = True

    return EndGameResponse(won=session.won, questions_asked=session.engine.question_count, game_over=session.game_over)


