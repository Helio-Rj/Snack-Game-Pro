import pygame
import os
from src.core.items import gerar_comida
from src.core.game import GameState
from src.utils.constants import LARGURA, ALTURA, TAMANHO, FPS

pygame.init()
pygame.mixer.init()
level_up_sound = pygame.mixer.Sound("assets/audio/level_up.wav")

screen = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()

# ===== HIGH SCORE =====
HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

highscore = load_highscore()

state = GameState()
gerar_comida(state)

# ===== CONTROLE START =====
game_started = False
game_over = False

# ===== CONFIG NÍVEIS =====
level = 1
speed = FPS
previous_level = level

# ===== CONTROLE TEXTO LEVEL UP =====
level_up_time = None
LEVEL_UP_DURATION = 500

while state.running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state.running = False

        if event.type == pygame.KEYDOWN:

            if not game_started:
                game_started = True

            if game_over and event.key == pygame.K_r:
                state = GameState()
                gerar_comida(state)

                level = 1
                speed = FPS
                previous_level = level
                level_up_time = None

                game_started = False
                game_over = False

            if event.key == pygame.K_UP and state.direction != (0, TAMANHO):
                state.direction = (0, -TAMANHO)
            elif event.key == pygame.K_DOWN and state.direction != (0, -TAMANHO):
                state.direction = (0, TAMANHO)
            elif event.key == pygame.K_LEFT and state.direction != (TAMANHO, 0):
                state.direction = (-TAMANHO, 0)
            elif event.key == pygame.K_RIGHT and state.direction != (-TAMANHO, 0):
                state.direction = (TAMANHO, 0)

    # ===== UPDATE =====
    if game_started and not game_over:

        dx, dy = state.direction

        if (dx, dy) != (0, 0):
            head_x, head_y = state.snake[0]
            nova_head = (head_x + dx, head_y + dy)

            if not (0 <= nova_head[0] < LARGURA and 0 <= nova_head[1] < ALTURA):
                game_over = True

            if nova_head in state.snake:
                game_over = True

            state.snake.insert(0, nova_head)

            if nova_head == state.food:
                state.score += 1
                gerar_comida(state)
            else:
                state.snake.pop()

        # ===== SISTEMA DE NÍVEL =====
        if state.score >= 10:
            level = 3
            speed = FPS + 8
        elif state.score >= 5:
            level = 2
            speed = FPS + 4
        else:
            level = 1
            speed = FPS

        if level != previous_level:
            level_up_sound.play()
            level_up_time = pygame.time.get_ticks()
            previous_level = level

    # ===== SE MORREU SALVA RECORD =====
    if game_over and state.score > highscore:
        highscore = state.score
        save_highscore(highscore)

    # ===== RENDER =====
    screen.fill((0, 0, 0))

    for segment in state.snake:
        pygame.draw.rect(screen, (0, 255, 0), (*segment, TAMANHO, TAMANHO))

    pygame.draw.rect(screen, (255, 0, 0), (*state.food, TAMANHO, TAMANHO))

    font = pygame.font.SysFont("consolas", 24)
    score_surface = font.render(f"Score: {state.score}", True, (255, 255, 255))
    level_surface = font.render(f"Level: {level}", True, (255, 255, 0))
    high_surface = font.render(f"High: {highscore}", True, (0, 200, 255))

    screen.blit(score_surface, (10, 10))
    screen.blit(level_surface, (10, 40))
    screen.blit(high_surface, (10, 70))

    # START
    if not game_started:
        big_font = pygame.font.SysFont("consolas", 64, bold=True)
        start_surface = big_font.render("START", True, (255, 255, 255))
        rect = start_surface.get_rect(center=(LARGURA // 2, ALTURA // 2))
        screen.blit(start_surface, rect)

    # LEVEL UP
    if game_started and level_up_time is not None:
        if pygame.time.get_ticks() - level_up_time < LEVEL_UP_DURATION:
            big_font = pygame.font.SysFont("consolas", 64, bold=True)
            level_up_surface = big_font.render("LEVEL UP!", True, (255, 255, 0))
            rect = level_up_surface.get_rect(center=(LARGURA // 2, ALTURA // 2))
            screen.blit(level_up_surface, rect)

    # GAME OVER
    if game_over:
        big_font = pygame.font.SysFont("consolas", 64, bold=True)
        small_font = pygame.font.SysFont("consolas", 24)

        over_surface = big_font.render("GAME OVER", True, (255, 50, 50))
        restart_surface = small_font.render("Press R to restart", True, (255, 255, 255))
        high_surface_big = small_font.render(f"High Score: {highscore}", True, (0, 200, 255))

        rect1 = over_surface.get_rect(center=(LARGURA // 2, ALTURA // 2 - 40))
        rect2 = restart_surface.get_rect(center=(LARGURA // 2, ALTURA // 2 + 20))
        rect3 = high_surface_big.get_rect(center=(LARGURA // 2, ALTURA // 2 + 60))

        screen.blit(over_surface, rect1)
        screen.blit(restart_surface, rect2)
        screen.blit(high_surface_big, rect3)

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
