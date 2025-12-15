[![DOI](https://zenodo.org/badge/1017124544.svg)](https://doi.org/10.5281/zenodo.15875241)

# piqtree-demo

A demonstation as seen in the `piqtree` [paper](https://www.biorxiv.org/lookup/doi/10.1101/2025.07.13.664626). To reproduce do as follows:

## Setup uv

We use `uv` to ensure reproducability. If you haven't installed uv, but have Python, it can be installed as follows:

`pip install uv`

## Setup data

The data the demo relies on can be extracted by running:

`uv run setup_data.py`

## Running the demo

The demos can be run with the command:

`uv run <script name>.py`

For example

`uv run piqtree_app__demo.py`

