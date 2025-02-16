import pygame
import sys

# Definições de cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
CINZA = (128, 128, 128)
DOURADO = (255, 215, 0)

# Tabuleiro
LINHAS, COLUNAS = 8, 8
TAMANHO_QUADRADO = 80
LARGURA, ALTURA = COLUNAS * TAMANHO_QUADRADO, LINHAS * TAMANHO_QUADRADO

# Iniciando pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Damas")

def desenhar_tabuleiro():
    """Desenha o tabuleiro."""
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            cor = BRANCO if (linha + coluna) % 2 == 0 else PRETO
            pygame.draw.rect(tela, cor, (coluna * TAMANHO_QUADRADO, linha * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO))

def desenhar_pecas(tabuleiro):
    """Desenha as peças no tabuleiro."""
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            peca = tabuleiro[linha][coluna]
            if peca == 1:  # Peça do jogador
                pygame.draw.circle(tela, VERMELHO, (coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2, linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2), TAMANHO_QUADRADO // 2 - 5)
            elif peca == 2:  # Peça da IA
                pygame.draw.circle(tela, CINZA, (coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2, linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2), TAMANHO_QUADRADO // 2 - 5)
            elif peca == 3:  # Dama do jogador
                pygame.draw.circle(tela, DOURADO, (coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2, linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2), TAMANHO_QUADRADO // 2 - 5)
            elif peca == 4:  # Dama da IA
                pygame.draw.circle(tela, DOURADO, (coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2, linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2), TAMANHO_QUADRADO // 2 - 5)

def inicializar_tabuleiro():
    """Inicializa o tabuleiro com as peças nas posições iniciais."""
    tabuleiro = [[0] * COLUNAS for _ in range(LINHAS)]
    for linha in range(3):
        for coluna in range(COLUNAS):
            if (linha + coluna) % 2 == 1:
                tabuleiro[linha][coluna] = 1  # Peças do jogador
    for linha in range(5, 8):
        for coluna in range(COLUNAS):
            if (linha + coluna) % 2 == 1:
                tabuleiro[linha][coluna] = 2  # Peças da IA
    return tabuleiro

def obter_quadrado_do_mouse(pos):
    """Converte a posição do mouse em coordenadas do tabuleiro."""
    x, y = pos
    return y // TAMANHO_QUADRADO, x // TAMANHO_QUADRADO

def movimento_valido(tabuleiro, inicio, fim, jogador):
    """
    Verifica se um movimento é válido.
    
    Parâmetros:
    - tabuleiro: matriz 8x8 representando o estado atual do jogo.
    - inicio: tupla (linha, coluna) indicando a posição inicial da peça.
    - fim: tupla (linha, coluna) indicando a posição final da peça.
    - jogador: inteiro (1 para jogador, 2 para IA).
    
    Retorna:
    - True se o movimento for válido, False caso contrário.
    """
    linha, coluna = inicio
    nova_linha, nova_coluna = fim
    peca = tabuleiro[linha][coluna]
    
    # Verifica se a nova posição está dentro do tabuleiro
    if not (0 <= nova_linha < LINHAS and 0 <= nova_coluna < COLUNAS):
        return False
    
    # Verifica se a nova posição está vazia
    if tabuleiro[nova_linha][nova_coluna] != 0:
        return False
    
    # Movimento para peças comuns (não damas)
    if peca == 1 or peca == 2:
        # Direção do movimento (1 para baixo, -1 para cima)
        direcao = 1 if jogador == 1 else -1
        
        # Movimento simples (uma casa na diagonal)
        if abs(nova_linha - linha) == 1 and abs(nova_coluna - coluna) == 1 and (nova_linha - linha) == direcao:
            return True
        
        # Movimento de captura (duas casas na diagonal)
        if abs(nova_linha - linha) == 2 and abs(nova_coluna - coluna) == 2:
            linha_meio = (linha + nova_linha) // 2
            coluna_meio = (coluna + nova_coluna) // 2
            peca_meio = tabuleiro[linha_meio][coluna_meio]
            
            # Verifica se há uma peça adversária no meio
            if peca_meio != 0 and peca_meio != jogador and peca_meio != jogador + 2:
                return True
    
    # Movimento para damas
    elif peca == 3 or peca == 4:
        # Verifica se o movimento é diagonal
        if abs(nova_linha - linha) == abs(nova_coluna - coluna):
            passo_linha = 1 if nova_linha > linha else -1
            passo_coluna = 1 if nova_coluna > coluna else -1
            linha_atual, coluna_atual = linha + passo_linha, coluna + passo_coluna
            capturada = False
            
            # Verifica o caminho até a nova posição
            while linha_atual != nova_linha and coluna_atual != nova_coluna:
                if tabuleiro[linha_atual][coluna_atual] != 0:
                    if capturada or tabuleiro[linha_atual][coluna_atual] == jogador or tabuleiro[linha_atual][coluna_atual] == jogador + 2:
                        return False
                    capturada = True
                linha_atual += passo_linha
                coluna_atual += passo_coluna
            return True
    
    return False

def promover_a_dama(tabuleiro, linha, coluna, jogador):
    """Promove uma peça a dama se atingir a última linha."""
    if (jogador == 1 and linha == LINHAS - 1) or (jogador == 2 and linha == 0):
        tabuleiro[linha][coluna] = 3 if jogador == 1 else 4

def obter_movimentos_validos(tabuleiro, jogador):
    """Retorna todos os movimentos válidos para um jogador."""
    movimentos = []
    movimentos_captura = []
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            if tabuleiro[linha][coluna] == jogador or tabuleiro[linha][coluna] == jogador + 2:
                for dr in [-1, 1]:
                    for dc in [-1, 1]:
                        if tabuleiro[linha][coluna] == 3 or tabuleiro[linha][coluna] == 4:
                            # Movimento para damas: múltiplas casas
                            nova_linha, nova_coluna = linha + dr, coluna + dc
                            while 0 <= nova_linha < LINHAS and 0 <= nova_coluna < COLUNAS:
                                if movimento_valido(tabuleiro, (linha, coluna), (nova_linha, nova_coluna), jogador):
                                    if abs(nova_linha - linha) > 1 or abs(nova_coluna - coluna) > 1:
                                        movimentos_captura.append(((linha, coluna), (nova_linha, nova_coluna)))
                                    else:
                                        movimentos.append(((linha, coluna), (nova_linha, nova_coluna)))
                                if tabuleiro[nova_linha][nova_coluna] != 0:
                                    break
                                nova_linha += dr
                                nova_coluna += dc
                        else:
                            # Movimento para peças comuns: uma casa ou captura
                            nova_linha, nova_coluna = linha + dr, coluna + dc
                            if movimento_valido(tabuleiro, (linha, coluna), (nova_linha, nova_coluna), jogador):
                                if abs(nova_linha - linha) > 1 or abs(nova_coluna - coluna) > 1:
                                    movimentos_captura.append(((linha, coluna), (nova_linha, nova_coluna)))
                                else:
                                    movimentos.append(((linha, coluna), (nova_linha, nova_coluna)))
    # Prioriza movimentos de captura
    return movimentos_captura if movimentos_captura else movimentos

def avaliar_tabuleiro(tabuleiro):
    """Avalia o tabuleiro para a IA."""
    pecas_jogador1 = 0
    pecas_jogador2 = 0
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            if tabuleiro[linha][coluna] == 1 or tabuleiro[linha][coluna] == 3:
                pecas_jogador1 += 1
            elif tabuleiro[linha][coluna] == 2 or tabuleiro[linha][coluna] == 4:
                pecas_jogador2 += 1
    return pecas_jogador2 - pecas_jogador1

def minimax(tabuleiro, profundidade, maximizando):
    """Implementa o algoritmo Minimax."""
    movimentos_validos = obter_movimentos_validos(tabuleiro, 2 if maximizando else 1)
    if profundidade == 0 or not movimentos_validos:
        return avaliar_tabuleiro(tabuleiro), None
    
    if maximizando:
        max_avaliacao = -float('inf')
        melhor_movimento = None
        for movimento in movimentos_validos:
            novo_tabuleiro = [linha[:] for linha in tabuleiro]
            novo_tabuleiro[movimento[0][0]][movimento[0][1]] = 0
            novo_tabuleiro[movimento[1][0]][movimento[1][1]] = 2
            if abs(movimento[1][0] - movimento[0][0]) > 1 or abs(movimento[1][1] - movimento[0][1]) > 1:
                linha_meio = (movimento[0][0] + movimento[1][0]) // 2
                coluna_meio = (movimento[0][1] + movimento[1][1]) // 2
                novo_tabuleiro[linha_meio][coluna_meio] = 0
            avaliacao, _ = minimax(novo_tabuleiro, profundidade - 1, False)
            if avaliacao > max_avaliacao:
                max_avaliacao = avaliacao
                melhor_movimento = movimento
        return max_avaliacao, melhor_movimento
    else:
        min_avaliacao = float('inf')
        melhor_movimento = None
        for movimento in movimentos_validos:
            novo_tabuleiro = [linha[:] for linha in tabuleiro]
            novo_tabuleiro[movimento[0][0]][movimento[0][1]] = 0
            novo_tabuleiro[movimento[1][0]][movimento[1][1]] = 1
            if abs(movimento[1][0] - movimento[0][0]) > 1 or abs(movimento[1][1] - movimento[0][1]) > 1:
                linha_meio = (movimento[0][0] + movimento[1][0]) // 2
                coluna_meio = (movimento[0][1] + movimento[1][1]) // 2
                novo_tabuleiro[linha_meio][coluna_meio] = 0
            avaliacao, _ = minimax(novo_tabuleiro, profundidade - 1, True)
            if avaliacao < min_avaliacao:
                min_avaliacao = avaliacao
                melhor_movimento = movimento
        return min_avaliacao, melhor_movimento

def verificar_fim_de_jogo(tabuleiro):
    """Verifica se o jogo acabou."""
    movimentos_jogador1 = obter_movimentos_validos(tabuleiro, 1)
    movimentos_jogador2 = obter_movimentos_validos(tabuleiro, 2)
    if not movimentos_jogador1:
        return "Jogador 2 venceu!"
    if not movimentos_jogador2:
        return "Jogador 1 venceu!"
    return None

def main():
    """Função principal do jogo."""
    tabuleiro = inicializar_tabuleiro()
    executando = True
    peca_selecionada = None
    vez_do_jogador = 1
    
    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and vez_do_jogador == 1:
                linha, coluna = obter_quadrado_do_mouse(evento.pos)
                if peca_selecionada:
                    if movimento_valido(tabuleiro, peca_selecionada[:2], (linha, coluna), peca_selecionada[2]):
                        tabuleiro[peca_selecionada[0]][peca_selecionada[1]] = 0
                        tabuleiro[linha][coluna] = peca_selecionada[2]
                        if abs(linha - peca_selecionada[0]) > 1 or abs(coluna - peca_selecionada[1]) > 1:
                            linha_meio = (peca_selecionada[0] + linha) // 2
                            coluna_meio = (peca_selecionada[1] + coluna) // 2
                            tabuleiro[linha_meio][coluna_meio] = 0
                        promover_a_dama(tabuleiro, linha, coluna, peca_selecionada[2])
                        vez_do_jogador = 2
                    peca_selecionada = None
                elif tabuleiro[linha][coluna] == 1 or tabuleiro[linha][coluna] == 3:
                    peca_selecionada = (linha, coluna, tabuleiro[linha][coluna])
        
        if vez_do_jogador == 2:
            _, movimento_ia = minimax(tabuleiro, 3, True)
            if movimento_ia:
                tabuleiro[movimento_ia[0][0]][movimento_ia[0][1]] = 0
                tabuleiro[movimento_ia[1][0]][movimento_ia[1][1]] = 2
                if abs(movimento_ia[1][0] - movimento_ia[0][0]) > 1 or abs(movimento_ia[1][1] - movimento_ia[0][1]) > 1:
                    linha_meio = (movimento_ia[0][0] + movimento_ia[1][0]) // 2
                    coluna_meio = (movimento_ia[0][1] + movimento_ia[1][1]) // 2
                    tabuleiro[linha_meio][coluna_meio] = 0
                promover_a_dama(tabuleiro, movimento_ia[1][0], movimento_ia[1][1], 2)
            vez_do_jogador = 1
        
        fim_de_jogo = verificar_fim_de_jogo(tabuleiro)
        if fim_de_jogo:
            print(fim_de_jogo)
            executando = False
        
        desenhar_tabuleiro()
        desenhar_pecas(tabuleiro)
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()