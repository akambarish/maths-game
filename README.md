# Math Guessing Game

A CLI Python application where players guess numbers between 0-500 using mathematical questions. The game features two modes and uses OpenAI LLM for intelligent question generation and answer validation.

## Features

- **Mode 1: Computer Guesses** - You pick a number, and the computer asks up to 10 mathematical questions to guess it
- **Mode 2: User Guesses** - The computer picks a number, and you ask questions to figure it out
- **LLM-Powered Questions** - Uses OpenAI API to generate smart mathematical questions
- **Range Tracking** - System tracks and narrows down possible numbers based on answers
- **Scoring System** - Tracks wins, losses, average questions, and best performance

## Setup

### Prerequisites

- Python 3.7 or higher
- OpenAI API key

### Installation

1. Clone or download this repository

2. Set up a virtual environment (recommended):

   **Windows:**
   ```bash
   setup_venv.bat
   ```

   **Linux/Mac:**
   ```bash
   chmod +x setup_venv.sh
   ./setup_venv.sh
   ```

   **Manual setup:**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   
   # Install dependencies
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:

   Option A: Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

   Option B: Set environment variable:
   ```bash
   # Windows
   set OPENAI_API_KEY=your_api_key_here

   # Linux/Mac
   export OPENAI_API_KEY=your_api_key_here
   ```

   Option C: Edit `config.py` directly (not recommended for production)

4. (Optional) Configure model in `.env`:
   ```
   OPENAI_MODEL=gpt-4
   ```
   Default is `gpt-3.5-turbo`.

## Usage

Run the game:
```bash
python main.py
```

### Game Modes

**Mode 1: Computer Guesses Your Number**
1. Select option 1 from the menu
2. Enter a number between 0-500
3. Answer the computer's mathematical questions with Yes/No
4. The computer will make a final guess after 10 questions (or when narrowed to one possibility)

**Mode 2: You Guess Computer's Number**
1. Select option 2 from the menu
2. Ask mathematical questions (e.g., "Is the number even?", "Is it less than 200?")
3. Provide your expected answer (Yes/No)
4. The system will tell you if your answer is correct
5. Type 'guess' when ready to make your final guess

### Example Questions

- "Is the number even?"
- "Is the number less than 200?"
- "Is the number a perfect square?"
- "Is the number divisible by 7?"
- "Is the number prime?"
- "Is the number greater than 300?"

## Scoring

The game tracks:
- Total games played
- Wins and losses
- Win rate percentage
- Average questions per game
- Best game (fewest questions to win)
- Statistics by game mode

View statistics by selecting option 3 from the main menu.

## Configuration

Edit `config.py` to change:
- `MIN_NUMBER`: Minimum number in range (default: 0)
- `MAX_NUMBER`: Maximum number in range (default: 500)
- `MAX_QUESTIONS`: Maximum questions allowed (default: 10)
- `SCORING_FILE`: Path to statistics file (default: "game_stats.json")

## How It Works

### Mode 1 (Computer Guesses)
- System maintains a set of all possible numbers (0-500)
- LLM generates questions based on current possible numbers and Q&A history
- Each Yes/No answer filters the possible numbers using pattern matching
- After 10 questions (or when narrowed to 1), system makes final guess
- If exactly one number remains, that's the guess; otherwise random from remaining

### Mode 2 (User Guesses)
- Computer randomly selects a secret number
- User asks mathematical questions
- LLM validates if user's expected answer matches the actual answer for the secret number
- User makes final guess after gathering information

## File Structure

- `main.py` - Entry point and menu system
- `game_engine.py` - Core game logic and state management
- `range_manager.py` - Number range filtering and narrowing
- `llm_service.py` - OpenAI API integration
- `mode_computer_guesses.py` - Mode 1 implementation
- `mode_user_guesses.py` - Mode 2 implementation
- `scoring.py` - Statistics and scoring system
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies

## Troubleshooting

**Error: OPENAI_API_KEY not set**
- Make sure you've set your API key in `.env` file or environment variable

**Error: Failed to generate question**
- Check your internet connection
- Verify your OpenAI API key is valid
- Check if you have API credits available

**Questions not narrowing down range**
- Some question types may not be recognized by the pattern matcher
- The system will still work but may not filter optimally
- Try asking more specific questions (e.g., "Is the number less than 250?")

## License

This project is open source and available for educational purposes.

