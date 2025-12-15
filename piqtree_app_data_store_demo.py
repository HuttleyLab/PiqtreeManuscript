from cogent3 import get_app, open_data_store
from sc_supertree import construct_supertree

# the input data
dstore = open_data_store("turtle_partitions", suffix="fa")

result_path = "turtle_trees_out"
out = open_data_store(result_path, suffix="json", mode="w")

loader = get_app("load_aligned", moltype="dna")
tree_builder = get_app("piq_build_tree", model="UNREST+FO", rand_seed=1)
lower_length = 471
min_length = get_app("min_length", subtract_degen=False, length=lower_length)
writer = get_app("write_json", data_store=out)
app = loader + min_length + tree_builder + writer

out = app.apply_to(dstore, parallel=True, show_progress=True)

# summarise the results, and run conditions
print(out.describe)
print(out.summary_logs)
print(out.summary_not_completed)

# now we can load the trees from the data store
dstore = open_data_store(result_path, suffix="json")
loader = get_app("load_json")
trees = list(loader.as_completed(dstore, parallel=False, show_progress=False))
print(trees[0])

supertree = construct_supertree(trees, pcg_weighting="branch", random_state=1)

print(supertree)
