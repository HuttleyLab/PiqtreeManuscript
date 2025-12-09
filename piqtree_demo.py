from pathlib import Path

from cogent3 import load_aligned_seqs
from piqtree import build_tree
from sc_supertree import construct_supertree
from tqdm import tqdm

aln_dir = Path("turtle_partitions/")

min_length = 471
trees = []
omitted = 0
for aln_file in tqdm(list(aln_dir.glob("*.fa"))):
    aln = load_aligned_seqs(aln_file, moltype="dna")
    if len(aln) < min_length:
        omitted += 1
        continue
    trees.append(build_tree(aln, "UNREST+FO"))

supertree = construct_supertree(trees, pcg_weighting="branch")

print(supertree)
print(f"Omitted {omitted} partitions due to length < {min_length}")
