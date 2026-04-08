from dataclasses import dataclass


@dataclass(frozen=True)
class TypeTerrain:
    name: str
    weight: int


TYPES = {
    0: TypeTerrain("Asfalto", 1),
    1: TypeTerrain("Grama", 2),
    2: TypeTerrain("Floresta", 5),
    3: TypeTerrain("Deserto", 8),
    4: TypeTerrain("Lama", 12),
    5: TypeTerrain("Pântano", 20),
    6: TypeTerrain("Água", 22),
    7: TypeTerrain("Montanha", 60),
    8: TypeTerrain("Abismo", 1000000),
}
