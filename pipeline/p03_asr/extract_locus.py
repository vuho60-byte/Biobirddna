#!/usr/bin/env python3
"""Extract CDS-exon alignment across the 363-avian bigMaf for one or more galGal4 genes.

Sản phẩm C phiên bản 0 (T-C locus-c). Python 3.11 stdlib only.

Với mỗi exon thuộc vùng CDS (cdsStart..cdsEnd) của một gene trên galGal4, gọi
`bigBedToBed` (Docker, image co san quay.io/biocontainers/ucsc-bigbedtobed)
doc chicken.bigMaf.bb TU XA theo dung vung do (khong tai file). Ket qua la cac
dong BED (chrom start end mafBlock) voi mafBlock la cac dong MAF noi bang ';'.
Script parse cac dong nay, xay ma tran loai x vi tri neo tren toa do ga (chi
giu cot ung voi vi tri KHONG gap cua Gallus_gallus trong tung block), noi cac
exon theo chieu 5'->3' cua gene (dao bo sung neu strand '-'), va ghi:
  data/c_loci/<GENE>/<GENE>.cds363.fa      - 363 hang, ten loai
  data/c_loci/<GENE>/<GENE>.blocks.tsv     - so block, base ga, % loai co du lieu

Gioi han da biet (ghi trong research/synthesis/04-locus-c-v0.md):
  - Chi cac vi tri con lai sau khi bo gap o Gallus_gallus moi duoc giu (alignment
    neo tren ga theo dung kien truc bigMaf cua hub nay).
  - Toa do cua 362 loai con lai trong file la GIA (vd "Alca_torda.1 1 1 + 6000") -
    chi trinh tu la that, khong dung de suy vi tri tren bo gene loai khac.
  - chr9, chr11, chr12, chr14, chr16, chr18, chr24, chr27, chr32 VANG MAT khoi
    chicken.bigMaf.bb (xac nhan bang `bigBedInfo -chroms`) -> gene nam tren cac
    NST nay khong the rut duoc, phai thay gene (vi du MC1R -> DCT).

Usage:
  python extract_locus.py --loci data/c_loci/loci_galGal4.tsv \
      --species data/c_loci/species_363.txt --outdir data/c_loci --gene MC1R [--gene TYR ...]
  (khong --gene nao -> chay het cac dong trong file loci)
"""
from __future__ import annotations

import argparse
import csv
import os
import subprocess
import sys
import time
from pathlib import Path

BIGMAF_URL = "https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020-hub/Gallus_gallus/chicken.bigMaf.bb"
IMAGE = "quay.io/biocontainers/ucsc-bigbedtobed:482--h0b57e2e_0"
DELIM = "###EXON_BOUNDARY###"
COMPLEMENT = str.maketrans("ACGTacgtNn-", "TGCAtgcaNn-")


def revcomp(seq: str) -> str:
    return seq.translate(COMPLEMENT)[::-1]


def load_species(path: str) -> list[str]:
    with open(path, encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]


def load_loci(path: str) -> dict[str, dict]:
    out = {}
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            out[row["gene"]] = row
    return out


def cds_exon_windows(row: dict) -> list[tuple[int, int]]:
    """Trả về danh sách (start,end) 0-based half-open, đã cắt vào [cdsStart,cdsEnd)."""
    cds_start = int(row["cdsStart"])
    cds_end = int(row["cdsEnd"])
    exon_starts = [int(x) for x in row["exonStarts"].strip(",").split(",") if x != ""]
    exon_ends = [int(x) for x in row["exonEnds"].strip(",").split(",") if x != ""]
    windows = []
    for s, e in zip(exon_starts, exon_ends):
        cs = max(s, cds_start)
        ce = min(e, cds_end)
        if ce > cs:
            windows.append((cs, ce))
    return windows


def build_container_script(chrom: str, windows: list[tuple[int, int]]) -> str:
    parts = []
    for i, (s, e) in enumerate(windows):
        if i > 0:
            parts.append(f"echo '{DELIM}'")
        parts.append(
            f"bigBedToBed {BIGMAF_URL} -chrom={chrom} -start={s} -end={e} stdout"
        )
    return " ; ".join(parts)


def run_docker_batch(chrom: str, windows: list[tuple[int, int]], timeout: int = 900) -> str:
    script = build_container_script(chrom, windows)
    env = dict(os.environ)
    env["MSYS_NO_PATHCONV"] = "1"
    cmd = ["docker", "run", "--rm", "--entrypoint", "sh", IMAGE, "-c", script]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env)
    if res.returncode != 0:
        print(f"  [WARN] docker exit {res.returncode}: {res.stderr[-500:]}", file=sys.stderr)
    return res.stdout


def parse_maf_block_line(line: str):
    """line: chrom \t start \t end \t mafBlock(';'-joined 's ...' tokens, first token 'a')"""
    cols = line.rstrip("\n").split("\t")
    if len(cols) < 4:
        return None
    bstart, bend = int(cols[1]), int(cols[2])
    tokens = cols[3].split(";")
    s_lines = {}
    for tok in tokens:
        tok = tok.strip()
        if not tok.startswith("s "):
            continue
        fields = tok.split()
        if len(fields) < 7:
            continue
        src = fields[1]
        text = fields[6]
        species = src.split(".")[0]
        if species not in s_lines:  # giữ bản đầu tiên nếu loài lặp trong 1 block
            s_lines[species] = text
    return bstart, bend, s_lines


def window_matrix(raw_text: str, win_start: int, win_end: int, species_set: set[str]):
    """Trả {genomic_pos: {species: base}} cho các vị trí trong [win_start, win_end)."""
    pos_map: dict[int, dict[str, str]] = {}
    n_blocks = 0
    for line in raw_text.splitlines():
        line = line.strip("\n")
        if not line or line.startswith(DELIM):
            continue
        parsed = parse_maf_block_line(line)
        if not parsed:
            continue
        bstart, bend, s_lines = parsed
        gallus_text = s_lines.get("Gallus_gallus")
        if gallus_text is None:
            continue
        n_blocks += 1
        genomic_pos = bstart
        for i, gc in enumerate(gallus_text):
            if gc == "-":
                continue
            if win_start <= genomic_pos < win_end:
                col = pos_map.setdefault(genomic_pos, {})
                col["Gallus_gallus"] = gc
                for sp, text in s_lines.items():
                    if sp == "Gallus_gallus":
                        continue
                    if i < len(text):
                        col[sp] = text[i]
            genomic_pos += 1
    return pos_map, n_blocks


def extract_gene(gene: str, row: dict, species_order: list[str], outdir: Path,
                  timeout: int = 900) -> dict:
    chrom = row["chrom"]
    strand = row["strand"]
    windows = cds_exon_windows(row)
    if not windows:
        return {"gene": gene, "status": "NO_CDS_WINDOWS"}
    t0 = time.time()
    raw = run_docker_batch(chrom, windows, timeout=timeout)
    elapsed = time.time() - t0
    raw_sections = raw.split(DELIM + "\n") if raw else [""]
    # docker/echo may add trailing newline variants; be tolerant
    if len(raw_sections) != len(windows):
        raw_sections = raw.split(DELIM)
    species_set = set(species_order)
    seqs = {sp: [] for sp in species_order}
    block_counts = []
    total_bp = 0
    for (ws, we), section in zip(windows, raw_sections):
        pos_map, n_blocks = window_matrix(section, ws, we, species_set)
        block_counts.append(n_blocks)
        total_bp += (we - ws)
        for pos in range(ws, we):
            col = pos_map.get(pos, {})
            for sp in species_order:
                seqs[sp].append(col.get(sp, "-"))
    final_seqs = {}
    for sp in species_order:
        s = "".join(seqs[sp])
        if strand == "-":
            s = revcomp(s)
        final_seqs[sp] = s
    gene_dir = outdir / gene
    gene_dir.mkdir(parents=True, exist_ok=True)
    fa_path = gene_dir / f"{gene}.cds363.fa"
    with open(fa_path, "w", encoding="utf-8") as f:
        for sp in species_order:
            f.write(f">{sp}\n{final_seqs[sp]}\n")
    gallus_seq = final_seqs.get("Gallus_gallus", "")
    n_species_present = 0
    n_species_ge50 = 0
    for sp in species_order:
        s = final_seqs[sp]
        if not s:
            continue
        non_gap = sum(1 for c in s if c != "-")
        pct = 100.0 * non_gap / len(s) if s else 0.0
        if non_gap > 0:
            n_species_present += 1
        if pct >= 50.0:
            n_species_ge50 += 1
    bulbul = final_seqs.get("Pycnonotus_jocosus", "")
    bulbul_gap_pct = (
        100.0 * sum(1 for c in bulbul if c == "-") / len(bulbul) if bulbul else 100.0
    )
    blocks_path = gene_dir / f"{gene}.blocks.tsv"
    with open(blocks_path, "w", encoding="utf-8") as f:
        f.write("gene\tchrom\tstrand\tn_exon_windows\ttotal_block_lines\tcds_bp"
                "\tgallus_nongap_bp\tn_species_present\tn_species_ge50pct"
                "\tpycnonotus_gap_pct\telapsed_sec\n")
        f.write(
            f"{gene}\t{chrom}\t{strand}\t{len(windows)}\t{sum(block_counts)}\t{total_bp}"
            f"\t{sum(1 for c in gallus_seq if c != '-')}\t{n_species_present}"
            f"\t{n_species_ge50}\t{bulbul_gap_pct:.2f}\t{elapsed:.1f}\n"
        )
    return {
        "gene": gene, "status": "OK", "cds_bp": total_bp,
        "n_species_present": n_species_present, "n_species_ge50": n_species_ge50,
        "bulbul_gap_pct": bulbul_gap_pct, "elapsed": elapsed,
        "n_blocks": sum(block_counts), "n_windows": len(windows),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loci", default="data/c_loci/loci_galGal4.tsv")
    ap.add_argument("--species", default="data/c_loci/species_363.txt")
    ap.add_argument("--outdir", default="data/c_loci")
    ap.add_argument("--gene", action="append", default=None)
    ap.add_argument("--timeout", type=int, default=900)
    args = ap.parse_args()

    species_order = load_species(args.species)
    loci = load_loci(args.loci)
    genes = args.gene or list(loci.keys())
    outdir = Path(args.outdir)

    print("gene\tstatus\tcds_bp\tn_species_present\tn_species_ge50\tbulbul_gap_pct\telapsed_s\tn_blocks")
    for gene in genes:
        row = loci.get(gene)
        if not row or row.get("chrom") == "UNVERIFIED":
            print(f"{gene}\tSKIP_UNVERIFIED\t-\t-\t-\t-\t-\t-")
            continue
        try:
            res = extract_gene(gene, row, species_order, outdir, timeout=args.timeout)
        except subprocess.TimeoutExpired:
            print(f"{gene}\tTIMEOUT\t-\t-\t-\t-\t-\t-")
            continue
        except Exception as e:  # noqa: BLE001
            print(f"{gene}\tERROR:{e}\t-\t-\t-\t-\t-\t-", file=sys.stderr)
            print(f"{gene}\tERROR\t-\t-\t-\t-\t-\t-")
            continue
        if res["status"] != "OK":
            print(f"{gene}\t{res['status']}\t-\t-\t-\t-\t-\t-")
            continue
        print(
            f"{gene}\tOK\t{res['cds_bp']}\t{res['n_species_present']}\t{res['n_species_ge50']}"
            f"\t{res['bulbul_gap_pct']:.2f}\t{res['elapsed']:.1f}\t{res['n_blocks']}"
        )


if __name__ == "__main__":
    main()
