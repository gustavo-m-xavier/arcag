
from pathlib import Path
from urllib.request import urlretrieve


BASE_URL = "https://snap.stanford.edu/data/"

DATASET_FILES = {
    "cit-HepTh.txt.gz": BASE_URL + "cit-HepTh.txt.gz",
    "cit-HepTh-dates.txt.gz": BASE_URL + "cit-HepTh-dates.txt.gz",
    "cit-HepTh-abstracts.tar.gz": BASE_URL + "cit-HepTh-abstracts.tar.gz",
}


def download_dataset() -> None:
    output_dir = Path(__file__).resolve().parent.parent / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    for filename, url in DATASET_FILES.items():
        output_path = output_dir / filename

        if output_path.exists():
            print(f"[SKIP] {filename} already exists.")
            continue

        print(f"[DOWNLOAD] {filename}")
        urlretrieve(url, output_path)
        print(f"[DONE] {output_path}")


if __name__ == "__main__":
    download_dataset()