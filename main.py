"""Main entry point for the Math Guessing Game."""

from mode_user_guesses import play_user_guesses_mode
from scoring import Scoring

def display_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("         MATH GUESSING GAME")
    print("="*50)
    print("1. Mode 2: You guess computer's number")
    print("2. View statistics")
    print("3. Exit")
    print("="*50)

def main():
    """Main game loop."""
    print("Welcome to the Math Guessing Game!")
    print("A game where mathematical questions help narrow down numbers between 0-500.")
    
    scoring = Scoring()
    
    while True:
        display_menu()
        choice = input("\nSelect an option (1-3): ").strip()
        
        if choice == "1":
            try:
                play_user_guesses_mode()
            except KeyboardInterrupt:
                print("\n\nGame interrupted.")
            except Exception as e:
                print(f"\nError: {e}")
                print("Please make sure your OpenAI API key is set correctly.")
        
        elif choice == "2":
            scoring.display_stats()
        
        elif choice == "3":
            print("\nThanks for playing! Goodbye!")
            break
        
        else:
            print("Invalid choice. Please select 1-3.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()


