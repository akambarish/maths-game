"""Configuration settings for the Math Guessing Game."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Game Configuration
MIN_NUMBER = 0
MAX_NUMBER = 500
MAX_QUESTIONS = 10

# Scoring file path
SCORING_FILE = "game_stats.json"

