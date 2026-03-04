import pygame
from core.snake import Snake
from core.food import Food
from core.score import ScoreManager
from core.ui import UI  # módulo para interface


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.running = True
        self.score = 0
        self.state = "MENU"  # MENU, PLAYING, GAME_OVER
        self.score_manager = ScoreManager()
        self.ui = UI(screen)
        self.difficulty = 10  # velocidade inicial (FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.state == "MENU":
                    if event.key == pygame.K_RETURN:  # Enter para começar
                        self.state = "PLAYING"
                elif self.state == "PLAYING":
                    self.snake.change_direction(event.key)
                elif self.state == "GAME_OVER":
                    if event.key == pygame.K_RETURN:  # Enter para reiniciar
                        self.reset()

    def update(self):
        if self.state == "PLAYING":
            self.snake.move()
            if self.snake.eat(self.food):
                self.food.spawn()
                self.score += 1
                # aumenta a velocidade conforme a pontuação
                if self.score % 5 == 0:
                    self.difficulty += 1
            if self.snake.check_collision():
                self.score_manager.save_score(self.score)
                self.state = "GAME_OVER"

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.state == "MENU":
            self.ui.draw_text("Snake Game Pro", 50, (0, 200, 200), 80, font_name="Calibri", bold=True)
            self.ui.draw_text("Press ENTER to Play", 30, (255, 255, 255), 150, font_name="Verdana")
            self.ui.draw_text("High Scores:", 25, (255, 255, 0), 220, font_name="Verdana", bold=True)
            y = 260
            for s in self.score_manager.get_high_scores():
                self.ui.draw_text(str(s), 22, (255, 255, 255), y, font_name="Verdana")
                y += 30
        elif self.state == "PLAYING":
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.ui.draw_text(f"Score: {self.score}", 20, (255, 255, 255), 20, font_name="Verdana")
        elif self.state == "GAME_OVER":
            self.ui.draw_text("GAME OVER", 50, (255, 0, 0), 120, font_name="Calibri", bold=True)
            self.ui.draw_text(f"Final Score: {self.score}", 30, (255, 255, 255), 180, font_name="Verdana")
            self.ui.draw_text("Press ENTER to Restart", 25, (255, 255, 255), 240, font_name="Verdana")
        pygame.display.flip()

    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.state = "PLAYING"
        self.difficulty = 10

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.difficulty)
