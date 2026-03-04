import pygame

class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = "RIGHT"

    def change_direction(self, key):
        if key == pygame.K_UP and self.direction != "DOWN":
            self.direction = "UP"
        elif key == pygame.K_DOWN and self.direction != "UP":
            self.direction = "DOWN"
        elif key == pygame.K_LEFT and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif key == pygame.K_RIGHT and self.direction != "LEFT":
            self.direction = "RIGHT"

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == "RIGHT":
            new_head = (head_x + 10, head_y)
        elif self.direction == "LEFT":
            new_head = (head_x - 10, head_y)
        elif self.direction == "UP":
            new_head = (head_x, head_y - 10)
        elif self.direction == "DOWN":
            new_head = (head_x, head_y + 10)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def eat(self, food):
        if self.body[0] == food.position:
            self.grow()
            return True
        return False

    def check_collision(self):
        head = self.body[0]
        return (
            head in self.body[1:] or
            head[0] < 0 or head[0] >= 600 or
            head[1] < 0 or head[1] >= 400
        )

    def draw(self, screen):
        for pos in self.body:
            pygame.draw.rect(screen, (0,255,0), pygame.Rect(pos[0], pos[1], 10, 10))