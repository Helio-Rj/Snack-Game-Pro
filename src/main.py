import pygame
from core.game import Game  # importa da pasta core


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Snake Game Pro")
    game = Game(screen)
    game.run()
    pygame.quit()


if __name__ == "__main__":
    main()
