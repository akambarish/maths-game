"""Mode 1: Computer asks questions to guess user's number."""

from game_engine import GameEngine
from llm_service import LLMService
from scoring import Scoring
from config import MIN_NUMBER, MAX_NUMBER

def play_computer_guesses_mode():
    """Play the game mode where computer guesses user's number."""
    print("\n=== Mode 1: Computer Guesses Your Number ===")
    print(f"Think of a number between {MIN_NUMBER} and {MAX_NUMBER}.")
    
    # Get user's number
    while True:
        try:
            user_input = input(f"\nEnter your number ({MIN_NUMBER}-{MAX_NUMBER}): ").strip()
            secret_number = int(user_input)
            if MIN_NUMBER <= secret_number <= MAX_NUMBER:
                break
            else:
                print(f"Please enter a number between {MIN_NUMBER} and {MAX_NUMBER}.")
        except ValueError:
            print("Please enter a valid number.")
    
    print(f"\nGreat! I'll try to guess your number ({secret_number}) by asking up to 10 questions.")
    print("Answer with 'Yes' or 'No' (or 'Y'/'N').\n")
    
    # Initialize game components
    engine = GameEngine()
    llm_service = LLMService()
    scoring = Scoring()
    
    # Game loop
    while engine.can_ask_more_questions():
        remaining = engine.get_remaining_questions()
        possible_count = engine.get_possible_count()
        
        print(f"[Question {engine.question_count + 1}/10] {possible_count} possible numbers remaining")
        
        # Generate question using LLM
        try:
            question = llm_service.generate_question(
                engine.get_possible_numbers(),
                engine.qa_history
            )
            print(f"Question: {question}")
        except Exception as e:
            print(f"Error generating question: {e}")
            print("Using fallback question...")
            # Fallback question
            if possible_count > 250:
                question = "Is the number even?"
            elif possible_count > 100:
                question = "Is the number less than 250?"
            else:
                question = "Is the number divisible by 5?"
            print(f"Question: {question}")
        
        # Get user's answer
        while True:
            answer = input("Your answer (Yes/No): ").strip()
            if answer.lower() in ["yes", "y", "no", "n"]:
                # Normalize to Yes/No
                answer = "Yes" if answer.lower() in ["yes", "y"] else "No"
                break
            else:
                print("Please answer with 'Yes' or 'No' (or 'Y'/'N').")
        
        # Check if answer is correct for the secret number
        # We need to validate the answer matches the actual number
        actual_answer = validate_answer_for_number(secret_number, question)
        if actual_answer != answer:
            #print(f"⚠️  Warning: Your answer doesn't match the question for number!")
            #print(f"   The correct answer should be: {actual_answer}")
            print("   Continuing with your answer anyway...\n")
        
        # Record Q&A
        engine.record_qa(question, answer)
        
        # Check if we've narrowed it down to one number
        if engine.get_possible_count() == 1:
            print(f"\nI've narrowed it down to one possibility!")
            break
        
        print()  # Empty line for readability
    
    # Make final guess
    final_guess = engine.make_final_guess()
    print(f"\n{'='*50}")
    print(f"Final Guess: {final_guess}")
    print(f"Your number was: {secret_number}")
    
    if final_guess == secret_number:
        print("🎉 Correct! I guessed your number!")
        won = True
    else:
        print(f"❌ Incorrect. I couldn't guess your number.")
        print(f"Remaining possibilities: {engine.get_possible_count()}")
        if engine.get_possible_count() <= 10:
            print(f"Possible numbers: {sorted(list(engine.get_possible_numbers()))}")
        won = False
    
    # Record game
    scoring.record_game(won, engine.question_count, mode=1)
    
    return won

def validate_answer_for_number(number, question):
    """
    Determine the correct Yes/No answer for a question about a specific number.
    This is used to validate user's answers match their secret number.
    """
    question_lower = question.lower()
    
    # Even/Odd
    if "even" in question_lower:
        return "Yes" if number % 2 == 0 else "No"
    if "odd" in question_lower:
        return "Yes" if number % 2 != 0 else "No"
    
    # Comparison
    import re
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
        import math
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
        import math
        for i in range(3, int(math.sqrt(number)) + 1, 2):
            if number % i == 0:
                return "No"
        return "Yes"
    
    # Default: return "Yes" if we can't determine
    return "Yes"

