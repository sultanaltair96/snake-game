import pygame
from .constants import GRID_SIZE, CELL_SIZE, COLORS


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        center = GRID_SIZE // 2
        self.segments = [(center, center), (center - 1, center), (center - 2, center)]
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
        if head[0] < 0 or head[0] >= GRID_SIZE or head[1] < 0 or head[1] >= GRID_SIZE:
            return True
        if head in self.segments[1:]:
            return True
        return False

    def get_head(self):
        return self.segments[0]

    def draw(self, surface):
        for i, segment in enumerate(self.segments):
            x = segment[0] * CELL_SIZE
            y = segment[1] * CELL_SIZE
            rect = pygame.Rect(x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4)

            if i == 0:
                color = COLORS["snake_head"]
            else:
                ratio = i / len(self.segments)
                color = self._interpolate_color(
                    COLORS["snake_head"], COLORS["snake_tail"], ratio
                )

            pygame.draw.rect(surface, color, rect, border_radius=8)

    def _interpolate_color(self, color1, color2, ratio):
        return tuple(int(c1 + (c2 - c1) * ratio) for c1, c2 in zip(color1, color2))
