class Checkers:
    def __init__(self):
        self.board = []
        self.create_board()
        self.current_player = 'X'

    def create_board(self):
        for row in range(8):
            self.board.append([])
            for col in range(8):
                if (row + col) % 2 == 0:
                    if row < 3:
                        self.board[row].append('X')
                    elif row > 4:
                        self.board[row].append('O')
                    else:
                        self.board[row].append(' ')
                else:
                    self.board[row].append(' ')

    def print_board(self):
        print("  0 1 2 3 4 5 6 7")
        for i, row in enumerate(self.board):
            print(i, end=" ")
            for cell in row:
                print(cell, end=" ")
            print()

    def is_valid_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end

        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        if self.board[end_row][end_col] != ' ':
            return False

        if self.current_player == 'X':
            if self.board[start_row][start_col] != 'X':
                return False
            if end_row != start_row + 1 or abs(end_col - start_col) != 1:
                return False
        else:
            if self.board[start_row][start_col] != 'O':
                return False
            if end_row != start_row - 1 or abs(end_col - start_col) != 1:
                return False

        return True

    def make_move(self, start, end):
        if self.is_valid_move(start, end):
            start_row, start_col = start
            end_row, end_col = end

            self.board[end_row][end_col] = self.board[start_row][start_col]
            self.board[start_row][start_col] = ' '

            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def play(self):
        while True:
            self.print_board()
            print(f"Vez do jogador {self.current_player}")
            start = tuple(map(int, input("Digite a posição inicial (linha coluna): ").split()))
            end = tuple(map(int, input("Digite a posição final (linha coluna): ").split()))

            if self.make_move(start, end):
                print("Movimento válido!")
            else:
                print("Movimento inválido! Tente novamente.")

if __name__ == "__main__":
    game = Checkers()
    game.play()