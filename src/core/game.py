class GameState:
    def __init__(self):
        self.running = True
        self.snake = [(100, 100)]
        self.direction = (20, 0)
        self.food = None
        self.score = 0
