import tarfile
import pandas as pd

from .parser import parse_abstract


def extract_articles(archive_path) -> pd.DataFrame:
    articles = []

    with tarfile.open(archive_path, "r:gz") as tar:
        for member in tar.getmembers():

            if not member.name.endswith(".abs"):
                continue

            file = tar.extractfile(member)

            if file is None:
                continue

            content = file.read().decode("utf-8", errors="replace")

            article = parse_abstract(content)

            articles.append(article)

    return pd.DataFrame(articles)