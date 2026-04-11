from src.core.constants import TYPES, TypeTerrain
import random, math
from noise import pnoise2


def generate_map(m: int, n: int) -> list[list[TypeTerrain]]:
    """
    Função que retorna uma grid MxN, mapa do RPG,
    e a lista de adjacência desse mapa.
    """

    # Criando a matriz
    grid = []
    scale = 15

    for i in range(m):
        row = []
        for j in range(n):

            value = pnoise2(i / scale, j / scale)

            if value < -0.3:
                terrain = TYPES[6]  # Água
            elif value < -0.1:
                terrain = TYPES[5]  # Pântano
            elif value < 0.1:
                terrain = TYPES[1]  # Grama
            elif value < 0.25:
                terrain = TYPES[2]  # Floresta
            elif value < 0.4:
                terrain = TYPES[3]  # Deserto
            else:
                terrain = TYPES[7]  # Montanha

            if random.random() < 0.07:  # 7% de chance de ser falha na matrix
                terrain = TYPES[8]

            row.append(terrain)

        grid.append(row)

    return grid


def generate_adjacency_list(grid: list[list[TypeTerrain]]) -> list[list[int]]:
    """
    Retorna a lista de adjacência de uma grid MxN.
    """

    # Essa lista considera os índices de cada célula da esquerda pra direita,
    # de cima para baixo, conforme exemplo:
    # |-----------|
    # | 0 1 2 3 4 |
    # | 5 6 7 8 9 |
    # |-----------|


    m, n = len(grid), len(grid[0])
    adj_list = [[] for _ in range(m*n)]

    for idx in range(m*n):

        row = idx // n
        column = idx % n

        # Cima
        if row > 0:
            if grid[row-1][column].weight != math.inf:
                adj_list[idx].append(idx - n)

        # Baixo
        if row < m - 1:
            if grid[row+1][column].weight != math.inf:
                adj_list[idx].append(idx + n)

        # Esquerda
        if column > 0:
            if grid[row][column-1].weight != math.inf:
                adj_list[idx].append(idx - 1)

        # Direita
        if column < n - 1:
            if grid[row][column+1].weight != math.inf:
                adj_list[idx].append(idx + 1)


    return adj_list
