"""2b) Intervalo (max - min) para vetor desordenado em uma única passagem
"""

def intervalo_desordenado(vetor):
    if not vetor:
        raise ValueError("Vetor vazio.")
    minimo = vetor[0]
    maximo = vetor[0]
    for v in vetor[1:]:
        if v < minimo:
            minimo = v
        if v > maximo:
            maximo = v
    return maximo - minimo

print("Intervalo de [4, 9, 1] =", intervalo_desordenado([4, 9, 1]))
print("Intervalo de [-5, 10, 0, 5, -10] =", intervalo_desordenado([-5, 10, 0, 5, -10]))
