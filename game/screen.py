import pygame
from .constants import SCREEN_SHAKE_AMPLITUDE, SCREEN_SHAKE_DURATION


class ScreenEffects:
    def __init__(self):
        self.shake_offset = (0, 0)
        self.shake_start_time = 0
        self.is_shaking = False

    def trigger_shake(self):
        self.is_shaking = True
        self.shake_start_time = pygame.time.get_ticks()

    def update(self):
        if self.is_shaking:
            elapsed = pygame.time.get_ticks() - self.shake_start_time
            if elapsed < SCREEN_SHAKE_DURATION:
                progress = elapsed / SCREEN_SHAKE_DURATION
                amplitude = SCREEN_SHAKE_AMPLITUDE * (1 - progress)
                self.shake_offset = (
                    int((pygame.time.get_ticks() % 20 - 10) * amplitude / 10),
                    int((pygame.time.get_ticks() % 20 - 10) * amplitude / 10),
                )
            else:
                self.is_shaking = False
                self.shake_offset = (0, 0)

    def get_offset(self):
        return self.shake_offset
