import pygame, random


class Food:
    def __init__(self):
        self.position = (200, 200)

    def spawn(self):
        self.position = (
            random.randrange(0, 600, 10),
            random.randrange(0, 400, 10)
        )

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.position[0], self.position[1], 10, 10))
