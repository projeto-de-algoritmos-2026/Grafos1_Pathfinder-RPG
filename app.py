import pygame
import sys

from src.core.generators import generate_map
from src.core.constants import TYPES

# --- CONSTANTES DE TELA E UI ---
LARGURA_PAINEL = 250
MAX_LARGURA_MAPA = 800
ALTURA_TELA = 800

LARGURA_TELA_TOTAL = LARGURA_PAINEL + MAX_LARGURA_MAPA
FPS = 60

# --- CORES ---
COR_PAINEL = (40, 40, 40)
COR_TEXTO = (255, 255, 255)
COR_BOTAO = (70, 130, 180)
COR_BOTAO_HOVER = (100, 149, 237)
COR_START = (50, 205, 50)
COR_FINAL = (220, 20, 60)
COR_INPUT_ATIVO = (100, 100, 100)
COR_INPUT_INATIVO = (60, 60, 60)


def desenhar_texto(tela, texto, fonte, cor, x, y):
    imagem_texto = fonte.render(texto, True, cor)
    tela.blit(imagem_texto, (x, y))


def criar_superficie_mapa(mapa_grid, dimensao):
    tamanho_bloco = max(1, min(MAX_LARGURA_MAPA // dimensao, ALTURA_TELA // dimensao))
    tamanho_real = dimensao * tamanho_bloco
    superficie = pygame.Surface((tamanho_real, tamanho_real))

    for linha in range(dimensao):
        for coluna in range(dimensao):
            terreno = mapa_grid[linha][coluna]
            cor = terreno.color
            x = coluna * tamanho_bloco
            y = linha * tamanho_bloco

            pygame.draw.rect(superficie, cor, (x, y, tamanho_bloco, tamanho_bloco))
            if tamanho_bloco > 2:
                pygame.draw.rect(superficie, (50, 50, 50), (x, y, tamanho_bloco, tamanho_bloco), 1)

    return superficie, tamanho_bloco


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA_TOTAL, ALTURA_TELA))
    pygame.display.set_caption("Pathfinder RPG")
    clock = pygame.time.Clock()

    fonte = pygame.font.SysFont("Arial", 16, bold=True)
    fonte_input = pygame.font.SysFont("Arial", 18)

    # --- VARIÁVEIS DE ESTADO ---
    dimensao_atual = 100
    texto_dimensao = str(dimensao_atual)
    input_focado = None

    # --- VARIÁVEIS DE ZOOM E CÂMERA ---
    zoom_level = 1.0
    camera_x = 0
    camera_y = 0
    arrastando_mapa = False
    inicio_arrasto_mouse = (0, 0)
    inicio_arrasto_camera = (0, 0)

    mapa_grid = generate_map(dimensao_atual, dimensao_atual)
    mapa_surface, tamanho_bloco = criar_superficie_mapa(mapa_grid, dimensao_atual)
    mapa_surface_zoom = mapa_surface.copy() # Cópia em cache para otimização

    ponto_start = None
    ponto_final = None
    estado_atual = "ESPERANDO"

    # --- DEFINIÇÃO DOS RETÂNGULOS DA UI ---
    caixa_dimensao = pygame.Rect(25, 45, 185, 30)
    btn_gerar = pygame.Rect(25, 90, 185, 40)
    btn_start = pygame.Rect(25, 150, 185, 40)
    btn_final = pygame.Rect(25, 200, 185, 40)
    btn_dijkstra = pygame.Rect(25, 280, 185, 40)

    rodando = True
    while rodando:
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            # --- TRATAMENTO DE ZOOM (Scroll do Mouse) ---
            if evento.type == pygame.MOUSEWHEEL:
                mx, my = pygame.mouse.get_pos()

                # Verifica se o clique foi na área do mapa (fora do painel)
                if mx >= LARGURA_PAINEL:
                    # Posição relativa do mouse na área do mapa (descontando o painel)
                    rel_mouse_x = mx - LARGURA_PAINEL
                    rel_mouse_y = my

                    # 1. Calcula onde o mouse estava NO MAPA ORIGINAL antes do zoom
                    world_x_antes = (rel_mouse_x - camera_x) / zoom_level
                    world_y_antes = (rel_mouse_y - camera_y) / zoom_level

                    # 2. Altera o nível de zoom
                    fator = 0.5
                    if evento.y > 0 and zoom_level < 5.0: # Rolar para cima
                        zoom_level += fator
                    elif evento.y < 0 and zoom_level > 1.0: # Rolar para baixo
                        zoom_level -= fator

                    # 3. Atualiza a Surface cacheada do mapa com o novo zoom
                    nova_largura = int(mapa_surface.get_width() * zoom_level)
                    nova_altura = int(mapa_surface.get_height() * zoom_level)
                    mapa_surface_zoom = pygame.transform.scale(mapa_surface, (nova_largura, nova_altura))

                    # 4. Calcula a NOVA POSIÇÃO DA CÂMERA para centralizar no mouse
                    # Com o novo zoom, queremos que o ponto original permaneça sob o mouse.
                    # rel_mouse_x = (world_x_antes * zoom_level) + nova_camera_x
                    # Isolando nova_camera_x:
                    camera_x = rel_mouse_x - (world_x_antes * zoom_level)
                    camera_y = rel_mouse_y - (world_y_antes * zoom_level)

                    # 5. Garante que a câmera não fique presa fora dos limites
                    limite_x = min(0, MAX_LARGURA_MAPA - nova_largura)
                    limite_y = min(0, ALTURA_TELA - nova_altura)
                    camera_x = max(limite_x, min(0, camera_x))
                    camera_y = max(limite_y, min(0, camera_y))

            # --- TRATAMENTO DO TECLADO ---
            if evento.type == pygame.KEYDOWN:
                if input_focado == "DIMENSAO":
                    if evento.key == pygame.K_BACKSPACE:
                        texto_dimensao = texto_dimensao[:-1]
                    elif evento.unicode.isnumeric() and len(texto_dimensao) < 3:
                        texto_dimensao += evento.unicode

            # --- INICIAR ARRASTO DA CÂMERA ---
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 3: # Botão Direito
                if mouse_x >= LARGURA_PAINEL:
                    arrastando_mapa = True
                    inicio_arrasto_mouse = mouse_pos
                    inicio_arrasto_camera = (camera_x, camera_y)

            # --- PARAR ARRASTO DA CÂMERA ---
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 3:
                arrastando_mapa = False

            # --- TRATAMENTO DOS CLIQUES (Botão Esquerdo) ---
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                # 1. Clique no Painel (Esquerda)
                if mouse_x < LARGURA_PAINEL:
                    if caixa_dimensao.collidepoint(mouse_pos):
                        input_focado = "DIMENSAO"
                    else:
                        input_focado = None

                    if btn_gerar.collidepoint(mouse_pos):
                        input_focado = None
                        d = int(texto_dimensao) if texto_dimensao else 10
                        dimensao_atual = max(10, min(200, d))
                        texto_dimensao = str(dimensao_atual)

                        mapa_grid = generate_map(dimensao_atual, dimensao_atual)
                        mapa_surface, tamanho_bloco = criar_superficie_mapa(mapa_grid, dimensao_atual)

                        # Reseta a câmera e o zoom ao gerar um novo mapa
                        zoom_level = 1.0
                        camera_x = 0
                        camera_y = 0
                        mapa_surface_zoom = mapa_surface.copy()

                        ponto_start = None
                        ponto_final = None
                        estado_atual = "ESPERANDO"

                    elif btn_start.collidepoint(mouse_pos):
                        estado_atual = "SELECIONANDO_START"

                    elif btn_final.collidepoint(mouse_pos):
                        estado_atual = "SELECIONANDO_FINAL"

                    elif btn_dijkstra.collidepoint(mouse_pos):
                        if ponto_start and ponto_final:
                            estado_atual = "CALCULANDO"
                            estado_atual = "ESPERANDO"

                # 2. Clique no Mapa (Direita) - Atualizado com a Matemática da Câmera
                elif mouse_x >= LARGURA_PAINEL:
                    rel_mouse_x = mouse_x - LARGURA_PAINEL

                    world_x = int((rel_mouse_x - camera_x) / zoom_level)
                    world_y = int((mouse_y - camera_y) / zoom_level)

                    coluna_clicada = world_x // tamanho_bloco
                    linha_clicada = world_y // tamanho_bloco

                    # Verifica se o clique foi dentro dos limites válidos do mapa
                    if 0 <= linha_clicada < dimensao_atual and 0 <= coluna_clicada < dimensao_atual:
                        terreno_clicado = mapa_grid[linha_clicada][coluna_clicada]

                        # Só permite a seleção se o terreno NÃO for uma "Falha na Matrix" (peso infinito)
                        if terreno_clicado.weight != float('inf'):
                            if estado_atual == "SELECIONANDO_START":
                                ponto_start = (linha_clicada, coluna_clicada)
                                estado_atual = "ESPERANDO"

                            elif estado_atual == "SELECIONANDO_FINAL":
                                ponto_final = (linha_clicada, coluna_clicada)
                                estado_atual = "ESPERANDO"


            # --- MOVIMENTO DO MOUSE (Lógica do Arrasto) ---
            if evento.type == pygame.MOUSEMOTION:
                if arrastando_mapa:
                    dx = mouse_pos[0] - inicio_arrasto_mouse[0]
                    dy = mouse_pos[1] - inicio_arrasto_mouse[1]

                    # Calcula nova posição provisória
                    nova_camera_x = inicio_arrasto_camera[0] + dx
                    nova_camera_y = inicio_arrasto_camera[1] + dy

                    # Limita para não arrastar o mapa para fora da tela
                    limite_x = min(0, MAX_LARGURA_MAPA - mapa_surface_zoom.get_width())
                    limite_y = min(0, ALTURA_TELA - mapa_surface_zoom.get_height())

                    camera_x = max(limite_x, min(0, nova_camera_x))
                    camera_y = max(limite_y, min(0, nova_camera_y))


        # --- RENDERIZAÇÃO ---
        tela.fill((0, 0, 0))

        # 1. Desenhar o Mapa (Agora blitado na posição da câmera usando o cache do zoom)
        tela.blit(mapa_surface_zoom, (LARGURA_PAINEL + camera_x, camera_y))

        # 1.5 Desenhar os pontos Start e Final no Mapa (Acompanhando o Zoom e Câmera)
        tamanho_bloco_zoom = tamanho_bloco * zoom_level
        if ponto_start:
            px = LARGURA_PAINEL + camera_x + (ponto_start[1] * tamanho_bloco_zoom)
            py = camera_y + (ponto_start[0] * tamanho_bloco_zoom)
            pygame.draw.rect(tela, COR_START, (px, py, tamanho_bloco_zoom, tamanho_bloco_zoom))
            pygame.draw.rect(tela, (255, 255, 255), (px, py, tamanho_bloco_zoom, tamanho_bloco_zoom), 2)

        if ponto_final:
            px = LARGURA_PAINEL + camera_x + (ponto_final[1] * tamanho_bloco_zoom)
            py = camera_y + (ponto_final[0] * tamanho_bloco_zoom)
            pygame.draw.rect(tela, COR_FINAL, (px, py, tamanho_bloco_zoom, tamanho_bloco_zoom))
            pygame.draw.rect(tela, (255, 255, 255), (px, py, tamanho_bloco_zoom, tamanho_bloco_zoom), 2)


        # 2. Desenhar o Painel Lateral
        pygame.draw.rect(tela, COR_PAINEL, (0, 0, LARGURA_PAINEL, ALTURA_TELA))

        desenhar_texto(tela, "Tamanho (Máx 200):", fonte, (200, 200, 200), 25, 25)

        cor_cx_dim = COR_INPUT_ATIVO if input_focado == "DIMENSAO" else COR_INPUT_INATIVO
        pygame.draw.rect(tela, cor_cx_dim, caixa_dimensao, border_radius=3)

        txt_d_render = texto_dimensao + ("_" if input_focado == "DIMENSAO" and pygame.time.get_ticks() % 1000 < 500 else "")
        desenhar_texto(tela, txt_d_render, fonte_input, COR_TEXTO, 30, 50)

        def desenhar_botao(rect, texto, cor_base):
            cor = COR_BOTAO_HOVER if rect.collidepoint(mouse_pos) else cor_base
            pygame.draw.rect(tela, cor, rect, border_radius=5)
            desenhar_texto(tela, texto, fonte, COR_TEXTO, rect.x + 15, rect.y + 10)

        desenhar_botao(btn_gerar, "Gerar Novo Mapa", (60, 100, 60))

        cor_btn_s = (100, 200, 100) if estado_atual == "SELECIONANDO_START" else COR_BOTAO
        desenhar_botao(btn_start, "Selecionar Start", cor_btn_s)

        cor_btn_f = (200, 100, 100) if estado_atual == "SELECIONANDO_FINAL" else COR_BOTAO
        desenhar_botao(btn_final, "Selecionar Final", cor_btn_f)

        desenhar_botao(btn_dijkstra, "Rodar Dijkstra", (180, 140, 30))

        # --- Textos de Status no final ---
        pygame.draw.line(tela, (100, 100, 100), (25, 340), (210, 340), 2)
        desenhar_texto(tela, "Informações:", fonte, (200, 200, 200), 25, 355)

        txt_start = f"Início: {ponto_start}" if ponto_start else "Início: Não definido"
        txt_final = f"Destino: {ponto_final}" if ponto_final else "Destino: Não definido"
        txt_estado = f"Estado: {estado_atual}"

        desenhar_texto(tela, txt_start, fonte, COR_START, 25, 385)
        desenhar_texto(tela, txt_final, fonte, COR_FINAL, 25, 415)
        desenhar_texto(tela, txt_estado, fonte, (200, 200, 200), 25, 455)

        # Opcional: mostrar o nível de zoom
        desenhar_texto(tela, f"Zoom: {zoom_level}x", fonte, (150, 150, 150), 25, 500)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()