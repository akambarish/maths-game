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
    llm_service = LLMService()
    engine = GameEngine(llm_service=llm_service)
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
            
        # Get user's answer
        while True:
            answer = input("Your answer (Yes/No): ").strip()
            if answer.lower() in ["yes", "y", "no", "n"]:
                # Normalize to Yes/No
                answer = "Yes" if answer.lower() in ["yes", "y"] else "No"
                break
            else:
                print("Please answer with 'Yes' or 'No' (or 'Y'/'N').")
        
        # Validate answer silently using LLM
        try:
            is_correct = llm_service.validate_answer_for_number(secret_number, question, answer)
            # Silent validation - no warnings shown regardless of result
        except Exception as e:
            print(f"Error validating answer: {e}")
        
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

