"""Questão 1b) Inserção no final da lista sem ponteiro para o último nó
"""

class Node:
    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo

def inserir_no_final_sem_cauda(cabeca, x):
    novo = Node(x)
    if cabeca is None:
        return novo
    atual = cabeca
    while atual.proximo is not None:
        atual = atual.proximo
    atual.proximo = novo
    return cabeca

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
cabeca = inserir_no_final_sem_cauda(cabeca, 10)
cabeca = inserir_no_final_sem_cauda(cabeca, 20)
cabeca = inserir_no_final_sem_cauda(cabeca, 30)
exibir(cabeca)
