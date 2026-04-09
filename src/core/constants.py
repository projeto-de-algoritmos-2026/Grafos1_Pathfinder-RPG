from dataclasses import dataclass


@dataclass(frozen=True)
class TypeTerrain:
    name: str
    weight: int
    color: tuple[int, int, int]


TYPES = {
    0: TypeTerrain("Asfalto", 1, (204, 204, 204)),                # Cinza
    1: TypeTerrain("Grama", 2, (147, 196, 125)),                  # Verde
    2: TypeTerrain("Floresta", 5, (39, 78, 19)),                  # Verde Escuro
    3: TypeTerrain("Deserto", 8, (241, 194, 50)),                 # Areia
    4: TypeTerrain("Lama", 12, (120, 63, 4)),                     # Marrom
    5: TypeTerrain("Pântano", 20, (116, 27, 71)),                 # Roxo/Azulado escuro
    6: TypeTerrain("Água", 22, (28, 69, 135)),                    # Azul
    7: TypeTerrain("Montanha", 60, (67, 67, 67)),                 # Cinza pedra
    8: TypeTerrain("Falha na Matrix", float('inf'), (0, 0, 0)),   # Preto
}
