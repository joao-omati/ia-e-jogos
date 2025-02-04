import tkinter as tk

# Cores do tabuleiro
tema_fundo = "#DDB88C"
tema_claro = "#FFFACD"
tema_escuro = "#8B4513"
tema_p1 = "#000000"
tema_p2 = "#FFFFFF"

dimensao = 8  # Tabuleiro 8x8
tamanho_celula = 60

class Damas:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo de Damas")
        self.canvas = tk.Canvas(root, width=dimensao * tamanho_celula, height=dimensao * tamanho_celula)
        self.canvas.pack()
        self.tabuleiro = [[None for _ in range(dimensao)] for _ in range(dimensao)]
        self.jogador_atual = "P1"  # Começa com o jogador 1
        self.selecionado = None
        self.desenhar_tabuleiro()
        self.posicionar_pecas()
        self.canvas.bind("<Button-1>", self.clique)
    
    def desenhar_tabuleiro(self):
        for linha in range(dimensao):
            for coluna in range(dimensao):
                cor = tema_claro if (linha + coluna) % 2 == 0 else tema_escuro
                self.canvas.create_rectangle(
                    coluna * tamanho_celula, linha * tamanho_celula,
                    (coluna + 1) * tamanho_celula, (linha + 1) * tamanho_celula,
                    fill=cor
                )
    
    def posicionar_pecas(self):
        for linha in range(dimensao):
            for coluna in range(dimensao):
                if (linha + coluna) % 2 == 1:
                    if linha < 3:
                        self.tabuleiro[linha][coluna] = "P2"
                        self.desenhar_peca(linha, coluna, tema_p2)
                    elif linha > 4:
                        self.tabuleiro[linha][coluna] = "P1"
                        self.desenhar_peca(linha, coluna, tema_p1)
    
    def desenhar_peca(self, linha, coluna, cor):
        x1 = coluna * tamanho_celula + 10
        y1 = linha * tamanho_celula + 10
        x2 = (coluna + 1) * tamanho_celula - 10
        y2 = (linha + 1) * tamanho_celula - 10
        self.canvas.create_oval(x1, y1, x2, y2, fill=cor, tags=f"peca_{linha}_{coluna}")
    
    def clique(self, event):
        coluna = event.x // tamanho_celula
        linha = event.y // tamanho_celula
        if self.selecionado:
            self.mover_peca(linha, coluna)
        elif self.tabuleiro[linha][coluna] == self.jogador_atual:
            self.selecionado = (linha, coluna)
    
    def mover_peca(self, linha, coluna):
        linha_antiga, coluna_antiga = self.selecionado
        if abs(linha - linha_antiga) == 1 and abs(coluna - coluna_antiga) == 1:
            if self.tabuleiro[linha][coluna] is None:
                self.tabuleiro[linha][coluna] = self.jogador_atual
                self.tabuleiro[linha_antiga][coluna_antiga] = None
                self.atualizar_tabuleiro()
                self.jogador_atual = "P2" if self.jogador_atual == "P1" else "P1"
        self.selecionado = None
    
    def atualizar_tabuleiro(self):
        self.canvas.delete("all")
        self.desenhar_tabuleiro()
        for linha in range(dimensao):
            for coluna in range(dimensao):
                if self.tabuleiro[linha][coluna] == "P1":
                    self.desenhar_peca(linha, coluna, tema_p1)
                elif self.tabuleiro[linha][coluna] == "P2":
                    self.desenhar_peca(linha, coluna, tema_p2)

if __name__ == "__main__":
    root = tk.Tk()
    jogo = Damas(root)
    root.mainloop()
