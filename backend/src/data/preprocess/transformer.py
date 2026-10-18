import pandas as pd


def normalize_paper_ids(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalizes paper identifiers.
    """

    result = df.copy()

    result["citing_paper"] = result["citing_paper"].str.strip()
    result["cited_paper"] = result["cited_paper"].str.strip()

    return result