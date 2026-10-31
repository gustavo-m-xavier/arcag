# ARCAG

O ARCAG é um sistema para explorar e analisar relações entre artigos
científicos usando redes de citações. O projeto combina uma API de busca e
construção de grafos com uma interface web interativa para visualizar as
conexões entre artigos.

## Requisitos

- Python 3.10 ou superior
- Node.js e npm
- Acesso à internet para baixar o conjunto de dados do SNAP

## Preparar os dados

O projeto usa o conjunto de dados **cit-HepTh**, disponibilizado pelo
[Stanford Network Analysis Project (SNAP)](https://snap.stanford.edu/data/).
Ele contém relações de citação e metadados de artigos de física de altas
energias. Os arquivos originais e processados não são versionados no Git.

Crie e ative o ambiente virtual Python. Os comandos abaixo partem da raiz do
repositório.

Linux/macOS:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Com o ambiente virtual ativado, baixe os arquivos brutos:

```bash
python src/scripts/download_dataset.py
```

O script salva os arquivos em `backend/src/data/raw/`. Em seguida, abra o
notebook `backend/src/notebooks/01-data-exploration-and-treatment.ipynb` no
Jupyter e execute todas as células, da primeira à última. Para que os caminhos
relativos do notebook sejam resolvidos corretamente, inicie o Jupyter a partir
do diretório `backend/src/notebooks/`, mantendo o ambiente virtual ativado:

```bash
cd src/notebooks
jupyter notebook
```

O notebook gera `papers.csv` e `citations.csv` em
`backend/src/data/processed/`. A API precisa desses arquivos para responder às
buscas. Mais detalhes sobre os dados estão em
[backend/src/data/README.md](backend/src/data/README.md) e
[docs/data-processing.md](docs/data-processing.md).

## Executar o backend

Com os dados processados disponíveis, inicie a API em um terminal. A partir da
raiz do repositório, entre em `backend/`, ative o ambiente virtual caso ainda
não esteja ativo e execute:

```bash
cd backend
source .venv/bin/activate
uvicorn src.api.main:app --reload
```

No PowerShell, use `.venv\Scripts\Activate.ps1` para ativar o ambiente virtual.
Por padrão, a API fica disponível em `http://127.0.0.1:8000`. A documentação
interativa do FastAPI pode ser acessada em
[`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs).

O endpoint de busca é `GET /api/v1/graph`. Por exemplo:

```text
http://127.0.0.1:8000/api/v1/graph?q=quantum%20field
```

Consulte a documentação da [API de grafos](docs/citation-graph-api.md) para
conhecer os parâmetros, limites e formato da resposta.

## Executar o frontend

Mantenha o backend em execução e abra outro terminal na raiz do repositório:

```bash
cd frontend
npm install
npm run dev
```

Abra o endereço exibido pelo Vite (normalmente
[`http://localhost:5173`](http://localhost:5173)). Durante o desenvolvimento,
o Vite encaminha as requisições `/api` para `http://127.0.0.1:8000`.

Digite um tema, autor ou título e envie a busca para montar o grafo. Selecione
um nó para ver os metadados, o resumo e as contagens de citações do artigo. Os
artigos são mantidos no idioma original da fonte de dados.

### Organização do frontend (MVVM)

O frontend separa responsabilidades nas seguintes camadas:

- `frontend/src/models/`: tipos dos dados do grafo.
- `frontend/src/services/`: comunicação com a API.
- `frontend/src/viewmodels/`: estado da busca e interações com o grafo.
- `frontend/src/views/`: telas e componentes da interface.

## Testes

Com as dependências do backend instaladas e o ambiente virtual ativado, volte
à raiz do repositório e execute:

```bash
python -m unittest backend.tests.test_graph_api
```

Para validar a compilação do frontend:

```bash
cd frontend
npm run build
```

## Estrutura do repositório

```text
backend/
├── src/
│   ├── api/          # API FastAPI, rotas, esquemas e serviço do grafo
│   ├── data/         # Dados brutos, processados e módulos de processamento
│   ├── notebooks/    # Exploração e preparação dos dados
│   └── scripts/      # Scripts auxiliares, incluindo o download do dataset
├── tests/            # Testes do backend
└── requirements.txt
docs/                 # Documentação da API e do processamento
frontend/
└── src/
    ├── models/
    ├── services/
    ├── viewmodels/
    └── views/
```
