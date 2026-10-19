from functools import lru_cache
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel

from .graph import CitationGraph, DEFAULT_DATA_DIR


class GraphNodeResponse(BaseModel):
    id: str
    paper_id: str | None
    title: str
    authors: str
    subjects: str
    abstract_excerpt: str
    citations_received: int
    citations_made: int
    relevance_score: int
    is_match: bool


class GraphEdgeResponse(BaseModel):
    source: str
    target: str


class GraphResponse(BaseModel):
    query: str
    nodes: list[GraphNodeResponse]
    edges: list[GraphEdgeResponse]
    total_matches: int
    truncated: bool


app = FastAPI(
    title="ARCAG Citation Graph API",
    description="Search scientific papers and explore their citation relationships.",
    version="1.0.0",
)


@lru_cache(maxsize=1)
def _load_graph(data_dir: Path = DEFAULT_DATA_DIR) -> CitationGraph:
    return CitationGraph(data_dir)


def get_graph() -> CitationGraph:
    try:
        return _load_graph()
    except FileNotFoundError as error:
        raise HTTPException(
            status_code=503,
            detail=(
                "Processed paper and citation CSV files are unavailable. "
                "Run the data-processing notebook first."
            ),
        ) from error


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/graph", response_model=GraphResponse)
def search_graph(
    q: str = Query(min_length=1, max_length=200),
    limit: int = Query(default=10, ge=1, le=20),
    max_nodes: int = Query(default=100, ge=1, le=200),
    graph: CitationGraph = Depends(get_graph),
) -> dict[str, object]:
    if not q.strip():
        raise HTTPException(status_code=422, detail="Search query must not be blank.")
    return graph.graph_for_search(q, limit=limit, max_nodes=max_nodes)
