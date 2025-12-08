from cogent3 import get_app, open_data_store
from sc_supertree import construct_supertree

loader = get_app("load_aligned", moltype="dna")

tree_builder = get_app("piq_build_tree", model="UNREST+FO")
min_length = get_app("min_length", 450)
app = loader + min_length + tree_builder
dstore = open_data_store("turtle_partitions", suffix="fa")

trees = list(app.as_completed(dstore, parallel=True))
completeds = [t for t in trees if t]
supertree = construct_supertree(completeds, pcg_weighting="branch")

print(supertree)
print(f"Omitted {len(trees) - len(completeds)} partitions due to length < 450")
