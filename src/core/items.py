import random
from src.utils.constants import LARGURA, ALTURA, TAMANHO


def gerar_comida(state):
    x = random.randrange(0, LARGURA, TAMANHO)
    y = random.randrange(0, ALTURA, TAMANHO)
    state.food = (x, y)
