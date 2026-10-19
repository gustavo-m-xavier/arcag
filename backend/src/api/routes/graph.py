from fastapi import APIRouter, Depends, HTTPException, Query

from ..dependencies import get_citation_graph
from ..schemas.graph import GraphResponse
from ..services.citation_graph import CitationGraphService


router = APIRouter(prefix="/api/v1/graph", tags=["graph"])


@router.get("", response_model=GraphResponse)
def search_graph(
    q: str = Query(min_length=1, max_length=200),
    limit: int = Query(default=10, ge=1, le=20),
    max_nodes: int = Query(default=100, ge=1, le=200),
    graph: CitationGraphService = Depends(get_citation_graph),
) -> dict[str, object]:
    if not q.strip():
        raise HTTPException(status_code=422, detail="Search query must not be blank.")
    return graph.graph_for_search(q, limit=limit, max_nodes=max_nodes)
