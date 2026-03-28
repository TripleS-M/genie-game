"""
game_state.py — Game state machine for The Fine Print.

Manages transitions between game states and tracks wish history.
"""

from enum import Enum
from settings import MAX_WISHES


class GameState(Enum):
    INTRO = "intro"
    INPUT = "input"
    CASTING = "casting"
    RESULT = "result"
    GAME_OVER = "game_over"


class WishRecord:
    """Stores data for one wish cycle."""
    def __init__(self, wish_text: str, response: str, result: str):
        self.wish_text = wish_text
        self.response = response
        self.result = result  # "genie_win" or "player_win"


class GameManager:
    """
    Manages the overall game state, wish counting, and score tracking.
    """

    def __init__(self):
        self.state = GameState.INTRO
        self.wish_count = 0
        self.player_score = 0
        self.genie_score = 0
        self.wish_history: list[WishRecord] = []
        self.current_response = ""
        self.current_result = ""
        self.current_wish = ""

    def reset(self):
        """Reset the game to the beginning."""
        self.state = GameState.INTRO
        self.wish_count = 0
        self.player_score = 0
        self.genie_score = 0
        self.wish_history = []
        self.current_response = ""
        self.current_result = ""
        self.current_wish = ""

    def start_game(self):
        """Transition from INTRO to INPUT."""
        self.state = GameState.INPUT

    def submit_wish(self, wish_text: str):
        """Transition from INPUT to CASTING."""
        self.current_wish = wish_text
        self.state = GameState.CASTING

    def receive_result(self, response: str, result: str):
        """
        Receive the AI's response and transition to RESULT.
        
        Args:
            response: The genie's dialogue text.
            result: 'genie_win' or 'player_win'.
        """
        self.current_response = response
        self.current_result = result
        self.wish_count += 1

        # Update scores
        if result == "player_win":
            self.player_score += 1
        else:
            self.genie_score += 1

        # Store wish history
        self.wish_history.append(
            WishRecord(self.current_wish, response, result)
        )

        self.state = GameState.RESULT

    def next_wish(self):
        """Transition from RESULT to INPUT or GAME_OVER."""
        if self.wish_count >= MAX_WISHES:
            self.state = GameState.GAME_OVER
        else:
            self.state = GameState.INPUT

    def get_winner(self) -> str:
        """Return the overall winner after all wishes are used."""
        if self.player_score > self.genie_score:
            return "player"
        elif self.genie_score > self.player_score:
            return "genie"
        else:
            return "tie"

    def get_genie_state(self) -> str:
        """Return the genie's visual state based on game state."""
        if self.state == GameState.CASTING:
            return "casting"
        elif self.state == GameState.RESULT:
            return self.current_result  # "genie_win" or "player_win"
        elif self.state == GameState.GAME_OVER:
            winner = self.get_winner()
            if winner == "player":
                return "player_win"
            else:
                return "genie_win"
        else:
            return "idle"
