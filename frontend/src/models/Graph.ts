export interface GraphNode {
  id: string;
  paper_id: string | null;
  title: string;
  authors: string;
  subjects: string;
  abstract_excerpt: string;
  citations_received: number;
  citations_made: number;
  relevance_score: number;
  is_match: boolean;
}

export interface GraphEdge {
  source: string;
  target: string;
}

export interface GraphResponse {
  query: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  total_matches: number;
  truncated: boolean;
}
