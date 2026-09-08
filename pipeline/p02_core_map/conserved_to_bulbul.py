#!/usr/bin/env python3
"""conserved_to_bulbul.py -- loi A2: vung bao ton 363 loai chim (toa do ga
galGal4, tu ancRep_separate_models_rev.bw.conserved.bb) -> toa do bo gene
chao mao (Pycnonotus jocosus, GCA_013400435.1).

4 lenh con, chi dung Python 3.11 stdlib, xu ly theo luong (khong nap toan
bo dau vao vao bo nho tru khi noi ro):

  merge     BED 3 cot (bigBedToBed) -> gop khoang gan nhau -> BED 4 cot
  paf2bed   PAF (minimap2 -c) -> chon 1 hit tot nhat/query -> BED 6+
  annotate  BED (tu paf2bed) + GFF3.gz -> gan feature_class + gene
  enrich    core_annot.tsv [+ ban accelerated] + GFF3.gz -> kiem dinh gene
            giau vung loi so voi nen (nhi thuc, xap xi chuan) + doi chung
            am accelerated

Xem README.md trong cung thu muc de biet chi tiet cot dau ra va gioi han.
"""

from __future__ import annotations

import argparse
import bisect
import gzip
import math
import statistics
import sys
import urllib.parse
from collections import Counter, defaultdict
from contextlib import contextmanager

# ---------------------------------------------------------------------------
# Tien ich dung chung
# ---------------------------------------------------------------------------

LENGTH_BINS = [
    ("20_49", 20, 50),
    ("50_99", 50, 100),
    ("100_199", 100, 200),
    ("200_499", 200, 500),
    ("500_plus", 500, None),
]


def length_bin_label(length):
    """Xep 1 do dai (bp) vao histogram bin. Tra ve 'lt_20' cho truong hop
    hiem la min-len < 20 nen co phan tu ngan hon bin dau tien."""
    for label, lo, hi in LENGTH_BINS:
        if length >= lo and (hi is None or length < hi):
            return label
    return "lt_20"


IDENTITY_BINS = [
    ("lt_0.70", 0.0, 0.70),
    ("0.70_0.80", 0.70, 0.80),
    ("0.80_0.90", 0.80, 0.90),
    ("0.90_0.95", 0.90, 0.95),
    ("0.95_1.00", 0.95, 1.00),
    ("eq_1.00", 1.00, None),
]


def identity_bin_label(identity):
    for label, lo, hi in IDENTITY_BINS:
        if identity >= lo and (hi is None or identity < hi):
            return label
    return IDENTITY_BINS[0][0]


@contextmanager
def smart_open_read(path):
    """Mo doc: '-' = stdin. newline='' de tu xu ly CRLF/LF (khong de Python
    dich ngam), dong 'r' + rstrip('\\r\\n') o noi goi."""
    if path == "-":
        yield sys.stdin
    else:
        f = open(path, "r", newline="", encoding="utf-8")
        try:
            yield f
        finally:
            f.close()


@contextmanager
def smart_open_write(path):
    """Mo ghi: '-' = stdout. newline='' de ghi LF thuan tuy tren moi he dieu hanh."""
    if path == "-":
        yield sys.stdout
    else:
        f = open(path, "w", newline="", encoding="utf-8")
        try:
            yield f
        finally:
            f.close()


# ---------------------------------------------------------------------------
# merge: BED 3 cot -> BED 4 cot (gop khoang gan nhau)
# ---------------------------------------------------------------------------


def add_merge_parser(sub):
    p = sub.add_parser(
        "merge",
        help="Gop cac khoang bao ton lien ke thanh phan tu (BED 3 cot -> BED 4 cot)",
        description=(
            "Doc BED 3 cot (chrom,start,end) da sap theo chrom roi start "
            "(dung thu tu bigBedToBed xuat ra). Gop cac khoang cung chrom "
            "co khoang cach <= --gap; giu phan tu dai >= --min-len. "
            "Xu ly tung dong theo luong, khong nap toan bo dau vao vao bo nho."
        ),
    )
    p.add_argument(
        "--in",
        dest="in_path",
        required=True,
        help="BED 3 cot dau vao, hoac - de doc tu stdin (pipe truc tiep tu bigBedToBed, tranh file trung gian lon)",
    )
    p.add_argument(
        "--out",
        dest="out_path",
        required=True,
        help="BED 4 cot dau ra (cot 4 = ID dang chrom:start-end), hoac - de ghi ra stdout",
    )
    p.add_argument(
        "--gap",
        type=int,
        default=10,
        help="Khoang cach toi da (bp) giua 2 khoang de gop lam mot (mac dinh 10)",
    )
    p.add_argument(
        "--min-len",
        dest="min_len",
        type=int,
        default=20,
        help="Do dai toi thieu (bp) de giu phan tu sau khi gop (mac dinh 20)",
    )
    p.add_argument(
        "--stats",
        default=None,
        help="Duong dan ghi thong ke TSV (bo qua neu khong truyen)",
    )
    p.set_defaults(func=cmd_merge)


def cmd_merge(args):
    intervals_in = 0
    bp_in = 0
    elements_out = 0
    bp_out = 0
    length_hist = Counter()
    chrom_counts = Counter()

    state = {"chrom": None, "start": None, "end": None}

    def flush(writer):
        nonlocal elements_out, bp_out
        if state["chrom"] is None:
            return
        length = state["end"] - state["start"]
        if length >= args.min_len:
            name = "{}:{}-{}".format(state["chrom"], state["start"], state["end"])
            writer.write(
                "{}\t{}\t{}\t{}\n".format(state["chrom"], state["start"], state["end"], name)
            )
            elements_out += 1
            bp_out += length
            length_hist[length_bin_label(length)] += 1
            chrom_counts[state["chrom"]] += 1

    seen_chroms = set()
    last_start_in_chrom = None

    with smart_open_read(args.in_path) as fin, smart_open_write(args.out_path) as fout:
        for lineno, raw_line in enumerate(fin, 1):
            line = raw_line.rstrip("\r\n")
            if not line:
                continue
            fields = line.split("\t")
            if len(fields) < 3:
                raise SystemExit(
                    "merge: dong {} khong du 3 cot BED: {!r}".format(lineno, line)
                )
            chrom = fields[0]
            try:
                start = int(fields[1])
                end = int(fields[2])
            except ValueError:
                raise SystemExit(
                    "merge: dong {} start/end khong phai so nguyen: {!r}".format(lineno, line)
                )
            if end <= start:
                raise SystemExit(
                    "merge: dong {} end <= start (khoang rong/am): {!r}".format(lineno, line)
                )

            intervals_in += 1
            bp_in += end - start

            if chrom != state["chrom"]:
                flush(fout)
                if chrom in seen_chroms:
                    raise SystemExit(
                        "merge: dong {} chrom {!r} xuat hien lai sau khi da chuyen sang "
                        "chrom khac - dau vao phai duoc nhom lien tuc theo chrom "
                        "(bigBedToBed xuat dung thu tu)".format(lineno, chrom)
                    )
                seen_chroms.add(chrom)
                state["chrom"] = chrom
                state["start"] = start
                state["end"] = end
                last_start_in_chrom = start
            else:
                if start < last_start_in_chrom:
                    raise SystemExit(
                        "merge: dong {} start {} < start dong truoc {} tren chrom {!r} "
                        "- dau vao phai sap tang dan theo start".format(
                            lineno, start, last_start_in_chrom, chrom
                        )
                    )
                last_start_in_chrom = start
                if start <= state["end"] + args.gap:
                    if end > state["end"]:
                        state["end"] = end
                else:
                    flush(fout)
                    state["start"] = start
                    state["end"] = end
        flush(fout)

    if args.stats:
        with smart_open_write(args.stats) as sf:
            sf.write("metric\tvalue\n")
            sf.write("intervals_in\t{}\n".format(intervals_in))
            sf.write("elements_out\t{}\n".format(elements_out))
            sf.write("bp_in\t{}\n".format(bp_in))
            sf.write("bp_out\t{}\n".format(bp_out))
            for label, _, _ in LENGTH_BINS:
                sf.write("length_{}\t{}\n".format(label, length_hist.get(label, 0)))
            if length_hist.get("lt_20", 0):
                sf.write("length_lt_20\t{}\n".format(length_hist["lt_20"]))
            sf.write("\nchrom\telements\n")
            for chrom, cnt in chrom_counts.most_common(40):
                sf.write("{}\t{}\n".format(chrom, cnt))

    return 0


# ---------------------------------------------------------------------------
# paf2bed: PAF (minimap2 -c) -> BED 6+ (1 hit tot nhat / query)
# ---------------------------------------------------------------------------


def add_paf2bed_parser(sub):
    p = sub.add_parser(
        "paf2bed",
        help="Chon hit tot nhat moi query trong PAF minimap2 -> BED toa do chao mao",
        description=(
            "Doc PAF chuan 12 cot (minimap2 -c). Voi moi query giu 1 hit tot nhat "
            "(uu tien mapq, roi so match cot 10, roi do dai align cot 11). "
            "identity = matches/alignment-block-length; coverage = (qend-qstart)/qlen. "
            "Hit duoi nguong hoac query khong co hit nao (--query-list) -> vao unmapped."
        ),
    )
    p.add_argument("--paf", required=True, help="File PAF dau vao, hoac - de doc tu stdin")
    p.add_argument("--out", required=True, help="BED 6+ dau ra cho cac query dat nguong")
    p.add_argument(
        "--unmapped",
        required=True,
        help="TSV liet ke query bi loai kem ly do (no_hit/low_identity/low_coverage)",
    )
    p.add_argument("--stats", default=None, help="Duong dan ghi thong ke TSV")
    p.add_argument(
        "--min-identity",
        dest="min_identity",
        type=float,
        default=0.70,
        help="Nguong identity toi thieu (0-1, mac dinh 0.70)",
    )
    p.add_argument(
        "--min-coverage",
        dest="min_coverage",
        type=float,
        default=0.80,
        help="Nguong coverage toi thieu (0-1, mac dinh 0.80)",
    )
    p.add_argument(
        "--query-list",
        dest="query_list",
        default=None,
        help=(
            "File liet ke toan bo ten query da dua vao minimap2 (vd elements.bed, "
            "lay cot 4). Neu co, query khong xuat hien trong PAF duoc bao no_hit. "
            "Neu khong truyen, chi phat hien duoc low_identity/low_coverage "
            "(khong biet duoc query nao hoan toan khong co hit)."
        ),
    )
    p.set_defaults(func=cmd_paf2bed)


def _read_query_universe(path):
    """Doc danh sach toan bo query da dua vao minimap2 (--query-list, thuong
    la elements.bed). Tra ve list (qname, length_hint): length_hint =
    end-start neu dong co dang BED >=4 cot voi cot 2/3 la so nguyen, nguoc
    lai None. length_hint dung de xep query KHONG co hit nao (no_hit) vao
    dung bin do dai cho bang mapped_pct theo qlen_bin (query co hit da co
    qlen thuc tu PAF, khong can length_hint)."""
    entries = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip("\r\n")
            if not line:
                continue
            fields = line.split("\t")
            if len(fields) >= 4:
                qname = fields[3]
                try:
                    length_hint = int(fields[2]) - int(fields[1])
                except ValueError:
                    length_hint = None
            else:
                qname = line.split()[0]
                length_hint = None
            entries.append((qname, length_hint))
    return entries


def cmd_paf2bed(args):
    best = {}
    hit_count = Counter()

    with smart_open_read(args.paf) as fin:
        for lineno, raw_line in enumerate(fin, 1):
            line = raw_line.rstrip("\r\n")
            if not line:
                continue
            fields = line.split("\t")
            if len(fields) < 12:
                raise SystemExit(
                    "paf2bed: dong {} thieu cot (can >=12 cot PAF): {!r}".format(lineno, line)
                )
            qname = fields[0]
            try:
                qlen = int(fields[1])
                qstart = int(fields[2])
                qend = int(fields[3])
                strand = fields[4]
                tname = fields[5]
                tstart = int(fields[7])
                tend = int(fields[8])
                nmatch = int(fields[9])
                alnlen = int(fields[10])
                mapq = int(fields[11])
            except (ValueError, IndexError):
                raise SystemExit(
                    "paf2bed: dong {} truong so khong hop le: {!r}".format(lineno, line)
                )

            hit_count[qname] += 1
            rank_key = (mapq, nmatch, alnlen)
            prev = best.get(qname)
            if prev is None or rank_key > prev["rank_key"]:
                identity = (nmatch / alnlen) if alnlen > 0 else 0.0
                coverage = ((qend - qstart) / qlen) if qlen > 0 else 0.0
                best[qname] = {
                    "rank_key": rank_key,
                    "tname": tname,
                    "tstart": tstart,
                    "tend": tend,
                    "qname": qname,
                    "qlen": qlen,
                    "strand": strand,
                    "mapq": mapq,
                    "identity": identity,
                    "coverage": coverage,
                }

    if args.query_list:
        query_entries = _read_query_universe(args.query_list)
    else:
        query_entries = [(q, None) for q in best.keys()]
    query_names = [q for q, _ in query_entries]
    length_hint_by_name = dict(query_entries)
    total_queries = len(query_names)

    mapped_rows = []
    unmapped_rows = []
    identity_dist = Counter()
    length_hist = Counter()
    total_by_bin = Counter()
    mapped_by_bin = Counter()

    for qname in query_names:
        rec = best.get(qname)
        qlen_for_bin = rec["qlen"] if rec is not None else length_hint_by_name.get(qname)
        if qlen_for_bin is not None:
            total_by_bin[length_bin_label(qlen_for_bin)] += 1
        if rec is None:
            unmapped_rows.append((qname, "no_hit", ""))
            continue
        identity_dist[identity_bin_label(rec["identity"])] += 1
        length_hist[length_bin_label(rec["qlen"])] += 1
        if rec["identity"] < args.min_identity:
            unmapped_rows.append(
                (qname, "low_identity", "identity={:.4f}".format(rec["identity"]))
            )
        elif rec["coverage"] < args.min_coverage:
            unmapped_rows.append(
                (qname, "low_coverage", "coverage={:.4f}".format(rec["coverage"]))
            )
        else:
            mapped_rows.append(rec)
            mapped_by_bin[length_bin_label(rec["qlen"])] += 1

    mapped_rows.sort(key=lambda r: (r["tname"], r["tstart"]))

    with smart_open_write(args.out) as fout:
        for r in mapped_rows:
            score = max(0, min(1000, round(r["identity"] * 1000)))
            fout.write(
                "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{:.4f}\t{}\n".format(
                    r["tname"],
                    r["tstart"],
                    r["tend"],
                    r["qname"],
                    score,
                    r["strand"],
                    r["qlen"],
                    r["coverage"],
                    r["mapq"],
                )
            )

    with smart_open_write(args.unmapped) as uf:
        uf.write("qname\treason\tdetail\n")
        for qname, reason, detail in unmapped_rows:
            uf.write("{}\t{}\t{}\n".format(qname, reason, detail))

    second_hit_count = sum(1 for q in query_names if hit_count.get(q, 0) > 1)

    if args.stats:
        with smart_open_write(args.stats) as sf:
            sf.write("metric\tvalue\n")
            sf.write("total_queries\t{}\n".format(total_queries))
            sf.write("mapped\t{}\n".format(len(mapped_rows)))
            pct = (len(mapped_rows) / total_queries * 100) if total_queries else 0.0
            sf.write("mapped_pct\t{:.2f}\n".format(pct))
            sf.write("unmapped\t{}\n".format(len(unmapped_rows)))
            sf.write("second_hit_queries\t{}\n".format(second_hit_count))
            sf.write("\nqlen_bin\tcount\n")
            for label, _, _ in LENGTH_BINS:
                sf.write("{}\t{}\n".format(label, length_hist.get(label, 0)))
            if length_hist.get("lt_20", 0):
                sf.write("lt_20\t{}\n".format(length_hist["lt_20"]))
            sf.write("\nidentity_bin\tcount\n")
            for label, _, _ in IDENTITY_BINS:
                sf.write("{}\t{}\n".format(label, identity_dist.get(label, 0)))
            # mapped_pct theo qlen_bin: mapped/total (total = toan bo query
            # trong bin, ke ca no_hit qua length_hint tu --query-list), khac
            # voi bang "qlen_bin\tcount" o tren chi dem query CO hit (ke ca
            # bi loai vi identity/coverage).
            sf.write("\nqlen_bin\tmapped\ttotal\tmapped_pct\n")
            bin_labels = [label for label, _, _ in LENGTH_BINS]
            if total_by_bin.get("lt_20", 0):
                bin_labels = bin_labels + ["lt_20"]
            for label in bin_labels:
                tot = total_by_bin.get(label, 0)
                mp = mapped_by_bin.get(label, 0)
                pct = (mp / tot * 100) if tot else 0.0
                sf.write("{}\t{}\t{}\t{:.2f}\n".format(label, mp, tot, pct))

    return 0


# ---------------------------------------------------------------------------
# annotate: BED (tu paf2bed) + GFF3.gz -> feature_class + gene
# ---------------------------------------------------------------------------


class IntervalIndex:
    """Chi muc khoang cho 1 scaffold: sap theo start, tim giao qua bisect +
    prefix-max-end (xu ly duoc khoang chong lan ma khong quet O(n) toan bo)."""

    __slots__ = ("starts", "ends", "payload", "prefix_max_end")

    def __init__(self, intervals):
        ordered = sorted(intervals, key=lambda t: t[0])
        self.starts = [t[0] for t in ordered]
        self.ends = [t[1] for t in ordered]
        self.payload = [t[2] for t in ordered]
        prefix = []
        running_max = None
        for e in self.ends:
            running_max = e if running_max is None else max(running_max, e)
            prefix.append(running_max)
        self.prefix_max_end = prefix

    def best_overlap(self, q_start, q_end):
        """Tra ve (payload, do_dai_giao) cua khoang giao lon nhat voi
        [q_start, q_end), hoac None neu khong khoang nao giao."""
        if not self.starts:
            return None
        idx = bisect.bisect_right(self.starts, q_end - 1) - 1
        best_payload = None
        best_len = 0
        i = idx
        while i >= 0:
            s = self.starts[i]
            e = self.ends[i]
            if e > q_start and s < q_end:
                ov = min(e, q_end) - max(s, q_start)
                if ov > best_len:
                    best_len = ov
                    best_payload = self.payload[i]
            if self.prefix_max_end[i] <= q_start:
                break
            i -= 1
        if best_payload is None:
            return None
        return best_payload, best_len


def add_annotate_parser(sub):
    p = sub.add_parser(
        "annotate",
        help="Gan feature_class (CDS/exon_noncoding/intron/intergenic) + gene cho tung vung BED",
        description=(
            "Doc GFF3.gz, lay feature gene/pseudogene/exon/CDS/mRNA (mRNA de noi "
            "gene qua Parent/ID; pseudogene xu ly nhu gene). Voi moi vung BED: "
            "giao voi CDS truoc, roi exon, roi gene/pseudogene; giao ma "
            "khong giao exon la intron; khong giao gene/pseudogene nao la intergenic. "
            "Index theo scaffold (142 nghin scaffold), sap theo start, dung bisect."
        ),
    )
    p.add_argument(
        "--bed",
        required=True,
        help="BED (>=3 cot, thuong la dau ra paf2bed) can gan nhan, hoac - de doc tu stdin",
    )
    p.add_argument("--gff", required=True, help="GFF3 .gz cua bo gene chao mao (NCBI)")
    p.add_argument(
        "--out",
        required=True,
        help="TSV dau ra: giu nguyen cac cot BED goc + them feature_class, gene_id, gene_name",
    )
    p.add_argument("--stats", default=None, help="Duong dan ghi thong ke TSV")
    p.set_defaults(func=cmd_annotate)


def _parse_gff_attributes(attr_str):
    attrs = {}
    for part in attr_str.split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        key, _, value = part.partition("=")
        attrs[key] = urllib.parse.unquote(value)
    return attrs


def _first_parent(parent_value):
    # Parent co the la danh sach cach nhau boi dau phay (nhieu ban sao/isoform);
    # lay phan tu dau tien lam dai dien (gioi han da ghi trong README).
    if not parent_value:
        return ""
    return parent_value.split(",")[0]


def _load_gff(gff_path):
    """Doc GFF3.gz 1 lan, tra ve 3 dict scaffold -> IntervalIndex cho
    gene+pseudogene (payload=(gene_id,gene_name)), CDS va exon
    (payload=(gene_id,gene_name) suy tu Parent/ID cua chinh CDS/exon do,
    khong phai tu vi tri khong gian - tranh gan nham gene khi 2 gene chong
    toa do). pseudogene duoc nap chung voi gene (cung 1 nhanh) vi GFF chao
    mao co 1653 ban ghi pseudogene, moi ban ghi co mRNA(pseudo=true) con roi
    exon/CDS con - neu khong nap, than pseudogene ngoai exon se bi bao sai
    thanh intergenic va gene_name cua CDS/exon thuoc pseudogene se hien ID
    tho thay vi ten sach (REQUIRED_FIX #1)."""
    gene_name_by_id = {}
    mrna_to_gene = {}
    gene_raw = defaultdict(list)  # scaffold -> [(start0, end, gene_id)]
    exon_raw = defaultdict(list)  # scaffold -> [(start0, end, parent)]
    cds_raw = defaultdict(list)

    opener = gzip.open if gff_path.endswith(".gz") else open
    with opener(gff_path, "rt", encoding="utf-8", errors="replace") as f:
        for raw_line in f:
            line = raw_line.rstrip("\r\n")
            if not line or line[0] == "#":
                continue
            fields = line.split("\t")
            if len(fields) < 9:
                continue
            seqid, _source, ftype, start_s, end_s, _score, _strand, _phase, attr_str = fields[:9]
            try:
                start0 = int(start_s) - 1
                end_i = int(end_s)
            except ValueError:
                continue
            if end_i <= start0:
                continue
            attrs = _parse_gff_attributes(attr_str)
            if ftype in ("gene", "pseudogene"):
                # pseudogene xu ly giong gene: than pseudogene ngoai moi exon
                # cua no -> "intron" thay vi "intergenic" (REQUIRED_FIX #1,
                # xac nhan 1653 ban ghi pseudogene trong GFF chao mao that,
                # xem research/synthesis/05-review-code-x1.md Finding #1).
                gene_id = attrs.get("ID", "")
                if not gene_id:
                    continue
                name = attrs.get("Name") or attrs.get("gene") or gene_id
                gene_name_by_id[gene_id] = name
                gene_raw[seqid].append((start0, end_i, gene_id))
            elif ftype == "mRNA":
                mrna_id = attrs.get("ID", "")
                parent = _first_parent(attrs.get("Parent", ""))
                if mrna_id and parent:
                    mrna_to_gene[mrna_id] = parent
            elif ftype == "exon":
                parent = _first_parent(attrs.get("Parent", ""))
                exon_raw[seqid].append((start0, end_i, parent))
            elif ftype == "CDS":
                parent = _first_parent(attrs.get("Parent", ""))
                cds_raw[seqid].append((start0, end_i, parent))

    def resolve_gene(parent):
        gene_id = mrna_to_gene.get(parent, parent)
        name = gene_name_by_id.get(gene_id, gene_id)
        return (gene_id, name)

    gene_index = {}
    for seqid, entries in gene_raw.items():
        gene_index[seqid] = IntervalIndex(
            [(s, e, (gid, gene_name_by_id.get(gid, gid))) for s, e, gid in entries]
        )

    cds_index = {}
    for seqid, entries in cds_raw.items():
        cds_index[seqid] = IntervalIndex(
            [(s, e, resolve_gene(parent)) for s, e, parent in entries]
        )

    exon_index = {}
    for seqid, entries in exon_raw.items():
        exon_index[seqid] = IntervalIndex(
            [(s, e, resolve_gene(parent)) for s, e, parent in entries]
        )

    gene_span = {}
    for _scaf, rows in gene_raw.items():
        for start0, end_i, gene_id in rows:
            span = end_i - start0
            if span > gene_span.get(gene_id, 0):
                gene_span[gene_id] = span

    return gene_index, cds_index, exon_index, gene_span


def _classify_region(chrom, start, end, gene_index, cds_index, exon_index):
    cds_idx = cds_index.get(chrom)
    if cds_idx is not None:
        hit = cds_idx.best_overlap(start, end)
        if hit is not None:
            gene_id, gene_name = hit[0]
            return "CDS", gene_id, gene_name

    exon_idx = exon_index.get(chrom)
    if exon_idx is not None:
        hit = exon_idx.best_overlap(start, end)
        if hit is not None:
            gene_id, gene_name = hit[0]
            return "exon_noncoding", gene_id, gene_name

    gene_idx = gene_index.get(chrom)
    if gene_idx is not None:
        hit = gene_idx.best_overlap(start, end)
        if hit is not None:
            gene_id, gene_name = hit[0]
            return "intron", gene_id, gene_name

    return "intergenic", "", ""


MIN_GENE_LEN_FOR_DENSITY = 1000
MIN_BP_FOR_DENSITY = 200


def cmd_annotate(args):
    gene_index, cds_index, exon_index, gene_span = _load_gff(args.gff)

    class_bp = Counter()
    class_count = Counter()
    gene_bp = Counter()
    gene_name_lookup = {}

    with smart_open_read(args.bed) as fin, smart_open_write(args.out) as fout:
        for lineno, raw_line in enumerate(fin, 1):
            line = raw_line.rstrip("\r\n")
            if not line:
                continue
            fields = line.split("\t")
            if len(fields) < 3:
                raise SystemExit(
                    "annotate: dong {} khong du 3 cot BED: {!r}".format(lineno, line)
                )
            chrom = fields[0]
            try:
                start = int(fields[1])
                end = int(fields[2])
            except ValueError:
                raise SystemExit(
                    "annotate: dong {} start/end khong phai so nguyen: {!r}".format(lineno, line)
                )

            feature_class, gene_id, gene_name = _classify_region(
                chrom, start, end, gene_index, cds_index, exon_index
            )

            length = end - start
            class_bp[feature_class] += length
            class_count[feature_class] += 1
            if gene_id:
                gene_bp[gene_id] += length
                gene_name_lookup[gene_id] = gene_name

            fout.write("\t".join(fields) + "\t{}\t{}\t{}\n".format(feature_class, gene_id, gene_name))

    if args.stats:
        with smart_open_write(args.stats) as sf:
            sf.write("feature_class\tregions\tbp\n")
            for fc in ("CDS", "exon_noncoding", "intron", "intergenic"):
                sf.write("{}\t{}\t{}\n".format(fc, class_count.get(fc, 0), class_bp.get(fc, 0)))
            sf.write("\ngene_id\tgene_name\tbp\tgene_len\tbp_per_kb\n")
            for gene_id, bp in gene_bp.most_common(50):
                glen = gene_span.get(gene_id, 0)
                dens = (1000.0 * bp / glen) if glen else 0.0
                sf.write("{}\t{}\t{}\t{}\t{:.2f}\n".format(
                    gene_id, gene_name_lookup.get(gene_id, ""), bp, glen, dens))

            # Bang thu hai: xep theo MAT DO (bp loi tren moi kb chieu dai gene).
            # Xep theo tong bp thien vi gene dai - canh bao cua A1/Antigravity
            # (research/raw/A1-antigravity-gene-interpretation.md muc 5).
            sf.write("\n# xep theo mat do; loc gene_len >= {} bp va bp >= {}\n".format(
                MIN_GENE_LEN_FOR_DENSITY, MIN_BP_FOR_DENSITY))
            sf.write("gene_id\tgene_name\tbp\tgene_len\tbp_per_kb\n")
            dens_rows = []
            for gene_id, bp in gene_bp.items():
                glen = gene_span.get(gene_id, 0)
                if glen >= MIN_GENE_LEN_FOR_DENSITY and bp >= MIN_BP_FOR_DENSITY:
                    dens_rows.append((1000.0 * bp / glen, gene_id, bp, glen))
            dens_rows.sort(key=lambda r: (-r[0], r[1]))
            for dens, gene_id, bp, glen in dens_rows[:50]:
                sf.write("{}\t{}\t{}\t{}\t{:.2f}\n".format(
                    gene_id, gene_name_lookup.get(gene_id, ""), bp, glen, dens))

    return 0


# ---------------------------------------------------------------------------
# enrich: gene giau vung loi so voi nen (null model nhi thuc) + doi chung
# am bang bo accelerated. Dac ta: research/briefs/X5-enrichment-null-model.md
# + research/raw/A2-antigravity-null-model.md (muc 1, 2).
# ---------------------------------------------------------------------------


def _sum_chrom_sizes(path):
    """Doc file chrom.sizes (>=2 cot: chrom, size, ...; tach boi khoang trang
    bat ky de tuong thich ca .chrom.sizes lan .fai). Tra ve tong cot 2."""
    total = 0
    with open(path, "r", newline="", encoding="utf-8") as f:
        for lineno, raw_line in enumerate(f, 1):
            line = raw_line.rstrip("\r\n")
            if not line:
                continue
            fields = line.split()
            if len(fields) < 2:
                raise SystemExit(
                    "enrich: dong {} cua --chrom-sizes thieu cot kich thuoc: {!r}".format(
                        lineno, line
                    )
                )
            try:
                total += int(fields[1])
            except ValueError:
                raise SystemExit(
                    "enrich: dong {} cua --chrom-sizes cot 2 khong phai so nguyen: {!r}".format(
                        lineno, line
                    )
                )
    return total


def _read_annot_gene_bp(path):
    """Doc 1 file dau ra cua lenh 'annotate' (KHONG header; >=6 cot, 3 cot
    dau la chrom/start/end, 3 cot CUOI la feature_class/gene_id/gene_name --
    dung vi tri tuong doi tu dau/cuoi de tuong thich moi so cot BED goc,
    giong cach cmd_annotate() tu doc lai dau vao cua no).

    Tra ve (total_bp, gene_bp, gene_name_by_id):
      total_bp        tong bp CUA MOI DONG (ke ca dong intergenic/gene_id
                       rong) - dung lam tu so P0, khop dinh nghia brief
                       "tong bp loi trong --annot".
      gene_bp         Counter gene_id -> tong bp cac dong co gene_id (giong
                       het gene_bp trong cmd_annotate).
      gene_name_by_id dict gene_id -> gene_name (lay tu chinh cot cuoi cua
                       --annot, KHONG doc lai tu GFF).
    """
    total_bp = 0
    gene_bp = Counter()
    gene_name_by_id = {}
    with smart_open_read(path) as f:
        for lineno, raw_line in enumerate(f, 1):
            line = raw_line.rstrip("\r\n")
            if not line:
                continue
            fields = line.split("\t")
            if len(fields) < 6:
                raise SystemExit(
                    "enrich: dong {} cua {} khong du 6 cot (can toi thieu "
                    "chrom,start,end,feature_class,gene_id,gene_name): {!r}".format(
                        lineno, path, line
                    )
                )
            try:
                start = int(fields[1])
                end = int(fields[2])
            except ValueError:
                raise SystemExit(
                    "enrich: dong {} cua {} start/end khong phai so nguyen: {!r}".format(
                        lineno, path, line
                    )
                )
            length = end - start
            total_bp += length
            gene_id = fields[-2]
            gene_name = fields[-1]
            if gene_id:
                gene_bp[gene_id] += length
                gene_name_by_id[gene_id] = gene_name
    return total_bp, gene_bp, gene_name_by_id


def benjamini_hochberg(pvalues):
    """Hieu chinh da kiem dinh Benjamini-Hochberg (FDR).

    Nhan list p-value theo BAT KY thu tu, tra ve list q-value CUNG THU TU
    voi dau vao (khong sap lai). Thuat toan chuan: sap tang dan theo
    p-value, q(rank) = p(rank) * m / rank, roi lay MIN LUY TICH tu rank lon
    ve rank nho de dam bao q khong giam dan khi p tang (buoc step-up)."""
    m = len(pvalues)
    if m == 0:
        return []
    order = sorted(range(m), key=lambda i: pvalues[i])
    q = [0.0] * m
    running_min = 1.0
    for rank in range(m, 0, -1):
        idx = order[rank - 1]
        val = pvalues[idx] * m / rank
        running_min = min(running_min, val)
        q[idx] = min(running_min, 1.0)
    return q


def _one_sided_rank_p(bp_obs, gene_len, p0):
    """p-value MOT PHIA ("giau hon nen") xap xi chuan co hieu chinh lien tuc
    cho mo hinh nhi thuc (so phep thu n=gene_len, xac suat p=p0, so thanh
    cong=bp_obs). gene_len lon (10^4-10^6) nen KHONG tinh chinh xac tong
    nhi thuc duoc - day la XAP XI, CHI dung de XEP HANG (xem 3 canh bao
    trong README, dac biet: cac base trong 1 vung loi KHONG doc lap nen
    p-value nay khong dung de tuyen bo y nghia thong ke chat).

    statistics.NormalDist khong co san ham survival function (.sf) trong
    thu vien chuan (xac nhan tren Python 3.14: hasattr(...,'sf') == False)
    nen tinh tay bang 1 - cdf() de chay dung tren moi ban Python >= 3.8.

    Tra ve (rank_score_p, approx_warn). approx_warn=1 khi gene_len*p0 < 10
    (kinh nghiem chuan: xap xi chuan cho nhi thuc doi hoi n*p va n*(1-p)
    deu du lon; o day p0 thuong nho nen chi kiem ve phia n*p, dung dung
    nhu brief yeu cau)."""
    mu = gene_len * p0
    approx_warn = 1 if mu < 10 else 0
    var = gene_len * p0 * (1.0 - p0)
    if var <= 0.0:
        # p0 la 0/1 (hoac gene_len=0 khi nguoi dung ha --min-gene-len xuong
        # 0): phan phoi suy bien, khong co do lech - so bp_obs truc tiep
        # voi trung binh de tra p bien (0/0.5/1) thay vi chia cho 0.
        if bp_obs > mu:
            return 0.0, approx_warn
        if bp_obs < mu:
            return 1.0, approx_warn
        return 0.5, approx_warn
    sigma = math.sqrt(var)
    dist = statistics.NormalDist(mu=mu, sigma=sigma)
    p = 1.0 - dist.cdf(bp_obs - 0.5)
    return min(1.0, max(0.0, p)), approx_warn


def add_enrich_parser(sub):
    p = sub.add_parser(
        "enrich",
        help=(
            "Kiem dinh gene giau vung loi so voi nen ngau nhien (nhi thuc) "
            "+ doi chung am bang bo accelerated"
        ),
        description=(
            "Doc dau ra cua 'annotate' tren bo conserved (--annot, bat buoc) "
            "va tuy chon tren bo accelerated (--annot-accel) + GFF3 (lay do "
            "dai gene) -> xep hang gene theo do giau vung loi SO VOI NEN "
            "ngau nhien P0 = tong bp loi / tong khong gian he gen. p-value "
            "mot phia (cot rank_score_p) la XAP XI CHUAN co hieu chinh lien "
            "tuc cho mo hinh nhi thuc - CHI dung de xep hang, KHONG dung de "
            "tuyen bo y nghia thong ke (base trong 1 vung loi khong doc "
            "lap - xem README muc canh bao)."
        ),
    )
    p.add_argument(
        "--annot",
        required=True,
        help="TSV dau ra cua lenh 'annotate' tren bo conserved (vd core_annot.tsv)",
    )
    p.add_argument(
        "--annot-accel",
        dest="annot_accel",
        default=None,
        help=(
            "TSV dau ra cua lenh 'annotate' tren bo accelerated (doi chung am, "
            "tuy chon). Neu truyen, dau ra co them accel_bp/accel_fold/ca_ratio"
        ),
    )
    p.add_argument(
        "--gff",
        required=True,
        help="GFF3 .gz (hoac khong nen) cua bo gene chao mao - dung de lay do dai gene",
    )
    space = p.add_mutually_exclusive_group(required=True)
    space.add_argument(
        "--genome-size",
        dest="genome_size",
        type=int,
        default=None,
        help="Tong so bp khong gian xet (vd tong do dai he gen/tap NST dang xet)",
    )
    space.add_argument(
        "--chrom-sizes",
        dest="chrom_sizes",
        default=None,
        help="File >=2 cot (chrom, size, ...); tong cot 2 dung lam khong gian xet",
    )
    p.add_argument(
        "--out",
        required=True,
        help="TSV dau ra (co header), 1 dong/gene qua nguong loc, sap theo fold giam dan",
    )
    p.add_argument(
        "--stats",
        default=None,
        help="Duong dan ghi thong ke TSV (P0, top 20 theo fold, top 20 theo ca_ratio...)",
    )
    p.add_argument(
        "--min-gene-len",
        dest="min_gene_len",
        type=int,
        default=MIN_GENE_LEN_FOR_DENSITY,
        help="Chi xet gene co do dai (bp, tu GFF) >= nguong nay (mac dinh {})".format(
            MIN_GENE_LEN_FOR_DENSITY
        ),
    )
    p.add_argument(
        "--min-bp",
        dest="min_bp",
        type=int,
        default=MIN_BP_FOR_DENSITY,
        help="Chi xet gene co bp_obs >= nguong nay (mac dinh {})".format(MIN_BP_FOR_DENSITY),
    )
    p.add_argument(
        "--fdr",
        type=float,
        default=0.05,
        help="Nguong Benjamini-Hochberg (bh_q) de bat signif_flag (mac dinh 0.05)",
    )
    p.set_defaults(func=cmd_enrich)


ENRICH_OUT_HEADER = [
    "gene_id",
    "gene_name",
    "bp_obs",
    "gene_len",
    "bp_exp",
    "fold",
    "rank_score_p",
    "bh_q",
    "signif_flag",
    "approx_warn",
]
ENRICH_OUT_HEADER_ACCEL = ENRICH_OUT_HEADER + ["accel_bp", "accel_fold", "ca_ratio"]


def _fmt_cell(value):
    if isinstance(value, float):
        return "{:.6g}".format(value)
    return str(value)


def cmd_enrich(args):
    if args.genome_size is not None:
        total_space = args.genome_size
    else:
        total_space = _sum_chrom_sizes(args.chrom_sizes)
    if total_space <= 0:
        raise SystemExit(
            "enrich: tong khong gian xet (--genome-size/--chrom-sizes) phai > 0"
        )

    total_core_bp, gene_bp, gene_name_by_id = _read_annot_gene_bp(args.annot)
    p0 = total_core_bp / total_space

    have_accel = args.annot_accel is not None
    if have_accel:
        total_accel_bp, accel_gene_bp, _accel_names = _read_annot_gene_bp(args.annot_accel)
        p0_accel = total_accel_bp / total_space
    else:
        total_accel_bp, accel_gene_bp, p0_accel = 0, Counter(), 0.0

    _gene_idx, _cds_idx, _exon_idx, gene_span = _load_gff(args.gff)

    rows = []
    for gene_id, bp_obs in gene_bp.items():
        gene_len = gene_span.get(gene_id, 0)
        if gene_len < args.min_gene_len or bp_obs < args.min_bp:
            continue
        bp_exp = p0 * gene_len
        if bp_exp > 0:
            fold = bp_obs / bp_exp
        elif bp_obs > 0:
            fold = float("inf")
        else:
            fold = 1.0
        rank_score_p, approx_warn = _one_sided_rank_p(bp_obs, gene_len, p0)

        row = {
            "gene_id": gene_id,
            "gene_name": gene_name_by_id.get(gene_id, gene_id),
            "bp_obs": bp_obs,
            "gene_len": gene_len,
            "bp_exp": bp_exp,
            "fold": fold,
            "rank_score_p": rank_score_p,
            "approx_warn": approx_warn,
        }

        if have_accel:
            accel_bp = accel_gene_bp.get(gene_id, 0)
            accel_bp_exp = p0_accel * gene_len
            accel_fold = (accel_bp / accel_bp_exp) if accel_bp_exp > 0 else 0.0
            if accel_bp == 0:
                ca_ratio = float("inf")
            elif accel_fold > 0:
                ca_ratio = fold / accel_fold
            else:
                ca_ratio = float("inf")
            row["accel_bp"] = accel_bp
            row["accel_fold"] = accel_fold
            row["ca_ratio"] = ca_ratio

        rows.append(row)

    qvalues = benjamini_hochberg([r["rank_score_p"] for r in rows])
    for row, q in zip(rows, qvalues):
        row["bh_q"] = q
        row["signif_flag"] = 1 if q < args.fdr else 0

    rows.sort(key=lambda r: (-r["fold"], r["gene_id"]))

    header = ENRICH_OUT_HEADER_ACCEL if have_accel else ENRICH_OUT_HEADER
    with smart_open_write(args.out) as fout:
        fout.write("\t".join(header) + "\n")
        for r in rows:
            fout.write("\t".join(_fmt_cell(r[k]) for k in header) + "\n")

    if args.stats:
        genes_pass_fdr = sum(1 for r in rows if r["signif_flag"] == 1)
        with smart_open_write(args.stats) as sf:
            sf.write("metric\tvalue\n")
            sf.write("p0\t{}\n".format(_fmt_cell(p0)))
            sf.write("total_core_bp\t{}\n".format(total_core_bp))
            sf.write("total_space\t{}\n".format(total_space))
            sf.write("genes_tested\t{}\n".format(len(rows)))
            sf.write("genes_pass_fdr\t{}\n".format(genes_pass_fdr))
            if have_accel:
                sf.write("p0_accel\t{}\n".format(_fmt_cell(p0_accel)))
                sf.write("total_accel_bp\t{}\n".format(total_accel_bp))

            sf.write("\n# top 20 theo fold\n")
            sf.write("\t".join(header) + "\n")
            for r in rows[:20]:
                sf.write("\t".join(_fmt_cell(r[k]) for k in header) + "\n")

            if have_accel:
                sf.write("\n# top 20 theo ca_ratio\n")
                ca_header = [
                    "gene_id", "gene_name", "bp_obs", "fold",
                    "accel_bp", "accel_fold", "ca_ratio",
                ]
                sf.write("\t".join(ca_header) + "\n")
                by_ca = sorted(rows, key=lambda r: (-r["ca_ratio"], r["gene_id"]))
                for r in by_ca[:20]:
                    sf.write("\t".join(_fmt_cell(r[k]) for k in ca_header) + "\n")

    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(
        prog="conserved_to_bulbul.py",
        description=(
            "Loi A2: vung bao ton 363 loai chim (toa do ga galGal4) -> toa do "
            "chao mao (Pycnonotus jocosus, GCA_013400435.1). 4 lenh con: "
            "merge, paf2bed, annotate, enrich. Chi dung Python 3.11 stdlib."
        ),
        epilog=(
            "Vi du:\n"
            "  merge    --in all.bed --out elements.bed --gap 10 --min-len 20 --stats merge_stats.tsv\n"
            "  paf2bed  --paf elements.paf --out bulbul_core.bed --unmapped unmapped.txt "
            "--stats map_stats.tsv --min-identity 0.70 --min-coverage 0.80\n"
            "  annotate --bed bulbul_core.bed --gff genomic.gff.gz --out core_annot.tsv "
            "--stats annot_stats.tsv\n"
            "  enrich   --annot core_annot.tsv --gff genomic.gff.gz "
            "--genome-size 1000000000 --out gene_enrichment.tsv --stats enrich_stats.tsv\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)
    add_merge_parser(sub)
    add_paf2bed_parser(sub)
    add_annotate_parser(sub)
    add_enrich_parser(sub)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
