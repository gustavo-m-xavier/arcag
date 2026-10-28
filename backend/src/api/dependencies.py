from functools import lru_cache

from fastapi import HTTPException

from .services.citation_graph import CitationGraphService


@lru_cache(maxsize=1)
def _load_citation_graph() -> CitationGraphService:
    return CitationGraphService()


def get_citation_graph() -> CitationGraphService:
    try:
        return _load_citation_graph()
    except FileNotFoundError as error:
        raise HTTPException(
            status_code=503,
            detail=(
                "Processed paper and citation CSV files are unavailable. "
                "Run the data-processing notebook first."
            ),
        ) from error
