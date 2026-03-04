import json
import os

class ScoreManager:
    def __init__(self, filename="scores.json"):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return []

    def save_score(self, score):
        self.scores.append(score)
        # Mantém apenas os 5 melhores
        self.scores = sorted(self.scores, reverse=True)[:5]
        with open(self.filename, "w") as f:
            json.dump(self.scores, f)

    def get_high_scores(self):
        return self.scores