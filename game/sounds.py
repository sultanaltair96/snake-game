import pygame
import numpy as np


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sample_rate = 44100
        self._eat_sound = self._generate_blip(440, 0.1)
        self._game_over_sound = self._generate_buzz(200, 0.5)
        self._click_sound = self._generate_blip(800, 0.05)

    def _generate_blip(self, frequency, duration):
        n_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        wave = np.sin(2 * np.pi * frequency * t)
        envelope = np.ones(n_samples)
        envelope[: int(n_samples * 0.1)] = np.linspace(0, 1, int(n_samples * 0.1))
        envelope[-int(n_samples * 0.1) :] = np.linspace(1, 0, int(n_samples * 0.1))
        wave = (wave * envelope * 0.5 * 32767).astype(np.int16)
        stereo = np.column_stack((wave, wave))
        return pygame.sndarray.make_sound(stereo)

    def _generate_buzz(self, frequency, duration):
        n_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        wave = np.zeros(n_samples)
        for k in range(1, 5):
            wave += np.sin(2 * np.pi * (frequency * k) * t) / k
        envelope = np.exp(-t * 5)
        wave = (wave * envelope * 0.3 * 32767).astype(np.int16)
        stereo = np.column_stack((wave, wave))
        return pygame.sndarray.make_sound(stereo)

    def play_eat(self):
        self._eat_sound.play()

    def play_game_over(self):
        self._game_over_sound.play()

    def play_click(self):
        self._click_sound.play()
