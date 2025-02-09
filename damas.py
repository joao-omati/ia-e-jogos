import pygame
import sys
import random

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

def is_valid_move(board, start, end, player):
    row, col = start
    new_row, new_col = end
    direction = 1 if player == 1 else -1
    
    if not (0 <= new_row < ROWS and 0 <= new_col < COLS):
        return False
    
    if board[new_row][new_col] != 0:
        return False
    
    if abs(new_row - row) == 1 and abs(new_col - col) == 1 and (new_row - row) == direction:
        return True
    
    if abs(new_row - row) == 2 and abs(new_col - col) == 2:
        mid_row = (row + new_row) // 2
        mid_col = (col + new_col) // 2
        if board[mid_row][mid_col] != 0 and board[mid_row][mid_col] != player:
            board[mid_row][mid_col] = 0
            return True
    
    return False

def get_valid_moves(board, player):
    moves = []
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    new_row, new_col = row + dr, col + dc
                    if is_valid_move(board, (row, col), (new_row, new_col), player):
                        moves.append(((row, col), (new_row, new_col)))
    return moves

def minimax(board, depth, maximizing_player):
    if depth == 0 or not get_valid_moves(board, 2 if maximizing_player else 1):
        return None, random.choice(get_valid_moves(board, 2)) if maximizing_player else None
    
    best_move = None
    if maximizing_player:
        for move in get_valid_moves(board, 2):
            new_board = [row[:] for row in board]
            new_board[move[0][0]][move[0][1]] = 0
            new_board[move[1][0]][move[1][1]] = 2
            _, _ = minimax(new_board, depth - 1, False)
            best_move = move if best_move is None else best_move
    else:
        for move in get_valid_moves(board, 1):
            new_board = [row[:] for row in board]
            new_board[move[0][0]][move[0][1]] = 0
            new_board[move[1][0]][move[1][1]] = 1
            _, _ = minimax(new_board, depth - 1, True)
            best_move = move if best_move is None else best_move
    return None, best_move

def main():
    board = initialize_board()
    running = True
    selected_piece = None
    player_turn = 1
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and player_turn == 1:
                row, col = get_square_from_mouse(event.pos)
                if selected_piece:
                    if is_valid_move(board, selected_piece[:2], (row, col), selected_piece[2]):
                        board[selected_piece[0]][selected_piece[1]] = 0
                        board[row][col] = selected_piece[2]
                        player_turn = 2
                    selected_piece = None
                elif board[row][col] == 1:
                    selected_piece = (row, col, board[row][col])
        
        if player_turn == 2:
            _, ai_move = minimax(board, 3, True)
            if ai_move:
                board[ai_move[0][0]][ai_move[0][1]] = 0
                board[ai_move[1][0]][ai_move[1][1]] = 2
            player_turn = 1
        
        draw_board()
        draw_pieces(board)
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()