import pygame
import sys

# Definições de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Configurações do tabuleiro
ROWS, COLS = 8, 8
SQUARE_SIZE = 80
WIDTH, HEIGHT = COLS * SQUARE_SIZE, ROWS * SQUARE_SIZE

# Inicializando pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Damas")

# Classe para representar as peças
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece == 1:
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            elif piece == 2:
                pygame.draw.circle(screen, GRAY, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

def initialize_board():
    board = [[0] * COLS for _ in range(ROWS)]
    for row in range(3):
        for col in range(COLS):
            if (row + col) % 2 == 1:
                board[row][col] = 1
    for row in range(5, 8):
        for col in range(COLS):
            if (row + col) % 2 == 1:
                board[row][col] = 2
    return board

def get_square_from_mouse(pos):
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE

def main():
    board = initialize_board()
    running = True
    selected_piece = None
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_square_from_mouse(event.pos)
                if selected_piece:
                    board[selected_piece[0]][selected_piece[1]] = 0
                    board[row][col] = selected_piece[2]
                    selected_piece = None
                elif board[row][col] != 0:
                    selected_piece = (row, col, board[row][col])
        
        draw_board()
        draw_pieces(board)
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
