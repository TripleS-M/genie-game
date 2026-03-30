"""
ui.py — UI rendering for The Fine Print.

Handles all visual elements: genie images, dialogue boxes, input field,
wish counter, intro screen, game over screen, and casting animation.
"""

import pygame
import math
import time
from settings import *


def load_genie_images() -> dict:
    """Load and scale all genie state images."""
    images = {}
    for state, path in GENIE_IMAGES.items():
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(img, GENIE_IMAGE_SIZE)
            
            # Create a circular mask and blit using BLEND_RGBA_MIN
            circular_image = pygame.Surface(GENIE_IMAGE_SIZE, pygame.SRCALPHA)
            pygame.draw.circle(circular_image, (255, 255, 255, 255), (GENIE_IMAGE_SIZE[0]//2, GENIE_IMAGE_SIZE[1]//2), GENIE_IMAGE_SIZE[0]//2)
            circular_image.blit(img, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            
            images[state] = circular_image
        except (pygame.error, FileNotFoundError) as e:
            print(f"Warning: Could not load genie image for '{state}': {e}")
            # Create a placeholder surface
            surf = pygame.Surface(GENIE_IMAGE_SIZE, pygame.SRCALPHA)
            surf.fill((80, 40, 120, 200))
            images[state] = surf
    return images


def get_fonts() -> dict:
    """Initialize and return all fonts used in the game."""
    pygame.font.init()
    
    # Try to use a nice system font, fallback to default
    font_name = None
    for name in ["segoeui", "arial", "helvetica", "verdana"]:
        if name in [f.lower() for f in pygame.font.get_fonts()]:
            font_name = name
            break
    
    return {
        "title": pygame.font.SysFont(font_name, FONT_SIZE_TITLE, bold=True),
        "subtitle": pygame.font.SysFont(font_name, FONT_SIZE_SUBTITLE),
        "body": pygame.font.SysFont(font_name, FONT_SIZE_BODY),
        "input": pygame.font.SysFont(font_name, FONT_SIZE_INPUT),
        "small": pygame.font.SysFont(font_name, FONT_SIZE_SMALL),
        "counter": pygame.font.SysFont(font_name, FONT_SIZE_COUNTER, bold=True),
    }


def draw_gradient_bg(surface: pygame.Surface):
    """Draw a vertical gradient background."""
    height = surface.get_height()
    width = surface.get_width()
    for y in range(height):
        ratio = y / height
        r = int(BG_GRADIENT_TOP[0] + (BG_GRADIENT_BOTTOM[0] - BG_GRADIENT_TOP[0]) * ratio)
        g = int(BG_GRADIENT_TOP[1] + (BG_GRADIENT_BOTTOM[1] - BG_GRADIENT_TOP[1]) * ratio)
        b = int(BG_GRADIENT_TOP[2] + (BG_GRADIENT_BOTTOM[2] - BG_GRADIENT_TOP[2]) * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))


def draw_stars(surface: pygame.Surface, tick: int):
    """Draw twinkling stars on the background."""
    import random
    random.seed(42)  # Consistent star positions
    for i in range(50):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        # Twinkle effect
        brightness = int(120 + 80 * math.sin((tick + i * 37) * 0.02))
        brightness = max(60, min(255, brightness))
        size = 1 if i % 3 != 0 else 2
        color = (brightness, brightness, int(brightness * 0.9))
        pygame.draw.circle(surface, color, (x, y), size)


def draw_genie(surface: pygame.Surface, images: dict, state: str, tick: int):
    """Draw the genie image with appropriate effects based on state."""
    if state not in images:
        state = "idle"
    
    image = images[state]
    x = GENIE_X
    y = GENIE_Y

    # Floating animation (subtle bob up and down)
    float_offset = int(5 * math.sin(tick * 0.03))
    y += float_offset

    # Glow effect behind the genie
    glow_radius = GENIE_IMAGE_SIZE[0] // 2 + 20
    glow_center = (x + GENIE_IMAGE_SIZE[0] // 2, y + GENIE_IMAGE_SIZE[1] // 2)
    
    if state == "casting":
        # Pulsing bright purple glow
        alpha = int(60 + 40 * math.sin(tick * 0.1))
        glow_color = (*PURPLE_GLOW, alpha)
    elif state == "genie_win":
        glow_color = (255, 40, 40, 50)
    elif state == "player_win":
        glow_color = (40, 255, 100, 50)
    else:
        glow_color = (*PURPLE, 30)

    # Draw glow as a circle
    glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, glow_color, (glow_radius, glow_radius), glow_radius)
    surface.blit(glow_surf, (glow_center[0] - glow_radius, glow_center[1] - glow_radius))

    surface.blit(image, (x, y))


def draw_particles(surface: pygame.Surface, tick: int, state: str):
    """Draw floating magical particles."""
    if state == "casting":
        # More intense particles during casting
        num_particles = 20
        colors = [GOLD, PURPLE_GLOW, TEXT_WHITE]
    elif state == "genie_win":
        num_particles = 10
        colors = [GENIE_WIN_COLOR, GOLD_DARK]
    elif state == "player_win":
        num_particles = 15
        colors = [PLAYER_WIN_COLOR, GOLD]
    else:
        num_particles = 8
        colors = [GOLD_DIM, PURPLE]

    for i in range(num_particles):
        phase = (tick * 0.02 + i * 1.7) % (2 * math.pi)
        x = int(SCREEN_WIDTH // 2 + 250 * math.sin(phase + i * 0.8))
        y_base = 180 + i * 20
        y = int(y_base + 15 * math.cos(tick * 0.03 + i))
        
        if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
            color = colors[i % len(colors)]
            size = 2 + int(1.5 * abs(math.sin(tick * 0.05 + i)))
            alpha = int(100 + 100 * abs(math.sin(tick * 0.04 + i * 0.5)))
            
            particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, (*color, min(alpha, 255)), (size, size), size)
            surface.blit(particle_surf, (x - size, y - size))


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list:
    """Wrap text to fit within a given pixel width."""
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


class DialogueBox:
    """Renders dialogue text with a typing animation effect."""

    def __init__(self, fonts: dict):
        self.fonts = fonts
        self.text = ""
        self.start_time = 0
        self.chars_revealed = 0
        self.fully_revealed = False

    def set_text(self, text: str):
        """Set new dialogue text and reset typing animation."""
        self.text = text
        self.start_time = time.time()
        self.chars_revealed = 0
        self.fully_revealed = False

    def skip_animation(self):
        """Skip to fully revealed text."""
        self.fully_revealed = True
        self.chars_revealed = len(self.text)

    def update(self):
        """Update the typing animation."""
        if not self.fully_revealed and self.text:
            elapsed = time.time() - self.start_time
            self.chars_revealed = min(int(elapsed * TYPING_SPEED), len(self.text))
            if self.chars_revealed >= len(self.text):
                self.fully_revealed = True

    def draw(self, surface: pygame.Surface, result_color=None):
        """Draw the dialogue box with current text."""
        # Draw box background
        box_rect = pygame.Rect(DIALOGUE_X, DIALOGUE_Y, DIALOGUE_WIDTH, DIALOGUE_HEIGHT)
        box_surf = pygame.Surface((DIALOGUE_WIDTH, DIALOGUE_HEIGHT), pygame.SRCALPHA)
        box_surf.fill((20, 15, 40, 220))
        surface.blit(box_surf, (DIALOGUE_X, DIALOGUE_Y))

        # Draw border
        border_color = result_color if result_color else DIALOGUE_BORDER
        pygame.draw.rect(surface, border_color, box_rect, 2, border_radius=8)

        # Draw corner accents
        accent_len = 15
        corners = [
            (DIALOGUE_X, DIALOGUE_Y),
            (DIALOGUE_X + DIALOGUE_WIDTH, DIALOGUE_Y),
            (DIALOGUE_X, DIALOGUE_Y + DIALOGUE_HEIGHT),
            (DIALOGUE_X + DIALOGUE_WIDTH, DIALOGUE_Y + DIALOGUE_HEIGHT),
        ]
        for cx, cy in corners:
            dx = 1 if cx == DIALOGUE_X else -1
            dy = 1 if cy == DIALOGUE_Y else -1
            pygame.draw.line(surface, GOLD, (cx, cy), (cx + accent_len * dx, cy), 2)
            pygame.draw.line(surface, GOLD, (cx, cy), (cx, cy + accent_len * dy), 2)

        # Draw text (with typing animation)
        visible_text = self.text[:self.chars_revealed]
        if visible_text:
            lines = wrap_text(visible_text, self.fonts["body"], DIALOGUE_WIDTH - DIALOGUE_PADDING * 2)
            for i, line in enumerate(lines):
                text_surf = self.fonts["body"].render(line, True, TEXT_WHITE)
                y = DIALOGUE_Y + DIALOGUE_PADDING + i * 30
                if y + 30 < DIALOGUE_Y + DIALOGUE_HEIGHT - DIALOGUE_PADDING:
                    surface.blit(text_surf, (DIALOGUE_X + DIALOGUE_PADDING, y))

        # Draw blinking cursor during typing
        if not self.fully_revealed and self.text:
            if int(time.time() * 3) % 2 == 0:
                cursor_x = DIALOGUE_X + DIALOGUE_PADDING
                if visible_text:
                    last_line = wrap_text(visible_text, self.fonts["body"], DIALOGUE_WIDTH - DIALOGUE_PADDING * 2)
                    if last_line:
                        cursor_x += self.fonts["body"].size(last_line[-1])[0]
                cursor_y = DIALOGUE_Y + DIALOGUE_PADDING + (len(wrap_text(visible_text, self.fonts["body"], DIALOGUE_WIDTH - DIALOGUE_PADDING * 2)) - 1) * 30 if visible_text else DIALOGUE_Y + DIALOGUE_PADDING
                pygame.draw.rect(surface, GOLD, (cursor_x, cursor_y, 2, 24))


class InputBox:
    """Text input box for player wishes."""

    def __init__(self, fonts: dict):
        self.fonts = fonts
        self.text = ""
        self.active = True
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event: pygame.event) -> str | None:
        """
        Handle keyboard input. Returns the text if Enter is pressed.
        """
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                if self.text.strip():
                    submitted = self.text
                    self.text = ""
                    return submitted
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < MAX_INPUT_LENGTH and event.unicode.isprintable():
                    self.text += event.unicode
        return None

    def clear(self):
        """Clear the input text."""
        self.text = ""

    def draw(self, surface: pygame.Surface, tick: int):
        """Draw the input box."""
        # Box background
        box_rect = pygame.Rect(INPUT_BOX_X, INPUT_BOX_Y, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT)
        border_color = INPUT_BOX_ACTIVE if self.active else INPUT_BOX_BORDER

        box_surf = pygame.Surface((INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT), pygame.SRCALPHA)
        box_surf.fill((*INPUT_BOX_BG, 240))
        surface.blit(box_surf, (INPUT_BOX_X, INPUT_BOX_Y))

        # Border with glow
        pygame.draw.rect(surface, border_color, box_rect, 2, border_radius=6)

        # Text
        display_text = self.text
        font = self.fonts["input"]

        # If text is too wide, show only the end
        while font.size(display_text)[0] > INPUT_BOX_WIDTH - 20 and display_text:
            display_text = display_text[1:]

        text_surf = font.render(display_text, True, TEXT_INPUT)
        surface.blit(text_surf, (INPUT_BOX_X + 10, INPUT_BOX_Y + 12))

        # Blinking cursor
        cursor_blink = int(tick * 0.06) % 2 == 0
        if self.active and cursor_blink:
            cursor_x = INPUT_BOX_X + 10 + font.size(display_text)[0]
            pygame.draw.rect(surface, GOLD, (cursor_x + 2, INPUT_BOX_Y + 10, 2, 30))

        # Placeholder text
        if not self.text:
            placeholder = font.render("Type your wish here...", True, TEXT_DIM)
            surface.blit(placeholder, (INPUT_BOX_X + 10, INPUT_BOX_Y + 12))

        # Prompt label
        prompt_text = self.fonts["small"].render("Press ENTER to submit your wish", True, TEXT_DIM)
        surface.blit(prompt_text, (INPUT_BOX_X, INPUT_BOX_Y + INPUT_BOX_HEIGHT + 8))

        # Character count
        count_text = self.fonts["small"].render(
            f"{len(self.text)}/{MAX_INPUT_LENGTH}", True, TEXT_DIM
        )
        surface.blit(count_text, (INPUT_BOX_X + INPUT_BOX_WIDTH - count_text.get_width(), INPUT_BOX_Y + INPUT_BOX_HEIGHT + 8))


def draw_wish_counter(surface: pygame.Surface, fonts: dict, current: int, maximum: int):
    """Draw the wish counter in the top-right corner."""
    # Background pill
    text = f"Wish {current} / {maximum}"
    text_surf = fonts["counter"].render(text, True, GOLD)
    
    pill_w = text_surf.get_width() + 24
    pill_h = text_surf.get_height() + 12
    pill_x = COUNTER_X - pill_w // 2
    pill_y = COUNTER_Y

    pill_surf = pygame.Surface((pill_w, pill_h), pygame.SRCALPHA)
    pygame.draw.rect(pill_surf, (40, 20, 70, 200), (0, 0, pill_w, pill_h), border_radius=12)
    pygame.draw.rect(pill_surf, GOLD_DARK, (0, 0, pill_w, pill_h), 1, border_radius=12)
    surface.blit(pill_surf, (pill_x, pill_y))

    surface.blit(text_surf, (pill_x + 12, pill_y + 6))


def draw_intro_screen(surface: pygame.Surface, fonts: dict, tick: int, selected_difficulty: str = "regular"):
    """Draw the intro/title screen."""
    # Title with glow effect
    title_text = "The Fine Print"
    
    # Glow behind title
    glow_alpha = int(40 + 20 * math.sin(tick * 0.03))
    glow_surf = fonts["title"].render(title_text, True, (*PURPLE_GLOW, glow_alpha))
    glow_rect = glow_surf.get_rect(center=(SCREEN_WIDTH // 2 + 2, 200 + 2))
    
    # Main title
    title_surf = fonts["title"].render(title_text, True, GOLD)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 200))
    surface.blit(title_surf, title_rect)

    # Subtitle
    subtitle_surf = fonts["subtitle"].render("A Genie Wish Game", True, PURPLE_GLOW)
    subtitle_rect = subtitle_surf.get_rect(center=(SCREEN_WIDTH // 2, 260))
    surface.blit(subtitle_surf, subtitle_rect)

    # Description lines
    desc_lines = [
        "You have been granted 3 wishes by a mystical genie.",
        "But beware — the genie will twist any flawed wish!",
        "Word your wishes carefully to outsmart the genie.",
    ]
    for i, line in enumerate(desc_lines):
        desc_surf = fonts["body"].render(line, True, TEXT_DIM)
        desc_rect = desc_surf.get_rect(center=(SCREEN_WIDTH // 2, 340 + i * 35))
        surface.blit(desc_surf, desc_rect)

    # Difficulty Selection
    y_offset = 430
    diff_text = fonts["body"].render("Use Up/Down Arrows to Select Difficulty", True, TEXT_DIM)
    surface.blit(diff_text, diff_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset)))
    
    # Regular Mode
    reg_color = GOLD if selected_difficulty == "regular" else (100, 100, 120)
    reg_text = f"> REGULAR <" if selected_difficulty == "regular" else "  REGULAR  "
    reg_surf = fonts["subtitle"].render(reg_text, True, reg_color)
    surface.blit(reg_surf, reg_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 40)))
    
    # Hard Mode
    hard_color = GOLD if selected_difficulty == "hard" else (100, 100, 120)
    hard_text = f"> HARD <" if selected_difficulty == "hard" else "  HARD  "
    hard_surf = fonts["subtitle"].render(hard_text, True, hard_color)
    surface.blit(hard_surf, hard_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 80)))

    # Pulsing "Press Enter" prompt
    alpha = int(140 + 115 * math.sin(tick * 0.05))
    prompt_color = (GOLD[0], GOLD[1], GOLD[2])
    prompt_surf = fonts["subtitle"].render("Press ENTER to begin", True, prompt_color)
    
    # Apply alpha via a surface
    alpha_surf = pygame.Surface(prompt_surf.get_size(), pygame.SRCALPHA)
    alpha_surf.blit(prompt_surf, (0, 0))
    alpha_surf.set_alpha(alpha)
    
    prompt_rect = alpha_surf.get_rect(center=(SCREEN_WIDTH // 2, 580))
    surface.blit(alpha_surf, prompt_rect)

    # Decorative line
    line_y = 290
    line_width = 300
    line_x = (SCREEN_WIDTH - line_width) // 2
    pygame.draw.line(surface, GOLD_DIM, (line_x, line_y), (line_x + line_width, line_y), 1)


def draw_casting_overlay(surface: pygame.Surface, fonts: dict, tick: int):
    """Draw the casting animation overlay."""
    # "Casting" text with pulsing
    scale = 1.0 + 0.05 * math.sin(tick * 0.08)
    text = "The genie ponders your wish..."
    cast_font = fonts["subtitle"]
    cast_surf = cast_font.render(text, True, PURPLE_GLOW)
    
    alpha = int(160 + 95 * math.sin(tick * 0.06))
    alpha_surf = pygame.Surface(cast_surf.get_size(), pygame.SRCALPHA)
    alpha_surf.blit(cast_surf, (0, 0))
    alpha_surf.set_alpha(alpha)
    
    rect = alpha_surf.get_rect(center=(SCREEN_WIDTH // 2, 560))
    surface.blit(alpha_surf, rect)

    # Spinning dots
    num_dots = 8
    center_x, center_y = SCREEN_WIDTH // 2, 600
    radius = 20
    for i in range(num_dots):
        angle = (tick * 0.05) + (i * 2 * math.pi / num_dots)
        dx = int(center_x + radius * math.cos(angle))
        dy = int(center_y + radius * math.sin(angle))
        dot_alpha = int(100 + 155 * ((i / num_dots + tick * 0.01) % 1.0))
        dot_surf = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(dot_surf, (*GOLD, min(dot_alpha, 255)), (4, 4), 3)
        surface.blit(dot_surf, (dx - 4, dy - 4))


def draw_result_indicator(surface: pygame.Surface, fonts: dict, result: str, tick: int):
    """Draw a result indicator (GENIE WINS / PLAYER WINS) above the dialogue."""
    if result == "genie_win":
        text = "GENIE WINS"
        color = GENIE_WIN_COLOR
    else:
        text = "YOU WIN!"
        color = PLAYER_WIN_COLOR

    result_surf = fonts["subtitle"].render(text, True, color)
    
    # Pulsing effect
    alpha = int(180 + 75 * math.sin(tick * 0.08))
    alpha_surf = pygame.Surface(result_surf.get_size(), pygame.SRCALPHA)
    alpha_surf.blit(result_surf, (0, 0))
    alpha_surf.set_alpha(alpha)
    
    rect = alpha_surf.get_rect(center=(SCREEN_WIDTH // 2, DIALOGUE_Y - 25))
    surface.blit(alpha_surf, rect)


def draw_continue_prompt(surface: pygame.Surface, fonts: dict, tick: int, text: str = "Press ENTER to continue"):
    """Draw a 'press enter to continue' prompt at the bottom."""
    alpha = int(120 + 135 * math.sin(tick * 0.05))
    prompt_surf = fonts["small"].render(text, True, TEXT_DIM)
    alpha_surf = pygame.Surface(prompt_surf.get_size(), pygame.SRCALPHA)
    alpha_surf.blit(prompt_surf, (0, 0))
    alpha_surf.set_alpha(alpha)
    rect = alpha_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
    surface.blit(alpha_surf, rect)


def draw_game_over_screen(surface: pygame.Surface, fonts: dict, tick: int,
                           player_score: int, genie_score: int, winner: str,
                           wish_history: list):
    """Draw the game over screen with final results."""
    # Title
    if winner == "player":
        title = "You Outsmarted the Genie!"
        title_color = PLAYER_WIN_COLOR
    elif winner == "genie":
        title = "The Genie Outsmarted You!"
        title_color = GENIE_WIN_COLOR
    else:
        title = "It's a Draw!"
        title_color = GOLD

    title_surf = fonts["title"].render(title, True, title_color)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 80))
    surface.blit(title_surf, title_rect)

    # Score display
    score_text = f"Player: {player_score}  |  Genie: {genie_score}"
    score_surf = fonts["subtitle"].render(score_text, True, TEXT_WHITE)
    score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 140))
    surface.blit(score_surf, score_rect)

    # Decorative line
    pygame.draw.line(surface, GOLD_DIM, (150, 170), (650, 170), 1)

    # Wish history summary
    y_offset = 200
    for i, wish in enumerate(wish_history):
        # Wish number
        wish_label = fonts["counter"].render(f"Wish {i + 1}:", True, GOLD)
        surface.blit(wish_label, (100, y_offset))

        # Result indicator
        if wish.result == "player_win":
            result_txt = "✓ You Won"
            result_color = PLAYER_WIN_COLOR
        else:
            result_txt = "✗ Genie Won"
            result_color = GENIE_WIN_COLOR

        result_surf = fonts["counter"].render(result_txt, True, result_color)
        surface.blit(result_surf, (600, y_offset))

        # Wish text (truncated)
        wish_text = wish.wish_text
        if len(wish_text) > 70:
            wish_text = wish_text[:67] + "..."
        wish_surf = fonts["small"].render(f'"{wish_text}"', True, TEXT_DIM)
        surface.blit(wish_surf, (120, y_offset + 28))

        y_offset += 70

    # Play again prompt
    draw_continue_prompt(surface, fonts, tick, "Press ENTER to play again")
