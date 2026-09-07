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

### Download do Dataset

Após clonar o repositório, execute o script responsável pelo download:

```bash
python scripts/download_dataset.py
```

Os arquivos serão armazenados localmente em:

```text
data/raw/
```

Os arquivos do dataset não são versionados no repositório.

## Estrutura do Projeto

```text
ARCAG/
│
├── backend/
│   ├── .venv/
│   └── ...
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

## Backend

O backend do projeto está localizado no diretório `backend/`.

O projeto utiliza um ambiente virtual Python localizado dentro do
próprio diretório do backend.

### 1. Acessar o diretório do backend

```bash
cd backend
```

### 2. Criar o ambiente virtual

Caso o ambiente virtual ainda não exista:

```bash
python -m venv .venv
```

### 3. Ativar o ambiente virtual

No Windows:

```bash
.venv\Scripts\activate
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

### 4. Instalar as dependências

Com o ambiente virtual ativado:

```bash
pip install -r requirements.txt
```

### 5. Download do dataset

Com o ambiente virtual ativado, execute:

```bash
python scripts/download_dataset.py
```
