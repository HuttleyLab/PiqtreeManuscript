import os
from pathlib import Path
import tarfile

import cogent3
from cogent3.core.alignment import Alignment

COMPRESSED_DATA = Path("turtle_dataset.tar.gz")
TURTLE_PATH = Path("turtle_dataset/turtle.nex")
PARTITION_PATH = Path("turtle_dataset/partition.nex")
OUT_DIR = Path("turtle_partitions/")


def parse_nexus_charsets(nexus_text: str) -> dict[str, tuple[int, int]]:
    lines = nexus_text.splitlines()
    result = {}

    for line in lines:
        line = line.strip()
        if not line.lower().startswith("charset"):
            continue

        _, name, _, start, _, stop = line[:-1].split()

        start = int(start.strip())
        end = int(stop.strip())
        # convert 1-based coordinates to 0-based
        result[name.split(".")[0]] = (start - 1, end)

    return result


def extract_data(tar_gz_file: os.PathLike) -> None:
    with tarfile.open(tar_gz_file, "r:gz") as tar:
        tar.extractall(filter="data")


def get_alignment(path: os.PathLike) -> Alignment:
    aln = cogent3.load_aligned_seqs(path, moltype="dna")
    return aln.rename_seqs(lambda x: x.replace("_", "-").split("-")[0].title())


def get_splits(path: os.PathLike) -> dict[str, Alignment]:
    partitions = parse_nexus_charsets(path.read_text())
    splits = {name: aln[start:stop] for name, (start, stop) in partitions.items()}
    return splits


def write_sequences(
    out_dir: os.PathLike, aln: Alignment, splits: dict[str, Alignment]
) -> None:
    out_dir.mkdir(exist_ok=True)
    out = 0
    for name, aln in splits.items():
        counts = aln.counts_per_seq()
        num_valid = counts.row_sum().to_dict()
        aln = aln.take_seqs_if(
            lambda seq: num_valid[seq.name] > 0,
        )

        out += 1

        # following line has no effect except if it fails, we've made a mistake
        aln.get_translation(incomplete_ok=True)

        outpath = out_dir / f"{name}.fa"
        aln.write(outpath)

    print(f"Wrote {out}/{len(splits)} to {out_dir}")


if __name__ == "__main__":
    extract_data(COMPRESSED_DATA)

    aln = get_alignment(TURTLE_PATH)
    print(f"{aln.num_seqs} sequences")

    splits = get_splits(PARTITION_PATH)
    print(f"{len(splits)} partitions")

    write_sequences(OUT_DIR, aln, splits)
