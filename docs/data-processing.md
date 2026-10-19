# Data Processing

## Objective

The objective of the data processing stage is to prepare the
cit-HepTh dataset for use by the backend and graph analysis
components of the project.

## Dataset

The project uses the cit-HepTh citation network provided by the
Stanford Network Analysis Project (SNAP).

The dataset contains scientific papers and their citation
relationships.

## Processing pipeline

The data processing pipeline will consist of the following stages:

1. Dataset acquisition
2. Data exploration
3. Data cleaning
4. Data normalization
5. Relationship extraction
6. Data validation
7. Generation of processed data in `backend/src/data/processed/`

## Documentation

The exploratory analysis and implementation of the data treatment
are documented in:

`backend/src/notebooks/01-data-exploration-and-treatment.ipynb`

The generated `papers.csv` and `citations.csv` files are consumed by the
[Citation Graph API](./citation-graph-api.md).
