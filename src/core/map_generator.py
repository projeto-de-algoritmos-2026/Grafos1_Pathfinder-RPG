from constants import TYPES
import random


def generate_map(m: int, n: int) -> list[list[int]]:
    """Função que retorna uma grid MxN, mapa do RPG."""

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
        0.05   # Abismo
    ]

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