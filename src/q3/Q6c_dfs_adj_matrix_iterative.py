"""Questão 6c) Busca em Profundidade (DFS) iterativa com matriz de adjacência
"""

def dfs_matriz_iter(adj, inicio=0):
    n = len(adj)
    for linha in adj:
        if len(linha) != n:
            raise ValueError("A matriz deve ser quadrada.")
    if inicio < 0 or inicio >= n:
        raise ValueError("Vértice inicial inválido.")
    visitado = [False] * n
    ordem = []
    pilha = [inicio]
    while pilha:
        u = pilha.pop()
        if not visitado[u]:
            visitado[u] = True
            ordem.append(u)
            for v in range(n - 1, -1, -1):
                if adj[u][v] and not visitado[v]:
                    pilha.append(v)
    return ordem

def exibir_ordem(prefixo, ordem):
    print(prefixo + ":", ordem)


ADJ = [
    [0, 1, 1, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 1],
    [0, 0, 1, 0],
]
exibir_ordem("DFS (iter) a partir de 0", dfs_matriz_iter(ADJ, 0))
exibir_ordem("DFS (iter) a partir de 2", dfs_matriz_iter(ADJ, 2))
