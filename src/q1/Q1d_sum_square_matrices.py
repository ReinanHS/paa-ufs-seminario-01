"""Questão 1d) Soma de duas matrizes quadradas n×n
"""

def soma_matrizes_quadradas(A, B):
    n = len(A)
    C = []
    for i in range(n):
        linha = []
        for j in range(n):
            linha.append(A[i][j] + B[i][j])
        C.append(linha)
    return C

def exibir_matriz(titulo, M):
    print(titulo)
    for linha in M:
        print(" ", linha)
    print()


A = [[10, 20], [30, 40]]
B = [[50, 60], [70, 80]]
C = soma_matrizes_quadradas(A, B)
exibir_matriz("Matriz A:", A)
exibir_matriz("Matriz B:", B)
exibir_matriz("A + B:", C)
