"""Range Manager for filtering and narrowing down possible numbers."""

import re
import math

class RangeManager:
    """Manages the set of possible numbers and applies filters based on questions and answers."""
    
    def __init__(self, min_num=0, max_num=500):
        """
        Initialize with full range of possible numbers.
        
        Args:
            min_num: Minimum number in range (default: 0)
            max_num: Maximum number in range (default: 500)
        """
        self.possible_numbers = set(range(min_num, max_num + 1))
        self.min_num = min_num
        self.max_num = max_num
    
    def get_count(self):
        """Return the count of possible numbers remaining."""
        return len(self.possible_numbers)
    
    def get_numbers(self):
        """Return the set of possible numbers."""
        return self.possible_numbers.copy()
    
    def apply_filter(self, question, answer):
        """
        Apply a filter based on question and answer to narrow down possible numbers.
        
        Args:
            question: The mathematical question asked
            answer: "Yes" or "No"
        
        Returns:
            int: Number of possible numbers remaining after filter
        """
        question_lower = question.lower()
        answer_is_yes = answer.lower() in ["yes", "y"]
        
        # Even/Odd questions
        if "even" in question_lower:
            if answer_is_yes:
                self.possible_numbers = {n for n in self.possible_numbers if n % 2 == 0}
            else:
                self.possible_numbers = {n for n in self.possible_numbers if n % 2 != 0}
            return len(self.possible_numbers)
        
        if "odd" in question_lower:
            if answer_is_yes:
                self.possible_numbers = {n for n in self.possible_numbers if n % 2 != 0}
            else:
                self.possible_numbers = {n for n in self.possible_numbers if n % 2 == 0}
            return len(self.possible_numbers)
        
        # Comparison questions (<, >, <=, >=)
        # Pattern: "is number less than X", "is number greater than X", etc.
        comparison_patterns = [
            (r"less than (\d+)", lambda x, val: x < val),
            (r"greater than (\d+)", lambda x, val: x > val),
            (r"more than (\d+)", lambda x, val: x > val),
            (r"less than or equal to (\d+)", lambda x, val: x <= val),
            (r"greater than or equal to (\d+)", lambda x, val: x >= val),
            (r"at least (\d+)", lambda x, val: x >= val),
            (r"at most (\d+)", lambda x, val: x <= val),
            (r"(\d+) or less", lambda x, val: x <= val),
            (r"(\d+) or more", lambda x, val: x >= val),
        ]
        
        for pattern, condition_func in comparison_patterns:
            match = re.search(pattern, question_lower)
            if match:
                value = int(match.group(1))
                if answer_is_yes:
                    self.possible_numbers = {n for n in self.possible_numbers if condition_func(n, value)}
                else:
                    self.possible_numbers = {n for n in self.possible_numbers if not condition_func(n, value)}
                return len(self.possible_numbers)
        
        # Divisibility questions
        div_pattern = r"divisible by (\d+)"
        div_match = re.search(div_pattern, question_lower)
        if div_match:
            divisor = int(div_match.group(1))
            if answer_is_yes:
                self.possible_numbers = {n for n in self.possible_numbers if n % divisor == 0}
            else:
                self.possible_numbers = {n for n in self.possible_numbers if n % divisor != 0}
            return len(self.possible_numbers)
        
        # Perfect square questions
        if "perfect square" in question_lower or ("square" in question_lower and "root" not in question_lower):
            if answer_is_yes:
                self.possible_numbers = {n for n in self.possible_numbers if self._is_perfect_square(n)}
            else:
                self.possible_numbers = {n for n in self.possible_numbers if not self._is_perfect_square(n)}
            return len(self.possible_numbers)
        
        # Prime number questions
        if "prime" in question_lower:
            if answer_is_yes:
                self.possible_numbers = {n for n in self.possible_numbers if self._is_prime(n)}
            else:
                self.possible_numbers = {n for n in self.possible_numbers if not self._is_prime(n)}
            return len(self.possible_numbers)
        
        # If no pattern matches, return current count (no filtering applied)
        return len(self.possible_numbers)
    
    def _is_perfect_square(self, n):
        """Check if a number is a perfect square."""
        if n < 0:
            return False
        root = int(math.sqrt(n))
        return root * root == n
    
    def _is_prime(self, n):
        """Check if a number is prime."""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def reset(self, min_num=None, max_num=None):
        """Reset to full range."""
        if min_num is not None:
            self.min_num = min_num
        if max_num is not None:
            self.max_num = max_num
        self.possible_numbers = set(range(self.min_num, self.max_num + 1))

