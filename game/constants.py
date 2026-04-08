import os

GRID_SIZE = 20
CELL_SIZE = 30
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

COLORS = {
    "background": (26, 26, 46),
    "grid": (22, 33, 62),
    "snake_head": (0, 255, 136),
    "snake_tail": (0, 170, 85),
    "food": (255, 71, 87),
    "text": (255, 255, 255),
    "score": (0, 212, 255),
    "ui_bg": (10, 10, 30),
}

SPEEDS = {
    "easy": 8,
    "medium": 12,
    "hard": 15,
}

HIGHSCORE_FILE = "highscores.json"

SCREEN_SHAKE_AMPLITUDE = 10
SCREEN_SHAKE_DURATION = 300

FOOD_SCORE = 10
MAX_NAME_LENGTH = 15
MAX_HIGHSCORES = 10
