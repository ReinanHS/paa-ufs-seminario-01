import builtins
import math
import pathlib
import random

import matplotlib
import numpy as np
import pandas as pd
import pytest

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import src.main as mod


@pytest.fixture(autouse=True)
def _reseed():
    """Garante reprodutibilidade entre testes."""
    random.seed(mod.SEMENTE)
    np.random.seed(mod.SEMENTE)


@pytest.fixture
def square_instance():
    labels = ["A", "B", "C", "D"]
    coords = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]

    n = len(coords)
    dist = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = coords[i][0] - coords[j][0]
            dy = coords[i][1] - coords[j][1]
            dist[i, j] = math.hypot(dx, dy)

    return mod.TSPInstance(labels=labels, coords=coords, dist=dist)


def test_read_csv_clean_remove_prefix(tmp_path: pathlib.Path):
    p = tmp_path / "dados.csv"
    p.write_text("data:text/csv,col1,col2\n1,2\n3,4\n", encoding="utf-8")

    df = mod.read_csv_clean(str(p), dtype=int)
    assert list(df.columns) == ["col1", "col2"]
    assert df.shape == (2, 2)
    assert df.iloc[0, 0] == 1
    assert df.iloc[1, 1] == 4


def test_validar_coords_com_nome():
    df = pd.DataFrame(
        {
            "Nome": ["X", "Y", "Z"],
            "Latitude": [10.0, 11.0, 12.0],
            "Longitude": [20.0, 21.0, 22.0],
        }
    )
    labels, coords = mod.validar_coords(df)
    assert labels == ["X", "Y", "Z"]
    assert coords == [(20.0, 10.0), (21.0, 11.0), (22.0, 12.0)]


def test_validar_coords_sem_nome_usa_indices():
    df = pd.DataFrame({"lat": [0, 1], "lng": [2, 3]})
    labels, coords = mod.validar_coords(df)
    assert labels == ["0", "1"]
    assert coords == [(2.0, 0.0), (3.0, 1.0)]


def test_validar_coords_erro_colunas_invalidas():
    df = pd.DataFrame({"foo": [1, 2], "bar": [3, 4]})
    with pytest.raises(ValueError):
        mod.validar_coords(df)


def test_validar_matriz_ok_e_diagonal_zero():
    df = pd.DataFrame([[0, 2, 3], [4, 5, 6], [7, 8, 9]])
    mat = mod.validar_matriz(df, n=3)
    assert mat.shape == (3, 3)
    assert np.allclose(np.diag(mat), 0.0)


def test_validar_matriz_dimensoes_erradas():
    df = pd.DataFrame([[0, 1], [1, 0]])
    with pytest.raises(ValueError):
        mod.validar_matriz(df, n=3)


def test_carregar_instancia_happy_path(tmp_path: pathlib.Path):
    pontos = tmp_path / mod.PONTOS_FILENAME
    matriz = tmp_path / mod.MATRIZ_FILENAME

    pontos.write_text(
        "Nome,Latitude,Longitude\nA,0,0\nB,0,1\nC,1,1\nD,1,0\n",
        encoding="utf-8",
    )

    df = pd.DataFrame(
        [
            [0, 1, math.sqrt(2), 1],
            [1, 0, 1, math.sqrt(2)],
            [math.sqrt(2), 1, 0, 1],
            [1, math.sqrt(2), 1, 0],
        ],
        index=["A", "B", "C", "D"],
        columns=["A", "B", "C", "D"],
    )
    df.to_csv(matriz, index=True)

    tsp = mod.carregar_instancia(str(pontos), str(matriz))
    assert isinstance(tsp, mod.TSPInstance)
    assert len(tsp.labels) == 4
    assert tsp.dist.shape == (4, 4)
    assert np.allclose(np.diag(tsp.dist), 0.0)


def test_custo_rota_soma_com_retorno(square_instance):
    rota = [0, 1, 2, 3]
    c = mod.custo_rota(rota, square_instance.dist)
    assert pytest.approx(c, rel=1e-9) == 4.0


def test_gerar_populacao_formato():
    n = 5
    pop = mod.gerar_populacao(n, pop_size=20)
    assert len(pop) == 20
    for ind in pop:
        assert sorted(ind) == list(range(n))


def test_torneio_retorna_melhor_entre_participantes(monkeypatch):
    pop = [[0, 1, 2], [2, 1, 0], [1, 0, 2], [1, 2, 0]]
    fitness = [0.0, 10.0, 5.0, 2.0]

    original_sample = random.sample

    def fake_sample(seq, k):
        if isinstance(seq, range):
            return [0, 1, 3]
        return original_sample(seq, k)

    monkeypatch.setattr(random, "sample", fake_sample)
    vencedor = mod.torneio(pop, fitness, k=3)
    assert vencedor == pop[1]


def test_crossover_ox_preserva_segmento_e_permutacao(monkeypatch):
    pai = [0, 1, 2, 3, 4]
    mae = [4, 3, 2, 1, 0]

    original_sample = random.sample

    def fake_sample(seq, k):
        if isinstance(seq, range) and k == 2:
            return [1, 3]
        return original_sample(seq, k)

    monkeypatch.setattr(random, "sample", fake_sample)
    filho = mod.crossover_ox(pai, mae)

    assert filho[1:4] == pai[1:4]
    assert sorted(filho) == sorted(pai)


def test_mutacao_swap_forcada(monkeypatch):
    rota = [0, 1, 2, 3]
    monkeypatch.setattr(random, "random", lambda: 0.0)

    original_sample = random.sample

    def fake_sample(seq, k):
        if isinstance(seq, range) and k == 2:
            return [0, 2]
        return original_sample(seq, k)

    monkeypatch.setattr(random, "sample", fake_sample)

    mod.mutacao_swap(rota, taxa=1.0)
    assert rota == [2, 1, 0, 3]


def test_evoluir_propriedades_basicas(square_instance, monkeypatch):
    monkeypatch.setattr(mod, "POP_SIZE", 30)
    monkeypatch.setattr(mod, "N_GERACOES", 60)
    monkeypatch.setattr(mod, "TAXA_MUTACAO", 0.2)
    monkeypatch.setattr(mod, "TAMANHO_TORNEIO", 3)
    monkeypatch.setattr(mod, "ELITISMO", 2)

    monkeypatch.setattr(builtins, "print", lambda *a, **k: None)

    rota, custo, hist = mod.evoluir(square_instance)

    n = len(square_instance.labels)
    assert len(rota) == n
    assert sorted(rota) == list(range(n))
    assert pytest.approx(custo, rel=1e-12) == mod.custo_rota(rota, square_instance.dist)
    assert len(hist) == mod.N_GERACOES
    assert all(hist[i] <= hist[i - 1] for i in range(1, len(hist)))


def test_plot_melhor_rota_salva_arquivo(square_instance, tmp_path, monkeypatch):
    monkeypatch.setattr(plt, "show", lambda *a, **k: None)
    destino = tmp_path / "rota.png"
    rota = [0, 1, 2, 3]
    custo = mod.custo_rota(rota, square_instance.dist)
    mod.plot_melhor_rota(square_instance, rota, custo, save_as=str(destino))
    assert destino.exists() and destino.stat().st_size > 0


def test_plot_convergencia_salva_arquivo(tmp_path, monkeypatch):
    monkeypatch.setattr(plt, "show", lambda *a, **k: None)
    destino = tmp_path / "conv.png"
    historico = [5.0, 4.0, 3.5, 3.5, 3.2]
    mod.plot_convergencia(historico, save_as=str(destino))
    assert destino.exists() and destino.stat().st_size > 0
