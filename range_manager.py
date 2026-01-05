"""Range Manager for filtering and narrowing down possible numbers."""

class RangeManager:
    """Manages the set of possible numbers and applies filters based on questions and answers."""
    
    def __init__(self, min_num=0, max_num=500, llm_service=None):
        """
        Initialize with full range of possible numbers.
        
        Args:
            min_num: Minimum number in range (default: 0)
            max_num: Maximum number in range (default: 500)
            llm_service: LLMService instance for filtering (required)
        """
        self.possible_numbers = set(range(min_num, max_num + 1))
        self.min_num = min_num
        self.max_num = max_num
        self.llm_service = llm_service
    
    def get_count(self):
        """Return the count of possible numbers remaining."""
        return len(self.possible_numbers)
    
    def get_numbers(self):
        """Return the set of possible numbers."""
        return self.possible_numbers.copy()
    
    def apply_filter(self, question, answer):
        """
        Apply a filter based on question and answer to narrow down possible numbers using LLM.
        
        Args:
            question: The mathematical question asked
            answer: "Yes" or "No"
        
        Returns:
            int: Number of possible numbers remaining after filter
        """
        if self.llm_service is None:
            raise ValueError("LLMService is required for filtering. Pass llm_service to RangeManager constructor.")
        
        try:
            # Use LLM to filter numbers
            self.possible_numbers = self.llm_service.filter_numbers(
                self.possible_numbers,
                question,
                answer
            )
        except Exception as e:
            # If LLM filtering fails, don't filter (keep all numbers)
            # This ensures the game can continue even if LLM has issues
            print(f"Warning: LLM filtering failed: {e}. Keeping all possible numbers.")
        
        return len(self.possible_numbers)
    
    def reset(self, min_num=None, max_num=None):
        """Reset to full range."""
        if min_num is not None:
            self.min_num = min_num
        if max_num is not None:
            self.max_num = max_num
        self.possible_numbers = set(range(self.min_num, self.max_num + 1))

