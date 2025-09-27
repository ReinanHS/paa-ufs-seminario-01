<div align="center">

<img src="https://upload.wikimedia.org/wikipedia/commons/1/1c/Ufs_principal_positiva-nova.png" alt="ufs-logo" width="20%">

<h1>Seminário 1 — PAA <br>Problema do Caixeiro</h1>

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ReinanHS/paa-ufs-seminario-01?machine=standardLinux2gb)

<p align="center">
  <!-- CI -->
  <a href="https://github.com/ReinanHS/paa-ufs-seminario-01/actions/workflows/python-ci.yml">
    <img src="https://github.com/ReinanHS/paa-ufs-seminario-01/actions/workflows/python-ci.yml/badge.svg" alt="Status - CI Testes Python">
  </a>
  <!-- GitHub Pages (online/offline) -->
  <a href="https://reinanhs.github.io/paa-ufs-seminario-01/">
    <img src="https://img.shields.io/website?url=https%3A%2F%2Freinanhs.github.io%2Fpaa-ufs-seminario-01%2F&label=GitHub%20Pages" alt="GitHub Pages">
  </a>
  <!-- Python version -->
  <img src="https://img.shields.io/badge/python-3.12%2B-blue.svg" alt="Python 3.12+">
  <!-- License -->
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="Licença MIT">
  </a>
  <!-- Last commit -->
  <a href="https://github.com/ReinanHS/paa-ufs-seminario-01/commits/main">
    <img src="https://img.shields.io/github/last-commit/ReinanHS/paa-ufs-seminario-01.svg" alt="Último commit">
  </a>
  <!-- Stars -->
  <a href="https://github.com/ReinanHS/paa-ufs-seminario-01/stargazers">
    <img src="https://img.shields.io/github/stars/ReinanHS/paa-ufs-seminario-01.svg?style=social" alt="Stars">
  </a>
</p>

</div>

## 📚 Sobre

Repositório do seminário de **Projeto e Análise de Algoritmos (PAA)** sobre o **Problema do Caixeiro Viajante (PCV/TSP)
**.
Veja abaixo as principais implementações que estão contidas neste projeto:

- Implementação **em Python** (código principal a ser executado pelo professor);
- Uma **visualização web** (GitHub Pages) para **definir pontos**, **gerar CSVs** e **simular** a evolução do AG no
  navegador (caráter ilustrativo/plus);
- Scripts, dados e testes automatizados.

---

## Colaboradores

Apresentamos os principais membros da equipe:

<div align="center">
<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/ReinanHS">
        <img src="https://github.com/reinanhs.png" height="64" width="64" alt="Reinan Gabriel"/>
      </a><br/>
      <a href="https://github.com/ReinanHS">Reinan Gabriel</a>
    </td>
    <td align="center">
      <a href="https://github.com/pauloEzequiel">
        <img src="https://github.com/pauloEzequiel.png" height="64" width="64" alt="Paulo Ezequiel"/>
      </a><br/>
      <a href="https://github.com/pauloEzequiel">Paulo Ezequiel</a>
    </td>
    <td align="center">
      <a href="https://github.com/joaorabelo">
        <img src="https://github.com/joaorabelo.png" height="64" width="64" alt="João Rabelo"/>
      </a><br/>
      <a href="https://github.com/joaorabelo">João Rabelo</a>
    </td>
  </tr>
</table>
</div>

---

## Vídeo da apresentação

O link abaixo direciona para o vídeo hospedado no YouTube, que registra a apresentação do seminário sobre o problema do
caixeiro viajante. Nele, são abordados os principais aspectos do tema, juntamente com um exemplo prático da execução do
algoritmo desenvolvido neste repositório.

[![Youtube Video](https://gitlab.com/reinanhs/repo-slide-presentation/-/wikis/uploads/b199b81b500596ac3a93a542b6a17775/image.png)](https://youtu.be/dQw4w9WgXcQ)

- 📹 **Assista:** [https://youtu.be/dQw4w9WgXcQ](https://youtu.be/dQw4w9WgXcQ)

> Exigência do professor: O README deve conter o link do vídeo no YouTube.

---

## Diretrizes do seminário

### Tema do grupo

- **Problema do Caixeiro Viajante (PCV/TSP).**

### O que apresentar

- **Introdução** breve ao problema e **uma aplicação real**.

- **Como o algoritmo escolhido resolve o problema** (ótimo ou aproximado), focando no **problema** e na **ideia do
  algoritmo**.

- **Exemplo funcional**:

    - Definir **uma instância** do problema,
    - Mostrar o **código-fonte**,
    - **Executar** e apresentar a **solução/resultado**.

- **Não explicar técnicas gerais** (programação dinâmica, gulosa etc.); o professor cobrirá essas bases.

### Estrutura sugerida dos slides

- Introdução
- Definição do problema
- Como o algoritmo resolve
- Código/Experimento
- Resultados
- Referências.

### Duração

- **Tempo máximo: 15 minutos.**

### Entregáveis no repositório (GitHub)

- **Slides** do seminário em **PDF**.

- **Pasta com dados e códigos** usados no experimento.

    - Evitar dependências específicas; preferir **Python, R ou Java**.
    - Código **portável** (qualquer SO) e **sem vínculo** com IDE específica.

- **README** com **link para o vídeo** da apresentação no YouTube.

> **Atenção:** a **data do último commit** **não pode** ser posterior à data de entrega do Seminário 1.

---

## 🧠 Por que Algoritmo Genético (AG) para o TSP?

- **Escalabilidade prática**: TSP exato cresce de forma explosiva (busca exaustiva é inviável; Held–Karp é (O(n^2
  2^n))). O AG encontra **boas soluções** em tempo razoável.
- **Qualidade x tempo**: Permite **trade-off controlável** via número de gerações e tamanho da população.
- **Exploração + Preservação**: Combina recombinação (ex.: **OX – Order Crossover**) com **mutação** para evitar mínimos
  locais.
- **Flexibilidade**: Fácil incorporar **restrições** (janelas de tempo, arestas proibidas) e **funções de custo**
  específicas.
- **Reprodutibilidade**: Com semente fixa, você obtém resultados comparáveis entre execuções.

**Resumo da implementação deste projeto:**

- **Seleção**: Torneio (`k=5` por padrão);
- **Crossover**: **OX (Order Crossover)**;
- **Mutação**: **swap** com taxa configurável;
- **Elitismo**: mantém os melhores indivíduos a cada geração;
- **Parâmetros padrão**: `POP_SIZE=200`, `N_GERACOES=200`, `TAXA_MUTACAO=0.15`, `ELITISMO=2`, `SEMENTE=42`.

---

## Estrutura do repositório

```
├── src/                # Código Python principal
│   └── main.py
├── data/               # Dados e frontend ilustrativo
│   ├── index.html      # Visualização web (MapLibre + Chart.js)
│   ├── matriz_distancias.csv
│   └── pontos_caixeiro_viajante.csv
├── tests/              # Testes automatizados (pytest)
├── .github/workflows/  # CI (tests, artefatos, Pages)
├── README.md
├── requirements.txt
└── LICENSE
```

---

## Execução

Veja abaixo as instruções de como executar o código.

### Pré-requisitos

- **Python 3.12+**

### Instalação e execução

```bash
# opcional: criar e ativar venv
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\activate

# dependências mínimas
pip install --upgrade pip
pip install -r requirements.txt  # ou: pip install numpy pandas matplotlib pytest

# executar
python src/main.py
```

**Saída esperada (exemplo compacto no console):**

```
Iniciando a execução do Algoritmo Genético...
Geração    0 | melhor custo: 6xx.xxxx
...
--- Resultados ---
Melhor custo (distância) encontrado: 547.8900
Melhor rota (sequência de cidades): [2, 0, 1, 6, 9, 8, 3, 4, 7, 11, 5, 10]

Gerando visualizações...
```

O script também abre:

- **Melhor Rota Encontrada** (scatter + polilinha fechando o ciclo);

<img width="450" height="350" alt="Figure_1" src="https://github.com/user-attachments/assets/73c89e75-dd25-47c8-9e47-d7fef7111b1c" />

- **Convergência do AG** (melhor custo por geração).

<img width="450" height="200" alt="Figure_2" src="https://github.com/user-attachments/assets/41939057-9f7e-4857-beca-4f32821b7d30" />

> **Reprodutibilidade**: o projeto utiliza `SEMENTE=42` para `random` e `numpy`.

---

## Visualização pelo navegador

- **Página**: [https://reinanhs.github.io/paa-ufs-seminario-01/](https://reinanhs.github.io/paa-ufs-seminario-01/)
- **Arquivo-fonte**: `data/index.html`

**O que dá para fazer no navegador:**

1. **Definir cidades** (adicionar, mover, remover) sobre o mapa;
2. **Gerar e visualizar** rotas durante a evolução do AG (play/step/pause/reset);
3. **Acompanhar** convergência (melhor x média por geração) e tabela de “top indivíduos”;
4. **Exportar/baixar** os dados gerados (pontos e matriz) para uso no Python.

   > Depois de baixar, **salve** como:
   >
   > - `data/pontos_caixeiro_viajante.csv`
   > - `data/matriz_distancias.csv`
       > e **execute** `python src/main.py` para reproduzir no ambiente oficial (Python).

> **Nota**: a visualização web é um **plus** pedagógico para demonstrar o processo evolutivo. A **entrega oficial** a
> ser avaliada é o **código em Python**.

---

## Testes

A seguir, apresentamos o procedimento para execução dos testes unitários desenvolvidos para este repositório:

```bash
pytest -q
```

Os testes cobrem:

- Leitura/limpeza de CSV (`read_csv_clean`);
- Validação de coordenadas e matriz de distâncias;
- Funções do AG (seleção por torneio, OX, mutação, custo);
- Geração das figuras (salvando arquivos com `MPLBACKEND=Agg`).

---

## CI/CD

- **Workflow**: `.github/workflows/python-ci.yml`

    - **jobs `tests`**: instala dependências e executa `pytest`.
    - **job `run-and-artifacts`**: roda o AG com os dados de `data/`, salva:

        - `artifacts/melhor_rota.png`
        - `artifacts/convergencia.png`
        - `artifacts/index.html` (com os resultados)
        - publica como **artifact** do GitHub Actions.

    - **jobs `build-pages` → `deploy-pages`**: publicam **GitHub Pages** a partir da pasta `data/`.

* [Clique nesse link para visualizar um exemplo](https://github.com/ReinanHS/paa-ufs-seminario-01/actions/runs/18051367409)

---

## Dados de entrada (CSV)

- `data/pontos_caixeiro_viajante.csv`
  Colunas esperadas: `Indice, Nome, Latitude, Longitude`

- `data/matriz_distancias.csv`
  Matriz **quadrada** (N×N) de distâncias com **diagonal zero**.

---

## Parâmetros e ajustes rápidos

- `POP_SIZE=200` — Tamanho da população
- `N_GERACOES=200` — Número de gerações
- `TAXA_MUTACAO=0.15` — Probabilidade de mutação (swap)
- `TAMANHO_TORNEIO=5` — Intensidade de seleção
- `ELITISMO=2` — Indivíduos preservados
- `SEMENTE=42` — Reprodutibilidade

Ajuste esses valores em `src/main.py` conforme o tempo disponível e a qualidade desejada da solução.

---

## Links úteis

- [Slides (Google Slides)](https://docs.google.com/presentation/d/1X6qxrnNSXACRhkNveZjIO241CHSsGpuZnD-f4Vr6eQY/edit?slide=id.p#slide=id.p)
- [Slide em PDF](./data/slide.pdf)
- [GitHub Pages (Frontend)](https://reinanhs.github.io/paa-ufs-seminario-01/)
- [CI (Actions)](https://github.com/ReinanHS/paa-ufs-seminario-01/actions)
- [Vídeo no Youtube](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

---

## Licença

Este projeto está sob a licença [MIT](LICENSE).

---

## Contribuindo

Quer contribuir? Leia nosso guia de contribuição: [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Estatísticas do repositório

[![Contribuidores](https://contrib.rocks/image?repo=ReinanHS/paa-ufs-seminario-01)](https://github.com/ReinanHS/paa-ufs-seminario-01/graphs/contributors)
![Gráfico de commits](https://img.shields.io/github/commit-activity/m/ReinanHS/paa-ufs-seminario-01)
![Histórico de estrelas](https://starchart.cc/ReinanHS/paa-ufs-seminario-01.svg)
