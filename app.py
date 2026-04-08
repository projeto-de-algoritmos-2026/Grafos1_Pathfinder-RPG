import pygame
import sys

from src.core.map_generator import generate_map
from src.core.constants import TYPES

TAMANHO_BLOCO = 30
LINHAS = 20
COLUNAS = 25

LARGURA_TELA = COLUNAS * TAMANHO_BLOCO
ALTURA_TELA = LINHAS * TAMANHO_BLOCO
FPS = 60

def main():
    pygame.init()
    
    # criando a janela principal
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Pathfinder RPG")
    clock = pygame.time.Clock()

    mapa_grid = generate_map(LINHAS, COLUNAS)

    rodando = True
    while rodando:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        tela.fill((0, 0, 0))

        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                terreno = mapa_grid[linha][coluna]
                
                cor = terreno.color 

                x = coluna * TAMANHO_BLOCO
                y = linha * TAMANHO_BLOCO

                pygame.draw.rect(tela, cor, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
                
                pygame.draw.rect(tela, (50, 50, 50), (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO), 1)

        # atualizar o ecrã
        pygame.display.flip()
        clock.tick(FPS)

    # encerra o Pygame ao sair do loop
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()