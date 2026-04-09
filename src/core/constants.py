from dataclasses import dataclass


@dataclass(frozen=True)
class TypeTerrain:
    name: str
    weight: int
    color: tuple[int, int, int]


TYPES = {
    0: TypeTerrain("Asfalto", 1, (105, 105, 105)),                 # Cinza
    1: TypeTerrain("Grama", 2, (34, 139, 34)),                     # Verde
    2: TypeTerrain("Floresta", 5, (0, 100, 0)),                    # Verde Escuro
    3: TypeTerrain("Deserto", 8, (237, 201, 175)),                 # Areia
    4: TypeTerrain("Lama", 12, (139, 69, 19)),                     # Marrom
    5: TypeTerrain("Pântano", 20, (72, 61, 139)),                  # Roxo/Azulado escuro
    6: TypeTerrain("Água", 22, (30, 144, 255)),                    # Azul
    7: TypeTerrain("Montanha", 60, (139, 137, 137)),               # Cinza pedra
    8: TypeTerrain("Falha na Matrix", float('inf'), (0, 0, 0)),    # Preto
}
