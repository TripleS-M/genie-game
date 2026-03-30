"""
main.py — Main game loop for The Fine Print.

Handles Pygame initialization, event processing, state management,
and rendering. Orchestrates all other frontend modules.
"""

import pygame
import sys
from settings import *
from game_state import GameManager, GameState
from api import send_wish
from ui import (
    load_genie_images,
    get_fonts,
    draw_gradient_bg,
    draw_stars,
    draw_genie,
    draw_particles,
    DialogueBox,
    InputBox,
    draw_wish_counter,
    draw_intro_screen,
    draw_casting_overlay,
    draw_result_indicator,
    draw_continue_prompt,
    draw_game_over_screen,
)


def main():
    """Main entry point for the game."""
    # ── Initialize Pygame ────────────────────────────────────────
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # ── Pre-render background (performance optimization) ─────────
    bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    draw_gradient_bg(bg_surface)

    # ── Load assets ──────────────────────────────────────────────
    genie_images = load_genie_images()
    fonts = get_fonts()

    # ── Initialize game objects ──────────────────────────────────
    game = GameManager()
    dialogue = DialogueBox(fonts)
    input_box = InputBox(fonts)
    current_request = None  # Active WishRequest during CASTING state
    tick = 0  # Frame counter for animations

    # Set intro dialogue
    dialogue.set_text("Greetings, mortal! I am the Genie of the Fine Print. "
                      "I shall grant you three wishes... but choose your words wisely!")

    # ── Main Game Loop ───────────────────────────────────────────
    running = True
    while running:
        dt = clock.tick(FPS)
        tick += 1

        # ── Event Handling ───────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # ── INTRO state ──────────────────────────────────
                if game.state == GameState.INTRO:
                    if event.key == pygame.K_RETURN:
                        game.start_game()
                        input_box.clear()
                        dialogue.set_text("What is your first wish, mortal?")
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        game.difficulty = "hard" if game.difficulty == "regular" else "regular"

                # ── INPUT state ──────────────────────────────────
                elif game.state == GameState.INPUT:
                    submitted = input_box.handle_event(event)
                    if submitted:
                        game.submit_wish(submitted)
                        dialogue.set_text("")
                        current_request = send_wish(submitted, game.difficulty)

                # ── CASTING state ────────────────────────────────
                elif game.state == GameState.CASTING:
                    pass  # No input during casting

                # ── RESULT state ─────────────────────────────────
                elif game.state == GameState.RESULT:
                    if event.key == pygame.K_RETURN:
                        if not dialogue.fully_revealed:
                            dialogue.skip_animation()
                        else:
                            game.next_wish()
                            if game.state == GameState.INPUT:
                                wish_num = game.wish_count
                                ordinals = {1: "first", 2: "second", 3: "third"}
                                ordinal = ordinals.get(wish_num, f"#{wish_num}")
                                dialogue.set_text(f"Very well... what is your {ordinal} wish?")
                                input_box.clear()
                            elif game.state == GameState.GAME_OVER:
                                dialogue.set_text("")

                # ── GAME_OVER state ──────────────────────────────
                elif game.state == GameState.GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        game.reset()
                        dialogue.set_text("Greetings, mortal! I am the Genie of the Fine Print. "
                                          "I shall grant you three wishes... but choose your words wisely!")
                        input_box.clear()

        # ── Update Logic ────────────────────────────────────────
        # Check if casting request is done
        if game.state == GameState.CASTING and current_request:
            if current_request.is_done():
                result = current_request.get_result()
                game.receive_result(result["response"], result["result"])
                dialogue.set_text(result["response"])
                current_request = None

        # Update dialogue typing animation
        dialogue.update()

        # ── Rendering ───────────────────────────────────────────
        # Background
        screen.blit(bg_surface, (0, 0))
        draw_stars(screen, tick)

        # Get current genie visual state
        genie_state = game.get_genie_state()

        # Particles
        draw_particles(screen, tick, genie_state)

        if game.state == GameState.GAME_OVER:
            # ── Game Over Screen ────────────────────────────────
            draw_genie(screen, genie_images, genie_state, tick)
            draw_game_over_screen(screen, fonts, tick,
                                  game.player_score, game.genie_score,
                                  game.get_winner(), game.wish_history)
        else:
            # ── Regular Game Screens ─────────────────────────────
            # Genie (only show outside intro screen)
            if game.state != GameState.INTRO:
                draw_genie(screen, genie_images, genie_state, tick)

            # Wish counter (visible during gameplay)
            if game.state in (GameState.INPUT, GameState.CASTING, GameState.RESULT):
                draw_wish_counter(screen, fonts, game.wish_count, MAX_WISHES)

            # State-specific rendering
            if game.state == GameState.INTRO:
                draw_intro_screen(screen, fonts, tick, game.difficulty)

            elif game.state == GameState.INPUT:
                # Dialogue box and input
                result_color = None
                dialogue.draw(screen, result_color)
                input_box.draw(screen, tick)

            elif game.state == GameState.CASTING:
                # Casting animation
                draw_casting_overlay(screen, fonts, tick)

            elif game.state == GameState.RESULT:
                # Result display
                result_color = GENIE_WIN_COLOR if game.current_result == "genie_win" else PLAYER_WIN_COLOR
                draw_result_indicator(screen, fonts, game.current_result, tick)
                dialogue.draw(screen, result_color)
                if dialogue.fully_revealed:
                    draw_continue_prompt(screen, fonts, tick)

        # ── Flip Display ────────────────────────────────────────
        pygame.display.flip()

    # ── Cleanup ──────────────────────────────────────────────────
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
