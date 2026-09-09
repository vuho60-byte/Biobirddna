"""Tinh phan GIAO THAT (base-level) giua vung loi va cac lop chu giai.

Vi sao can: lenh `annotate` phan loai MOI vung BED vao dung mot lop roi cong
NGUYEN chieu dai vung do. Mot vung loi 300 bp chi nam mot phan trong CDS van
duoc cong tron 300 bp cho CDS -> con so "% CDS nam trong loi" bi thoi phong.
Script nay cat theo phan giao that, va gop trung lap truoc khi cong.

Dung:
  python -B pipeline/p02_core_map/overlap_stats.py \
      --core data/a2/bulbul_core.bed \
      --gff data/ncbi/GCA_013400435.1/GCA_013400435.1_ASM1340043v1_genomic.gff.gz \
      --genome-size 1024591993 \
      --out data/a2/overlap_stats.tsv

Chi dung Python stdlib. Khong xoa file nao.
"""

import argparse
import gzip
import sys
from collections import defaultdict

FEATURES = ("CDS", "exon", "gene", "pseudogene")


def merge_intervals(raw):
    """dict scaffold -> [(start, end)] chua sap xep  ->  da sap va gop trung lap."""
    out = {}
    for scaf, rows in raw.items():
        if not rows:
            continue
        rows.sort()
        merged = []
        cur_s, cur_e = rows[0]
        for s, e in rows[1:]:
            if s > cur_e:
                merged.append((cur_s, cur_e))
                cur_s, cur_e = s, e
            else:
                cur_e = max(cur_e, e)
        merged.append((cur_s, cur_e))
        out[scaf] = merged
    return out


def total_bp(iv):
    return sum(e - s for rows in iv.values() for s, e in rows)


def overlap_bp(a, b):
    """Tong base giao nhau giua hai tap khoang DA GOP (thuat toan hai con tro)."""
    tot = 0
    for scaf, A in a.items():
        B = b.get(scaf)
        if not B:
            continue
        i = j = 0
        while i < len(A) and j < len(B):
            s = max(A[i][0], B[j][0])
            e = min(A[i][1], B[j][1])
            if e > s:
                tot += e - s
            if A[i][1] < B[j][1]:
                i += 1
            else:
                j += 1
    return tot


def load_gff(path):
    raw = {f: defaultdict(list) for f in FEATURES}
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if not line or line[0] == "#":
                continue
            f = line.split("\t")
            if len(f) < 9:
                continue
            ftype = f[2]
            if ftype not in raw:
                continue
            try:
                start0 = int(f[3]) - 1
                end = int(f[4])
            except ValueError:
                continue
            if end > start0:
                raw[ftype][f[0]].append((start0, end))
    return {k: merge_intervals(v) for k, v in raw.items()}


def load_bed(path):
    raw = defaultdict(list)
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.rstrip("\r\n")
            if not line:
                continue
            f = line.split("\t")
            if len(f) < 3:
                raise SystemExit("overlap_stats: dong {} khong du 3 cot".format(lineno))
            raw[f[0]].append((int(f[1]), int(f[2])))
    return merge_intervals(raw)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--core", required=True, help="BED vung loi (toa do chao mao)")
    ap.add_argument("--gff", required=True, help="GFF(.gz) chu giai chao mao")
    ap.add_argument("--genome-size", type=int, required=True)
    ap.add_argument("--out", help="TSV ket qua; khong co thi in ra stdout")
    a = ap.parse_args(argv)

    core = load_bed(a.core)
    ann = load_gff(a.gff)
    G = a.genome_size
    core_bp = total_bp(core)

    rows = [
        ("genome_size", G, ""),
        ("core_bp_merged", core_bp, "{:.2f}% bo gene".format(100.0 * core_bp / G)),
    ]
    for feat in FEATURES:
        fbp = total_bp(ann[feat])
        if not fbp:
            continue
        x = overlap_bp(core, ann[feat])
        exp = core_bp * fbp / G
        rows.append((feat + "_bp_merged", fbp, "{:.2f}% bo gene".format(100.0 * fbp / G)))
        rows.append((feat + "_core_overlap_bp", x, ""))
        rows.append((feat + "_pct_of_feature_in_core", round(100.0 * x / fbp, 2), "%"))
        rows.append((feat + "_pct_of_core_in_feature", round(100.0 * x / core_bp, 2), "%"))
        rows.append((feat + "_fold_enrichment", round(x / exp, 2) if exp else 0, "quan sat/ky vong"))

    text = "metric\tvalue\tnote\n" + "\n".join(
        "{}\t{}\t{}".format(k, v, n) for k, v, n in rows
    ) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        sys.stdout.write("da ghi {}\n".format(a.out))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
