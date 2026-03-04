import pygame
from core.snake import Snake
from core.food import Food
from core.score import ScoreManager  # se já estiver usando ranking


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.running = True
        self.score = 0
        self.state = "MENU"  # MENU, PLAYING, GAME_OVER

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
            if self.snake.check_collision():
                self.state = "GAME_OVER"

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.state == "MENU":
            self.draw_text("Press ENTER to Play", 40, (255, 255, 255), 150, 180)
        elif self.state == "PLAYING":
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.draw_text(f"Score: {self.score}", 20, (255, 255, 255), 10, 10)
        elif self.state == "GAME_OVER":
            self.draw_text("GAME OVER", 50, (255, 0, 0), 180, 150)
            self.draw_text(f"Final Score: {self.score}", 30, (255, 255, 255), 200, 220)
            self.draw_text("Press ENTER to Restart", 25, (255, 255, 255), 160, 260)
        pygame.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont("Arial", size)
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.state = "PLAYING"

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)
