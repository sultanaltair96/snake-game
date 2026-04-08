import pygame
from .constants import GRID_SIZE, CELL_SIZE, WINDOW_SIZE, COLORS


class UI:
    def __init__(self):
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

    def draw_text(self, surface, text, pos, font, color):
        label = font.render(text, True, color)
        rect = label.get_rect(center=pos)
        surface.blit(label, rect)

    def draw_grid(self, surface):
        for i in range(GRID_SIZE + 1):
            x = i * CELL_SIZE
            pygame.draw.line(surface, COLORS["grid"], (x, 0), (x, WINDOW_SIZE))
            pygame.draw.line(surface, COLORS["grid"], (0, x), (WINDOW_SIZE, x))

    def draw_score(self, surface, score, name):
        score_text = f"{name}: {score}"
        label = self.font_small.render(score_text, True, COLORS["score"])
        surface.blit(label, (10, 10))

    def draw_paused(self, surface):
        overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
        overlay.set_alpha(128)
        overlay.fill(COLORS["ui_bg"])
        surface.blit(overlay, (0, 0))
        self.draw_text(
            surface,
            "PAUSED",
            (WINDOW_SIZE // 2, WINDOW_SIZE // 2),
            self.font_large,
            COLORS["text"],
        )

    def draw_leaderboard(self, surface, scores, title="LEADERBOARD"):
        overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
        overlay.set_alpha(220)
        overlay.fill(COLORS["ui_bg"])
        surface.blit(overlay, (0, 0))

        self.draw_text(
            surface, title, (WINDOW_SIZE // 2, 60), self.font_large, COLORS["score"]
        )

        y_start = 130
        for i, entry in enumerate(scores):
            text = f"{i + 1}. {entry['name']} - {entry['score']} ({entry['date']})"
            self.draw_text(
                surface,
                text,
                (WINDOW_SIZE // 2, y_start + i * 40),
                self.font_small,
                COLORS["text"],
            )

    def draw_name_input(self, surface, name, error=""):
        surface.fill(COLORS["background"])
        self.draw_text(
            surface,
            "ENTER YOUR NAME",
            (WINDOW_SIZE // 2, 150),
            self.font_large,
            COLORS["text"],
        )

        input_rect = pygame.Rect(WINDOW_SIZE // 2 - 150, 250, 300, 60)
        pygame.draw.rect(surface, COLORS["grid"], input_rect, border_radius=10)
        pygame.draw.rect(surface, COLORS["snake_head"], input_rect, 3, border_radius=10)

        name_text = name + "_"
        self.draw_text(
            surface,
            name_text,
            (WINDOW_SIZE // 2, 280),
            self.font_medium,
            COLORS["score"],
        )

        self.draw_text(
            surface,
            "Press ENTER to confirm",
            (WINDOW_SIZE // 2, 400),
            self.font_small,
            COLORS["text"],
        )

        if error:
            self.draw_text(
                surface, error, (WINDOW_SIZE // 2, 450), self.font_small, COLORS["food"]
            )

    def draw_main_menu(self, surface, selection, paused=False):
        if paused:
            overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
            overlay.set_alpha(220)
            overlay.fill(COLORS["ui_bg"])
            surface.blit(overlay, (0, 0))

        title = "PySnake" if not paused else "PAUSED"
        self.draw_text(
            surface,
            title,
            (WINDOW_SIZE // 2, 100),
            self.font_large,
            COLORS["snake_head"],
        )

        options = ["PLAY", "LEADERBOARD", "QUIT"]
        if paused:
            options = ["RESUME", "QUIT"]

        for i, option in enumerate(options):
            color = COLORS["snake_head"] if i == selection else COLORS["text"]
            self.draw_text(
                surface,
                f"> {option}",
                (WINDOW_SIZE // 2, 250 + i * 80),
                self.font_medium,
                color,
            )

    def draw_game_over(self, surface, score, is_high_score):
        surface.fill(COLORS["background"])
        self.draw_text(
            surface,
            "GAME OVER",
            (WINDOW_SIZE // 2, 100),
            self.font_large,
            COLORS["food"],
        )

        score_text = f"Score: {score}"
        color = COLORS["snake_head"] if is_high_score else COLORS["score"]
        self.draw_text(
            surface, score_text, (WINDOW_SIZE // 2, 180), self.font_medium, color
        )

        if is_high_score:
            self.draw_text(
                surface,
                "NEW HIGH SCORE!",
                (WINDOW_SIZE // 2, 230),
                self.font_small,
                COLORS["snake_head"],
            )

        self.draw_text(
            surface,
            "Press ENTER to retry",
            (WINDOW_SIZE // 2, 300),
            self.font_small,
            COLORS["text"],
        )
        self.draw_text(
            surface,
            "Press ESC for menu",
            (WINDOW_SIZE // 2, 350),
            self.font_small,
            COLORS["text"],
        )
