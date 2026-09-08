#!/usr/bin/env python3
"""short_elements.py -- loi X4: phan tu bao ton NGAN (<100 bp) chua can duoc
bang minimap2 (loi A2, xem conserved_to_bulbul.py) -> can lai bang LAST, doi
sang toa do bo gene chao mao, gop voi ket qua A2.

3 lenh con, chi dung Python 3.11 stdlib, xu ly theo luong khi hop ly:

  filter      elements.fa + elements.bed -> short.fa (chi giu phan tu ngan)
  maf2bed     MAF (lastal | last-split)  -> BED 6+ (cung dinh dang cot voi
              conserved_to_bulbul.py paf2bed, de ghep duoc voi bulbul_core.bed)
  merge-beds  >=1 BED 6+ -> 1 BED 6+ da gop, loai trung theo id query

Xem README.md trong cung thu muc de biet chi tiet cot dau ra va gioi han.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from contextlib import contextmanager

# ---------------------------------------------------------------------------
# Tien ich dung chung (nhan ban tu conserved_to_bulbul.py de giu file nay
# doc lap, khong import cheo giua cac module pipeline - dung quy uoc san co
# cua repo, xem pipeline/p02_core_map/conserved_to_bulbul.py)
# ---------------------------------------------------------------------------

LENGTH_BINS = [
    ("20_49", 20, 50),
    ("50_99", 50, 100),
    ("100_199", 100, 200),
    ("200_499", 200, 500),
    ("500_plus", 500, None),
]


def length_bin_label(length):
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
    if path == "-":
        yield sys.stdout
    else:
        f = open(path, "w", newline="", encoding="utf-8")
        try:
            yield f
        finally:
            f.close()


def _read_query_universe(path):
    """Doc danh sach toan bo ten query (--query-list, thuong la elements.bed).
    BED >=4 cot -> (id=cot4, length_hint=cot3-cot2); nguoc lai -> (token dau
    dong, length_hint=None). Giong het _read_query_universe cua paf2bed."""
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


# ---------------------------------------------------------------------------
# filter: elements.fa + elements.bed -> short.fa (chi giu phan tu ngan)
# ---------------------------------------------------------------------------


def add_filter_parser(sub):
    p = sub.add_parser(
        "filter",
        help="Loc phan tu ngan (do dai trong [--min-len, --max-len]) ra FASTA rieng cho LAST",
        description=(
            "Doc BED >=4 cot (--in-bed, cot 4 = id) de lay do dai chuan tung "
            "phan tu (end-start). Doc FASTA (--in-fa, header = id khop cot 4 "
            "BED, co the nhieu dong moi record) theo luong; ghi lai record co "
            "do dai trong [--min-len, --max-len] vao --out, giu nguyen noi "
            "dung/cach xuong dong cua tung dong trinh tu. Khong nap toan bo "
            "FASTA vao bo nho."
        ),
    )
    p.add_argument(
        "--in-fa",
        dest="in_fa",
        required=True,
        help="FASTA dau vao (header = id khop cot 4 --in-bed), hoac - de doc tu stdin",
    )
    p.add_argument(
        "--in-bed",
        dest="in_bed",
        required=True,
        help="BED >=4 cot dau vao (cot 4 = id; dung lam nguon do dai chuan, khong dem tu FASTA)",
    )
    p.add_argument(
        "--out",
        required=True,
        help="FASTA dau ra chi gom phan tu dat khoang do dai, hoac - de ghi ra stdout",
    )
    p.add_argument(
        "--max-len",
        dest="max_len",
        type=int,
        required=True,
        help="Do dai toi da (bp, bao gom ca gia tri nay) de giu phan tu",
    )
    p.add_argument(
        "--min-len",
        dest="min_len",
        type=int,
        default=20,
        help="Do dai toi thieu (bp, bao gom ca gia tri nay) de giu phan tu (mac dinh 20)",
    )
    p.add_argument(
        "--stats",
        default=None,
        help="Duong dan ghi thong ke TSV (bo qua neu khong truyen)",
    )
    p.set_defaults(func=cmd_filter)


def _read_bed_lengths(path):
    """Doc BED >=4 cot -> dict id -> do dai (end-start). BED la nguon do dai
    CHUAN (thay vi dem ky tu trong FASTA, tranh sai lech neu FASTA bi xuong
    dong/khoang trang khac thuong). Bao loi ro neu id lap lai (elements.bed
    tu A2 dat ten id = chrom:start-end nen phai duy nhat theo cau truc)."""
    lengths = {}
    with open(path, "r", newline="", encoding="utf-8") as f:
        for lineno, raw_line in enumerate(f, 1):
            line = raw_line.rstrip("\r\n")
            if not line:
                continue
            fields = line.split("\t")
            if len(fields) < 4:
                raise SystemExit(
                    "filter: dong {} cua --in-bed khong du 4 cot: {!r}".format(lineno, line)
                )
            try:
                start = int(fields[1])
                end = int(fields[2])
            except ValueError:
                raise SystemExit(
                    "filter: dong {} cua --in-bed start/end khong phai so nguyen: {!r}".format(
                        lineno, line
                    )
                )
            if end <= start:
                raise SystemExit(
                    "filter: dong {} cua --in-bed end <= start: {!r}".format(lineno, line)
                )
            name = fields[3]
            if name in lengths:
                raise SystemExit(
                    "filter: id {!r} xuat hien >1 lan trong --in-bed (dong {})".format(name, lineno)
                )
            lengths[name] = end - start
    return lengths


def _iter_fasta(fileobj):
    """Sinh (header_id, header_rest, seq_lines) tung record FASTA theo luong.
    header_id = token dau tien sau '>' (khop cot 4 BED); header_rest = phan
    con lai cua dong header (giu nguyen neu can ghi lai); seq_lines = danh
    sach cac dong trinh tu goc (giu nguyen do rong tung dong) cua record do."""
    header_id = None
    header_rest = ""
    seq_lines = []
    for raw_line in fileobj:
        line = raw_line.rstrip("\r\n")
        if line.startswith(">"):
            if header_id is not None:
                yield header_id, header_rest, seq_lines
            rest = line[1:]
            parts = rest.split(None, 1)
            header_id = parts[0] if parts else ""
            header_rest = parts[1] if len(parts) > 1 else ""
            seq_lines = []
        else:
            if header_id is None:
                if line == "":
                    continue
                raise SystemExit(
                    "filter: --in-fa co du lieu truoc dong header '>' dau tien"
                )
            seq_lines.append(line)
    if header_id is not None:
        yield header_id, header_rest, seq_lines


def cmd_filter(args):
    lengths = _read_bed_lengths(args.in_bed)

    total_in_fasta = 0
    kept = 0
    too_long = 0
    too_short = 0
    bp_kept = 0
    length_hist = Counter()

    with smart_open_read(args.in_fa) as fin, smart_open_write(args.out) as fout:
        for header_id, header_rest, seq_lines in _iter_fasta(fin):
            total_in_fasta += 1
            length = lengths.get(header_id)
            if length is None:
                raise SystemExit(
                    "filter: id {!r} co trong --in-fa nhung khong co trong --in-bed".format(
                        header_id
                    )
                )
            length_hist[length_bin_label(length)] += 1
            if length > args.max_len:
                too_long += 1
                continue
            if length < args.min_len:
                too_short += 1
                continue
            kept += 1
            bp_kept += length
            header_line = ">" + header_id + (" " + header_rest if header_rest else "")
            fout.write(header_line + "\n")
            for sline in seq_lines:
                fout.write(sline + "\n")

    if args.stats:
        with smart_open_write(args.stats) as sf:
            sf.write("metric\tvalue\n")
            sf.write("total_in_bed\t{}\n".format(len(lengths)))
            sf.write("total_in_fasta\t{}\n".format(total_in_fasta))
            sf.write("kept\t{}\n".format(kept))
            sf.write("excluded_too_long\t{}\n".format(too_long))
            sf.write("excluded_too_short\t{}\n".format(too_short))
            sf.write("bp_kept\t{}\n".format(bp_kept))
            sf.write("\nlength_bin\tcount\n")
            for label, _, _ in LENGTH_BINS:
                sf.write("{}\t{}\n".format(label, length_hist.get(label, 0)))
            if length_hist.get("lt_20", 0):
                sf.write("lt_20\t{}\n".format(length_hist["lt_20"]))

    return 0


# ---------------------------------------------------------------------------
# maf2bed: MAF (lastal | last-split) -> BED 6+ (cung dinh dang cot paf2bed)
# ---------------------------------------------------------------------------


def add_maf2bed_parser(sub):
    p = sub.add_parser(
        "maf2bed",
        help="Chon hit tot nhat moi query trong MAF LAST -> BED toa do chao mao",
        description=(
            "Doc MAF LAST (khoi 'a score=...' + 2 dong 's': dong 1 = target "
            "tu lastdb tren bo gene chao mao, dong 2 = query tu short.fa - "
            "phan tu ngan tren toa do ga). Voi moi query giu 1 hit tot nhat "
            "(uu tien score LAST, roi so base khop, roi do dai align). "
            "identity = base khop / do dai align (so cot cua khoi, ke ca "
            "gap); coverage = do dai query duoc gan trong khoi / do dai goc "
            "query. Xuat BED 6+ CUNG DINH DANG COT voi "
            "conserved_to_bulbul.py paf2bed (chrom,start,end,qname,score,"
            "strand,qlen,coverage,X) de merge-beds ghep duoc voi bulbul_core.bed; "
            "cot cuoi (X) la diem LAST tho lam tron (thay cho mapq cua PAF - "
            "LAST khong co khai niem mapq)."
        ),
    )
    p.add_argument(
        "--maf",
        required=True,
        help="File MAF dau vao (co the la nhieu manh da noi lai), hoac - de doc tu stdin",
    )
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
            "File liet ke toan bo ten query (vd elements.bed, cot 4). Neu co, "
            "query khong xuat hien trong MAF duoc bao no_hit va tinh vao mau "
            "so bang mapped_pct theo qlen_bin. Neu khong truyen, chi phat "
            "hien duoc low_identity/low_coverage."
        ),
    )
    p.set_defaults(func=cmd_maf2bed)


def _finalize_block(score, s_lines):
    """Kiem tra 1 khoi MAF da gom du: can dung 2 dong 's' hop le, co score,
    va 2 chuoi align cung do dai (bat buoc theo dinh nghia MAF - 2 dong cua
    1 khoi luon duoc dem cung so cot). Tra ve dict {'ok':True,'score':...,
    's1':...,'s2':...} hoac {'ok':False,'reason':...} - khong bao gio nem
    loi, de 1 khoi hong (file MAF that co the bi cat cut o cuoi, hoac thieu
    score=) khong lam sap ca lan xu ly hang chuc GB MAF."""
    if score is None:
        return {"ok": False, "reason": "missing_score"}
    real = [s for s in s_lines if s is not None]
    if len(s_lines) != 2 or len(real) != 2:
        return {"ok": False, "reason": "wrong_s_count"}
    s1, s2 = real
    if len(s1["text"]) != len(s2["text"]):
        return {"ok": False, "reason": "text_len_mismatch"}
    return {"ok": True, "score": score, "s1": s1, "s2": s2}


def _iter_maf_blocks(fileobj):
    """Sinh tung khoi MAF da qua _finalize_block (luon la dict co khoa 'ok').
    Khoi ket thuc khi gap dong trong hoac dong 'a' moi (phong file thieu dong
    trong ngan cach) hoac EOF. Dong bat dau bang ky tu khac 'a'/'s'/'#' (vd
    'i'/'e'/'q'/'p' - cac dong phu MAF/LAST co the ghi them trong 1 khoi)
    duoc bo qua nhung KHONG lam ket thuc khoi dang mo."""
    score = None
    s_lines = []
    pending = False

    for raw_line in fileobj:
        stripped = raw_line.rstrip("\r\n").strip()
        if stripped == "":
            if pending:
                yield _finalize_block(score, s_lines)
                score, s_lines, pending = None, [], False
            continue
        tag = stripped[0]
        if tag == "#":
            continue
        if tag == "a":
            if pending:
                yield _finalize_block(score, s_lines)
            score, s_lines, pending = None, [], True
            for tok in stripped.split():
                if tok.startswith("score="):
                    try:
                        score = float(tok[len("score="):])
                    except ValueError:
                        score = None
                    break
        elif tag == "s":
            pending = True
            fields = stripped.split()
            parsed = None
            if len(fields) == 7:
                _tag, src, start_s, size_s, strand, src_size_s, text = fields
                try:
                    start = int(start_s)
                    size = int(size_s)
                    src_size = int(src_size_s)
                except ValueError:
                    parsed = None
                else:
                    if strand in ("+", "-"):
                        parsed = {
                            "src": src,
                            "start": start,
                            "size": size,
                            "strand": strand,
                            "src_size": src_size,
                            "text": text,
                        }
            s_lines.append(parsed)
        else:
            # dong phu (i/e/q/p/...) - noi dung khong can cho maf2bed, giu
            # khoi dang mo va bo qua.
            pending = True
    if pending:
        yield _finalize_block(score, s_lines)


def _count_matches(text1, text2):
    """Dem so cot khop giua 2 chuoi align cung do dai (khong tinh cot co gap
    '-' o mot trong hai ben; so sanh khong phan biet hoa/thuong)."""
    matches = 0
    for c1, c2 in zip(text1, text2):
        if c1 != "-" and c2 != "-" and c1.upper() == c2.upper():
            matches += 1
    return matches


def _plus_strand_coords(start, size, strand, src_size):
    """Doi (start,size,strand) kieu MAF (start tinh theo mach `strand`) sang
    (begin,end) 0-based tren mach '+' - dung duoc thang cho cot 2/3 cua BED."""
    if strand == "+":
        return start, start + size
    end = src_size - start
    begin = end - size
    return begin, end


def cmd_maf2bed(args):
    best = {}
    hit_count = Counter()
    bad_block_reasons = Counter()
    blocks_total = 0

    with smart_open_read(args.maf) as fin:
        for block in _iter_maf_blocks(fin):
            blocks_total += 1
            if not block["ok"]:
                bad_block_reasons[block["reason"]] += 1
                continue

            score = block["score"]
            s1 = block["s1"]
            s2 = block["s2"]

            qname = s2["src"]
            qlen = s2["src_size"]
            matches = _count_matches(s1["text"], s2["text"])
            alnlen = len(s1["text"])
            identity = (matches / alnlen) if alnlen > 0 else 0.0
            coverage = (s2["size"] / qlen) if qlen > 0 else 0.0
            tstart, tend = _plus_strand_coords(
                s1["start"], s1["size"], s1["strand"], s1["src_size"]
            )
            rel_strand = "+" if s1["strand"] == s2["strand"] else "-"

            hit_count[qname] += 1
            rank_key = (score, matches, alnlen)
            prev = best.get(qname)
            if prev is None or rank_key > prev["rank_key"]:
                best[qname] = {
                    "rank_key": rank_key,
                    "tname": s1["src"],
                    "tstart": tstart,
                    "tend": tend,
                    "qname": qname,
                    "qlen": qlen,
                    "strand": rel_strand,
                    "last_score": score,
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
            score_col = max(0, min(1000, round(r["identity"] * 1000)))
            fout.write(
                "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{:.4f}\t{}\n".format(
                    r["tname"],
                    r["tstart"],
                    r["tend"],
                    r["qname"],
                    score_col,
                    r["strand"],
                    r["qlen"],
                    r["coverage"],
                    round(r["last_score"]),
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
            sf.write("blocks_total\t{}\n".format(blocks_total))
            sf.write("blocks_bad\t{}\n".format(sum(bad_block_reasons.values())))
            sf.write("total_queries\t{}\n".format(total_queries))
            sf.write("mapped\t{}\n".format(len(mapped_rows)))
            pct = (len(mapped_rows) / total_queries * 100) if total_queries else 0.0
            sf.write("mapped_pct\t{:.2f}\n".format(pct))
            sf.write("unmapped\t{}\n".format(len(unmapped_rows)))
            sf.write("second_hit_queries\t{}\n".format(second_hit_count))
            sf.write("\nbad_block_reason\tcount\n")
            for reason, cnt in bad_block_reasons.most_common():
                sf.write("{}\t{}\n".format(reason, cnt))
            sf.write("\nqlen_bin\tcount\n")
            for label, _, _ in LENGTH_BINS:
                sf.write("{}\t{}\n".format(label, length_hist.get(label, 0)))
            if length_hist.get("lt_20", 0):
                sf.write("lt_20\t{}\n".format(length_hist["lt_20"]))
            sf.write("\nidentity_bin\tcount\n")
            for label, _, _ in IDENTITY_BINS:
                sf.write("{}\t{}\n".format(label, identity_dist.get(label, 0)))
            sf.write("\nqlen_bin\tmapped\ttotal\tmapped_pct\n")
            bin_labels = [label for label, _, _ in LENGTH_BINS]
            if total_by_bin.get("lt_20", 0):
                bin_labels = bin_labels + ["lt_20"]
            for label in bin_labels:
                tot = total_by_bin.get(label, 0)
                mp = mapped_by_bin.get(label, 0)
                pct2 = (mp / tot * 100) if tot else 0.0
                sf.write("{}\t{}\t{}\t{:.2f}\n".format(label, mp, tot, pct2))

    return 0


# ---------------------------------------------------------------------------
# merge-beds: >=1 BED 6+ -> 1 BED 6+ da gop, loai trung theo id query
# ---------------------------------------------------------------------------


def add_merge_beds_parser(sub):
    p = sub.add_parser(
        "merge-beds",
        help="Gop nhieu BED 6+ (cung dinh dang cot paf2bed/maf2bed) loai trung theo id query",
        description=(
            "Doc >=1 file BED >=6 cot (--in, lap lai duoc nhieu lan) cung "
            "dinh dang cot voi paf2bed/maf2bed (cot 4 = id query, cot 5 = "
            "score 0-1000 tu identity). Voi id trung nhau (cung file hoac "
            "khac file), giu dong co score cao hon (bang diem thi giu dong "
            "gap truoc, de ket qua on dinh giua cac lan chay); ghi so id "
            "trung ra --stats."
        ),
    )
    p.add_argument(
        "--in",
        dest="in_paths",
        action="append",
        required=True,
        metavar="BED",
        help="BED 6+ dau vao, lap lai --in cho tung file (>=1 file)",
    )
    p.add_argument(
        "--out",
        required=True,
        help="BED 6+ dau ra da gop + loai trung, hoac - de ghi ra stdout",
    )
    p.add_argument("--stats", default=None, help="Duong dan ghi thong ke TSV")
    p.set_defaults(func=cmd_merge_beds)


def _read_bed6plus(path):
    rows = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        for lineno, raw_line in enumerate(f, 1):
            line = raw_line.rstrip("\r\n")
            if not line:
                continue
            fields = line.split("\t")
            if len(fields) < 6:
                raise SystemExit(
                    "merge-beds: {} dong {} khong du 6 cot BED: {!r}".format(
                        path, lineno, line
                    )
                )
            try:
                start = int(fields[1])
                score = int(fields[4])
            except ValueError:
                raise SystemExit(
                    "merge-beds: {} dong {} start/score khong phai so nguyen: {!r}".format(
                        path, lineno, line
                    )
                )
            rows.append({"fields": fields, "start": start, "score": score, "qname": fields[3]})
    return rows


def cmd_merge_beds(args):
    total_in = 0
    best = {}
    order = []
    per_source = []

    for path in args.in_paths:
        rows = _read_bed6plus(path)
        per_source.append((path, len(rows)))
        total_in += len(rows)
        for row in rows:
            qname = row["qname"]
            if qname not in best:
                order.append(qname)
                best[qname] = row
            elif row["score"] > best[qname]["score"]:
                best[qname] = row

    out_rows = [best[q] for q in order]
    out_rows.sort(key=lambda r: (r["fields"][0], r["start"]))

    with smart_open_write(args.out) as fout:
        for row in out_rows:
            fout.write("\t".join(row["fields"]) + "\n")

    duplicate_ids = total_in - len(order)

    if args.stats:
        with smart_open_write(args.stats) as sf:
            sf.write("metric\tvalue\n")
            sf.write("inputs\t{}\n".format(len(args.in_paths)))
            sf.write("total_rows_in\t{}\n".format(total_in))
            sf.write("unique_ids_out\t{}\n".format(len(order)))
            sf.write("duplicate_ids\t{}\n".format(duplicate_ids))
            sf.write("\nsource\trows\n")
            for path, n in per_source:
                sf.write("{}\t{}\n".format(path, n))

    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(
        prog="short_elements.py",
        description=(
            "Loi X4: phan tu bao ton ngan (<100 bp) -> can bang LAST -> BED "
            "toa do chao mao -> gop voi ket qua A2 (minimap2/paf2bed). 3 lenh "
            "con: filter, maf2bed, merge-beds. Chi dung Python 3.11 stdlib."
        ),
        epilog=(
            "Vi du:\n"
            "  filter     --in-fa elements.fa --in-bed elements.bed --out short.fa "
            "--max-len 99 --stats filter_stats.tsv\n"
            "  maf2bed    --maf aln.maf --out bulbul_short.bed --unmapped unmapped_short.txt "
            "--stats map_stats_short.tsv --min-identity 0.70 --min-coverage 0.80 "
            "--query-list elements.bed\n"
            "  merge-beds --in bulbul_core.bed --in bulbul_short.bed --out bulbul_core_all.bed "
            "--stats merge_beds_stats.tsv\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)
    add_filter_parser(sub)
    add_maf2bed_parser(sub)
    add_merge_beds_parser(sub)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
