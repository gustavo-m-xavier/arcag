# ARCAG

## Sobre

Este projeto tem como objetivo desenvolver um sistema para exploração
e análise de relacionamentos entre artigos científicos por meio de
redes de citações.

O projeto utiliza técnicas baseadas em grafos para representar os
relacionamentos entre os artigos e fornecer mecanismos para busca,
análise e visualização de publicações científicas.

## Dataset

O projeto utiliza o dataset **cit-HepTh**, disponibilizado pelo
[Stanford Network Analysis Project (SNAP)](https://snap.stanford.edu/data/cit-HepTh.html).

O dataset representa relacionamentos de citação entre artigos
científicos da área de física de altas energias.

O dataset não está incluído neste repositório.

Para obter instruções sobre como realizar o download e configurar os
dados, consulte:

`data/README.md`

## Estrutura do Projeto

```text
ARCAG/
│
├── backend/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
│
├── notebooks/
│   └── 01-data-exploration-and-treatment.ipynb
│
├── scripts/
│   └── download_dataset.py
│
├── docs/
│   └── data-processing.md
│
├── .gitignore
├── README.md
└── requirements.txt
```
