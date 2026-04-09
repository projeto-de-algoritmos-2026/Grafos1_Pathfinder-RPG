from src.core.constants import TYPES, TypeTerrain
import random, math


def generate_map(m: int, n: int) -> list[list[TypeTerrain]]:
    """
    Função que retorna uma grid MxN, mapa do RPG,
    e a lista de adjacência desse mapa.
    """

    types_of_terrain = list(TYPES.keys())
    probs_of_each_terrain = [
        0.2,   # Asfalto
        0.2,   # Grama
        0.1,   # Floresta
        0.1,   # Deserto
        0.05,  # Lama
        0.1,   # Pântano
        0.15,  # Água
        0.05,  # Montanha
        0.05   # Falha na matrix
    ]

    # Criando a matriz
    grid = []

    for i in range(m):
        row = []
        for j in range(n):

            type_of_terrain = random.choices(
                types_of_terrain,
                weights=probs_of_each_terrain
            )[0]

            new_terrain = TYPES[type_of_terrain]
            row.append(new_terrain)

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
