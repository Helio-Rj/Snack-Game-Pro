import pygame

class UI:
    def __init__(self, screen):
        self.screen = screen

    def draw_text(self, text, size, color, y, font_name="Verdana", bold=False):
        font = pygame.font.SysFont(font_name, size, bold=bold)
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(self.screen.get_width()/2, y))
        self.screen.blit(surface, rect)