import curses
import random
import json
import os
from datetime import date
from enum import Enum

COLS = 30
ROWS = 20
FOOD_SCORE = 10
MAX_NAME_LENGTH = 15
MAX_HIGHSCORES = 10
HIGHSCORE_FILE = "highscores.json"
TICK_RATES = {"easy": 0.2, "medium": 0.15, "hard": 0.1}


class GameState(Enum):
    NAME_INPUT = 1
    MAIN_MENU = 2
    PLAYING = 3
    PAUSED = 4
    GAME_OVER = 5
    LEADERBOARD = 6


class ScoreManager:
    def __init__(self):
        self.scores = []
        self._load_scores()

    def _load_scores(self):
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, "r") as f:
                    self.scores = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.scores = []
        else:
            self.scores = []
            self._save_scores()

    def _save_scores(self):
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump(self.scores, f, indent=2)

    def add_score(self, name, score):
        entry = {"name": name, "score": score, "date": date.today().isoformat()}
        self.scores.append(entry)
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:MAX_HIGHSCORES]
        self._save_scores()

    def get_top_scores(self):
        return self.scores[:MAX_HIGHSCORES]

    def is_high_score(self, score):
        if len(self.scores) < MAX_HIGHSCORES:
            return True
        return score > self.scores[-1]["score"]


class Snake:
    def __init__(self):
        self.segments = []
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.growing = False
        self.reset()

    def reset(self):
        center_x = COLS // 2
        center_y = ROWS // 2
        self.segments = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y),
        ]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.growing = False

    def set_direction(self, direction):
        opposite = (-direction[0], -direction[1])
        if self.direction != opposite:
            self.next_direction = direction

    def move(self):
        self.direction = self.next_direction
        head = self.segments[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        if self.growing:
            self.segments = [new_head] + self.segments
            self.growing = False
        else:
            self.segments = [new_head] + self.segments[:-1]

    def grow(self):
        self.growing = True

    def check_collision(self):
        head = self.segments[0]
        if head[0] < 0 or head[0] >= COLS or head[1] < 0 or head[1] >= ROWS:
            return True
        if head in self.segments[1:]:
            return True
        return False

    def get_head(self):
        return self.segments[0]


class TUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.timeout(0)
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        self.snake = Snake()
        self.food_pos = (0, 0)
        self.score_manager = ScoreManager()
        self.score = 0
        self.player_name = ""
        self.current_state = GameState.NAME_INPUT
        self.speed_mode = "medium"
        self.menu_selection = 0
        self.difficulty_selection = 1
        self.session_names = set()
        self.is_high_score = False
        self.show_leaderboard = False
        self.name_input = ""
        self.name_error = ""
        self.game_loop = None

        self._spawn_food()

    def _spawn_food(self):
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in self.snake.segments:
                self.food_pos = pos
                break

    def _get_input_char(self):
        try:
            return self.stdscr.getch()
        except curses.error:
            return -1

    def _draw_border(self):
        height, width = self.stdscr.getmaxyx()
        border_win = curses.newwin(height, width, 0, 0)
        border_win.clear()
        border_win.border()
        border_win.refresh()

    def _draw_game_area(self, offset_y=0, offset_x=0):
        height, width = self.stdscr.getmaxyx()
        game_height = ROWS + 4
        game_width = COLS + 4

        max_y = min(game_height, height - 2)
        max_x = min(game_width, width - 2)
        start_y = (height - max_y) // 2
        start_x = (width - max_x) // 2

        for y in range(start_y, start_y + max_y):
            for x in range(start_x, start_x + max_x):
                try:
                    if y == start_y or y == start_y + max_y - 1:
                        self.stdscr.addch(y, x, "#")
                    elif x == start_x or x == start_x + max_x - 1:
                        self.stdscr.addch(y, x, "#")
                except curses.error:
                    pass

    def _draw_frame(self, start_y, start_x, height, width):
        for x in range(start_x, start_x + width):
            try:
                self.stdscr.addch(start_y, x, "+")
                self.stdscr.addch(start_y + height - 1, x, "+")
            except curses.error:
                pass
        for y in range(start_y, start_y + height):
            try:
                self.stdscr.addch(y, start_x, "+")
                self.stdscr.addch(y, start_x + width - 1, "+")
            except curses.error:
                pass

    def _centered_text(self, text, y):
        height, width = self.stdscr.getmaxyx()
        x = (width - len(text)) // 2
        try:
            self.stdscr.addstr(y, max(0, x), text)
        except curses.error:
            pass

    def _clear_area(self, start_y, end_y):
        height, width = self.stdscr.getmaxyx()
        for y in range(start_y, end_y):
            try:
                self.stdscr.addstr(y, 0, " " * (width - 1))
            except curses.error:
                pass

    def draw_name_input(self):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        self._centered_text("=== PySnake TUI ===", 2)
        self._centered_text("ENTER YOUR NAME", height // 2 - 4)
        self._centered_text(f"Name: {self.name_input}_", height // 2 - 2)

        if self.name_error:
            self._centered_text(self.name_error, height // 2)

        self._centered_text("(Max 15 chars, alphanumeric)", height // 2 + 2)
        self._centered_text("Press ENTER to confirm", height // 2 + 4)
        self.stdscr.refresh()

    def draw_main_menu(self):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        self._centered_text("=== PySnake TUI ===", 2)

        options = ["PLAY", "LEADERBOARD", "QUIT"]
        if self.show_leaderboard:
            options = ["BACK", "QUIT"]
            self.menu_selection = min(self.menu_selection, 1)

        for i, option in enumerate(options):
            prefix = "> " if i == self.menu_selection else "  "
            self._centered_text(f"{prefix}{option}", height // 2 - 2 + i * 2)

        if self.show_leaderboard:
            self.draw_leaderboard_internal(height // 2 + 4)
        else:
            self._centered_text(f"Speed: {self.speed_mode.upper()}", height // 2 + 8)
            self._centered_text("Use UP/DOWN to change speed", height // 2 + 10)

        self.stdscr.refresh()

    def draw_leaderboard_internal(self, start_y):
        scores = self.score_manager.get_top_scores()
        self._centered_text("--- LEADERBOARD ---", start_y)
        start_y += 2

        if not scores:
            self._centered_text("No scores yet!", start_y)
            return

        for i, entry in enumerate(scores):
            text = f"{i + 1}. {entry['name']:<15} {entry['score']:>5}  {entry['date']}"
            self._centered_text(text, start_y + i)
            if start_y + i + 2 > self.stdscr.getmaxyx()[0]:
                break

    def draw_game(self):
        height, width = self.stdscr.getmaxyx()
        self.stdscr.clear()

        header_y = 1
        self._centered_text(
            f"{self.player_name} | Score: {self.score} | Speed: {self.speed_mode.upper()}",
            header_y,
        )

        border_top = 3
        border_left = max(0, (width - COLS) // 2 - 1)

        for x in range(border_left, border_left + COLS + 2):
            try:
                self.stdscr.addch(border_top, x, "#")
                self.stdscr.addch(border_top + ROWS + 1, x, "#")
            except curses.error:
                pass
        for y in range(border_top + 1, border_top + ROWS + 1):
            try:
                self.stdscr.addch(y, border_left, "#")
                self.stdscr.addch(y, border_left + COLS + 1, "#")
            except curses.error:
                pass

        for segment in self.snake.segments:
            try:
                y = border_top + 1 + segment[1]
                x = border_left + 1 + segment[0]
                if 0 < y < height - 1 and 0 < x < width - 1:
                    self.stdscr.addch(y, x, "#")
            except curses.error:
                pass

        try:
            food_y = border_top + 1 + self.food_pos[1]
            food_x = border_left + 1 + self.food_pos[0]
            if 0 < food_y < height - 1 and 0 < food_x < width - 1:
                self.stdscr.addch(food_y, food_x, "@")
        except curses.error:
            pass

        controls_y = border_top + ROWS + 3
        if controls_y < height - 1:
            self._centered_text("Arrow Keys: Move | P: Pause | ESC: Menu", controls_y)

        self.stdscr.refresh()

    def draw_paused(self):
        height, width = self.stdscr.getmaxyx()
        self.draw_game()

        self.stdscr.attron(curses.A_REVERSE)
        self._centered_text("      PAUSED      ", height // 2)
        self.stdscr.attroff(curses.A_REVERSE)
        self._centered_text("Press P to resume", height // 2 + 2)
        self._centered_text("Press ESC for menu", height // 2 + 4)
        self.stdscr.refresh()

    def draw_game_over(self):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        self.stdscr.attron(curses.A_BOLD)
        self._centered_text("========== GAME OVER ==========", height // 2 - 8)
        self.stdscr.attroff(curses.A_BOLD)

        self._centered_text(f"Final Score: {self.score}", height // 2 - 4)

        if self.is_high_score and self.score > 0:
            self.stdscr.attron(curses.A_BLINK)
            self._centered_text("*** NEW HIGH SCORE! ***", height // 2 - 2)
            self.stdscr.attroff(curses.A_BLINK)

        self._centered_text("--- TOP SCORES ---", height // 2 + 2)
        self.draw_leaderboard_internal(height // 2 + 4)

        self._centered_text("Press ENTER to retry", height - 6)
        self._centered_text("Press ESC for menu", height - 4)
        self.stdscr.refresh()

    def handle_name_input(self, key):
        if key in (curses.KEY_ENTER, 10, 13):
            if not self.name_input.strip():
                self.name_error = "Name cannot be empty!"
                curses.beep()
            elif not self.name_input.replace(" ", "").isalnum():
                self.name_error = "Use letters and numbers only!"
                curses.beep()
            elif self.name_input in self.session_names:
                self.name_error = "Name already used this session!"
                curses.beep()
            else:
                self.player_name = self.name_input
                self.session_names.add(self.name_input)
                self.current_state = GameState.MAIN_MENU
                curses.beep()
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            self.name_input = self.name_input[:-1]
            self.name_error = ""
        elif len(self.name_input) < MAX_NAME_LENGTH and chr(key).isprintable():
            self.name_input += chr(key)
            self.name_error = ""

    def handle_main_menu(self, key):
        if key == curses.KEY_UP:
            self.menu_selection = (self.menu_selection - 1) % (
                3 if not self.show_leaderboard else 2
            )
            curses.beep()
        elif key == curses.KEY_DOWN:
            self.menu_selection = (self.menu_selection + 1) % (
                3 if not self.show_leaderboard else 2
            )
            curses.beep()
        elif key in (curses.KEY_ENTER, 10, 13):
            curses.beep()
            if self.show_leaderboard:
                if self.menu_selection == 0:
                    self.show_leaderboard = False
                    self.menu_selection = 1
                elif self.menu_selection == 1:
                    return "quit"
            else:
                if self.menu_selection == 0:
                    self.current_state = GameState.PLAYING
                    self.snake.reset()
                    self._spawn_food()
                    self.score = 0
                    self.is_high_score = False
                elif self.menu_selection == 1:
                    self.show_leaderboard = not self.show_leaderboard
                elif self.menu_selection == 2:
                    return "quit"
        elif key in (curses.KEY_LEFT, curses.KEY_RIGHT) and not self.show_leaderboard:
            if key == curses.KEY_LEFT:
                self.difficulty_selection = (self.difficulty_selection - 1) % 3
            else:
                self.difficulty_selection = (self.difficulty_selection + 1) % 3
            self.speed_mode = list(TICK_RATES.keys())[self.difficulty_selection]
            curses.beep()
        return None

    def handle_playing(self, key):
        if key == ord("p") or key == ord("P"):
            self.current_state = GameState.PAUSED
            curses.beep()
        elif key == 27:
            self.current_state = GameState.MAIN_MENU
            self.menu_selection = 0
            curses.beep()
        elif key == curses.KEY_UP:
            self.snake.set_direction((0, -1))
        elif key == curses.KEY_DOWN:
            self.snake.set_direction((0, 1))
        elif key == curses.KEY_LEFT:
            self.snake.set_direction((-1, 0))
        elif key == curses.KEY_RIGHT:
            self.snake.set_direction((1, 0))

    def handle_paused(self, key):
        if key == ord("p") or key == ord("P"):
            self.current_state = GameState.PLAYING
            curses.beep()
        elif key == 27:
            self.current_state = GameState.MAIN_MENU
            self.menu_selection = 0
            curses.beep()

    def handle_game_over(self, key):
        if key in (curses.KEY_ENTER, 10, 13):
            self.current_state = GameState.PLAYING
            self.snake.reset()
            self._spawn_food()
            self.score = 0
            self.is_high_score = False
            curses.beep()
        elif key == 27:
            self.current_state = GameState.MAIN_MENU
            self.menu_selection = 0
            curses.beep()

    def flash_effect(self):
        try:
            self.stdscr.bkgd(" ", curses.A_REVERSE)
            self.stdscr.noutrefresh()
            curses.doupdate()
            curses.napms(100)
            self.stdscr.bkgd(" ", curses.A_NORMAL)
            self.stdscr.noutrefresh()
            curses.doupdate()
        except curses.error:
            pass

    def game_tick(self):
        self.snake.move()

        if self.snake.check_collision():
            self.flash_effect()
            curses.beep()
            curses.beep()
            self.is_high_score = self.score_manager.is_high_score(self.score)
            if self.is_high_score and self.score > 0:
                self.score_manager.add_score(self.player_name, self.score)
            self.current_state = GameState.GAME_OVER
            return

        if self.snake.get_head() == self.food_pos:
            self.snake.grow()
            self.score += FOOD_SCORE
            curses.beep()
            self._spawn_food()

    def run(self):
        self.game_loop = curses.wrapper(self._run_game)

    def _run_game(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.timeout(0)
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)

        tick_rate = TICK_RATES[self.speed_mode]
        last_tick = 0

        running = True
        while running:
            current_time = curses.napms(1) or 0

            key = self._get_input_char()

            if self.current_state == GameState.NAME_INPUT:
                if key != -1:
                    self.handle_name_input(key)
                self.draw_name_input()

            elif self.current_state == GameState.MAIN_MENU:
                if key != -1:
                    result = self.handle_main_menu(key)
                    if result == "quit":
                        running = False
                        continue
                    if not self.show_leaderboard:
                        self.speed_mode = list(TICK_RATES.keys())[
                            self.difficulty_selection
                        ]
                self.draw_main_menu()

            elif self.current_state == GameState.PLAYING:
                self.handle_playing(key)
                self.draw_game()

            elif self.current_state == GameState.PAUSED:
                self.handle_paused(key)
                self.draw_paused()

            elif self.current_state == GameState.GAME_OVER:
                if key != -1:
                    self.handle_game_over(key)
                self.draw_game_over()

            curses.napms(int(tick_rate * 1000))
