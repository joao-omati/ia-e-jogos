import tkinter as tk
from tkinter import messagebox

# Cores e estilos
tema_fundo = "#2C3E50"
tema_texto = "#ECF0F1"
tema_botao_fundo = "#34495E"
tema_x_cor = "#E74C3C"
tema_o_cor = "#3498DB"

def verificar_vencedor(tabuleiro, jogador):
    for linha in tabuleiro:
        if all(celula == jogador for celula in linha):
            return True
    
    for coluna in range(3):
        if all(tabuleiro[linha][coluna] == jogador for linha in range(3)):
            return True
    
    if all(tabuleiro[i][i] == jogador for i in range(3)) or all(tabuleiro[i][2 - i] == jogador for i in range(3)):
        return True
    
    return False

def movimentos_disponiveis(tabuleiro):
    return [(r, c) for r in range(3) for c in range(3) if tabuleiro[r][c] == " "]

def minimax(tabuleiro, maximizando):
    if verificar_vencedor(tabuleiro, "O"):
        return 1
    if verificar_vencedor(tabuleiro, "X"):
        return -1
    if not movimentos_disponiveis(tabuleiro):
        return 0
    
    if maximizando:
        melhor_pontuacao = -float("inf")
        for (r, c) in movimentos_disponiveis(tabuleiro):
            tabuleiro[r][c] = "O"
            pontuacao = minimax(tabuleiro, False)
            tabuleiro[r][c] = " "
            melhor_pontuacao = max(pontuacao, melhor_pontuacao)
        return melhor_pontuacao
    else:
        melhor_pontuacao = float("inf")
        for (r, c) in movimentos_disponiveis(tabuleiro):
            tabuleiro[r][c] = "X"
            pontuacao = minimax(tabuleiro, True)
            tabuleiro[r][c] = " "
            melhor_pontuacao = min(pontuacao, melhor_pontuacao)
        return melhor_pontuacao

def melhor_movimento(tabuleiro):
    melhor_pontuacao = -float("inf")
    movimento = None
    for (r, c) in movimentos_disponiveis(tabuleiro):
        tabuleiro[r][c] = "O"
        pontuacao = minimax(tabuleiro, False)
        tabuleiro[r][c] = " "
        if pontuacao > melhor_pontuacao:
            melhor_pontuacao = pontuacao
            movimento = (r, c)
    return movimento

def ao_clicar(r, c):
    if tabuleiro[r][c] == " " and not verificar_vencedor(tabuleiro, "X") and not verificar_vencedor(tabuleiro, "O"):
        tabuleiro[r][c] = "X"
        botoes[r][c].config(text="X", fg=tema_x_cor)
        
        if verificar_vencedor(tabuleiro, "X"):
            messagebox.showinfo("Jogo da Velha", "Você venceu!")
            janela.destroy()  # Fecha a janela
            return
        
        if not movimentos_disponiveis(tabuleiro):
            messagebox.showinfo("Jogo da Velha", "Empate!")
            janela.destroy()  # Fecha a janela
            return
        
        movimento = melhor_movimento(tabuleiro)
        if movimento:
            tabuleiro[movimento[0]][movimento[1]] = "O"
            botoes[movimento[0]][movimento[1]].config(text="O", fg=tema_o_cor)
        
        if verificar_vencedor(tabuleiro, "O"):
            messagebox.showinfo("Jogo da Velha", "A IA venceu!")
            janela.destroy()  # Fecha a janela
        elif not movimentos_disponiveis(tabuleiro):
            messagebox.showinfo("Jogo da Velha", "Empate!")
            janela.destroy()  # Fecha a janela

def reiniciar_jogo():
    global tabuleiro
    tabuleiro = [[" " for _ in range(3)] for _ in range(3)]
    for r in range(3):
        for c in range(3):
            botoes[r][c].config(text=" ", bg=tema_botao_fundo)

# Configuração da Janela
janela = tk.Tk()
janela.title("Jogo da Velha")
janela.configure(bg=tema_fundo)
janela.resizable(False, False)

# Centralizar a janela
largura_janela = 400
altura_janela = 350
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
x = (largura_tela // 2) - (largura_janela // 2)
y = (altura_tela // 2) - (altura_janela // 2)
janela.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

tabuleiro = [[" " for _ in range(3)] for _ in range(3)]
botoes = [[None for _ in range(3)] for _ in range(3)]

quadro = tk.Frame(janela, bg=tema_fundo)
quadro.pack(pady=20)

for r in range(3):
    for c in range(3):
        botoes[r][c] = tk.Button(quadro, text=" ", font=("Arial", 20, "bold"), width=5, height=2, 
                                  bg=tema_botao_fundo, fg=tema_texto, relief=tk.RIDGE,
                                  command=lambda r=r, c=c: ao_clicar(r, c))
        botoes[r][c].grid(row=r, column=c, padx=5, pady=5)

botao_reiniciar = tk.Button(janela, text="Reiniciar", font=("Arial", 14, "bold"), 
                             bg=tema_x_cor, fg=tema_texto, 
                             command=reiniciar_jogo, relief=tk.RAISED)
botao_reiniciar.pack(pady=10)

janela.mainloop()
