"""Questão 1c) Encontrar o segundo menor elemento de um vetor,
"""

def segundo_menor(vetor):
    if len(vetor) < 2:
        return None
    menor = float("inf")
    segundo = float("inf")
    for numero in vetor:
        if numero < menor:
            segundo = menor
            menor = numero
        elif menor < numero < segundo:
            segundo = numero
    return segundo if segundo != float("inf") else None


v1 = [80, 60, 90, 10, 40, 20]
v2 = [70, 80, 40, 30, 50]
v3 = [100, 100, 100]
print("Segundo menor de", v1, "=", segundo_menor(v1))
print("Segundo menor de", v2, "=", segundo_menor(v2))
print("Segundo menor de", v3, "=", segundo_menor(v3))
