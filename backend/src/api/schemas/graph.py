from pydantic import BaseModel


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
