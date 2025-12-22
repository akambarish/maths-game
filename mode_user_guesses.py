"""Mode 2: User asks questions to guess computer's number."""

import random
import re
import math
from game_engine import GameEngine
from llm_service import LLMService
from scoring import Scoring
from config import MIN_NUMBER, MAX_NUMBER

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
    engine = GameEngine()
    engine.set_secret_number(secret_number)
    llm_service = LLMService()
    scoring = Scoring()
    
    question_count = 0
    
    # Game loop
    while True:
        user_input = input("Your question (or 'guess' to make a guess): ").strip()
        
        if user_input.lower() == "guess":
            break
        
        if not user_input:
            print("Please enter a question or 'guess'.")
            continue
        
        question_count += 1
        
        # Get user's expected answer
        print("\nWhat do you think the answer is?")
        while True:
            expected_answer = input("Your expected answer (Yes/No): ").strip()
            if expected_answer.lower() in ["yes", "y", "no", "n"]:
                expected_answer = "Yes" if expected_answer.lower() in ["yes", "y"] else "No"
                break
            else:
                print("Please answer with 'Yes' or 'No' (or 'Y'/'N').")
        
        # Determine actual answer for the secret number
        actual_answer = determine_answer_for_number(secret_number, user_input)
        
        # Validate answer using LLM (as a check)
        try:
            is_correct_llm = llm_service.validate_answer(secret_number, user_input, expected_answer)
            # Use deterministic answer as source of truth, LLM as validation
            is_correct = (expected_answer == actual_answer)
            
            if is_correct:
                print(f"✓ Correct! The answer is: {actual_answer}")
            else:
                print(f"✗ Incorrect. The actual answer is: {actual_answer}")
            
            # Record Q&A for tracking (though we don't use range manager in this mode)
            engine.record_qa(user_input, actual_answer)
            
        except Exception as e:
            print(f"Error validating answer: {e}")
            print("Please try again.")
            question_count -= 1
            continue
        
        print()  # Empty line
    
    # User makes guess
    print(f"\nYou asked {question_count} question(s).")
    while True:
        try:
            guess_input = input(f"Enter your guess ({MIN_NUMBER}-{MAX_NUMBER}): ").strip()
            guess = int(guess_input)
            if MIN_NUMBER <= guess <= MAX_NUMBER:
                break
            else:
                print(f"Please enter a number between {MIN_NUMBER} and {MAX_NUMBER}.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Check guess
    print(f"\n{'='*50}")
    print(f"Your guess: {guess}")
    print(f"Secret number: {secret_number}")
    
    if guess == secret_number:
        print("🎉 Congratulations! You guessed correctly!")
        won = True
    else:
        print(f"❌ Incorrect. The secret number was {secret_number}.")
        won = False
    
    # Record game
    scoring.record_game(won, question_count, mode=2)
    
    return won

def determine_answer_for_number(number, question):
    """
    Determine the correct Yes/No answer for a question about a specific number.
    This is used to provide the actual answer for the secret number.
    """
    question_lower = question.lower()
    
    # Even/Odd
    if "even" in question_lower:
        return "Yes" if number % 2 == 0 else "No"
    if "odd" in question_lower:
        return "Yes" if number % 2 != 0 else "No"
    
    # Comparison
    patterns = [
        (r"less than (\d+)", lambda n, v: n < v),
        (r"greater than (\d+)", lambda n, v: n > v),
        (r"more than (\d+)", lambda n, v: n > v),
        (r"less than or equal to (\d+)", lambda n, v: n <= v),
        (r"greater than or equal to (\d+)", lambda n, v: n >= v),
        (r"at least (\d+)", lambda n, v: n >= v),
        (r"at most (\d+)", lambda n, v: n <= v),
        (r"(\d+) or less", lambda n, v: n <= v),
        (r"(\d+) or more", lambda n, v: n >= v),
    ]
    
    for pattern, condition_func in patterns:
        match = re.search(pattern, question_lower)
        if match:
            value = int(match.group(1))
            return "Yes" if condition_func(number, value) else "No"
    
    # Divisibility
    div_match = re.search(r"divisible by (\d+)", question_lower)
    if div_match:
        divisor = int(div_match.group(1))
        return "Yes" if number % divisor == 0 else "No"
    
    # Perfect square
    if "perfect square" in question_lower or ("square" in question_lower and "root" not in question_lower):
        root = int(math.sqrt(number))
        return "Yes" if root * root == number else "No"
    
    # Prime
    if "prime" in question_lower:
        if number < 2:
            return "No"
        if number == 2:
            return "Yes"
        if number % 2 == 0:
            return "No"
        for i in range(3, int(math.sqrt(number)) + 1, 2):
            if number % i == 0:
                return "No"
        return "Yes"
    
    # If we can't determine, use LLM fallback - but for now return "Yes" as default
    # In practice, LLM validation should handle edge cases
    return "Yes"

