# piqtree-demo

A demonstation as seen in the `piqtree` paper. To reproduce do as follows:

## Setup uv

We use `uv` to ensure reproducability. If you haven't installed uv, but have Python, it can be installed as follows:

`pip install uv`

## Setup data

The data the demo relies on can be extracted by running:

`uv run setup_data.py`

## Running the demo

First be sure to set 

`export COGENT3_NEW_TYPE=1`

The demo can be run with the command:

`uv run piqtree_demo.py`