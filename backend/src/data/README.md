# Data

This directory contains the datasets used by the project.

## Dataset

The project uses the **cit-HepTh** dataset from the Stanford Network
Analysis Project (SNAP).

The dataset represents a citation network of scientific papers in
high-energy physics.

### Main files

The dataset provides different files containing information about
the citation relationships and metadata of the papers:

- `cit-HepTh.txt` — citation relationships between papers.
- `cit-HepTh-dates.txt` — submission dates of papers.
- `cit-HepTh-abstracts.tar.gz` — paper metadata, including titles,
  authors and abstracts.

## Directory structure

```text
data/
├── raw/
│   └── Original dataset files
│
└── preprocess/
    └── Python files that treat the data for use the dataset
```
