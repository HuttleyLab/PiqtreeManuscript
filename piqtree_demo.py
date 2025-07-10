from pathlib import Path

from cogent3 import load_aligned_seqs
from piqtree import build_tree
from sc_supertree import construct_supertree

aln_dir = Path("turtle_partitions/")

trees = []
for aln_file in aln_dir.glob("*.fa"):
    aln = load_aligned_seqs(aln_file, moltype="dna")
    trees.append(build_tree(aln, "UNREST"))

supertree = construct_supertree(trees, pcg_weighting="branch")

print(supertree)
