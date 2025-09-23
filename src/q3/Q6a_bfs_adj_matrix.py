"""6a) Busca em Largura (BFS) usando matriz de adjacência
"""

from collections import deque

def bfs_matriz(adj, inicio=0):
    n = len(adj)
    for linha in adj:
        if len(linha) != n:
            raise ValueError("A matriz deve ser quadrada.")
    if inicio < 0 or inicio >= n:
        raise ValueError("Vértice inicial inválido.")
    visitado = [False] * n
    ordem = []
    fila = deque([inicio])
    visitado[inicio] = True
    while fila:
        u = fila.popleft()
        ordem.append(u)
        for v in range(n):
            if adj[u][v] and not visitado[v]:
                visitado[v] = True
                fila.append(v)
    return ordem

def exibir_ordem(prefixo, ordem):
    print(prefixo + ":", ordem)

ADJ = [
    [0, 1, 0, 0],
    [1, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
]
exibir_ordem("BFS a partir de 0", bfs_matriz(ADJ, 0))
exibir_ordem("BFS a partir de 1", bfs_matriz(ADJ, 1))
