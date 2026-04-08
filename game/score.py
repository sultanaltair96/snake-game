import json
import os
from datetime import date
from .constants import HIGHSCORE_FILE, MAX_HIGHSCORES


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
