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
    """
    Parameters
    ----------
    jogo : matriz do jogo

    Returns
    -------
    ganhador : int
        -1 se for empate em um tabuleiro cheio;
        0 se não tiver ganhador;
        1 ou 2 se tiver ganhador
    """
    np.diagonal
    # colunas
    for i in range(len(jogo)):
        for j in range(len(jogo[0]) - 4, -1, -1):
            slice = jogo[i, j:j+4]
            # print(f"{i+1} {j+1}-{j+4} {slice}")
            if all(item == slice[0] and item != 0 for item in slice):
                return slice[0]
    # linhas
    for i in range(len(jogo) - 3):
        for j in range(len(jogo[0]) - 1, -1, -1):
            slice = jogo[i:i+4, j]
            # print(f"{i+1}-{i+4} {j+1} {slice}")
            if all(item == slice[0] and item != 0 for item in slice):
                return slice[0]
    # diagonal principal
    for i in range(len(jogo) - 3):
        for j in range(len(jogo[0]) - 4, -1, -1):
            slice = [jogo[i + x, j + x] for x in range(4)]
            # print(f"{i+1} {j+1} {slice}")
            if all(item == slice[0] and item != 0 for item in slice):
                return slice[0]
    # diagonal secundária
    for i in range(len(jogo) - 3):
        for j in range(len(jogo[0]) - 4, -1, -1):
            slice = [jogo[i - x + 3, j + x] for x in range(4)]
            # print(f"{i+4} {j+1} {slice}")
            if all(item == slice[0] and item != 0 for item in slice):
                return slice[0]
    # checa se tabuleiro ta cheio
    for i in range(len(jogo)):
        for j in range(len(jogo[0])):
            if jogo[i][j] == 0:
                return 0
    return -1

def printar_jogo(jogo) -> None:
    print("╭─1─2─3─4─5─6─7─╮")
    for c in range(len(jogo[0])):
        print(f"{c+1} ", end="")
        for l in range(len(jogo)):
            oq = jogo[l][c]
            if oq == 0:
                print("  ", end="")
            elif oq == 1:
                print("\x1b[31m⬤\x1b[0m ", end="")
            else:
                print("\x1b[33m⬤\x1b[0m ", end="")
        print("│")
    print("╰─1─2─3─4─5─6─7─╯")

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



def minimax_alfa_beta(tabuleiro, profundidade, alfa, beta, maximizando):
    vencedor = ganhou(tabuleiro)

    if vencedor != 0 or profundidade == 0:
        if vencedor == 2: return 100000 + profundidade
        if vencedor == 1: return -100000 - profundidade
        return heuristica_intermediaria(tabuleiro, 2) - heuristica_intermediaria(tabuleiro, 1)

    if maximizando:
        melhor_valor = -float('inf')
        for coluna in range(7):
            if tabuleiro[coluna][0] == 0:
                tabuleiro_novo = adicionar(tabuleiro, 2, coluna)
                valor = minimax_alfa_beta(tabuleiro_novo, profundidade - 1, alfa, beta, False)
                if valor > melhor_valor:
                    melhor_valor = valor
                alfa = max(alfa, melhor_valor)
                if alfa >= beta:
                    break
        return melhor_valor
    else:
        pior_valor = float('inf')
        for coluna in range(7):
            if tabuleiro[coluna][0] == 0:
                tabuleiro_novo = adicionar(tabuleiro, 1, coluna)
                valor = minimax_alfa_beta(tabuleiro_novo, profundidade - 1, alfa, beta, True)
                if valor < pior_valor:
                    pior_valor = valor
                beta = min(beta, pior_valor)
                if alfa >= beta:
                    break
        return pior_valor
    
def inteligencia2(tabuleiro) -> int:
    profundidade = 4
    melhor_jogada = 0
    melhor_valor = -float('inf')
    for coluna in range(7):
        if tabuleiro[coluna][0] == 0:
            novo_tabuleiro = adicionar(tabuleiro, 2, coluna)
            valor = minimax_alfa_beta(novo_tabuleiro,profundidade - 1,-float('inf'),float('inf'),False)
            if valor > melhor_valor:
                melhor_valor = valor
                melhor_jogada = coluna
    return melhor_jogada

# Kevin
def minimax_alfa_beta_ordenado(tabuleiro, profundidade, alfa, beta, maximizando, tempo_limite, inicio_tempo):
    if time() - inicio_tempo > tempo_limite:  # Verifica limite de tempo
        return heuristica_avancada(tabuleiro, 2) - heuristica_avancada(tabuleiro, 1)
    
    vencedor = ganhou(tabuleiro)
    if vencedor != 0 or profundidade == 0:
        if vencedor == 2: return 100000 + profundidade
        if vencedor == 1: return -100000 - profundidade
        return heuristica_avancada(tabuleiro, 2) - heuristica_avancada(tabuleiro, 1)

    # Ordena jogadas pela heurística para maximizar poda
    colunas_ordenadas = ordenar_jogadas(tabuleiro, 2 if maximizando else 1, heuristica_avancada)
    
    if maximizando:
        melhor_valor = -float('inf')
        for coluna in colunas_ordenadas:
            if tabuleiro[coluna][0] == 0:
                tabuleiro_novo = adicionar(tabuleiro, 2, coluna)
                valor = minimax_alfa_beta_ordenado(tabuleiro_novo, profundidade - 1, alfa, beta, False, tempo_limite, inicio_tempo)
                if valor > melhor_valor:
                    melhor_valor = valor
                alfa = max(alfa, melhor_valor)
                if alfa >= beta:
                    break  # Poda alfa-beta
        return melhor_valor
    else:
        pior_valor = float('inf')
        for coluna in colunas_ordenadas:
            if tabuleiro[coluna][0] == 0:
                tabuleiro_novo = adicionar(tabuleiro, 1, coluna)
                valor = minimax_alfa_beta_ordenado(tabuleiro_novo, profundidade - 1, alfa, beta, True, tempo_limite, inicio_tempo)
                if valor < pior_valor:
                    pior_valor = valor
                beta = min(beta, pior_valor)
                if alfa >= beta:
                    break  # Poda alfa-beta
        return pior_valor

def inteligencia3(tabuleiro) -> int:
    profundidade_max = 10
    melhor_jogada = 0
    tempo_limite = 3.0
    inicio_tempo = time()
    
    # Iterando profundidade com limite de tempo
    for prof in range(6, profundidade_max + 1):
        if time() - inicio_tempo > tempo_limite:
            break
            
        melhor_valor = -float('inf')
        colunas_ordenadas = ordenar_jogadas(tabuleiro, 2, heuristica_avancada)
        
        jogada_temp = melhor_jogada
        for coluna in colunas_ordenadas:
            if time() - inicio_tempo > tempo_limite:
                break
                
            if tabuleiro[coluna][0] == 0:
                novo_tabuleiro = adicionar(tabuleiro, 2, coluna)
                valor = minimax_alfa_beta_ordenado(novo_tabuleiro, prof - 1, -float('inf'), float('inf'), False, tempo_limite, inicio_tempo)
                
                if valor > melhor_valor:
                    melhor_valor = valor
                    jogada_temp = coluna
        
        # Se completou a busca dessa profundidade, atualiza melhor jogada
        if time() - inicio_tempo <= tempo_limite:
            melhor_jogada = jogada_temp
    
    return melhor_jogada
# /Kevin

# ----------------- testes -----------------

def teste():
    # j1 = novo_jogo(6, 7)
    # printar_jogo(j1)
    # j1 = adicionar(j1, 1, 3)
    # printar_jogo(j1)
    # j1 = adicionar(j1, 2, 3)
    # printar_jogo(j1)

    j2 = novo_jogo(6, 7)
    for i in range(50):
        j2 = adicionar(j2, i % 2 + 1, randint(0, 6))
        if ganhou(j2) != 0:
            break

    # print(j2)
    printar_jogo(j2)
    print(f"{ganhou(j2) = }")

    # j3 = novo_jogo(6, 7)
    # j3 = adicionar(j3, 2, 3)
    # j3 = adicionar(j3, 1, 4)
    # j3 = adicionar(j3, 1, 5)
    # j3 = adicionar(j3, 1, 6)
    # printar_jogo(j3)
    # print(f"{ganhou(j3) = }")

    # a = time()

    # for _ in range(100000):
    #     _ = adicionar(j2, 1, 1)
    # print(f"tempo: {time() - a}")

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
        dif_s = input("Valor: ")
        try:
            dif = int(dif_s)
        except:
            print("Valor não reconhecido")
            continue

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
            match ganhador:
                case -1:
                    print("Partida terminou em um empate")
                case 1:
                    print("Humano ganhou")
                case 2:
                    print("IA ganhou")
            break



if __name__ == "__main__":
    # teste()
    jogar()
