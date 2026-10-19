import csv
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from backend.src.api.main import app
from backend.src.api.routes.graph import get_citation_graph
from backend.src.api.services.citation_graph import CitationGraphService


class CitationGraphTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        data_dir = Path(self.temp_dir.name)
        self._write_csv(
            data_dir / "papers.csv",
            [
                "paper_id",
                "network_id",
                "title",
                "authors",
                "comments",
                "subjects",
                "journal_ref",
                "abstract",
                "citations_received",
                "citations_made",
            ],
            [
                {
                    "paper_id": "hep-th/9201001",
                    "network_id": "9201001",
                    "title": "Quantum fields and strings",
                    "authors": "A. Author",
                    "comments": "",
                    "subjects": "High Energy Physics",
                    "journal_ref": "",
                    "abstract": "A study of quantum field theory.",
                    "citations_received": "4",
                    "citations_made": "1",
                },
                {
                    "paper_id": "hep-th/9304045",
                    "network_id": "9304045",
                    "title": "A related paper",
                    "authors": "B. Author",
                    "comments": "",
                    "subjects": "High Energy Physics",
                    "journal_ref": "",
                    "abstract": "Related work.",
                    "citations_received": "2",
                    "citations_made": "0",
                },
            ],
        )
        self._write_csv(
            data_dir / "citations.csv",
            ["citing_paper", "cited_paper"],
            [
                {"citing_paper": "9201001", "cited_paper": "9304045"},
                {"citing_paper": "1001", "cited_paper": "9201001"},
            ],
        )
        self.graph = CitationGraphService(data_dir)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    @staticmethod
    def _write_csv(
        path: Path,
        fieldnames: list[str],
        rows: list[dict[str, str]],
    ) -> None:
        with path.open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def test_search_returns_relevant_paper_and_citation_neighbors(self) -> None:
        result = self.graph.graph_for_search("quantum field")

        self.assertEqual(result["total_matches"], 1)
        nodes = {node["id"]: node for node in result["nodes"]}
        self.assertEqual(set(nodes), {"9201001", "9304045", "0001001"})
        self.assertTrue(nodes["9201001"]["is_match"])
        self.assertEqual(nodes["9201001"]["citations_received"], 4)
        self.assertEqual(nodes["0001001"]["title"], "Metadata unavailable")
        self.assertEqual(
            result["edges"],
            [
                {"source": "0001001", "target": "9201001"},
                {"source": "9201001", "target": "9304045"},
            ],
        )

    def test_node_limit_marks_graph_as_truncated(self) -> None:
        result = self.graph.graph_for_search("high", limit=2, max_nodes=1)

        self.assertEqual(len(result["nodes"]), 1)
        self.assertEqual(result["nodes"][0]["id"], "9201001")
        self.assertTrue(result["truncated"])

    def test_blank_query_does_not_match_every_paper(self) -> None:
        result = self.graph.graph_for_search("   ")

        self.assertEqual(result["total_matches"], 0)
        self.assertEqual(result["nodes"], [])

    def test_api_returns_graph_response(self) -> None:
        app.dependency_overrides[get_citation_graph] = lambda: self.graph
        try:
            response = TestClient(app).get(
                "/api/v1/graph",
                params={"q": "quantum", "limit": 5, "max_nodes": 10},
            )
        finally:
            app.dependency_overrides.clear()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["query"], "quantum")
        self.assertEqual(response.json()["total_matches"], 1)


if __name__ == "__main__":
    unittest.main()
