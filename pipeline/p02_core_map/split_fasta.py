"""Chia FASTA(.gz) thành các mảnh ~N base, không cắt giữa scaffold. stdlib only, streaming.
Dùng: python -B split_fasta.py --in genome.fna.gz --out-dir chunks --max-bases 180000000
"""
import argparse, gzip, os, sys
ap = argparse.ArgumentParser(); ap.add_argument("--in", dest="inp", required=True); ap.add_argument("--out-dir", required=True); ap.add_argument("--max-bases", type=int, default=180_000_000)
a = ap.parse_args(); os.makedirs(a.out_dir, exist_ok=True)
op = gzip.open if a.inp.endswith(".gz") else open
idx, cum, total, nseq, fh = 0, 0, 0, 0, None
def new():
    global idx, cum, fh
    if fh: fh.close()
    idx += 1; cum = 0; fh = open(os.path.join(a.out_dir, f"chunk_{idx:02d}.fa"), "w", newline="\n")
with op(a.inp, "rt") as f:
    for line in f:
        if line.startswith(">"):
            if fh is None or cum >= a.max_bases: new()
            nseq += 1
        else:
            n = len(line.rstrip("\n")); cum += n; total += n
        fh.write(line)
if fh: fh.close()
print(f"chunks={idx} sequences={nseq} bases={total}")
