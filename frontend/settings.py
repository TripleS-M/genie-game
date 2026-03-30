"""
settings.py — Constants and configuration for the Pygame frontend.
"""

import os

# ── Screen Settings ──────────────────────────────────────────────
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
FPS = 60
TITLE = "The Fine Print"

# ── API Settings ─────────────────────────────────────────────────
API_URL = "http://localhost:8000"
API_TIMEOUT = 30  # seconds

# ── Game Settings ────────────────────────────────────────────────
MAX_WISHES = 3

# ── Colors (Dark Mystical Theme) ────────────────────────────────
BG_COLOR = (15, 10, 30)             # Deep dark purple-black
BG_GRADIENT_TOP = (20, 10, 45)      # Dark purple
BG_GRADIENT_BOTTOM = (10, 5, 20)    # Near black

GOLD = (255, 200, 50)               # Bright gold
GOLD_DARK = (200, 150, 30)          # Darker gold
GOLD_DIM = (150, 120, 40)           # Dimmed gold

PURPLE = (130, 60, 200)             # Vibrant purple
PURPLE_DARK = (60, 20, 100)         # Dark purple
PURPLE_GLOW = (160, 80, 255)        # Glowing purple

TEXT_WHITE = (240, 235, 255)         # Slightly purple-tinted white
TEXT_DIM = (160, 150, 180)           # Dimmed text
TEXT_INPUT = (255, 255, 255)         # Pure white for input

INPUT_BOX_BG = (30, 20, 50)         # Dark purple input bg
INPUT_BOX_BORDER = (130, 60, 200)   # Purple border
INPUT_BOX_ACTIVE = (180, 100, 255)  # Active purple border

DIALOGUE_BG = (20, 15, 40, 200)     # Semi-transparent dark
DIALOGUE_BORDER = (100, 60, 160)    # Purple border

GENIE_WIN_COLOR = (255, 60, 60)     # Red for genie wins
PLAYER_WIN_COLOR = (60, 255, 120)   # Green for player wins

# ── Font Sizes ───────────────────────────────────────────────────
FONT_SIZE_TITLE = 52
FONT_SIZE_SUBTITLE = 28
FONT_SIZE_BODY = 22
FONT_SIZE_INPUT = 24
FONT_SIZE_SMALL = 18
FONT_SIZE_COUNTER = 20

# ── Layout Constants ─────────────────────────────────────────────
GENIE_IMAGE_SIZE = (300, 300)       # Genie display size
GENIE_X = 40                        # Genie horizontal position
GENIE_Y = 120                        # Genie vertical position

DIALOGUE_X = 380
DIALOGUE_Y = 80
DIALOGUE_WIDTH = 380
DIALOGUE_HEIGHT = 300
DIALOGUE_PADDING = 20

INPUT_BOX_X = 40
INPUT_BOX_Y = 560
INPUT_BOX_WIDTH = 720
INPUT_BOX_HEIGHT = 60

COUNTER_X = 700
COUNTER_Y = 20

# ── Typing Animation ────────────────────────────────────────────
TYPING_SPEED = 30  # characters per second

# ── Asset Paths ──────────────────────────────────────────────────
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")

GENIE_IMAGES = {
    "idle": os.path.join(IMAGES_DIR, "genie_idle.png"),
    "casting": os.path.join(IMAGES_DIR, "genie_casting.png"),
    "genie_win": os.path.join(IMAGES_DIR, "genie_win.png"),
    "player_win": os.path.join(IMAGES_DIR, "genie_player_win.png"),
}

# ── Input Constraints ───────────────────────────────────────────
MAX_INPUT_LENGTH = 300
