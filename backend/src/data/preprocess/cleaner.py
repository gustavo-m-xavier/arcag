import pandas as pd


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes duplicated records from a DataFrame.
    """
    return df.drop_duplicates().reset_index(drop=True)


def remove_missing_values(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Removes records containing missing values in the specified columns.
    """
    return df.dropna(subset=columns).reset_index(drop=True)