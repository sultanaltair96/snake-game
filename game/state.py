import pygame
from enum import Enum
from .constants import SPEEDS


class GameState(Enum):
    NAME_INPUT = 1
    MAIN_MENU = 2
    PLAYING = 3
    GAME_OVER = 4


class StateManager:
    def __init__(self):
        self.current_state = GameState.NAME_INPUT
        self.player_name = ""
        self.score = 0
        self.speed_mode = "medium"
        self.is_paused = False
        self.session_names = set()
        self.difficulty_selection = 1

    def set_state(self, state):
        self.current_state = state

    def set_name(self, name):
        self.player_name = name
        self.session_names.add(name)

    def is_name_duplicate(self, name):
        return name in self.session_names

    def reset_game(self):
        self.score = 0
        self.is_paused = False

    def get_fps(self):
        return SPEEDS[self.speed_mode]
