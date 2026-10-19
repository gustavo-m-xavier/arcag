import csv
import re
from pathlib import Path
from typing import Iterator, TypedDict


DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"
ABSTRACT_EXCERPT_LENGTH = 500
_TOKEN_PATTERN = re.compile(r"[\w]+(?:[-'][\w]+)*", re.UNICODE)


class Paper(TypedDict):
    paper_id: str
    network_id: str
    title: str
    authors: str
    subjects: str
    journal_ref: str
    abstract: str
    comments: str
    citations_received: int
    citations_made: int


class GraphNode(TypedDict):
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


class GraphEdge(TypedDict):
    source: str
    target: str


def normalize_network_id(value: str) -> str:
    value = value.strip()
    return value.zfill(7) if value.isdigit() else value


def _read_csv(
    path: Path,
    required_columns: set[str],
) -> Iterator[dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(f"Required processed data file was not found: {path}")

    with path.open(encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        missing_columns = required_columns - set(reader.fieldnames or ())
        if missing_columns:
            raise ValueError(
                f"{path} is missing required columns: {', '.join(sorted(missing_columns))}"
            )
        yield from reader


class CitationGraph:
    """In-memory search index and citation graph loaded from processed CSV files."""

    _SEARCH_FIELDS = (
        ("title", 6),
        ("authors", 4),
        ("subjects", 3),
        ("journal_ref", 2),
        ("abstract", 1),
        ("comments", 1),
    )

    def __init__(self, data_dir: Path = DEFAULT_DATA_DIR) -> None:
        paper_rows = _read_csv(
            data_dir / "papers.csv",
            {
                "paper_id",
                "network_id",
                "title",
                "authors",
                "subjects",
                "journal_ref",
                "abstract",
                "comments",
                "citations_received",
                "citations_made",
            },
        )
        self.papers: dict[str, Paper] = {}
        self.search_documents: dict[str, dict[str, str]] = {}
        for row in paper_rows:
            network_id = normalize_network_id(row["network_id"])
            if not network_id:
                raise ValueError("papers.csv contains an empty network_id")
            if network_id in self.papers:
                raise ValueError(f"papers.csv contains duplicate network_id: {network_id}")

            paper: Paper = {
                "paper_id": row["paper_id"].strip(),
                "network_id": network_id,
                "title": row["title"].strip(),
                "authors": row["authors"].strip(),
                "subjects": row["subjects"].strip(),
                "journal_ref": row["journal_ref"].strip(),
                "abstract": row["abstract"].strip(),
                "comments": row["comments"].strip(),
                "citations_received": self._parse_count(
                    row["citations_received"], "citations_received", network_id
                ),
                "citations_made": self._parse_count(
                    row["citations_made"], "citations_made", network_id
                ),
            }
            self.papers[network_id] = paper
            self.search_documents[network_id] = {
                field: row[field].strip().casefold()
                for field, _ in self._SEARCH_FIELDS
            }

        self.outgoing: dict[str, set[str]] = {}
        self.incoming: dict[str, set[str]] = {}
        for row in _read_csv(
            data_dir / "citations.csv",
            {"citing_paper", "cited_paper"},
        ):
            source = normalize_network_id(row["citing_paper"])
            target = normalize_network_id(row["cited_paper"])
            if not source or not target:
                raise ValueError("citations.csv contains an empty citation endpoint")
            self.outgoing.setdefault(source, set()).add(target)
            self.incoming.setdefault(target, set()).add(source)

    @staticmethod
    def _parse_count(value: str, field: str, network_id: str) -> int:
        try:
            count = int(value)
        except ValueError as error:
            raise ValueError(
                f"Invalid {field} value for paper {network_id}: {value!r}"
            ) from error
        if count < 0:
            raise ValueError(f"Negative {field} value for paper {network_id}")
        return count

    def _score(self, network_id: str, tokens: list[str], phrase: str) -> int:
        fields = self.search_documents[network_id]
        score = sum(
            weight * min(fields[field].count(token), 3)
            for token in tokens
            for field, weight in self._SEARCH_FIELDS
        )
        if phrase in fields["title"]:
            score += 10
        elif phrase in fields["abstract"]:
            score += 2
        return score

    def search(self, query: str, limit: int = 10) -> list[tuple[str, int]]:
        return self._ranked_matches(query)[:limit]

    def _ranked_matches(self, query: str) -> list[tuple[str, int]]:
        phrase = query.strip().casefold()
        tokens = _TOKEN_PATTERN.findall(phrase)
        if not tokens:
            return []

        results = []
        for network_id in self.papers:
            score = self._score(network_id, tokens, phrase)
            if score:
                results.append((network_id, score))

        results.sort(
            key=lambda result: (
                -result[1],
                -self.papers[result[0]]["citations_received"],
                result[0],
            )
        )
        return results

    def graph_for_search(
        self,
        query: str,
        limit: int = 10,
        max_nodes: int = 100,
    ) -> dict[str, object]:
        ranked_matches = self._ranked_matches(query)
        matches = ranked_matches[:limit]
        total_matches = len(ranked_matches)
        match_ids = [network_id for network_id, _ in matches[:max_nodes]]
        match_scores = {
            network_id: score
            for network_id, score in matches
            if network_id in match_ids
        }
        truncated = len(match_ids) < len(matches)

        neighbors = {
            neighbor
            for network_id in match_ids
            for neighbor in (
                self.outgoing.get(network_id, set())
                | self.incoming.get(network_id, set())
            )
            if neighbor not in match_ids
        }
        ordered_neighbors = sorted(
            neighbors,
            key=lambda network_id: (
                -self._citation_count(network_id),
                network_id,
            ),
        )
        selected_neighbors = ordered_neighbors[: max(0, max_nodes - len(match_ids))]
        if len(selected_neighbors) < len(ordered_neighbors):
            truncated = True

        selected_ids = set(match_ids) | set(selected_neighbors)
        nodes = [
            self._make_node(
                network_id,
                match_scores.get(network_id, 0),
                network_id in match_scores,
            )
            for network_id in sorted(selected_ids)
        ]
        edge_set = {
            (network_id, neighbor)
            for network_id in match_ids
            for neighbor in self.outgoing.get(network_id, set())
            if neighbor in selected_ids
        } | {
            (neighbor, network_id)
            for network_id in match_ids
            for neighbor in self.incoming.get(network_id, set())
            if neighbor in selected_ids
        }
        edges = [
            {"source": source, "target": target}
            for source, target in sorted(edge_set)
        ]

        return {
            "query": query.strip(),
            "nodes": nodes,
            "edges": edges,
            "total_matches": total_matches,
            "truncated": truncated or total_matches > len(matches),
        }

    def _citation_count(self, network_id: str) -> int:
        paper = self.papers.get(network_id)
        if paper is not None:
            return paper["citations_received"]
        return len(self.incoming.get(network_id, set()))

    def _make_node(
        self,
        network_id: str,
        relevance_score: int,
        is_match: bool,
    ) -> GraphNode:
        paper = self.papers.get(network_id)
        return {
            "id": network_id,
            "paper_id": paper["paper_id"] if paper else None,
            "title": paper["title"] if paper else "Metadata unavailable",
            "authors": paper["authors"] if paper else "",
            "subjects": paper["subjects"] if paper else "",
            "abstract_excerpt": (
                paper["abstract"][:ABSTRACT_EXCERPT_LENGTH] if paper else ""
            ),
            "citations_received": (
                paper["citations_received"]
                if paper
                else len(self.incoming.get(network_id, set()))
            ),
            "citations_made": (
                paper["citations_made"]
                if paper
                else len(self.outgoing.get(network_id, set()))
            ),
            "relevance_score": relevance_score,
            "is_match": is_match,
        }
