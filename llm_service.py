"""LLM Service for question generation and answer validation using OpenAI."""

import json
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

class LLMService:
    """Service for interacting with OpenAI API for question generation and validation."""
    
    def __init__(self):
        """Initialize the OpenAI client."""
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set. Please set it in environment variables or .env file.")
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL
    
    def generate_question(self, possible_numbers, qa_history):
        """
        Generate a mathematical question based on current possible numbers and Q&A history.
        
        Args:
            possible_numbers: Set of possible numbers remaining
            qa_history: List of tuples (question, answer) representing previous Q&A
        
        Returns:
            str: A mathematical question about the number
        """
        range_size = len(possible_numbers)
        sample_numbers = sorted(list(possible_numbers))[:10]  # Sample first 10 for context
        
        # Build Q&A history string
        history_str = ""
        if qa_history:
            history_str = "\nPrevious questions and answers:\n"
            for q, a in qa_history:
                history_str += f"Q: {q}\nA: {a}\n"
        
        prompt = f"""You are mathametical and computational expert. You have to frame a mathamatical question to guess the number.
         The target number is between 0 and 500. The question should be answerable with Yes or No.

Current situation:
- There are {range_size} possible numbers remaining
- Sample of possible numbers: {sample_numbers}
{history_str}

Generate a single, clear mathematical question that will help narrow down the possible numbers.
The question should be answerable with Yes or No.

Examples of good questions:
- "Is the number even?"
- "Is the number less than 200?"
- "Is the number a perfect square?"
- "Is the number divisible by 7?"
- "Is the number prime?"
- "Is the number greater than 300?"

Return ONLY the question text, nothing else. Do not include "Q:" or any other prefix."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates mathematical questions for a number guessing game."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=100
            )
            question = response.choices[0].message.content.strip()
            # Remove any quotes or prefixes
            question = question.strip('"').strip("'")
            if question.startswith("Q:"):
                question = question[2:].strip()
            return question
        except Exception as e:
            raise Exception(f"Failed to generate question: {str(e)}")
    
    def validate_answer(self, secret_number, user_question, user_answer):
        """
        Validate if the user's answer to their question is correct for the secret number.
        
        Args:
            secret_number: The secret number the computer selected
            user_question: The mathematical question the user asked
            user_answer: The user's answer (Yes/No)
        
        Returns:
            bool: True if the answer is correct, False otherwise
        """
        prompt = f"""You are mathametical and numerical computational expert.You are validating an answer in a number guessing game.

Secret number: {secret_number}
User's question: "{user_question}"
User's answer: {user_answer}

Determine if the user's answer (Yes or No) correctly answers the question for the secret number {secret_number}.

Respond with ONLY "Yes" if the answer is correct, or "No" if the answer is incorrect.
 not include any explanation or other text."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that validates mathematical answers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=10
            )
            result = response.choices[0].message.content.strip().lower()
            return result.startswith("yes")
        except Exception as e:
            raise Exception(f"Failed to validate answer: {str(e)}")

