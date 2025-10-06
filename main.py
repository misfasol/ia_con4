import copy
from random import randint
from time import time
import numpy as np

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
            sl = col[i:i+4]
            if all(item == sl[0] and item != 0 for item in sl):
                return sl[0]
    for i in range(len(jogo[0])):
        for j in range(len(jogo) - 2):
            # print(i, j)
            pass
    return 0

def printar_jogo(jogo) -> None:
    print("+--------+")
    for c in range(len(jogo[0])):
        print("|", end="")
        for l in range(len(jogo)):
            oq = jogo[l][c]
            if oq == 0:
                print(" ", end="")
            elif oq == 1:
                print("X", end="")
            else:
                print("O", end="")
        print("|")

j1 = novo_jogo(6, 7)
# printar_jogo(j1)
j1 = adicionar(j1, 1, 3)
# printar_jogo(j1)
j1 = adicionar(j1, 2, 3)
printar_jogo(j1)

j2 = novo_jogo(6, 7)
for i in range(10):
    j2 = adicionar(j2, i % 2 + 1, randint(0, 6))

printar_jogo(j2)
print(f"{ganhou(j2) = }")

a = time()

for _ in range(100000):
    _ = adicionar(j2, 1, 1)

print(f"tempo: {time() - a}")
