#!/usr/bin/env python3
"""composition_scan.py -- loi X6: quet bat thuong thanh phan trong bo CDS
chao mao (Pycnonotus jocosus, GCA_013400435.1).

Cau hoi khoa hoc: chu du an dat gia thuyet bo gene chim co the chua doan
khong thuoc dong doi Trai Dat. Day la PHEP THU THAT cho gia thuyet do, va
no cung chinh la phuong phap chuan nganh de tim CHUYEN GENE NGANG (horizontal
gene transfer, HGT): mot doan DNA den tu nguon khac thuong mang CHU KY THANH
PHAN (thien lech GC, thien lech dung codon, pho k-mer) khac voi phan con lai
cua bo gene chu, vi moi dong doi co thien lech rieng.

Logic phep thu (xem README.md muc "Thu tu kha nang giai thich" de biet day
du): KHONG tim thay doan lech chuan -> bang chung CHONG LAI gia thuyet "co
doan ngoai lai", van la ket qua co gia tri. CO doan lech chuan -> phai kiem
theo dung thu tu: (1) loi lap rap/nhiem ban mau, (2) vung lap/transposon,
(3) HGT tu vi khuan/virus/sinh vat cong sinh (da duoc ghi nhan o nhieu loai),
(4) chi khi loai het moi ban toi kha nang khac.

3 lenh con, chi dung Python 3.11 stdlib. Buoc doc FASTA xu ly theo luong
(khong nap ca tep .fna.gz vao bo nho, chi giu 1 record tai 1 thoi diem):

  profile   CDS FASTA(.gz) -> moi trinh tu: do dai, GC, GC3, tan so 64 codon,
            tan so 256 4-mer (chuan hoa, tong = 1) -> profile.tsv
  outliers  profile.tsv (2 luot doc) -> z-score GC/GC3, khoang cach
            Mahalanobis XAP XI tren vector codon, phan ky Jensen-Shannon
            tren vector 4-mer so voi ho so nen toan bo gene -> danh dau khi
            >= 2 trong 3 thuoc do vuot nguong --z -> outliers.tsv + stats
  report    outliers.tsv -> bao cao Markdown top N trinh tu lech nhat, kem
            cot trong 'giai_thich_kha_di' va PHAN CANH BAO BAT BUOC

QUAN TRONG: day la CONG CU SANG LOC TIN HIEU, khong phai cong cu KET LUAN.
Xem README.md truoc khi dung ket qua cho bat ky phat bieu nao.
"""

from __future__ import annotations

import argparse
import gzip
import itertools
import math
import re
import statistics
import sys
from collections import Counter, namedtuple
from contextlib import contextmanager

# ---------------------------------------------------------------------------
# Tien ich dung chung (doc/ghi streaming, giong quy uoc pipeline/p02_core_map)
# ---------------------------------------------------------------------------


@contextmanager
def smart_open_read(path):
    """Mo doc: '-' = stdin. newline='' de tu xu ly CRLF/LF, dong 'r' +
    rstrip('\\r\\n') o noi goi."""
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
    """Mo ghi: '-' = stdout. newline='' de ghi LF thuan tuy tren moi he
    dieu hanh."""
    if path == "-":
        yield sys.stdout
    else:
        f = open(path, "w", newline="", encoding="utf-8")
        try:
            yield f
        finally:
            f.close()


def _fmt_cell(value):
    """Dinh dang 1 gia tri cho dong TSV: float -> 6 chu so co nghia, con
    lai -> str() thuong (giu nguyen so nguyen, khong them .0)."""
    if isinstance(value, float):
        return "{:.6g}".format(value)
    return str(value)


# ---------------------------------------------------------------------------
# Bang k-mer co dinh (thu tu tu dien tren bang chu A,C,G,T)
# ---------------------------------------------------------------------------

BASES = "ACGT"
ALL_CODONS = ["".join(t) for t in itertools.product(BASES, repeat=3)]  # 64
ALL_4MERS = ["".join(t) for t in itertools.product(BASES, repeat=4)]  # 256
CODON_COLUMNS = ["cod_" + c for c in ALL_CODONS]
KMER_COLUMNS = ["k4_" + k for k in ALL_4MERS]
PROFILE_HEADER = ["seq_id", "gene", "len", "gc", "gc3"] + CODON_COLUMNS + KMER_COLUMNS


# ---------------------------------------------------------------------------
# profile: CDS FASTA(.gz) -> do dai/GC/GC3/tan so codon/tan so 4-mer
# ---------------------------------------------------------------------------

_HEADER_ATTR_RE = re.compile(r"\[(\w+)=([^\[\]]*)\]")


def _parse_header_gene(header_rest):
    """Lay gia tri [gene=...] tu phan con lai cua dong header FASTA (sau
    token dau tien). Header CDS cua NCBI ghi dang '[key=value] [key2=..]'
    (vd '[gene=Efcc1] [locus_tag=..] [protein=..]'). Tra ve '' neu khong
    thay the gene."""
    for key, value in _HEADER_ATTR_RE.findall(header_rest):
        if key == "gene":
            return value
    return ""


def _iter_fasta(fileobj):
    """Sinh (seq_id, gene, sequence) tung record theo luong. Chi giu 1
    record (danh sach cac dong trinh tu goc cua record do) trong bo nho tai
    1 thoi diem -- khong nap ca tep .fna.gz vao bo nho (giong _iter_fasta
    cua pipeline/p02b_last/short_elements.py). seq_id = token dau tien sau
    '>' (vd 'lcl|VWYP01000003.1_cds_NXR70914.1_1')."""
    seq_id = None
    gene = ""
    chunks = []
    for raw_line in fileobj:
        line = raw_line.rstrip("\r\n")
        if not line:
            continue
        if line[0] == ">":
            if seq_id is not None:
                yield seq_id, gene, "".join(chunks)
            rest = line[1:]
            parts = rest.split(None, 1)
            seq_id = parts[0] if parts else ""
            gene = _parse_header_gene(parts[1] if len(parts) > 1 else "")
            chunks = []
        else:
            if seq_id is None:
                raise SystemExit(
                    "profile: --fasta co du lieu truoc dong header '>' dau tien"
                )
            chunks.append(line)
    if seq_id is not None:
        yield seq_id, gene, "".join(chunks)


def _composition_stats(seq):
    """Tra ve (gc, gc3, codon_freq[64 theo thu tu ALL_CODONS], kmer_freq
    [256 theo thu tu ALL_4MERS]) cho 1 trinh tu CDS (da uppercase o noi
    goi). Codon doc theo khung doc tu vi tri 0 (khong bu offset cho CDS
    'partial=5\\'' -- xem gioi han trong README.md). Chi dem base A/C/G/T
    hop le; codon/k-mer chua ky tu khac (N, IUPAC mo ho...) bi bo qua hoan
    toan khoi tu so LAN mau so cua chinh don vi do (khong lam sai lech cac
    don vi con lai). Neu mau so = 0 (trinh tu suy bien/toan N), tra tan so
    0.0 cho ca chieu -- truong hop hiem, khong crash."""
    length = len(seq)

    valid_bases = 0
    gc_bases = 0
    for ch in seq:
        if ch in "ACGT":
            valid_bases += 1
            if ch in "GC":
                gc_bases += 1
    gc = (gc_bases / valid_bases) if valid_bases else 0.0

    codon_counts = {c: 0 for c in ALL_CODONS}
    n_valid_codons = 0
    gc3_hits = 0
    n_codon_slots = length // 3
    for i in range(0, n_codon_slots * 3, 3):
        codon = seq[i : i + 3]
        if codon in codon_counts:  # chi True khi ca 3 ky tu deu A/C/G/T
            codon_counts[codon] += 1
            n_valid_codons += 1
            if codon[2] in "GC":
                gc3_hits += 1
    gc3 = (gc3_hits / n_valid_codons) if n_valid_codons else 0.0
    codon_freq = [
        (codon_counts[c] / n_valid_codons) if n_valid_codons else 0.0 for c in ALL_CODONS
    ]

    kmer_counts = {k: 0 for k in ALL_4MERS}
    n_valid_kmers = 0
    for i in range(length - 3):
        kmer = seq[i : i + 4]
        if kmer in kmer_counts:
            kmer_counts[kmer] += 1
            n_valid_kmers += 1
    kmer_freq = [
        (kmer_counts[k] / n_valid_kmers) if n_valid_kmers else 0.0 for k in ALL_4MERS
    ]

    return gc, gc3, codon_freq, kmer_freq


def add_profile_parser(sub):
    p = sub.add_parser(
        "profile",
        help="Tinh do dai/GC/GC3/tan so codon/tan so 4-mer cho tung trinh tu CDS",
        description=(
            "Doc CDS FASTA(.gz) theo luong (khong nap ca tep vao bo nho, chi "
            "giu 1 record tai 1 thoi diem). Voi moi trinh tu dai >= --min-len: "
            "do dai, GC, GC3 (GC o vi tri codon thu 3), tan so 64 codon va tan "
            "so 256 4-mer (moi tan so tu chuan hoa, tong = 1 tren tap hop le). "
            "Ghi profile.tsv (1 dong header + 1 dong/trinh tu)."
        ),
    )
    p.add_argument(
        "--fasta",
        required=True,
        help="CDS FASTA hoac FASTA.gz dau vao (vd *_cds_from_genomic.fna.gz)",
    )
    p.add_argument("--out", required=True, help="profile.tsv dau ra, hoac - de ghi ra stdout")
    p.add_argument(
        "--min-len",
        dest="min_len",
        type=int,
        default=300,
        help="Bo qua trinh tu ngan hon N bp (mac dinh 300)",
    )
    p.set_defaults(func=cmd_profile)


def cmd_profile(args):
    opener = gzip.open if args.fasta.endswith(".gz") else open
    with opener(args.fasta, "rt", encoding="utf-8", errors="replace") as fin, smart_open_write(
        args.out
    ) as fout:
        fout.write("\t".join(PROFILE_HEADER) + "\n")
        for seq_id, gene, raw_seq in _iter_fasta(fin):
            seq = raw_seq.upper()
            length = len(seq)
            if length < args.min_len:
                continue
            gc, gc3, codon_freq, kmer_freq = _composition_stats(seq)
            row = [seq_id, gene, length, gc, gc3] + codon_freq + kmer_freq
            fout.write("\t".join(_fmt_cell(v) for v in row) + "\n")

    return 0


# ---------------------------------------------------------------------------
# outliers: profile.tsv -> z-score GC/GC3 + Mahalanobis xap xi (codon) +
#           Jensen-Shannon (4-mer) so voi ho so nen -> danh dau >= 2/3
# ---------------------------------------------------------------------------

ProfileRow = namedtuple(
    "ProfileRow", ["seq_id", "gene", "length", "gc", "gc3", "codon_freq", "kmer_freq"]
)

OUTLIERS_HEADER = [
    "seq_id",
    "gene",
    "len",
    "gc",
    "gc3",
    "z_gc",
    "z_gc3",
    "codon_dist",
    "kmer_js",
    "n_flags",
]


def _iter_profile_rows(path):
    """Sinh ProfileRow tung dong tu profile.tsv. Tra cuu cot theo TEN (khong
    theo vi tri) nen thu tu cot trong file khong quan trong. Goi ham nay 2
    LAN (2 luot doc) trong cmd_outliers -- vi vay 'path' phai la duong dan
    file mo lai duoc, KHONG duoc la '-' (stdin khong doc lai lan 2 duoc)."""
    with smart_open_read(path) as f:
        header_line = f.readline()
        if not header_line:
            raise SystemExit("outliers: --profile rong (khong co dong header)")
        header = header_line.rstrip("\r\n").split("\t")
        idx = {name: i for i, name in enumerate(header)}
        required = ["seq_id", "gene", "len", "gc", "gc3"] + CODON_COLUMNS + KMER_COLUMNS
        missing = [c for c in required if c not in idx]
        if missing:
            raise SystemExit(
                "outliers: --profile thieu cot {} (dung dung file do lenh "
                "'profile' xuat ra chua?)".format(missing[:5])
            )
        for lineno, raw_line in enumerate(f, 2):
            line = raw_line.rstrip("\r\n")
            if not line:
                continue
            fields = line.split("\t")
            try:
                yield ProfileRow(
                    seq_id=fields[idx["seq_id"]],
                    gene=fields[idx["gene"]],
                    length=int(fields[idx["len"]]),
                    gc=float(fields[idx["gc"]]),
                    gc3=float(fields[idx["gc3"]]),
                    codon_freq=[float(fields[idx[c]]) for c in CODON_COLUMNS],
                    kmer_freq=[float(fields[idx[k]]) for k in KMER_COLUMNS],
                )
            except (ValueError, IndexError) as e:
                raise SystemExit(
                    "outliers: dong {} cua --profile khong doc duoc: {!r} ({})".format(
                        lineno, line[:80], e
                    )
                )


def approx_mahalanobis(x, mean, var):
    """Khoang cach Mahalanobis XAP XI: dung PHUONG SAI TUNG CHIEU (duong
    cheo ma tran hiep phuong sai), KHONG dung ma tran hiep phuong sai day du
    (bo qua tuong quan giua cac chieu) -- dung nhu brief X6 yeu cau, va day
    LA XAP XI, khong phai Mahalanobis chuan. Chieu co phuong sai = 0 (khong
    bien thien trong nen) dong gop 0 vao tong, tranh chia cho 0."""
    total = 0.0
    for xi, mi, vi in zip(x, mean, var):
        if vi > 0.0:
            diff = xi - mi
            total += (diff * diff) / vi
    return math.sqrt(total)


def _kl_divergence_log2(p, m):
    """KL(p || m), log co so 2 (don vi bit). Quy uoc 0*log(0)=0. p, m phai
    da chuan hoa (tong = 1)."""
    total = 0.0
    for pi, mi in zip(p, m):
        if pi > 0.0:
            total += pi * math.log(pi / mi, 2)
    return total


def jensen_shannon_divergence(p, q):
    """Phan ky Jensen-Shannon giua 2 phan phoi roi rac p, q (cung do dai).
    Tu chuan hoa lai theo tong (phong truong hop dau vao chua chuan hoa het
    do lam tron float). Dung log co so 2 nen ket qua nam trong [0, 1] (don
    vi bit): JS(p,p)=0, JS doi xung theo p/q, JS([1,0,..],[0,1,..])=1 (max).
    Tu cai dat bang math.log (KHONG dung numpy/scipy) theo dung yeu cau
    brief X6. Neu 1 trong 2 phia co tong = 0 (khong co du lieu hop le) ->
    tra 0.0 (khong so sanh duoc, coi nhu khong lech)."""
    n = len(p)
    sp = sum(p)
    sq = sum(q)
    if sp <= 0.0 or sq <= 0.0:
        return 0.0
    pn = [x / sp for x in p]
    qn = [x / sq for x in q]
    m = [(pn[i] + qn[i]) / 2.0 for i in range(n)]
    return 0.5 * _kl_divergence_log2(pn, m) + 0.5 * _kl_divergence_log2(qn, m)


def _percentile(sorted_vals, pct):
    """Phan vi noi suy tuyen tinh (giong phuong phap mac dinh cua
    numpy.percentile) tren danh sach DA SAP XEP TANG DAN. pct trong [0,100]."""
    n = len(sorted_vals)
    if n == 0:
        return 0.0
    if n == 1:
        return sorted_vals[0]
    rank = (pct / 100.0) * (n - 1)
    lo = int(math.floor(rank))
    hi = int(math.ceil(rank))
    if lo == hi:
        return sorted_vals[lo]
    frac = rank - lo
    return sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac


def add_outliers_parser(sub):
    p = sub.add_parser(
        "outliers",
        help="z-score GC/GC3 + Mahalanobis xap xi (codon) + Jensen-Shannon (4-mer); danh dau khi >=2/3 vuot --z",
        description=(
            "Doc profile.tsv (tu lenh 'profile'), 2 luot: luot 1 tinh trung "
            "binh/phuong sai TOAN CUC (tren toan bo trinh tu trong file) cho "
            "GC, GC3 va 64 chieu tan so codon, va ho so 4-mer nen (trung binh "
            "khong trong so cua vector tan so 4-mer moi trinh tu). Luot 2 "
            "tinh cho TUNG trinh tu: z_gc, z_gc3, khoang cach Mahalanobis xap "
            "xi tren vector codon (codon_dist), phan ky Jensen-Shannon tren "
            "vector 4-mer so voi ho so nen (kmer_js). Danh dau bat thuong khi "
            ">= 2 trong 3 thuoc do (GC/GC3, codon, 4-mer) vuot nguong --z -- "
            "xem README.md muc 'Quy uoc danh dau' de biet chinh xac cach quy "
            "doi codon_dist/kmer_js ve don vi z. DAY LA SANG LOC TIN HIEU, "
            "khong phai KET LUAN."
        ),
    )
    p.add_argument(
        "--profile",
        required=True,
        help="profile.tsv dau vao (tu lenh 'profile'); phai la duong dan file that (doc 2 luot, khong nhan '-')",
    )
    p.add_argument("--out", required=True, help="outliers.tsv dau ra, hoac - de ghi ra stdout")
    p.add_argument(
        "--stats",
        required=True,
        help="outlier_stats.tsv: trung binh/do lech chuan toan cuc, so trinh tu xet, so bat thuong theo muc co, phan vi 50/90/99",
    )
    p.add_argument(
        "--z",
        type=float,
        default=4.0,
        help="Nguong z de tinh 1 thuoc do la vuot nguong (mac dinh 4.0)",
    )
    p.set_defaults(func=cmd_outliers)


def cmd_outliers(args):
    if args.profile == "-":
        raise SystemExit("outliers: --profile khong duoc la '-' (stdin) vi can doc 2 luot")

    n_codon_dims = len(ALL_CODONS)
    n_kmer_dims = len(ALL_4MERS)

    # Luot 1: tich luy tong/tong-binh-phuong toan cuc cho gc, gc3, tung
    # chieu cua vector tan so codon (can cho Mahalanobis xap xi), va tong
    # (chi can trung binh) cho vector tan so 4-mer (ho so nen). KHONG giu
    # ca 320 cot dau vao cua moi trinh tu trong bo nho cung luc.
    n = 0
    sum_gc = sum_gc2 = 0.0
    sum_gc3 = sum_gc3_2 = 0.0
    sum_cod = [0.0] * n_codon_dims
    sum_cod2 = [0.0] * n_codon_dims
    sum_kmer = [0.0] * n_kmer_dims

    for row in _iter_profile_rows(args.profile):
        n += 1
        sum_gc += row.gc
        sum_gc2 += row.gc * row.gc
        sum_gc3 += row.gc3
        sum_gc3_2 += row.gc3 * row.gc3
        for i, v in enumerate(row.codon_freq):
            sum_cod[i] += v
            sum_cod2[i] += v * v
        for i, v in enumerate(row.kmer_freq):
            sum_kmer[i] += v

    if n == 0:
        raise SystemExit("outliers: --profile khong co trinh tu nao (rong sau dong header)")

    mean_gc = sum_gc / n
    var_gc = max(sum_gc2 / n - mean_gc * mean_gc, 0.0)
    std_gc = math.sqrt(var_gc)

    mean_gc3 = sum_gc3 / n
    var_gc3 = max(sum_gc3_2 / n - mean_gc3 * mean_gc3, 0.0)
    std_gc3 = math.sqrt(var_gc3)

    mean_cod = [s / n for s in sum_cod]
    var_cod = [max(sum_cod2[i] / n - mean_cod[i] * mean_cod[i], 0.0) for i in range(n_codon_dims)]

    mean_kmer_raw = [s / n for s in sum_kmer]
    kmer_total = sum(mean_kmer_raw)
    if kmer_total > 0.0:
        mean_kmer = [v / kmer_total for v in mean_kmer_raw]
    else:
        mean_kmer = mean_kmer_raw

    # Luot 2: doc lai profile.tsw TU DAU, tinh codon_dist/kmer_js/z_gc/z_gc3
    # tung trinh tu. Chi giu lai ket qua RUT GON (9 gia tri/trinh tu) trong
    # bo nho, khong giu lai 320 cot dau vao.
    rows = []
    for row in _iter_profile_rows(args.profile):
        z_gc = (row.gc - mean_gc) / std_gc if std_gc > 0.0 else 0.0
        z_gc3 = (row.gc3 - mean_gc3) / std_gc3 if std_gc3 > 0.0 else 0.0
        codon_dist = approx_mahalanobis(row.codon_freq, mean_cod, var_cod)
        kmer_js = jensen_shannon_divergence(row.kmer_freq, mean_kmer)
        rows.append(
            {
                "seq_id": row.seq_id,
                "gene": row.gene,
                "len": row.length,
                "gc": row.gc,
                "gc3": row.gc3,
                "z_gc": z_gc,
                "z_gc3": z_gc3,
                "codon_dist": codon_dist,
                "kmer_js": kmer_js,
            }
        )

    # QUY UOC DANH DAU (gia dinh ro rang cua script -- brief khong noi ro
    # cach quy doi codon_dist/kmer_js ve "don vi z"; so sanh THO voi --z se
    # khien kmer_js, vi bi chan trong [0,1], khong bao gio vuot nguong mac
    # dinh 4.0). O day:
    #   - do GC/GC3 co the lech CA 2 PHIA (qua cao hoac qua thap deu la
    #     thanh phan la), dung |z_gc| hoac |z_gc3| >= --z (2 phia).
    #   - codon_dist va kmer_js la KHOANG CACH KHONG AM (chi huong "cao hon
    #     = khac nen hon" la dang chu y), nen tu tinh z-score CUA CHINH cac
    #     gia tri codon_dist/kmer_js tren toan quan the trinh tu dang xet,
    #     roi dung MOT PHIA (z_codon >= --z, z_kmer >= --z).
    #   - CHU Y: quan the dung de tinh trung binh/do lech chuan bao gom CA
    #     cac trinh tu se bi danh dau (khong loai outlier truoc khi tinh
    #     nen) -- neu co RAT NHIEU outlier cung huong, do lech chuan se bi
    #     thoi phong va lam giam do nhay. Xem gioi han trong README.md.
    cd_vals = [r["codon_dist"] for r in rows]
    js_vals = [r["kmer_js"] for r in rows]
    mean_cd = statistics.fmean(cd_vals)
    std_cd = statistics.pstdev(cd_vals) if len(cd_vals) > 1 else 0.0
    mean_js = statistics.fmean(js_vals)
    std_js = statistics.pstdev(js_vals) if len(js_vals) > 1 else 0.0

    n_flag_hist = Counter()
    for r in rows:
        z_codon = (r["codon_dist"] - mean_cd) / std_cd if std_cd > 0.0 else 0.0
        z_kmer = (r["kmer_js"] - mean_js) / std_js if std_js > 0.0 else 0.0
        flag_gc = 1 if (abs(r["z_gc"]) >= args.z or abs(r["z_gc3"]) >= args.z) else 0
        flag_codon = 1 if z_codon >= args.z else 0
        flag_kmer = 1 if z_kmer >= args.z else 0
        r["n_flags"] = flag_gc + flag_codon + flag_kmer
        n_flag_hist[r["n_flags"]] += 1

    rows.sort(key=lambda r: (-r["n_flags"], -r["kmer_js"]))

    with smart_open_write(args.out) as fout:
        fout.write("\t".join(OUTLIERS_HEADER) + "\n")
        for r in rows:
            fout.write("\t".join(_fmt_cell(r[k]) for k in OUTLIERS_HEADER) + "\n")

    with smart_open_write(args.stats) as sf:
        sf.write("metric\tvalue\n")
        sf.write("n_sequences\t{}\n".format(n))
        sf.write("z_threshold\t{}\n".format(_fmt_cell(args.z)))
        sf.write("mean_gc\t{}\n".format(_fmt_cell(mean_gc)))
        sf.write("std_gc\t{}\n".format(_fmt_cell(std_gc)))
        sf.write("mean_gc3\t{}\n".format(_fmt_cell(mean_gc3)))
        sf.write("std_gc3\t{}\n".format(_fmt_cell(std_gc3)))
        sf.write("mean_codon_dist\t{}\n".format(_fmt_cell(mean_cd)))
        sf.write("std_codon_dist\t{}\n".format(_fmt_cell(std_cd)))
        sf.write("mean_kmer_js\t{}\n".format(_fmt_cell(mean_js)))
        sf.write("std_kmer_js\t{}\n".format(_fmt_cell(std_js)))
        sf.write("\nn_flags\tcount\n")
        for level in (0, 1, 2, 3):
            sf.write("{}\t{}\n".format(level, n_flag_hist.get(level, 0)))
        sf.write("\nmeasure\tp50\tp90\tp99\n")
        for label, vals in (
            ("z_gc", [r["z_gc"] for r in rows]),
            ("z_gc3", [r["z_gc3"] for r in rows]),
            ("codon_dist", cd_vals),
            ("kmer_js", js_vals),
        ):
            s = sorted(vals)
            p50, p90, p99 = (_percentile(s, 50), _percentile(s, 90), _percentile(s, 99))
            sf.write(
                "{}\t{}\t{}\t{}\n".format(
                    label, _fmt_cell(p50), _fmt_cell(p90), _fmt_cell(p99)
                )
            )

    return 0


# ---------------------------------------------------------------------------
# report: outliers.tsv -> bao cao Markdown top N + canh bao bat buoc
# ---------------------------------------------------------------------------

REPORT_WARNING = """## CANH BAO BAT BUOC -- doc truoc khi dien `giai_thich_kha_di`

**Moi ket qua trong bao cao nay la TIN HIEU CAN KIEM TIEP, khong phai KET LUAN.**
Mot trinh tu bi danh dau bat thuong thanh phan CHUA chung minh no den tu
ngoai Trai Dat hay khong thuoc dong doi to tien -- no chi co nghia la thanh
phan (GC/GC3, codon, hoac 4-mer) cua trinh tu do khac ho so nen cua bo CDS
chao mao hon nguong thong ke da chon (`--z`).

Thu tu kha nang giai thich BAT BUOC phai kiem theo dung thu tu sau day (chi
chuyen sang muc tiep theo SAU KHI da loai duoc muc truoc):

1. **Loi lap rap hoac nhiem ban mau** (assembly error / sample contamination)
   -- kha nang PHO BIEN NHAT cho 1 outlier don le trong 1 ban lap rap muc do
   scaffold (N50 thap).
2. **Vung lap / transposon** (repeat region / transposable element) -- cac
   yeu to lap thuong tu mang thanh phan/pho k-mer khac han gene ma hoa binh
   thuong.
3. **HGT (chuyen gene ngang) tu vi khuan, virus, hoac sinh vat cong sinh** --
   day la hien tuong DA DUOC GHI NHAN o nhieu loai (khong phai gia thuyet
   moi la), va la kha nang ĐUOC XEP CUOI trong 3 kha nang "thong thuong".
4. Chi khi da loai het (1)-(3) moi ban toi kha nang khac. Bang nay KHONG TU
   DONG loai duoc bat ky muc nao trong 4 muc tren -- nguoi doc phai tu kiem.

**Buoc kiem bat buoc tiep theo (CHUA lam trong du an nay):** so sanh tung
trinh tu bi danh dau voi co so du lieu protein toan cau bang BLAST hoac
DIAMOND (vd so voi nr/UniProt). Trinh tu khop manh voi protein vi khuan/virus
va KHONG khop protein chim khac -> ung ho (3); nam trong vung da biet la
transposon/lap -> ung ho (2); chi xuat hien o scaffold ngan/do phu thap ->
uu tien xem xet (1) truoc.

Gioi han phuong phap (xem `pipeline/p04_anomaly/README.md`): cach nay KHONG
phat hien duoc doan da bi "dong hoa" thanh phan qua thoi gian tien hoa, va
CHUA doi chieu voi bat ky co so du lieu protein/nucleotide ben ngoai nao.
"""


def add_report_parser(sub):
    p = sub.add_parser(
        "report",
        help="Xuat bao cao Markdown top N trinh tu lech nhat + canh bao bat buoc",
        description=(
            "Doc outliers.tsv (tu lenh 'outliers'), tu sap xep lai theo dung "
            "quy uoc (n_flags giam dan roi kmer_js giam dan) va xuat --top "
            "trinh tu dau thanh bang Markdown, kem cot trong 'giai_thich_kha_di' "
            "de nguoi dien, VA PHAN CANH BAO BAT BUOC ve thu tu kha nang giai "
            "thich + buoc kiem tiep theo (BLAST/DIAMOND, chua lam trong du an)."
        ),
    )
    p.add_argument("--outliers", required=True, help="outliers.tsv dau vao (tu lenh 'outliers')")
    p.add_argument(
        "--top", type=int, default=50, help="So trinh tu lech nhat dua vao bao cao (mac dinh 50)"
    )
    p.add_argument("--out", required=True, help="report.md dau ra, hoac - de ghi ra stdout")
    p.set_defaults(func=cmd_report)


def cmd_report(args):
    header = None
    rows = []
    with smart_open_read(args.outliers) as f:
        for raw_line in f:
            line = raw_line.rstrip("\r\n")
            if not line:
                continue
            fields = line.split("\t")
            if header is None:
                header = fields
                continue
            rows.append(fields)

    if header is None:
        raise SystemExit("report: --outliers rong (khong co dong header)")

    idx = {name: i for i, name in enumerate(header)}
    missing = [c for c in OUTLIERS_HEADER if c not in idx]
    if missing:
        raise SystemExit(
            "report: --outliers thieu cot {} (dung file do lenh 'outliers' xuat ra chua?)".format(
                missing
            )
        )

    # Tu sap xep lai theo dung quy uoc cua lenh 'outliers' (khong am tham
    # tin tuong thu tu co san trong file -- xem SURGICAL-CHANGE/robustness).
    rows.sort(key=lambda r: (-int(r[idx["n_flags"]]), -float(r[idx["kmer_js"]])))

    top_rows = rows[: args.top]
    n_flagged = sum(1 for r in rows if int(r[idx["n_flags"]]) >= 1)

    lines = []
    lines.append(
        "# Bao cao quet bat thuong thanh phan -- top {} trinh tu lech nhat".format(len(top_rows))
    )
    lines.append("")
    lines.append(
        "Nguon: `{}` -- {} trinh tu duoc xet, {} trinh tu bi danh dau >= 1 co, "
        "hien {} dong dau (sap theo n_flags roi kmer_js giam dan).".format(
            args.outliers, len(rows), n_flagged, len(top_rows)
        )
    )
    lines.append("")
    lines.append(REPORT_WARNING)
    lines.append(
        "| seq_id | gene | len | gc | gc3 | z_gc | z_gc3 | codon_dist | kmer_js | n_flags | giai_thich_kha_di |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    display_cols = ["seq_id", "gene", "len", "gc", "gc3", "z_gc", "z_gc3", "codon_dist", "kmer_js", "n_flags"]
    for r in top_rows:
        cells = [r[idx[c]] for c in display_cols]
        lines.append("| " + " | ".join(cells) + " |  |")
    lines.append("")

    with smart_open_write(args.out) as fout:
        fout.write("\n".join(lines) + "\n")

    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(
        prog="composition_scan.py",
        description=(
            "Loi X6: quet bat thuong thanh phan trong CDS chao mao -- phep "
            "thu cho gia thuyet 'doan DNA la' + phuong phap chuan de tim HGT "
            "(chuyen gene ngang). 3 lenh con: profile, outliers, report. Chi "
            "dung Python 3.11 stdlib. KET QUA LA TIN HIEU CAN KIEM TIEP, "
            "KHONG PHAI KET LUAN -- xem README.md."
        ),
        epilog=(
            "Vi du:\n"
            "  profile  --fasta cds_from_genomic.fna.gz --out profile.tsv --min-len 300\n"
            "  outliers --profile profile.tsv --out outliers.tsv --stats outlier_stats.tsv --z 4.0\n"
            "  report   --outliers outliers.tsv --top 50 --out report.md\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)
    add_profile_parser(sub)
    add_outliers_parser(sub)
    add_report_parser(sub)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
