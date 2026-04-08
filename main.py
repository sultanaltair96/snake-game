#!/usr/bin/env python3
import sys
import os


def run_tui():
    from tui import TUI

    tui = TUI(None)
    curses_wrapper = __import__("curses").wrapper

    def run(stdscr):
        tui._run_game(stdscr)

    curses_wrapper(run)


def run_pygame_fallback():
    try:
        import pygame
        import sys as _sys
        from game import (
            GameState,
            StateManager,
            Snake,
            Food,
            ScoreManager,
            SoundManager,
            ScreenEffects,
            UI,
            COLORS,
            WINDOW_SIZE,
            FOOD_SCORE,
            MAX_NAME_LENGTH,
        )

        pygame.init()
        screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("PySnake")
        clock = pygame.time.Clock()

        state_manager = StateManager()
        snake = Snake()
        food = Food()
        score_manager = ScoreManager()
        sound_manager = SoundManager()
        screen_effects = ScreenEffects()
        ui = UI()

        name_input = ""
        name_error = ""
        show_leaderboard = False
        menu_selection = 0
        is_high_score = False

        food.spawn(snake.segments)

        running = True
        while running:
            dt = clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if state_manager.current_state == GameState.NAME_INPUT:
                        if event.key == pygame.K_RETURN:
                            if not name_input.strip():
                                name_error = "Name cannot be empty"
                                sound_manager.play_click()
                            elif not name_input.isalnum():
                                name_error = "Use only letters and numbers"
                                sound_manager.play_click()
                            elif state_manager.is_name_duplicate(name_input):
                                name_error = "Name already used this session"
                                sound_manager.play_click()
                            else:
                                state_manager.set_name(name_input)
                                state_manager.set_state(GameState.MAIN_MENU)
                                sound_manager.play_click()
                        elif event.key == pygame.K_BACKSPACE:
                            name_input = name_input[:-1]
                            name_error = ""
                        elif len(name_input) < MAX_NAME_LENGTH:
                            if event.unicode.isalnum():
                                name_input += event.unicode
                                name_error = ""

                    elif state_manager.current_state == GameState.MAIN_MENU:
                        if event.key == pygame.K_UP:
                            menu_selection = (menu_selection - 1) % 3
                            sound_manager.play_click()
                        elif event.key == pygame.K_DOWN:
                            menu_selection = (menu_selection + 1) % 3
                            sound_manager.play_click()
                        elif event.key == pygame.K_RETURN:
                            if menu_selection == 0:
                                state_manager.set_state(GameState.PLAYING)
                                snake.reset()
                                food.spawn(snake.segments)
                                state_manager.reset_game()
                                show_leaderboard = False
                                is_high_score = False
                                sound_manager.play_click()
                            elif menu_selection == 1:
                                show_leaderboard = not show_leaderboard
                                sound_manager.play_click()
                            elif menu_selection == 2:
                                running = False
                                sound_manager.play_click()

                    elif state_manager.current_state == GameState.PLAYING:
                        if event.key == pygame.K_p:
                            state_manager.is_paused = not state_manager.is_paused
                            sound_manager.play_click()
                        elif event.key == pygame.K_ESCAPE:
                            state_manager.set_state(GameState.MAIN_MENU)
                            sound_manager.play_click()
                        elif not state_manager.is_paused:
                            if event.key == pygame.K_UP:
                                snake.set_direction((0, -1))
                            elif event.key == pygame.K_DOWN:
                                snake.set_direction((0, 1))
                            elif event.key == pygame.K_LEFT:
                                snake.set_direction((-1, 0))
                            elif event.key == pygame.K_RIGHT:
                                snake.set_direction((1, 0))

                    elif state_manager.current_state == GameState.GAME_OVER:
                        if event.key == pygame.K_RETURN:
                            state_manager.set_state(GameState.PLAYING)
                            snake.reset()
                            food.spawn(snake.segments)
                            state_manager.reset_game()
                            is_high_score = False
                            sound_manager.play_click()
                        elif event.key == pygame.K_ESCAPE:
                            state_manager.set_state(GameState.MAIN_MENU)
                            menu_selection = 0
                            sound_manager.play_click()

            if state_manager.current_state == GameState.NAME_INPUT:
                screen.fill(COLORS["background"])
                ui.draw_name_input(screen, name_input, name_error)

            elif state_manager.current_state == GameState.MAIN_MENU:
                screen.fill(COLORS["background"])
                ui.draw_main_menu(screen, menu_selection)
                if show_leaderboard:
                    ui.draw_leaderboard(screen, score_manager.get_top_scores())

            elif state_manager.current_state == GameState.PLAYING:
                if not state_manager.is_paused:
                    snake.move()

                    if snake.check_collision():
                        screen_effects.trigger_shake()
                        sound_manager.play_game_over()
                        is_high_score = score_manager.is_high_score(state_manager.score)
                        if is_high_score:
                            score_manager.add_score(
                                state_manager.player_name, state_manager.score
                            )
                        state_manager.set_state(GameState.GAME_OVER)

                    if snake.get_head() == food.position:
                        snake.grow()
                        state_manager.score += FOOD_SCORE
                        sound_manager.play_eat()
                        food.spawn(snake.segments)

                    food.update(dt)
                    screen_effects.update()

                offset = screen_effects.get_offset()
                screen.fill(COLORS["background"])
                screen.blit(screen, offset)

                surface = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
                surface.fill(COLORS["background"])
                ui.draw_grid(surface)
                ui.draw_score(surface, state_manager.score, state_manager.player_name)
                snake.draw(surface)
                food.draw(surface)

                screen.blit(surface, offset)

                if state_manager.is_paused:
                    ui.draw_paused(screen)

            elif state_manager.current_state == GameState.GAME_OVER:
                ui.draw_game_over(screen, state_manager.score, is_high_score)
                ui.draw_leaderboard(screen, score_manager.get_top_scores())

            pygame.display.flip()

        pygame.quit()
        _sys.exit()
    except ImportError:
        print("Error: Neither curses nor pygame is available.")
        print("For TUI: This terminal may not support curses.")
        print("For GUI: Install pygame with: pip install pygame")
        sys.exit(1)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--pygame":
        run_pygame_fallback()
        return

    if os.environ.get("TERM") in (None, "", "dumb"):
        print("No terminal detected. Use --pygame flag for GUI mode.")
        sys.exit(1)

    try:
        import curses

        curses.initscr()
        curses.endwin()
        run_tui()
    except curses.error:
        print("Curses not supported in this environment.")
        print("Try: python main.py --pygame (requires pygame)")
        sys.exit(1)
    except ImportError:
        print("Curses module not available.")
        print("Try: python main.py --pygame (requires pygame)")
        sys.exit(1)


if __name__ == "__main__":
    main()
