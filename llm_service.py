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
    
    def validate_answer_for_number(self, number, question, user_answer):
        """
        Validate if the user's answer to a question is correct for a specific number.
        
        Args:
            number: The number being evaluated
            question: The mathematical question asked
            user_answer: The user's answer (Yes/No)
        
        Returns:
            bool: True if the answer is correct, False otherwise
        """
        prompt = f"""You are mathametical and numerical computational expert.You are validating an answer in a number guessing game.

Secret number: {number}
User's question: "{question}"
User's answer: {user_answer}

Determine if the user's answer (Yes or No) correctly answers the question for the secret number {number}.

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
    
    def determine_answer_for_number(self, number, question):
        """
        Determine the correct Yes/No answer for a question about a specific number.
        
        Args:
            number: The number being evaluated
            question: The mathematical question asked
        
        Returns:
            str: "Yes" or "No" - the correct answer for the question about the number
        """
        prompt = f"""You are mathametical and numerical computational expert. You are determining the correct answer for a question about a specific number in a number guessing game.

Secret number: {number}
Question: "{question}"

Determine what the correct answer (Yes or No) should be for this question about the number {number}.

Respond with ONLY "Yes" or "No", nothing else. Do not include any explanation or other text."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that determines correct mathematical answers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=10
            )
            result = response.choices[0].message.content.strip()
            # Normalize to Yes/No
            if result.lower().startswith("yes"):
                return "Yes"
            elif result.lower().startswith("no"):
                return "No"
            else:
                # Fallback if LLM returns unexpected format
                raise Exception(f"Unexpected response format: {result}")
        except Exception as e:
            raise Exception(f"Failed to determine answer: {str(e)}")
    
    def filter_numbers(self, numbers, question, answer):
        """
        Filter a set of numbers based on a question and answer using LLM.
        
        Args:
            numbers: Set or list of numbers to filter
            question: The mathematical question asked
            answer: "Yes" or "No" - the answer given
        
        Returns:
            set: Set of numbers that match the question/answer criteria
        """
        if not numbers:
            return set()
        
        numbers_list = sorted(list(numbers))
        expected_answer = answer if answer in ["Yes", "No"] else ("Yes" if answer.lower() in ["yes", "y"] else "No")
        
        # For efficiency, batch process numbers
        # If set is small, check all individually
        # If set is large, use batch processing
        filtered_numbers = set()
        
        # Batch size for LLM calls (process multiple numbers at once)
        batch_size = 50
        
        for i in range(0, len(numbers_list), batch_size):
            batch = numbers_list[i:i + batch_size]
            
            # Create prompt for batch filtering
            numbers_str = ", ".join(map(str, batch))
            prompt = f"""You are a mathematical and numerical computational expert. You are filtering numbers based on a question and answer.

Question: "{question}"
Expected answer: {expected_answer}

Given the following list of numbers: [{numbers_str}]

For each number, determine if the answer to the question would be "{expected_answer}".
Return ONLY a comma-separated list of numbers that match (i.e., numbers where the answer to the question is "{expected_answer}").

Example: If the question is "Is the number even?" and expected answer is "Yes", and the numbers are [1, 2, 3, 4, 5], return: 2, 4

Return ONLY the matching numbers as a comma-separated list, nothing else."""

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that filters numbers based on mathematical questions."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=500
                )
                result = response.choices[0].message.content.strip()
                
                # Parse the result to extract numbers
                # Remove any brackets, parentheses, or extra text
                result = result.strip("[]()")
                # Split by comma and extract numbers
                for part in result.split(","):
                    part = part.strip()
                    try:
                        num = int(part)
                        if num in batch:  # Only include numbers from this batch
                            filtered_numbers.add(num)
                    except ValueError:
                        continue
            except Exception as e:
                # If batch processing fails, fall back to individual checks
                for num in batch:
                    try:
                        num_answer = self.determine_answer_for_number(num, question)
                        if num_answer == expected_answer:
                            filtered_numbers.add(num)
                    except Exception:
                        continue
        
        return filtered_numbers

