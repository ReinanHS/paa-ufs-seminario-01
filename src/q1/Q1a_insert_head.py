"""Questão 1a) Inserção na cabeça de uma lista simplesmente ligada
"""

class Node:
    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo

def inserir_na_cabeca(cabeca, x):
    return Node(x, cabeca)

def para_lista(cabeca):
    valores = []
    atual = cabeca
    while atual is not None:
        valores.append(atual.valor)
        atual = atual.proximo
    return valores

def exibir(cabeca):
    print("Lista:", " -> ".join(map(str, para_lista(cabeca))) if cabeca else "(vazia)")


cabeca = None
exibir(cabeca)
cabeca = inserir_na_cabeca(cabeca, 3)
cabeca = inserir_na_cabeca(cabeca, 2)
cabeca = inserir_na_cabeca(cabeca, 1)
exibir(cabeca)
