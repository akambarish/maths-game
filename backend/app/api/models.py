"""Pydantic request/response models for the API."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


YesNo = Literal["Yes", "No"]


class StartGameResponse(BaseModel):
    game_id: str
    secret_number_set: bool = True
    possible_count: int
    max_questions: int
    max_guesses: int


class GameStatusResponse(BaseModel):
    game_id: str
    question_count: int
    remaining_questions: int
    possible_count: int
    guess_attempts: int
    remaining_guesses: int
    game_state: Literal["asking", "guess_only", "won", "lost"]
    won: bool
    game_over: bool


class AskQuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)


class AskQuestionResponse(BaseModel):
    answer: YesNo
    possible_count: int
    question_count: int
    remaining_questions: int
    game_state: Literal["asking", "guess_only", "won", "lost"]


class MakeGuessRequest(BaseModel):
    guess: int


class MakeGuessResponse(BaseModel):
    correct: bool
    game_over: bool
    won: bool
    secret_number: Optional[int] = None
    remaining_guesses: int


class EndGameResponse(BaseModel):
    won: bool
    questions_asked: int
    game_over: bool


