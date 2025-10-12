from random import randint
from time import time
import numpy as np

# ----------------- implementação -----------------

def novo_jogo(linhas: int, cols: int):
    return np.zeros((cols, linhas), dtype=int)

def adicionar(jogo, player: int, pos: int):
    nova = jogo.copy()
    col = nova[pos]
    for i in range(len(col) - 1, -1, -1):
        if col[i] == 0:
            col[i] = player
            break
    return nova

def ganhou(jogo) -> int:
    for col in jogo:
        for i in range(len(col) - 3):
            slice = col[i:i+4]
            if all(item == slice[0] and item != 0 for item in slice):
                return slice[0]
    for i in range(len(jogo) - 3):
        for j in range(len(jogo[0])):
            v = jogo[i][j]
            if v == 0:
                continue
            igual = True
            for o in range(1, 4):
                if int(jogo[i + o][j]) != int(v):
                    igual = False
            if igual:
                return int(v)
    # falta verificar se alguém ganhou na diagonal
    for i in range(len(jogo) - 3):
        pass
    return 0

def printar_jogo(jogo) -> None:
    print("╭1─2─3─4─5─6─7─╮")
    for c in range(len(jogo[0])):
        print("│", end="")
        for l in range(len(jogo)):
            oq = jogo[l][c]
            if oq == 0:
                print("  ", end="")
            elif oq == 1:
                print("\x1b[31m⬤\x1b[0m ", end="")
            else:
                print("\x1b[33m⬤\x1b[0m ", end="")
        print("│")
    print("╰1─2─3─4─5─6─7─╯")

# ----------------- inteligências -----------------
def heuristica_simples(tabuleiro, jogador):
    pontos = 0
    for coluna in range(7):
        for linha in range(6):
            if tabuleiro[coluna][linha] == jogador:
                pontos += 1
                if coluna == 3:
                    pontos += 1
    return pontos

def heuristica_intermediaria(tabuleiro, jogador):
    pontos = 0
    # Horizontal
    for linha in range(6):
        for coluna in range(4):
            janela = [tabuleiro[coluna+i][linha] for i in range(4)]
            if janela.count(jogador) == 3 and janela.count(0) == 1:
                pontos += 10
            elif janela.count(jogador) == 2 and janela.count(0) == 2:
                pontos += 3
    # Vertical
    for coluna in range(7):
        for linha in range(3):
            janela = [tabuleiro[coluna][linha+i] for i in range(4)]
            if janela.count(jogador) == 3 and janela.count(0) == 1:
                pontos += 10
            elif janela.count(jogador) == 2 and janela.count(0) == 2:
                pontos += 3
    # Diagonal 1
    for coluna in range(4):
        for linha in range(3):
            janela = [tabuleiro[coluna+i][linha+i] for i in range(4)]
            if janela.count(jogador) == 3 and janela.count(0) == 1:
                pontos += 10
            elif janela.count(jogador) == 2 and janela.count(0) == 2:
                pontos += 3
    # Diagonal 2
    for coluna in range(3, 7):
        for linha in range(3):
            janela = [tabuleiro[coluna-i][linha+i] for i in range(4)]
            if janela.count(jogador) == 3 and janela.count(0) == 1:
                pontos += 10
            elif janela.count(jogador) == 2 and janela.count(0) == 2:
                pontos += 3
    return pontos

def heuristica_avancada(tabuleiro, jogador):
    pontos = 0
    # Possíveis vitórias
    for linha in range(6):
        if tabuleiro[3][linha] == jogador:
            pontos += 4
    for linha in range(6):
        for coluna in range(4):
            janela = [tabuleiro[coluna+i][linha] for i in range(4)]
            pontos += avaliar_janela(janela, jogador)
    for coluna in range(7):
        for linha in range(3):
            janela = [tabuleiro[coluna][linha+i] for i in range(4)]
            pontos += avaliar_janela(janela, jogador)
    for coluna in range(4):
        for linha in range(3):
            janela = [tabuleiro[coluna+i][linha+i] for i in range(4)]
            pontos += avaliar_janela(janela, jogador)
    for coluna in range(3, 7):
        for linha in range(3):
            janela = [tabuleiro[coluna-i][linha+i] for i in range(4)]
            pontos += avaliar_janela(janela, jogador)
    # Bloquear
    pontos -= heuristica_intermediaria(tabuleiro, 3-jogador) * 2
    return pontos

# Jogadas Futuras
def avaliar_janela(janela, jogador):
    pontos = 0
    adversario = 1 if jogador == 2 else 2
    if janela.count(jogador) == 4:
        pontos += 1000
    elif janela.count(jogador) == 3 and janela.count(0) == 1:
        pontos += 50
    elif janela.count(jogador) == 2 and janela.count(0) == 2:
        pontos += 10
    # Bloqueios Possíveis
    if janela.count(adversario) == 3 and janela.count(0) == 1:
        pontos -= 80
    return pontos

def ordenar_jogadas(tabuleiro, jogador, heuristica_func):
    jogadas = [] 
    for coluna in range(7): 
        if tabuleiro[coluna][0] == 0:
            novo_tabuleiro = adicionar(tabuleiro, jogador, coluna)
            valor = heuristica_func(novo_tabuleiro, jogador)
            jogadas.append((valor, coluna))
    jogadas.sort(reverse=True)
    return [col for valor, col in jogadas]

def minimax_simples(tabuleiro, profundidade, maximizando):
    # Minimax simples, sem poda alfa-beta
    vencedor = ganhou(tabuleiro)
    if profundidade == 0 or vencedor != 0:
        return heuristica_simples(tabuleiro, 2) - heuristica_simples(tabuleiro, 1)

    # MAX
    if maximizando:
        melhor_valor = float('-inf')
        for coluna in range(7):
            if tabuleiro[coluna][0] == 0: # se a coluna não estiver cheia
                tabuleiro_novo = adicionar(tabuleiro, 2, coluna) # simula a jogada
                valor = minimax_simples(tabuleiro_novo, profundidade-1, False) # melhor jogada
                if valor > melhor_valor:
                    melhor_valor = valor
        return melhor_valor
    else:
        pior_valor = float('inf')
        for coluna in range(7):
            if tabuleiro[coluna][0] == 0:
                tabuleiro_novo = adicionar(tabuleiro, 1, coluna)
                valor = minimax_simples(tabuleiro_novo, profundidade-1, True)
                if valor < pior_valor:
                    pior_valor = valor
        return pior_valor


def inteligencia1(tabuleiro) -> int:
    melhor_jogada = 0 
    melhor_valor = -float('inf')
    for coluna in range(7): # para cada coluna
        if tabuleiro[coluna][0] == 0: # se a coluna não estiver cheia
            novo_tabuleiro = adicionar(tabuleiro, 2, coluna) # simula a jogada
            valor = minimax_simples(novo_tabuleiro, 2, False) # melhor jogada
            if valor > melhor_valor:
                melhor_valor = valor
                melhor_jogada = coluna
    return melhor_jogada

def inteligencia2(tabuleiro) -> int:
   return 0

def inteligencia3(tabuleiro) -> int:
   return 0 

# ----------------- testes -----------------

def teste():
    # j1 = novo_jogo(6, 7)
    # printar_jogo(j1)
    # j1 = adicionar(j1, 1, 3)
    # printar_jogo(j1)
    # j1 = adicionar(j1, 2, 3)
    # printar_jogo(j1)

    j2 = novo_jogo(6, 7)
    for i in range(10):
        j2 = adicionar(j2, i % 2 + 1, randint(0, 6))

    printar_jogo(j2)
    print(f"{ganhou(j2) = }")

    j3 = novo_jogo(6, 7)
    j3 = adicionar(j3, 2, 3)
    j3 = adicionar(j3, 1, 4)
    j3 = adicionar(j3, 1, 5)
    j3 = adicionar(j3, 1, 6)
    printar_jogo(j3)
    print(f"{ganhou(j3) = }")

    a = time()

    for _ in range(100000):
        _ = adicionar(j2, 1, 1)

    print(f"tempo: {time() - a}")

# ----------------- interação -----------------

def pegar_input(jogo) -> int:
    jogada = -1 # -1 pq é uma posição inválida

    while True:
        input_s = input("Qual sua jogada (1 - 7): ")
        # já não transforma em int aq pra ainda poder dar C-c
        try:
            jogada = int(input_s) - 1
        except:
            print("Valor não reconhecido")
            continue
        if jogada < 0 or jogada > 6: # checa se ta dentro do tabuleiro
            print("Selecione dentro do tabuleiro")
            continue
        if jogo[jogada][0] != 0: # checa se é uma posição válida
            print("Coluna cheia")
            continue
        break

    return jogada

def jogar():
    print("Selecione a dificuldade (1 - Iniciante, 2 - Intermediário, 3 - Profissional)")
    dif = -1
    while dif < 1 or dif > 3:
        try:
            dif = int(input("Valor: "))
        except:
            print("Valor não reconhecido")

    jogo = novo_jogo(6, 7)
    jogando = 1
    printar_jogo(jogo)
    while True:
        if jogando == 1:
            ini = time()
            jogada = pegar_input(jogo)
            jogo = adicionar(jogo, jogando, jogada)
            jogando = 2
            print(f"Você demorou {time() - ini :.2} segundos")
        else:
            ini = time()
            jogada = -1
            match dif:
                case 1:
                    jogada = inteligencia1(jogo)
                case 2:
                    jogada = inteligencia2(jogo)
                case 3:
                    jogada = inteligencia3(jogo)
            jogo = adicionar(jogo, jogando, jogada)
            jogando = 1
            print(f"A IA selecionou {jogada} e demorou {time() - ini :.2} segundos")
            pass
    
        printar_jogo(jogo)
        ganhador = ganhou(jogo)
        if ganhador != 0:
            print(f"Ganhador: {ganhador}")
            break



if "__main__" == __name__:
    # teste()
    jogar()
