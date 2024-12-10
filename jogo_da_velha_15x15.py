import tkinter as tk
from tkinter import messagebox
import random

class JogoDaVelha:
    def __init__(self, master):
        self.master = master
        self.master.title("Jogo da Velha 15x15")
        self.master.state('zoomed') 
        self.tabuleiro = [[' ' for _ in range(15)] for _ in range(15)]
        self.botoes = [[None for _ in range(15)] for _ in range(15)]
        self.placar_jogador = 0
        self.placar_pc = 0
        self.dificuldade = 'Fácil'  
        self.jogador = 'X'  
        self.adv = 'O'  
        self.iniciar_menu()

    def iniciar_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.menu_frame = tk.Frame(self.master, bg="lightblue", padx=20, pady=20)
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

        titulo = tk.Label(self.menu_frame, text="\n Bem-vindo ao Jogo da Velha 15x15 \n", foreground='black', 
                          font=("Arial", 24, "bold"), bg="lightblue", pady=20)
        titulo.pack()

        # Dificuldade
        dificuldade_frame = tk.Frame(self.menu_frame, bg="lightblue")
        dificuldade_frame.pack(pady=10)
        tk.Label(dificuldade_frame, text="Escolha a Dificuldade:", foreground='white', font=("Arial", 18), bg="lightblue").pack(anchor="center")
        self.dificuldade_var = tk.StringVar(value='Fácil')
        dificuldade_menu = tk.OptionMenu(dificuldade_frame, self.dificuldade_var, 'Fácil', 'Médio', 'Difícil')
        dificuldade_menu.config(font=("Arial", 14), bg="white")
        dificuldade_menu.pack(anchor="center")

        # Quem começa
        turno_frame = tk.Frame(self.menu_frame, bg="lightblue")
        turno_frame.pack(pady=10)
        tk.Label(turno_frame, text="Quem vai começar:", foreground='white', font=("Arial", 18), bg="lightblue").pack(anchor="center")
        self.turno_var = tk.StringVar(value='Você')
        turno_menu = tk.OptionMenu(turno_frame, self.turno_var, 'Você', 'Computador')
        turno_menu.config(font=("Arial", 14), bg="white")
        turno_menu.pack(anchor="center")

        # Escolha de símbolo
        simbolo_frame = tk.Frame(self.menu_frame, bg="lightblue")
        simbolo_frame.pack(pady=10)
        tk.Label(simbolo_frame, text="Escolha seu símbolo:", foreground='white', font=("Arial", 18), bg="lightblue").pack(anchor="center")
        self.simbolo_var = tk.StringVar(value='X')
        simbolo_menu = tk.OptionMenu(simbolo_frame, self.simbolo_var, 'X', 'O')
        simbolo_menu.config(font=("Arial", 14), bg="white")
        simbolo_menu.pack(anchor="center")

        # Botão de iniciar
        iniciar_btn = tk.Button(self.menu_frame, text="Iniciar Jogo", command=self.iniciar_jogo,
                                font=("Arial", 16, "bold"), bg="green", fg="white", padx=10, pady=5)
        iniciar_btn.pack(pady=20)
     

    def iniciar_jogo(self):
        self.menu_frame.pack_forget()
        self.tabuleiro = [[' ' for _ in range(15)] for _ in range(15)]  
        self.dificuldade = self.dificuldade_var.get()
        self.jogador = self.simbolo_var.get()
        self.adv = 'O' if self.jogador == 'X' else 'X'
        self.criar_botao()

        if self.turno_var.get() == 'Computador':
            self.jogada_pc()

    def criar_botao(self):
        for i in range(15):
            for j in range(15):
                btn = tk.Button(self.master, text=' ', font=('Arial', 15),
                                command=lambda linha=i, coluna=j: self.jogada(linha, coluna))
                btn.grid(row=i, column=j, sticky='nsew')
                self.botoes[i][j] = btn

        for i in range(15):
            self.master.grid_rowconfigure(i, weight=1)
            self.master.grid_columnconfigure(i, weight=1)

     
        voltar_btn = tk.Button(self.master, text="Voltar ao Menu", command=self.voltar_menu)
        voltar_btn.grid(row=16, column=0, columnspan=15)

    def voltar_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.iniciar_menu()

    def jogada(self, linha, coluna):
        if self.tabuleiro[linha][coluna] == ' ':
            self.tabuleiro[linha][coluna] = self.jogador
            self.botoes[linha][coluna].config(text=self.jogador)

            if self.checar_vencedor(self.jogador):
                messagebox.showinfo("Fim de Jogo", f"Você ganhou! Placar: {self.placar_jogador + 1} a {self.placar_pc}")
                self.placar_jogador += 1
                self.resetar_jogo()
                return

            if all(cell != ' ' for row in self.tabuleiro for cell in row):
                messagebox.showinfo("Empate", "O jogo terminou em empate!")
                self.resetar_jogo()
                return

            self.jogada_pc()

    def jogada_pc(self):
        if self.dificuldade == 'Fácil':
            self.jogada_aleatoria()
        elif self.dificuldade == 'Médio':
            if not self.jogada_defensiva():
                self.jogada_aleatoria()
        else:
            self.escolher_melhor_jogada()

        if self.checar_vencedor(self.adv):
            messagebox.showinfo("Fim de Jogo", f"O Computador ganhou! Placar: {self.placar_jogador} a {self.placar_pc + 1}")
            self.placar_pc += 1
            self.resetar_jogo()

    def jogada_aleatoria(self):
        vazios = [(i, j) for i in range(15) for j in range(15) if self.tabuleiro[i][j] == ' ']
        if vazios:
            linha, coluna = random.choice(vazios)
            self.tabuleiro[linha][coluna] = self.adv
            self.botoes[linha][coluna].config(text=self.adv)

    def jogada_defensiva(self):
        for i in range(15):
            for j in range(15):
                if self.tabuleiro[i][j] == ' ':
                    self.tabuleiro[i][j] = self.jogador
                    if self.checar_vencedor(self.jogador):
                        self.tabuleiro[i][j] = self.adv
                        self.botoes[i][j].config(text=self.adv)
                        return True
                    self.tabuleiro[i][j] = ' '
        return False

    def escolher_melhor_jogada(self):
        melhor_pontuacao = float('-inf')
        melhor_jogada = None

        for linha in range(15):
            for coluna in range(15):
                if self.tabuleiro[linha][coluna] == ' ':
                    self.tabuleiro[linha][coluna] = self.adv
                    pontuacao = self.avaliar_tabuleiro(self.adv)
                    self.tabuleiro[linha][coluna] = ' '

                    if pontuacao > melhor_pontuacao:
                        melhor_pontuacao = pontuacao
                        melhor_jogada = (linha, coluna)

        if melhor_jogada:
            linha, coluna = melhor_jogada
            self.tabuleiro[linha][coluna] = self.adv
            self.botoes[linha][coluna].config(text=self.adv)

    def avaliar_tabuleiro(self, jogador):
        pontos = 0
        adversario = self.jogador if jogador == self.adv else self.adv

        def contar_padroes(seq, peca):
            
            if seq.count(peca) == 5:
                return 1000
            elif seq.count(peca) == 4 and seq.count(' ') == 1:
                return 50
            elif seq.count(peca) == 3 and seq.count(' ') == 2:
                return 10
            elif seq.count(peca) == 2 and seq.count(' ') == 3:
                return 1
            return 0

      
        for linha in range(15):
            for coluna in range(11):
                seq = self.tabuleiro[linha][coluna:coluna + 5]
                pontos += contar_padroes(seq, jogador)
                pontos -= contar_padroes(seq, adversario)

      
        for coluna in range(15):
            for linha in range(11):
                seq = [self.tabuleiro[linha + k][coluna] for k in range(5)]
                pontos += contar_padroes(seq, jogador)
                pontos -= contar_padroes(seq, adversario)

       
        for linha in range(11):
            for coluna in range(11):
                seq = [self.tabuleiro[linha + k][coluna + k] for k in range(5)]
                pontos += contar_padroes(seq, jogador)
                pontos -= contar_padroes(seq, adversario)

      
        for linha in range(11):
            for coluna in range(4, 15):
                seq = [self.tabuleiro[linha + k][coluna - k] for k in range(5)]
                pontos += contar_padroes(seq, jogador)
                pontos -= contar_padroes(seq, adversario)

        return pontos

    def checar_vencedor(self, jogador):
        for linha in range(15):
            for coluna in range(11):
                if all(self.tabuleiro[linha][coluna + k] == jogador for k in range(5)):
                    return True

        for coluna in range(15):
            for linha in range(11):
                if all(self.tabuleiro[linha + k][coluna] == jogador for k in range(5)):
                    return True

        for linha in range(11):
            for coluna in range(11):
                if all(self.tabuleiro[linha + k][coluna + k] == jogador for k in range(5)):
                    return True

        for linha in range(11):
            for coluna in range(4, 15):
                if all(self.tabuleiro[linha + k][coluna - k] == jogador for k in range(5)):
                    return True

        return False

    def resetar_jogo(self):
        if self.placar_jogador == 3 or self.placar_pc == 3:
            vencedor = "Você" if self.placar_jogador == 3 else "O Computador"
            resposta = messagebox.askyesno("Fim da Série", f"{vencedor} venceu 3 partidas! Deseja continuar jogando na mesma dificuldade?")
            
            if resposta: 
                self.placar_jogador = 0
                self.placar_pc = 0
            else:  
                self.placar_jogador = 0
                self.placar_pc = 0
                self.voltar_menu()
                return

        self.tabuleiro = [[' ' for _ in range(15)] for _ in range(15)]
        for i in range(15):
            for j in range(15):
                self.botoes[i][j].config(text=' ')


if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoDaVelha(root)
    root.mainloop()
