from pathlib import Path

import pandas as pd


def load_citations(file_path: Path) -> pd.DataFrame:
    """
    Loads the citation relationships from the cit-HepTh dataset.

    Returns:
        DataFrame containing the citing and cited paper IDs.
    """

    return pd.read_csv(
        file_path,
        sep=r"\s+",
        comment="#",
        names=["citing_paper", "cited_paper"],
        dtype=str,
    )


def load_dates(file_path: Path) -> pd.DataFrame:
    """
    Loads paper submission dates from the cit-HepTh dataset.
    """

    return pd.read_csv(
        file_path,
        sep=r"\s+",
        comment="#",
        names=["paper_id", "date"],
        dtype=str,
    )