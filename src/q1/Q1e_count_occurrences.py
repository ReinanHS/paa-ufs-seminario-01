"""Questão 1e) Contar quantas vezes um valor aparece em um vetor desordenado
"""

def contar_ocorrencias(vetor, alvo):
    cont = 0
    for valor in vetor:
        if valor == alvo:
            cont += 1
    return cont

arr1 = [3, 8, 6, 3, 5, 4, 3]
arr2 = ["b", "c", "a", "c", "d", "a"]
print("Ocorrências de 3 em", arr1, "=", contar_ocorrencias(arr1, 3))
print("Ocorrências de 'a' em", arr2, "=", contar_ocorrencias(arr2, "a"))
