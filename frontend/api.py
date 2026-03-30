"""
api.py — Async API communication with the backend.

Uses threading to avoid freezing the Pygame game loop during API calls.
"""

import threading
import requests
from settings import API_URL, API_TIMEOUT


class WishRequest:
    """
    Manages an asynchronous wish request to the backend.
    
    Usage:
        req = WishRequest("I wish for...")
        req.start()
        # In game loop:
        if req.is_done():
            result = req.get_result()
    """

    def __init__(self, wish: str, difficulty: str = "regular"):
        self.wish = wish
        self.difficulty = difficulty
        self._result = None
        self._error = None
        self._done = False
        self._thread = None

    def start(self):
        """Start the API request in a background thread."""
        self._thread = threading.Thread(target=self._make_request, daemon=True)
        self._thread.start()

    def _make_request(self):
        """Perform the actual HTTP request (runs in background thread)."""
        try:
            response = requests.post(
                f"{API_URL}/wish",
                json={"wish": self.wish, "difficulty": self.difficulty},
                timeout=API_TIMEOUT,
            )
            response.raise_for_status()
            self._result = response.json()
        except requests.exceptions.Timeout:
            self._error = "The genie's magic timed out... Try again!"
            self._result = {
                "response": self._error,
                "result": "genie_win"
            }
        except requests.exceptions.ConnectionError:
            self._error = "Cannot connect to the genie's realm! Is the backend server running?"
            self._result = {
                "response": self._error,
                "result": "genie_win"
            }
        except Exception as e:
            self._error = f"Something went wrong: {str(e)}"
            self._result = {
                "response": "The genie's magic fizzled... Something went wrong. Try again!",
                "result": "genie_win"
            }
        finally:
            self._done = True

    def is_done(self) -> bool:
        """Check if the request has completed."""
        return self._done

    def get_result(self) -> dict:
        """
        Get the result of the API call.
        
        Returns:
            Dict with 'response' (str) and 'result' ('genie_win' or 'player_win')
        """
        return self._result

    def had_error(self) -> bool:
        """Check if the request encountered an error."""
        return self._error is not None


def send_wish(wish: str, difficulty: str = "regular") -> WishRequest:
    """
    Create and start an async wish request.
    
    Args:
        wish: The player's wish text.
        difficulty: The game mode ("regular" or "hard")
        
    Returns:
        WishRequest object to poll for completion.
    """
    req = WishRequest(wish, difficulty)
    req.start()
    return req
