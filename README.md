<div align="center">

<img src="https://upload.wikimedia.org/wikipedia/commons/1/1c/Ufs_principal_positiva-nova.png" alt="ufs-logo" width="20%">

<h1>Seminário 1 — PAA <br>Problema do Caixeiro</h1>

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ReinanHS/paa-ufs-seminario-01?machine=standardLinux2gb)

<p align="center">
  :star: Colaboradores :star:
</p>
<center>
<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/ReinanHS">
        <img src="https://github.com/reinanhs.png" height="64px" width="64px;" alt="Reinan Gabriel"/>
      </a>
      <br />
      <a href="https://github.com/ReinanHS">Reinan Gabriel</a>
    </td>
    <td align="center">
      <a href="https://github.com/pauloEzequiel">
        <img src="https://github.com/pauloEzequiel.png" height="64px" width="64px;" alt="Paulo Ezequiel"/>
      </a>
      <br />
      <a href="https://github.com/pauloEzequiel">Paulo Ezequiel</a>
    </td>
    <td align="center">
      <a href="https://github.com/joaorabelo">
        <img src="https://github.com/joaorabelo.png" height="64px" width="64px;" alt="João Rabelo"/>
      </a>
      <br />
      <a href="https://github.com/joaorabelo">João Rabelo</a>
    </td>
  </tr>
</table>
</center>

<p align="center">
  <a href="https://github.com/ReinanHS/paa-ufs-seminario-01/actions/workflows/python-ci.yml">
    <img src="https://github.com/ReinanHS/paa-ufs-seminario-01/actions/workflows/python-ci.yml/badge.svg" alt="Status - CI Testes Python">
  </a>
  <a href="https://github.com/ReinanHS/paa-ufs-seminario-01/actions/workflows/latex-pages.yml">
    <img src="https://github.com/ReinanHS/paa-ufs-seminario-01/actions/workflows/latex-pages.yml/badge.svg" alt="Status - Pages">
  </a>
</p>

</div>

## 📚 Sobre

Repositório que centraliza os materiais do seminário da disciplina **Projeto e Análise de Algoritmos (PAA)** sobre o **Problema do Caixeiro Viajante (PCV/TSP)**. Reúne conteúdos para estudo e apresentação, incluindo referências, notas e implementações de algoritmos clássicos e heurísticos, além de scripts para experimentos comparativos.

---

## Tema do grupo

- **Problema do Caixeiro Viajante (PCV/TSP).**

## O que apresentar

- **Introdução** breve ao problema e **uma aplicação real**.
- **Como o algoritmo escolhido resolve o problema** (ótimo ou aproximado), focando no **problema** e na **ideia do algoritmo**.
- **Exemplo funcional**:

  - Definir **uma instância** do problema,
  - Mostrar o **código-fonte**,
  - **Executar** e apresentar a **solução/resultado**.

- **Não explicar técnicas gerais** (programação dinâmica, gulosa etc.); o professor cobrirá essas bases.

## Estrutura sugerida dos slides

- Introdução
- Definição do problema
- Como o algoritmo resolve
- Código/Experimento
- Resultados
- Referências.

## Duração

- **Tempo máximo: 15 minutos.**

## Entregáveis no repositório (GitHub)

- **Slides** do seminário em **PDF**.
- **Pasta com dados e códigos** usados no experimento.

  - Evitar dependências específicas; preferir **Python, R ou Java**.
  - Código **portável** (qualquer SO) e **sem vínculo** com IDE específica.

- **README** com **link para o vídeo** da apresentação no YouTube.

> **Atenção:** a **data do último commit** **não pode** ser posterior à data de entrega do Seminário 1.

---

## Links

- [Link para o Google Slides](https://docs.google.com/presentation/d/1X6qxrnNSXACRhkNveZjIO241CHSsGpuZnD-f4Vr6eQY/edit?slide=id.p#slide=id.p)

---

## 🛠 Tecnologias principais

- **Python 3.12** (scripts de resolução)
- **GitHub Actions** (CI para Python)
- **GitHub Pages** (publicação do frontend)

---

## ▶️ Como executar localmente

### Pré-requisitos

- Python 3.12+

### Python

```bash
# opcional: criar e ativar venv
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows (PowerShell)

# executar um script específico
pip install pandas matplotlib pytest
python src/main.py
```

### Testes unitários

```bash
pip pytest
pytest -q
```

---

## 📊 Estatísticas do repositório

### Contribuidores

[![Contribuidores](https://contrib.rocks/image?repo=ReinanHS/paa-ufs-seminario-01)](https://github.com/ReinanHS/paa-ufs-seminario-01/graphs/contributors)

### Atividade de commits

![Gráfico de commits](https://img.shields.io/github/commit-activity/m/ReinanHS/paa-ufs-seminario-01)

### Observadores de estrelas ao longo do tempo

![Histórico de estrelas](https://starchart.cc/ReinanHS/paa-ufs-seminario-01.svg)

---

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE.md).

---

## 🤝 Contribuindo

Quer contribuir? Leia nosso guia de contribuição: [CONTRIBUTING.md](CONTRIBUTING.md).
