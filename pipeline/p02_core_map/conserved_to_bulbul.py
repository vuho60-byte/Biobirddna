#!/usr/bin/env python3
"""conserved_to_bulbul.py -- loi A2: vung bao ton 363 loai chim (toa do ga
galGal4, tu ancRep_separate_models_rev.bw.conserved.bb) -> toa do bo gene
chao mao (Pycnonotus jocosus, GCA_013400435.1).

3 lenh con, chi dung Python 3.11 stdlib, xu ly theo luong (khong nap toan
bo dau vao vao bo nho tru khi noi ro):

  merge     BED 3 cot (bigBedToBed) -> gop khoang gan nhau -> BED 4 cot
  paf2bed   PAF (minimap2 -c) -> chon 1 hit tot nhat/query -> BED 6+
  annotate  BED (tu paf2bed) + GFF3.gz -> gan feature_class + gene

Xem README.md trong cung thu muc de biet chi tiet cot dau ra va gioi han.
"""

from __future__ import annotations

import argparse
import bisect
import gzip
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

    return gene_index, cds_index, exon_index


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


def cmd_annotate(args):
    gene_index, cds_index, exon_index = _load_gff(args.gff)

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
            sf.write("\ngene_id\tgene_name\tbp\n")
            for gene_id, bp in gene_bp.most_common(50):
                sf.write("{}\t{}\t{}\n".format(gene_id, gene_name_lookup.get(gene_id, ""), bp))

    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(
        prog="conserved_to_bulbul.py",
        description=(
            "Loi A2: vung bao ton 363 loai chim (toa do ga galGal4) -> toa do "
            "chao mao (Pycnonotus jocosus, GCA_013400435.1). 3 lenh con: "
            "merge, paf2bed, annotate. Chi dung Python 3.11 stdlib."
        ),
        epilog=(
            "Vi du:\n"
            "  merge    --in all.bed --out elements.bed --gap 10 --min-len 20 --stats merge_stats.tsv\n"
            "  paf2bed  --paf elements.paf --out bulbul_core.bed --unmapped unmapped.txt "
            "--stats map_stats.tsv --min-identity 0.70 --min-coverage 0.80\n"
            "  annotate --bed bulbul_core.bed --gff genomic.gff.gz --out core_annot.tsv "
            "--stats annot_stats.tsv\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)
    add_merge_parser(sub)
    add_paf2bed_parser(sub)
    add_annotate_parser(sub)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
