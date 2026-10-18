def parse_abstract(content: str) -> dict:
    data = {
        "paper_id": None,
        "title": None,
        "authors": None,
        "comments": None,
        "subjects": None,
        "journal_ref": None,
        "abstract": None,
    }

    lines = content.splitlines()

    separator_count = 0
    abstract_lines = []

    for line in lines:
        line = line.strip()

        # Os arquivos .abs possuem três delimitadores "\\"
        # O primeiro marca o início do arquivo,
        # o segundo marca o início do abstract,
        # e o terceiro marca o fim do abstract.
        if line == r"\\":
            separator_count += 1

            if separator_count == 3:
                break

            continue

        # Antes do segundo delimitador, estamos lendo os metadados.
        if separator_count < 2:

            if line.startswith("Paper:"):
                data["paper_id"] = line.replace("Paper:", "", 1).strip()

            elif line.startswith("Title:"):
                data["title"] = line.replace("Title:", "", 1).strip()

            elif line.startswith("Authors:"):
                data["authors"] = line.replace("Authors:", "", 1).strip()

            elif line.startswith("Comments:"):
                data["comments"] = line.replace("Comments:", "", 1).strip()

            elif line.startswith("Subj-class:"):
                data["subjects"] = line.replace("Subj-class:", "", 1).strip()

            elif line.startswith("Journal-ref:"):
                data["journal_ref"] = line.replace(
                    "Journal-ref:", "", 1
                ).strip()

        # Depois do segundo delimitador, estamos no abstract.
        elif separator_count == 2:
            abstract_lines.append(line)

    data["abstract"] = " ".join(abstract_lines).strip()

    return data