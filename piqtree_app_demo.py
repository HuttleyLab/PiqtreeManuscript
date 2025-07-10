from cogent3 import get_app, open_data_store
from sc_supertree import construct_supertree

loader = get_app("load_aligned", moltype="dna")

tree_builder = get_app("piq_build_tree", model="UNREST")

app = loader + tree_builder

dstore = open_data_store("turtle_partitions", suffix="fa")

trees = list(app.as_completed(dstore, parallel=True))

supertree = construct_supertree(trees, pcg_weighting="branch")

print(supertree)
