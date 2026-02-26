from src.core.items import gerar_comida


def mover_snake(state):
    head_x, head_y = state.snake[0]
    dx, dy = state.direction

    nova_head = (head_x + dx, head_y + dy)
    state.snake.insert(0, nova_head)

    if nova_head == state.food:
        gerar_comida(state)
    else:
        state.snake.pop()
