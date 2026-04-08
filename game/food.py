import pygame
import random
import math
from .constants import GRID_SIZE, CELL_SIZE, COLORS


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.pulse_time = 0

    def spawn(self, snake_segments):
        while True:
            pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if pos not in snake_segments:
                self.position = pos
                break

    def update(self, dt):
        self.pulse_time += dt

    def draw(self, surface):
        x = self.position[0] * CELL_SIZE + CELL_SIZE // 2
        y = self.position[1] * CELL_SIZE + CELL_SIZE // 2

        pulse = abs(math.sin(self.pulse_time * 0.005)) * 0.3 + 0.7
        radius = int((CELL_SIZE // 2 - 4) * pulse)

        pygame.draw.circle(surface, COLORS["food"], (x, y), radius)
