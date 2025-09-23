"""6b) Busca em Profundidade (DFS) recursiva com matriz de adjacência
"""

def dfs_matriz_rec(adj, inicio=0):
    n = len(adj)
    for linha in adj:
        if len(linha) != n:
            raise ValueError("A matriz deve ser quadrada.")
    if inicio < 0 or inicio >= n:
        raise ValueError("Vértice inicial inválido.")
    visitado = [False] * n
    ordem = []
    def dfs(u):
        visitado[u] = True
        ordem.append(u)
        for v in range(n):
            if adj[u][v] and not visitado[v]:
                dfs(v)
    dfs(inicio)
    return ordem

def exibir_ordem(prefixo, ordem):
    print(prefixo + ":", ordem)

ADJ = [
    [0, 1, 1, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 1],
    [0, 0, 1, 0],
]
exibir_ordem("DFS (rec) a partir de 0", dfs_matriz_rec(ADJ, 0))
exibir_ordem("DFS (rec) a partir de 2", dfs_matriz_rec(ADJ, 2))
