# Citation Graph API

The backend exposes a search endpoint that returns matching papers together
with the papers they cite and the papers that cite them. It reads the processed
CSV files produced by the data-processing notebook; the original dataset does
not need to be loaded for each request.

## Start the API

From the `backend/` directory, install the project dependencies and run:

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

The processed files must exist at
`backend/src/data/processed/papers.csv` and
`backend/src/data/processed/citations.csv`. These files are generated locally
by the notebook and are ignored by Git. If they are not present, generate them
before using the graph endpoint. The API returns HTTP 503 when the files are
missing.

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Endpoints

### `GET /health`

Returns `{"status": "ok"}` when the API process is running.

### `GET /api/v1/graph`

Searches paper titles, authors, subjects, journal references, comments, and
abstracts, then returns a citation graph around the most relevant matches.

| Parameter | Default | Limits | Description |
| --- | ---: | ---: | --- |
| `q` | required | 1–200 characters | Search text; whitespace-only input is rejected. |
| `limit` | 10 | 1–20 | Maximum number of matching papers used as graph seeds. |
| `max_nodes` | 100 | 1–200 | Maximum total number of graph nodes, including matches. |

Example:

```text
GET /api/v1/graph?q=quantum%20field&limit=10&max_nodes=100
```

The response contains:

- `nodes`: paper IDs, available metadata, a 500-character abstract excerpt,
  `citations_received`, `citations_made`, search `relevance_score`, and
  `is_match`.
- `edges`: directed citation links where `source` is the citing paper and
  `target` is the cited paper.
- `total_matches`: number of papers matching the query before applying
  `limit`.
- `truncated`: whether matches or one-hop citation neighbors were omitted by
  the requested limits.

Matches are ranked by weighted text relevance (titles and authors receive more
weight than abstracts), then by citations received. Citation counts provide an
additional indication of a paper's influence; they are counts, not a
quality assessment. Results include direct incoming and outgoing citations
around the matched papers, not an unbounded traversal of the full network.

The citation IDs are normalized using the same seven-character zero-padding
convention used in the notebook. Citation endpoints without a row in
`papers.csv` are still included as graph nodes, with `paper_id` set to `null`
and the title `Metadata unavailable`. This preserves citation relationships
while making the missing metadata explicit.

## Implementation

The API is divided by responsibility under `backend/src/api/`:

- `main.py` creates the application and registers routers.
- `routes/` contains HTTP endpoint definitions and request handling.
- `schemas/` contains response models.
- `parsers/` reads and validates the processed CSV formats.
- `services/` implements search ranking and citation graph construction.
- `dependencies.py` provides the cached graph service to routes.

The service loads and indexes CSV data once per process. Tests for search
ranking, citation direction, unknown metadata nodes, graph limits, and the
HTTP response are in `backend/tests/test_graph_api.py`.
