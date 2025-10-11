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

# ----------------- inteligência -----------------

def inteligencia1(jogo) -> int:
    return 0

def inteligencia2(jogo) -> int:
    return 0

def inteligencia3(jogo) -> int:
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
