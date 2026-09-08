#!/usr/bin/env python3
"""Fetch galGal4 gene coordinates (refGene, fallback ncbiRefSeq/ensGene) via UCSC REST API.

Stdlib only (Python 3.11+). Writes data/c_loci/loci_galGal4.tsv.
Usage: python fetch_coords.py GENE1 GENE2 ...
"""
import json
import sys
import urllib.request
import urllib.error
import time

GENOME = "galGal4"
SEARCH_URL = "https://api.genome.ucsc.edu/search?genome={genome};search={gene}"
TRACK_URL = (
    "https://api.genome.ucsc.edu/getData/track?genome={genome};track={track};"
    "chrom={chrom};start={start};end={end}"
)


def http_get_json(url, retries=3, timeout=20):
    last_err = None
    for _ in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(1)
    raise last_err


def search_gene(gene, track="refGene"):
    url = SEARCH_URL.format(genome=GENOME, gene=gene)
    data = http_get_json(url)
    for block in data.get("positionMatches", []):
        if block.get("trackName") != track:
            continue
        matches = block.get("matches", [])
        # Prefer exact case-sensitive posName match, else first match.
        exact = [m for m in matches if m.get("posName", "").upper() == gene.upper()
                 and m.get("posName", "") == m.get("posName", "").upper()]
        chosen = exact[0] if exact else (matches[0] if matches else None)
        if chosen:
            pos = chosen["position"]  # e.g. chr11:18287877-18288821
            chrom, rng = pos.split(":")
            start, end = rng.replace(",", "").split("-")
            return {
                "chrom": chrom,
                "start": int(start) - 1,  # UCSC search is 1-based inclusive -> 0-based
                "end": int(end),
                "acc": chosen.get("hgFindMatches", ""),
                "track": track,
            }
    return None


def get_track_detail(chrom, start, end, track="refGene"):
    url = TRACK_URL.format(genome=GENOME, track=track, chrom=chrom, start=start, end=end)
    data = http_get_json(url)
    rows = data.get(track) or data.get("track") or []
    if isinstance(rows, dict):
        rows = rows.get(chrom, [])
    return rows


def resolve_gene(gene):
    for track in ("refGene", "ncbiRefSeq", "ensGene"):
        try:
            hit = search_gene(gene, track=track)
        except Exception as e:  # noqa: BLE001
            print(f"  [{gene}] search error on {track}: {e}", file=sys.stderr)
            continue
        if not hit:
            continue
        pad_start = max(0, hit["start"] - 2000)
        pad_end = hit["end"] + 2000
        try:
            rows = get_track_detail(hit["chrom"], pad_start, pad_end, track=track)
        except Exception as e:  # noqa: BLE001
            print(f"  [{gene}] track detail error on {track}: {e}", file=sys.stderr)
            continue
        # pick the row whose name matches accession or whose span best covers hit
        best = None
        for r in rows:
            if hit["acc"] and r.get("name") == hit["acc"]:
                best = r
                break
        if best is None and rows:
            # fallback: row with the largest overlap with hit span
            def overlap(r):
                return min(r.get("txEnd", 0), hit["end"]) - max(r.get("txStart", 0), hit["start"])
            best = max(rows, key=overlap)
        if best:
            return {
                "gene": gene,
                "chrom": best.get("chrom", hit["chrom"]),
                "strand": best.get("strand"),
                "txStart": best.get("txStart"),
                "txEnd": best.get("txEnd"),
                "cdsStart": best.get("cdsStart"),
                "cdsEnd": best.get("cdsEnd"),
                "exonStarts": best.get("exonStarts"),
                "exonEnds": best.get("exonEnds"),
                "exonCount": best.get("exonCount"),
                "name": best.get("name"),
                "track": track,
            }
    return None


def main():
    genes = sys.argv[1:]
    if not genes:
        print("usage: fetch_coords.py GENE1 GENE2 ...", file=sys.stderr)
        sys.exit(1)
    cols = [
        "gene", "chrom", "strand", "txStart", "txEnd", "cdsStart", "cdsEnd",
        "exonStarts", "exonEnds", "exonCount", "refseq_name", "track", "nguon",
    ]
    print("\t".join(cols))
    for gene in genes:
        rec = resolve_gene(gene)
        if not rec:
            print(f"  [{gene}] NOT FOUND on galGal4 refGene/ncbiRefSeq/ensGene -> UNVERIFIED",
                  file=sys.stderr)
            print("\t".join([gene] + ["UNVERIFIED"] * (len(cols) - 1)))
            continue
        exon_starts = rec["exonStarts"]
        exon_ends = rec["exonEnds"]
        if isinstance(exon_starts, list):
            exon_starts = ",".join(str(x) for x in exon_starts)
        if isinstance(exon_ends, list):
            exon_ends = ",".join(str(x) for x in exon_ends)
        row = [
            rec["gene"], rec["chrom"], str(rec["strand"]), str(rec["txStart"]), str(rec["txEnd"]),
            str(rec["cdsStart"]), str(rec["cdsEnd"]), str(exon_starts), str(exon_ends),
            str(rec["exonCount"]), rec["name"], rec["track"],
            f"UCSC REST {rec['track']} galGal4",
        ]
        print("\t".join(row))
        print(f"  [{gene}] OK {rec['chrom']}:{rec['txStart']}-{rec['txEnd']} "
              f"({rec['track']}, {rec['name']})", file=sys.stderr)


if __name__ == "__main__":
    main()
