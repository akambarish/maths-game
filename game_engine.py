"""Core game engine for managing game state and logic."""

from range_manager import RangeManager
from config import MIN_NUMBER, MAX_NUMBER, MAX_QUESTIONS

class GameEngine:
    """Core game engine managing game state."""
    
    def __init__(self, min_num=MIN_NUMBER, max_num=MAX_NUMBER, max_questions=MAX_QUESTIONS, llm_service=None):
        """
        Initialize game engine.
        
        Args:
            min_num: Minimum number in range
            max_num: Maximum number in range
            max_questions: Maximum questions allowed
            llm_service: LLMService instance (required for filtering)
        """
        self.llm_service = llm_service
        self.range_manager = RangeManager(min_num, max_num, llm_service=llm_service)
        self.min_num = min_num
        self.max_num = max_num
        self.max_questions = max_questions
        self.qa_history = []
        self.question_count = 0
        self.secret_number = None  # For mode 2 (user guesses)
    
    def reset(self):
        """Reset game state for a new game."""
        self.range_manager.reset(self.min_num, self.max_num)
        self.qa_history = []
        self.question_count = 0
        self.secret_number = None
    
    def set_secret_number(self, number):
        """Set the secret number (for mode 2)."""
        if not (self.min_num <= number <= self.max_num):
            raise ValueError(f"Number must be between {self.min_num} and {self.max_num}")
        self.secret_number = number
    
    def record_qa(self, question, answer):
        """
        Record a question and answer pair.
        
        Args:
            question: The question asked
            answer: The answer given ("Yes" or "No")
        """
        self.qa_history.append((question, answer))
        self.question_count += 1
        self.range_manager.apply_filter(question, answer)
    
    def get_possible_numbers(self):
        """Get the current set of possible numbers."""
        return self.range_manager.get_numbers()
    
    def get_possible_count(self):
        """Get the count of possible numbers remaining."""
        return self.range_manager.get_count()
    
    def can_ask_more_questions(self):
        """Check if more questions can be asked."""
        return self.question_count < self.max_questions
    
    def get_remaining_questions(self):
        """Get number of questions remaining."""
        return max(0, self.max_questions - self.question_count)
    
    def make_final_guess(self):
        """
        Make final guess based on remaining possible numbers.
        
        Returns:
            int: The guessed number
        """
        possible = list(self.get_possible_numbers())
        if not possible:
            # Fallback: return middle of range
            return (self.min_num + self.max_num) // 2
        
        if len(possible) == 1:
            return possible[0]
        
        # If multiple possibilities, return the first one (could be random)
        import random
        return random.choice(possible)
    
    def check_guess(self, guess):
        """
        Check if a guess matches the secret number.
        
        Args:
            guess: The number guessed
        
        Returns:
            bool: True if guess is correct
        """
        if self.secret_number is None:
            raise ValueError("Secret number not set")
        return guess == self.secret_number

