"""Questão 2a) Intervalo (max - min) para vetor já ordenado
"""

def intervalo_ordenado(vetor):
    if not vetor:
        raise ValueError("Vetor vazio.")
    return vetor[-1] - vetor[0]

print("Intervalo de [1, 4, 9] =", intervalo_ordenado([1, 4, 9]))
print("Intervalo de [-10, -5, 0, 5] =", intervalo_ordenado([-10, -5, 0, 5]))
