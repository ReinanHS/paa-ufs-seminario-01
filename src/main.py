import io
import pathlib
import random
import sys
from dataclasses import dataclass
from typing import List, Tuple, Optional

try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError:
    print("Erro: Bibliotecas 'pandas' e 'matplotlib' são necessárias.")
    print("Instale-as com: pip install pandas matplotlib")
    sys.exit(1)

PONTOS_FILENAME = "pontos_caixeiro_viajante.csv"
MATRIZ_FILENAME = "matriz_distancias.csv"

POP_SIZE = 200
N_GERACOES = 200
TAXA_MUTACAO = 0.15
TAMANHO_TORNEIO = 5
ELITISMO = 2
SEMENTE = 42


def read_text(path: pathlib.Path, encoding="utf-8") -> str:
    return path.read_text(encoding=encoding)


def read_csv_clean(path_or_str: str, **read_csv_kwargs) -> pd.DataFrame:
    """
    Lê CSV e corrige caso a primeira linha venha com prefixo 'data:text/csv,...'
    sem tocar nas demais linhas.
    """
    p = pathlib.Path(path_or_str)
    raw = read_text(p, encoding="utf-8")
    lines = raw.splitlines()
    if lines and lines[0].startswith("data:text/csv"):

        parts = lines[0].split(",", 1)
        if len(parts) == 2:
            lines[0] = parts[1]
        raw = "\n".join(lines)
    return pd.read_csv(io.StringIO(raw), **read_csv_kwargs)


def validar_coords(df_pontos: pd.DataFrame) -> Tuple[List[str], List[Tuple[float, float]]]:
    """
    Garante colunas e tipos de Latitude/Longitude e retorna (labels, coords).
    Labels: usa 'Nome' se existir, senão índice incremental como string.
    """
    col_lat = None
    col_lng = None

    candidatos_lat = ["Latitude", "latitude", "lat", "Lat"]
    candidatos_lng = ["Longitude", "longitude", "lng", "Lon", "long", "Long"]

    for c in candidatos_lat:
        if c in df_pontos.columns:
            col_lat = c
            break
    for c in candidatos_lng:
        if c in df_pontos.columns:
            col_lng = c
            break

    if col_lat is None or col_lng is None:
        raise ValueError(
            f"Não encontrei colunas de latitude/longitude. Colunas disponíveis: {list(df_pontos.columns)}"
        )

    df_pontos[col_lat] = pd.to_numeric(df_pontos[col_lat], errors="raise")
    df_pontos[col_lng] = pd.to_numeric(df_pontos[col_lng], errors="raise")

    if df_pontos[col_lat].isna().any() or df_pontos[col_lng].isna().any():
        raise ValueError("Latitude/Longitude contém NaN após leitura/conversão.")

    if "Nome" in df_pontos.columns:
        labels = df_pontos["Nome"].astype(str).tolist()
    else:
        labels = [str(i) for i in range(len(df_pontos))]

    coords = list(zip(df_pontos[col_lng].astype(float), df_pontos[col_lat].astype(float)))
    xs = np.array([c[0] for c in coords], dtype=float)
    ys = np.array([c[1] for c in coords], dtype=float)
    if not np.isfinite(xs).all() or not np.isfinite(ys).all():
        raise ValueError("Coordenadas não finitas detectadas (NaN/Inf).")

    return labels, coords


def validar_matriz(df_matriz: pd.DataFrame, n: int) -> np.ndarray:
    """
    Confirma que a matriz é NxN e numérica.
    Se tiver índice textual na 1ª coluna (rótulos), usar index_col=0 ao ler o CSV ajuda.
    """

    df_numeric = df_matriz.apply(pd.to_numeric, errors="raise")

    if df_numeric.shape[0] != df_numeric.shape[1]:
        raise ValueError(f"Matriz de distâncias não é quadrada: {df_numeric.shape}")

    if df_numeric.shape[0] != n:
        raise ValueError(
            f"Tamanho da matriz ({df_numeric.shape[0]}) difere da quantidade de pontos ({n})."
        )

    mat = df_numeric.values.astype(float)
    if not np.isfinite(mat).all():
        raise ValueError("Matriz de distâncias contém valores não finitos (NaN/Inf).")

    np.fill_diagonal(mat, 0.0)
    return mat


@dataclass
class TSPInstance:
    labels: List[str]
    coords: List[Tuple[float, float]]
    dist: np.ndarray


def custo_rota(rota: List[int], dist: np.ndarray) -> float:
    """
    Soma as arestas, incluindo retorno ao início.
    rota: permutação de [0..N-1]
    """
    n = len(rota)
    total = 0.0
    for i in range(n):
        a = rota[i]
        b = rota[(i + 1) % n]
        total += dist[a, b]
    return float(total)


def gerar_populacao(n: int, pop_size: int) -> List[List[int]]:
    base = list(range(n))
    pop = [random.sample(base, n) for _ in range(pop_size)]
    return pop


def torneio(pop: List[List[int]], fitness: List[float], k: int) -> List[int]:
    participantes = random.sample(range(len(pop)), k)
    melhor = max(participantes, key=lambda idx: fitness[idx])
    return pop[melhor][:]


def crossover_ox(pai: List[int], mae: List[int]) -> List[int]:
    """
    Order Crossover (OX): mantém segmento do pai e preenche na ordem do mae.
    """
    n = len(pai)
    a, b = sorted(random.sample(range(n), 2))
    filho = [None] * n

    filho[a:b + 1] = pai[a:b + 1]

    pos = (b + 1) % n
    for gene in mae:
        if gene not in filho:
            filho[pos] = gene
            pos = (pos + 1) % n
    return filho


def mutacao_swap(rota: List[int], taxa: float) -> None:
    if random.random() < taxa:
        i, j = random.sample(range(len(rota)), 2)
        rota[i], rota[j] = rota[j], rota[i]


def evoluir(tsp: TSPInstance) -> Tuple[List[int], float, List[float]]:
    n = len(tsp.labels)
    pop = gerar_populacao(n, POP_SIZE)
    historico_melhor = []
    melhor_rota: Optional[List[int]] = None
    melhor_custo: float = float("inf")

    for gen in range(N_GERACOES):
        custos = [custo_rota(ind, tsp.dist) for ind in pop]

        fitness = [-c for c in custos]

        for ind, c in zip(pop, custos):
            if c < melhor_custo:
                melhor_custo = c
                melhor_rota = ind[:]

        historico_melhor.append(melhor_custo)

        nova = []

        elite_idx = np.argsort(custos)[:ELITISMO]
        for idx in elite_idx:
            nova.append(pop[idx][:])

        while len(nova) < POP_SIZE:
            p1 = torneio(pop, fitness, TAMANHO_TORNEIO)
            p2 = torneio(pop, fitness, TAMANHO_TORNEIO)
            filho = crossover_ox(p1, p2)
            mutacao_swap(filho, TAXA_MUTACAO)
            nova.append(filho)

        pop = nova

    assert melhor_rota is not None
    return melhor_rota, melhor_custo, historico_melhor


def plot_melhor_rota(tsp: TSPInstance, rota: List[int], custo: float, save_as: Optional[str] = None):
    """
    Plota cidades (scatter), rótulos e polilinha na ordem da rota, fechando o ciclo.
    """
    xs = np.array([tsp.coords[i][0] for i in rota] + [tsp.coords[rota[0]][0]], dtype=float)
    ys = np.array([tsp.coords[i][1] for i in rota] + [tsp.coords[rota[0]][1]], dtype=float)

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.set_title(f"Melhor Rota Encontrada — Distância total: {custo:.3f}", pad=12)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    ax.plot(xs, ys, linewidth=2, alpha=0.9)

    all_x = np.array([c[0] for c in tsp.coords], dtype=float)
    all_y = np.array([c[1] for c in tsp.coords], dtype=float)
    ax.scatter(all_x, all_y, s=60, zorder=5)

    for i, (x, y) in enumerate(tsp.coords):
        ax.text(x, y, f" {tsp.labels[i]}", fontsize=9, ha="left", va="center")

    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(True, alpha=0.25)

    plt.tight_layout()
    if save_as:
        plt.savefig(save_as, dpi=150)
    plt.show()


def plot_convergencia(historico: List[float], save_as: Optional[str] = None):
    """
    Curva de convergência do melhor custo por geração.
    """
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(range(1, len(historico) + 1), historico, linewidth=2)
    ax.set_title("Convergência do AG (melhor custo por geração)")
    ax.set_xlabel("Geração")
    ax.set_ylabel("Custo (distância)")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_as:
        plt.savefig(save_as, dpi=150)
    plt.show()


def carregar_instancia(pontos_path: str, matriz_path: str) -> TSPInstance:
    df_pontos = read_csv_clean(pontos_path)

    labels, coords = validar_coords(df_pontos)

    df_matriz = read_csv_clean(matriz_path, index_col=0)

    dist = validar_matriz(df_matriz, n=len(coords))

    return TSPInstance(labels=labels, coords=coords, dist=dist)


def main():
    random.seed(SEMENTE)
    np.random.seed(SEMENTE)

    base_dir = pathlib.Path(".")
    caminhos_tentativa = [
        base_dir / PONTOS_FILENAME,
        pathlib.Path("../data") / PONTOS_FILENAME,
    ]
    pontos_path = None
    for c in caminhos_tentativa:
        if c.exists():
            pontos_path = str(c)
            break
    if pontos_path is None:
        raise FileNotFoundError(f"Arquivo de pontos não encontrado: {PONTOS_FILENAME}")

    caminhos_tentativa = [
        base_dir / MATRIZ_FILENAME,
        pathlib.Path("../data") / MATRIZ_FILENAME,
    ]
    matriz_path = None
    for c in caminhos_tentativa:
        if c.exists():
            matriz_path = str(c)
            break
    if matriz_path is None:
        raise FileNotFoundError(f"Arquivo de matriz não encontrado: {MATRIZ_FILENAME}")

    tsp = carregar_instancia(pontos_path, matriz_path)

    print("\nIniciando a execução do Algoritmo Genético...")
    melhor_rota, melhor_custo, historico = evoluir(tsp)

    print("\n--- Resultados ---")
    print(f"Melhor custo (distância) encontrado: {melhor_custo:.4f}")
    print(f"Melhor rota (sequência de cidades): {melhor_rota}")

    print("\nGerando visualizações...")
    plot_melhor_rota(tsp, melhor_rota, melhor_custo, save_as=None)
    plot_convergencia(historico, save_as=None)


if __name__ == "__main__":
    main()
