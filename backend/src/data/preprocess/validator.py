import pandas as pd


def validate_citations(df: pd.DataFrame) -> None:
    """
    Validates the citation dataset.
    """

    required_columns = {
        "citing_paper",
        "cited_paper",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if df.empty:
        raise ValueError("Citation dataset is empty.")

    if df.isnull().any().any():
        raise ValueError("Citation dataset contains null values.")