"""Mode 2: User asks questions to guess computer's number."""

import random
from game_engine import GameEngine
from llm_service import LLMService
from scoring import Scoring
from config import MIN_NUMBER, MAX_NUMBER, MAX_QUESTIONS

def play_user_guesses_mode():
    """Play the game mode where user guesses computer's number."""
    print("\n=== Mode 2: You Guess the Computer's Number ===")
    print(f"I've selected a secret number between {MIN_NUMBER} and {MAX_NUMBER}.")
    print("Ask me mathematical questions (answerable with Yes/No) to figure it out!")
    print("Examples: 'Is the number even?', 'Is it less than 200?', 'Is it a perfect square?'")
    print("Type 'guess' when you're ready to make your guess.\n")
    
    # Computer selects secret number
    secret_number = random.randint(MIN_NUMBER, MAX_NUMBER)
    
    # Initialize game components
    llm_service = LLMService()
    engine = GameEngine(llm_service=llm_service)
    engine.set_secret_number(secret_number)
    scoring = Scoring()

    # Show initial possibilities count once at game start
    print(f"Possible numbers remaining: {engine.get_possible_count()}\n")
    
    question_count = 0
    guess_attempts = 0
    max_guesses = 3
    won = False
    exhausted_msg_shown = False
    
    # Game loop
    while not won and guess_attempts < max_guesses:
        # If user has exhausted questions, switch to guess-only mode automatically
        if question_count >= MAX_QUESTIONS:
            if not exhausted_msg_shown:
                remaining_guesses = max_guesses - guess_attempts
                print(f"You have exhausted max no of questions. Now You have {remaining_guesses} chances to guess.")
                exhausted_msg_shown = True

            # Guess-only phase (no more questions allowed)
            guess_input = input(f"Enter your guess ({MIN_NUMBER}-{MAX_NUMBER}): ").strip()
            guess_attempts += 1

            try:
                guess = int(guess_input)
            except ValueError:
                print("Invalid guess.")
                continue

            if not (MIN_NUMBER <= guess <= MAX_NUMBER):
                print("Invalid guess.")
                continue

            if guess == secret_number:
                print("Congratulations! You guessed correctly!")
                won = True
                break

            print("Incorrect.")
            continue

        user_input = input("Your question (or 'guess' to make a guess): ").strip()

        if not user_input:
            print("Please enter a question or 'guess'.")
            continue

        if user_input.lower() == "guess":
            guess_input = input(f"Enter your guess ({MIN_NUMBER}-{MAX_NUMBER}): ").strip()
            guess_attempts += 1

            try:
                guess = int(guess_input)
            except ValueError:
                print("Invalid guess.")
                continue

            if not (MIN_NUMBER <= guess <= MAX_NUMBER):
                print("Invalid guess.")
                continue

            if guess == secret_number:
                print("Congratulations! You guessed correctly!")
                won = True
                break

            print("Incorrect.")
            continue

        question_count += 1

        # Determine answer for the secret number using LLM
        try:
            actual_answer = llm_service.determine_answer_for_number(secret_number, user_input)

            print(f"Answer: {actual_answer}")

            # Record Q&A for tracking and range narrowing
            engine.record_qa(user_input, actual_answer)

        except Exception as e:
            print(f"Error determining answer: {e}")
            print("Please try again.")
            question_count -= 1
            continue

        print()  # Empty line

        # After the 10th question, automatically move to guess mode
        if question_count >= MAX_QUESTIONS:
            if not exhausted_msg_shown:
                remaining_guesses = max_guesses - guess_attempts
                print(f"You have exhausted max no of questions. Now You have {remaining_guesses} chances to guess.")
                exhausted_msg_shown = True
    
    if not won and guess_attempts >= max_guesses:
        print(f"You have exhausted all guess attempts. You lose. The secret number was {secret_number}.")

    # Record game
    scoring.record_game(won, question_count, mode=2)
    
    return won

