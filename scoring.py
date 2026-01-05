"""Scoring system for tracking game statistics."""

import json
import os
from config import SCORING_FILE

class Scoring:
    """Manages game statistics and scoring."""
    
    def __init__(self):
        """Initialize scoring system and load existing stats."""
        self.stats = self._load_stats()
    
    def _load_stats(self):
        """Load statistics from file or return default stats."""
        if os.path.exists(SCORING_FILE):
            try:
                with open(SCORING_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._default_stats()
        return self._default_stats()
    
    def _default_stats(self):
        """Return default statistics structure."""
        return {
            "total_games": 0,
            "wins": 0,
            "losses": 0,
            "total_questions": 0,
            "best_game_questions": None,
            "mode1_games": 0,
            "mode1_wins": 0,
            "mode2_games": 0,
            "mode2_wins": 0
        }
    
    def _save_stats(self):
        """Save statistics to file."""
        try:
            with open(SCORING_FILE, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save statistics: {e}")
    
    def record_game(self, won, questions_asked, mode=1):
        """
        Record a completed game.
        
        Args:
            won: True if game was won, False otherwise
            questions_asked: Number of questions asked in this game
            mode: Game mode (1 or 2)
        """
        self.stats["total_games"] += 1
        self.stats["total_questions"] += questions_asked
        
        if mode == 1:
            self.stats["mode1_games"] += 1
            if won:
                self.stats["mode1_wins"] += 1
        else:
            self.stats["mode2_games"] += 1
            if won:
                self.stats["mode2_wins"] += 1
        
        if won:
            self.stats["wins"] += 1
            if self.stats["best_game_questions"] is None or questions_asked < self.stats["best_game_questions"]:
                self.stats["best_game_questions"] = questions_asked
        else:
            self.stats["losses"] += 1
        
        self._save_stats()
    
    def get_stats(self):
        """Get current statistics."""
        return self.stats.copy()
    
    def display_stats(self):
        """Display statistics in a formatted way."""
        stats = self.stats
        total = stats["total_games"]
        
        if total == 0:
            print("\n=== Game Statistics ===")
            print("No games played yet.")
            return
        
        print("\n=== Game Statistics ===")
        print(f"Total games played: {total}")
        print(f"Wins: {stats['wins']}")
        print(f"Losses: {stats['losses']}")
        
        if total > 0:
            win_rate = (stats['wins'] / total) * 100
            print(f"Win rate: {win_rate:.1f}%")
        
        if stats['total_questions'] > 0:
            avg_questions = stats['total_questions'] / total
            print(f"Average questions per game: {avg_questions:.1f}")
        
        if stats['best_game_questions'] is not None:
            print(f"Best game: {stats['best_game_questions']} questions")
        
        print(f"\nMode 1 (Computer Guesses):")
        print(f"  Games: {stats['mode1_games']}, Wins: {stats['mode1_wins']}")
        print(f"\nMode 2 (User Guesses):")
        print(f"  Games: {stats['mode2_games']}, Wins: {stats['mode2_wins']}")


