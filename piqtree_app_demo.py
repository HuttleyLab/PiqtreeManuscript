from cogent3 import get_app, open_data_store
from sc_supertree import construct_supertree

loader = get_app("load_aligned", moltype="dna")

tree_builder = get_app("piq_build_tree", model="UNREST+FO", rand_seed=1)
lower_length = 471
min_length = get_app("min_length", subtract_degen=False, length=lower_length)
app = loader + min_length + tree_builder
dstore = open_data_store("turtle_partitions", suffix="fa")

trees = list(app.as_completed(dstore, parallel=True, show_progress=True))
completeds = [t for t in trees if t]
supertree = construct_supertree(completeds, pcg_weighting="branch", random_state=1)

print(supertree)
print(
    f"Omitted {len(trees) - len(completeds)} partitions due to length < {lower_length}"
)

# the following is to compare against the published result of Chiari et al.
import cogent3 as c3

chiari_turtles = "(((Emys,Chelonoidis),Caretta),Phrynops)"
chiari_crocs = "(Alligator,Caiman)"
chiari_birds = "(Taeniopygia,Gallus)"
chiari_rept = "((Anolis,Python),Podarcis)"
chiari_mammals = "((Monodelphis,Homo),Ornithorhynchus)"
chiari_nt = c3.make_tree(
    f"(Protopterus,(Xenopus,({chiari_mammals},({chiari_rept},({chiari_birds},({chiari_crocs},{chiari_turtles}))))))"
)
if chiari_nt.unrooted().same_topology(supertree.unrooted()):
    message = "DOES"
else:
    message = "DOES NOT"
print(
    f"\nThe unrooted supertree {message} match the unrooted topology of Chiari et al Fig 3b (tree from nucleotide data).",
)
