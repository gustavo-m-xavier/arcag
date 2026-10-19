import csv
from collections.abc import Iterator
from pathlib import Path


PAPERS_COLUMNS = {
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
}
CITATIONS_COLUMNS = {"citing_paper", "cited_paper"}


def normalize_network_id(value: str) -> str:
    value = value.strip()
    return value.zfill(7) if value.isdigit() else value


def _read_csv_rows(
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


def parse_papers(data_dir: Path) -> Iterator[dict[str, str]]:
    """Read processed paper rows and verify the expected CSV columns."""
    yield from _read_csv_rows(data_dir / "papers.csv", PAPERS_COLUMNS)


def parse_citations(data_dir: Path) -> Iterator[dict[str, str]]:
    """Read processed citation rows and verify the expected CSV columns."""
    yield from _read_csv_rows(data_dir / "citations.csv", CITATIONS_COLUMNS)
