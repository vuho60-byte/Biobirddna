"""Unit test cho composition_scan.py -- unittest thuan, khong pytest, du lieu
nhung ngay trong file (khong doc/ghi ngoai thu muc tam cua test).

Chay: python -B -m unittest discover -s pipeline/p04_anomaly/tests -v
"""

import gzip
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import composition_scan as cs  # noqa: E402


def read_text(path):
    with open(path, "r", newline="", encoding="utf-8") as f:
        return f.read()


def write_text(path, content):
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(content)


class TempDirMixin:
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="cs_test_")
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def path(self, name):
        return os.path.join(self.tmp, name)


def tsv_rows(text):
    """Tach 1 khoi TSV (header + du lieu) thanh (header_list, [row_dict,...])."""
    lines = [ln for ln in text.splitlines() if ln != ""]
    header = lines[0].split("\t")
    rows = []
    for ln in lines[1:]:
        fields = ln.split("\t")
        rows.append(dict(zip(header, fields)))
    return header, rows


# ---------------------------------------------------------------------------
# _composition_stats (don vi, khong qua CLI)
# ---------------------------------------------------------------------------


class TestCompositionStats(unittest.TestCase):
    def test_gc_and_gc3_known_sequence(self):
        # 10x "AGG" (A,G,G -> 2/3 GC, vi tri 3 = G la GC) xen 10x "TTA"
        # (T,T,A -> 0/3 GC, vi tri 3 = A khong phai GC).
        # Tong base GC = 10*2 + 10*0 = 20 / 60 base = 1/3.
        # Tong codon co GC o vi tri 3 = 10 (AGG) + 0 (TTA) = 10/20 = 0.5.
        seq = ("AGG" + "TTA") * 10
        gc, gc3, codon_freq, kmer_freq = cs._composition_stats(seq)
        self.assertAlmostEqual(gc, 1.0 / 3.0, places=9)
        self.assertAlmostEqual(gc3, 0.5, places=9)
        self.assertAlmostEqual(codon_freq[cs.ALL_CODONS.index("AGG")], 0.5, places=9)
        self.assertAlmostEqual(codon_freq[cs.ALL_CODONS.index("TTA")], 0.5, places=9)
        self.assertAlmostEqual(sum(codon_freq), 1.0, places=9)
        self.assertAlmostEqual(sum(kmer_freq), 1.0, places=9)

    def test_ambiguous_base_excluded_from_denominator_not_from_others(self):
        # N o dau/cuoi (khong chia het cho 3 o giua) khong duoc lam sai
        # lech GC/GC3/tan so codon cua phan trinh tu hop le con lai.
        seq = "NNN" + ("AGG" + "TTA") * 10 + "NN"
        gc, gc3, codon_freq, _ = cs._composition_stats(seq)
        self.assertAlmostEqual(gc, 1.0 / 3.0, places=9)
        self.assertAlmostEqual(gc3, 0.5, places=9)
        self.assertAlmostEqual(codon_freq[cs.ALL_CODONS.index("AGG")], 0.5, places=9)

    def test_codon_containing_ambiguous_base_skipped_entirely(self):
        # "AGGNTTAGGATT": codon 1 = AGG (hop le), codon 2 = NTT (co N -> bi
        # bo qua HOAN TOAN, khong tinh vao mau so), codon 3 = AGG, codon 4
        # = ATT. Mau so hop le = 3 (khong phai 4); cod_AGG = 2/3.
        seq = "AGG" + "NTT" + "AGG" + "ATT"
        _, _, codon_freq, _ = cs._composition_stats(seq)
        self.assertAlmostEqual(codon_freq[cs.ALL_CODONS.index("AGG")], 2.0 / 3.0, places=9)
        self.assertAlmostEqual(sum(codon_freq), 1.0, places=9)

    def test_degenerate_all_n_sequence_returns_zero_not_crash(self):
        gc, gc3, codon_freq, kmer_freq = cs._composition_stats("N" * 30)
        self.assertEqual(gc, 0.0)
        self.assertEqual(gc3, 0.0)
        self.assertEqual(sum(codon_freq), 0.0)
        self.assertEqual(sum(kmer_freq), 0.0)


# ---------------------------------------------------------------------------
# jensen_shannon_divergence (don vi)
# ---------------------------------------------------------------------------


class TestJensenShannonDivergence(unittest.TestCase):
    def test_zero_for_identical_distribution(self):
        p = [0.5, 0.3, 0.2]
        self.assertAlmostEqual(cs.jensen_shannon_divergence(p, p), 0.0, places=12)

    def test_max_value_one_for_disjoint_two_point_distributions(self):
        # Truong hop cuc bien da biet: JS([1,0],[0,1]) voi log co so 2 = 1
        # bit dung (gia tri lon nhat co the co).
        p = [1.0, 0.0]
        q = [0.0, 1.0]
        self.assertAlmostEqual(cs.jensen_shannon_divergence(p, q), 1.0, places=9)

    def test_symmetric(self):
        p = [0.7, 0.2, 0.1]
        q = [0.1, 0.2, 0.7]
        self.assertAlmostEqual(
            cs.jensen_shannon_divergence(p, q), cs.jensen_shannon_divergence(q, p), places=12
        )

    def test_within_0_1_for_partial_overlap(self):
        p = [0.5, 0.5]
        q = [0.9, 0.1]
        v = cs.jensen_shannon_divergence(p, q)
        self.assertGreater(v, 0.0)
        self.assertLessEqual(v, 1.0)

    def test_handles_unnormalized_input(self):
        # Dau vao chua chuan hoa (tong != 1) van duoc tu chuan hoa lai ben
        # trong ham -- ket qua phai giong het truong hop da chuan hoa san.
        p_counts = [2, 6, 2]  # tong=10, chuan hoa = [0.2, 0.6, 0.2]
        p_norm = [0.2, 0.6, 0.2]
        q = [0.5, 0.3, 0.2]
        self.assertAlmostEqual(
            cs.jensen_shannon_divergence(p_counts, q), cs.jensen_shannon_divergence(p_norm, q), places=9
        )


# ---------------------------------------------------------------------------
# _percentile (don vi)
# ---------------------------------------------------------------------------


class TestPercentile(unittest.TestCase):
    def test_endpoints_and_median(self):
        s = [1, 2, 3, 4, 5]
        self.assertEqual(cs._percentile(s, 0), 1)
        self.assertEqual(cs._percentile(s, 50), 3)
        self.assertEqual(cs._percentile(s, 100), 5)

    def test_linear_interpolation(self):
        s = [1, 2, 3, 4]
        self.assertAlmostEqual(cs._percentile(s, 50), 2.5, places=9)

    def test_single_value(self):
        self.assertEqual(cs._percentile([7.0], 90), 7.0)

    def test_empty_list_returns_zero(self):
        self.assertEqual(cs._percentile([], 50), 0.0)


# ---------------------------------------------------------------------------
# approx_mahalanobis (don vi)
# ---------------------------------------------------------------------------


class TestApproxMahalanobis(unittest.TestCase):
    def test_zero_variance_dimension_ignored_no_crash(self):
        # Chieu 2 co phuong sai = 0 (moi diem deu = 5.0) -> phai bi bo qua
        # (dong gop 0), khong duoc chia cho 0 / crash.
        x = [1.0, 5.0]
        mean = [0.0, 5.0]
        var = [1.0, 0.0]
        d = cs.approx_mahalanobis(x, mean, var)
        self.assertAlmostEqual(d, 1.0, places=9)  # chi chieu 1 dong gop: sqrt((1-0)^2/1)

    def test_matches_manual_two_dim_case(self):
        # Chieu 1: (3-1)^2/4 = 1.0 ; chieu 2: (7-5)^2/1 = 4.0 ; tong=5.0
        x = [3.0, 7.0]
        mean = [1.0, 5.0]
        var = [4.0, 1.0]
        d = cs.approx_mahalanobis(x, mean, var)
        self.assertAlmostEqual(d, 5.0 ** 0.5, places=9)


# ---------------------------------------------------------------------------
# profile (qua CLI, main())
# ---------------------------------------------------------------------------


class TestProfileCommand(TempDirMixin, unittest.TestCase):
    LONG_SEQ = ("AGG" + "TTA") * 10  # 60bp, gc=1/3, gc3=0.5 (xem TestCompositionStats)
    SHORT_SEQ = "ACGTACGTAC"  # 10bp -- phai bi loai boi --min-len 50

    def _write_fasta(self, path, records, gz=False):
        opener = (lambda p: gzip.open(p, "wt", encoding="utf-8")) if gz else (
            lambda p: open(p, "w", newline="\n", encoding="utf-8")
        )
        with opener(path) as f:
            for seq_id, gene, seq in records:
                header = ">{} [gene={}]".format(seq_id, gene) if gene else ">{}".format(seq_id)
                f.write(header + "\n" + seq + "\n")

    def test_gc_gc3_and_min_len_filter(self):
        fasta_path = self.path("cds.fna")
        out_path = self.path("profile.tsv")
        self._write_fasta(
            fasta_path,
            [("seq_long", "Foo1", self.LONG_SEQ), ("seq_short", "Foo2", self.SHORT_SEQ)],
        )

        rc = cs.main(["profile", "--fasta", fasta_path, "--out", out_path, "--min-len", "50"])
        self.assertEqual(rc, 0)

        header, rows = tsv_rows(read_text(out_path))
        self.assertEqual(header, cs.PROFILE_HEADER)
        self.assertEqual(len(rows), 1)  # seq_short bi loai
        row = rows[0]
        self.assertEqual(row["seq_id"], "seq_long")
        self.assertEqual(row["gene"], "Foo1")
        self.assertEqual(row["len"], "60")
        self.assertAlmostEqual(float(row["gc"]), 1.0 / 3.0, places=6)
        self.assertAlmostEqual(float(row["gc3"]), 0.5, places=6)
        self.assertAlmostEqual(float(row["cod_AGG"]), 0.5, places=6)

    def test_gzip_fasta_input(self):
        fasta_gz = self.path("cds.fna.gz")
        out_path = self.path("profile.tsv")
        self._write_fasta(fasta_gz, [("seq_long", "Foo1", self.LONG_SEQ)], gz=True)

        rc = cs.main(["profile", "--fasta", fasta_gz, "--out", out_path, "--min-len", "50"])
        self.assertEqual(rc, 0)

        _, rows = tsv_rows(read_text(out_path))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["seq_id"], "seq_long")

    def test_gene_missing_from_header_is_empty_string(self):
        fasta_path = self.path("cds.fna")
        out_path = self.path("profile.tsv")
        self._write_fasta(fasta_path, [("seq_nogen", "", self.LONG_SEQ)])

        rc = cs.main(["profile", "--fasta", fasta_path, "--out", out_path, "--min-len", "50"])
        self.assertEqual(rc, 0)
        _, rows = tsv_rows(read_text(out_path))
        self.assertEqual(rows[0]["gene"], "")


# ---------------------------------------------------------------------------
# outliers (qua CLI, main()) -- du lieu nhung: 12 trinh tu nen (thanh phan
# gan giong nhau, tao bang cach xen nhieu codon khac nhau de mo phong CDS
# that) + 1 trinh tu lech manh (GC ~100%, chi dung 4 codon giau GC rieng
# biet). Da kiem thuc nghiem: o --z 2.0, moi trinh tu nen co n_flags=0 va
# trinh tu lech co n_flags=3 (GC/GC3, codon, 4-mer deu vuot nguong).
# ---------------------------------------------------------------------------

BACKGROUND_SEQS = [
    "GAGCTACACGACCTAAAGACTCACACGAACATCAATGATGAACTAGCAGCATGGCTAGAGGCAGTAGCAACGTCACAGCTGCGTGCACGTCAGACGAATATCGAAACGCTGCAGGATCTA",
    "CACTGCCACGAGCAGCACGAAAGTAGTCACAACGATCTAATCGAGACGTGCCGTCTGACTAGTGAAACTTGCTGGAATAAGGTACACCCATGGCTCGAATGGCCAGCACTAGACAGTCTG",
    "GCAATCCTGAATCTAGATAAGCACTGGGCACGTACGTCAGATAAGTTCCCACCACGTGTATGCGACACTGAAGACCTACTGGACAACTGCGCACTCACGGATCCATGGCCAAAGAACCTC",
    "CTACACGATCTCAACCTGGACACTCCACACGCATTCACTTTCTCAGCAATCCTGCACGAGCTGCTACCACACCCAGACCAGTCACTAAATATCCCACTCAGTCACCTAACGATCCAGGTA",
    "ACTCGTGAGGCAGATTGCTTCCAGAATGATCGTAAGGACATCCTCGACGATCTATCATGCCTGAGTACGCCATTCTGGCTGCTGTGGAACAAGTCAAGTAGTAACTGCAGTCTGGATGCA",
    "GACCTCCAGTGGGTAAAGGAACACATCACGCTGTGGCTCACTTCAATCGAGGACCCAATCAAGGTACTGCAGTGGACGAAGGATCTGCACAAGCTATCAACGGTAATCCTCAACCAGATC",
    "AATAACCGTCGTCACAATAATCTCCCATTCGAGGTAGAGGATAGTAAGGCATGCCTACCAACTGCAACGCCAGAGGAGAAGCGTAATTGGGTAACTTGGCAGATCGAAACGGAGATCGAG",
    "CCAAAGAACAACACTGACGAAAGTCAGGACGACGTATGGAAGGAGGACCCACTAGAGCTCCTGGATACTTGGGAAACTGATATCGACACTGATGCAGACTGGAATTCAGTACCACAGCTC",
    "CGTCACAACGAAAATCTCCAGACTCAGACTTCAATCACTAACACTAACATCGAGACTTCAACGGAGCCAGTAGACATCCTACACCAGGAGGAGCAGCTAGAAGAACGTACTCTGCTCGTA",
    "AGTCCACTCAAGAACTGCTGCACGCACGATTCAGTACTACTGCCAAAGCACGCACTGCGTTGGAGTGTAGAATCACAGAGTCAGACTTTCCAGCACAACTGCTCAAATCTATCACTCCAG",
    "CACATCACTAATCAGAACCCAAAGCAGAAGCCACGTCGTGATCTGGCAATCCGTTGCCCAAGTGTACCAGAATCAGACTGGAAGGAATTCCGTCTAAAGCACTGCAAGCACTGCTGGAAG",
    "CGTGAAGTAAGTCTCTGGGATACTAGTGATACGGACTGCGAGCACATCGATCTGCCACGTATCCACATCGAGGTACTGAAGCTCCACGAAGACACTCGTCACGAACCAGCAATCCCACTG",
]
OUTLIER_SEQ = ("GGC" + "GCC" + "CCG" + "GGG") * 15  # 180bp, GC~100%, codon rieng biet voi nen


class TestOutliersCommand(TempDirMixin, unittest.TestCase):
    def setUp(self):
        super().setUp()
        fasta_path = self.path("cds.fna")
        with open(fasta_path, "w", newline="\n", encoding="utf-8") as f:
            for i, seq in enumerate(BACKGROUND_SEQS):
                f.write(">bg_{:02d} [gene=GeneBG{}]\n{}\n".format(i, i, seq))
            f.write(">outlier_01 [gene=GeneOUT]\n{}\n".format(OUTLIER_SEQ))

        self.profile_path = self.path("profile.tsv")
        rc = cs.main(
            ["profile", "--fasta", fasta_path, "--out", self.profile_path, "--min-len", "50"]
        )
        self.assertEqual(rc, 0)

    def _run_outliers(self, z):
        out_path = self.path("outliers_z{}.tsv".format(z))
        stats_path = self.path("stats_z{}.tsv".format(z))
        rc = cs.main(
            [
                "outliers",
                "--profile",
                self.profile_path,
                "--out",
                out_path,
                "--stats",
                stats_path,
                "--z",
                str(z),
            ]
        )
        self.assertEqual(rc, 0)
        return out_path, stats_path

    def test_background_unflagged_and_extreme_outlier_flagged(self):
        out_path, _ = self._run_outliers(2.0)
        _, rows = tsv_rows(read_text(out_path))
        by_id = {r["seq_id"]: r for r in rows}

        self.assertEqual(len(rows), 13)
        for i in range(len(BACKGROUND_SEQS)):
            seq_id = "bg_{:02d}".format(i)
            self.assertLess(
                int(by_id[seq_id]["n_flags"]), 2, "background {} bi danh dau nham".format(seq_id)
            )

        outlier_row = by_id["outlier_01"]
        self.assertGreaterEqual(int(outlier_row["n_flags"]), 2)

    def test_sorted_by_n_flags_then_kmer_js_desc(self):
        out_path, _ = self._run_outliers(2.0)
        _, rows = tsv_rows(read_text(out_path))
        keys = [(-int(r["n_flags"]), -float(r["kmer_js"])) for r in rows]
        self.assertEqual(keys, sorted(keys))

    def test_z_threshold_changes_flagged_count_in_correct_direction(self):
        low_out, _ = self._run_outliers(2.0)
        high_out, _ = self._run_outliers(5.0)

        def count_flagged(path):
            _, rows = tsv_rows(read_text(path))
            return sum(1 for r in rows if int(r["n_flags"]) >= 1)

        n_low = count_flagged(low_out)
        n_high = count_flagged(high_out)
        # Nguong thap hon PHAI cho >= so bat thuong so voi nguong cao hon.
        self.assertGreaterEqual(n_low, n_high)
        # Voi bo du lieu nay da kiem thuc nghiem: z=2.0 bat duoc outlier
        # (1), z=5.0 khong bat duoc gi (0) -- xac nhan chieu thay doi that.
        self.assertEqual(n_low, 1)
        self.assertEqual(n_high, 0)

    def test_stats_file_has_required_metrics_and_consistent_histogram(self):
        _, stats_path = self._run_outliers(2.0)
        stats_text = read_text(stats_path)
        for key in (
            "n_sequences\t13",
            "mean_gc\t",
            "std_gc\t",
            "mean_gc3\t",
            "std_gc3\t",
            "mean_codon_dist\t",
            "std_codon_dist\t",
            "mean_kmer_js\t",
            "std_kmer_js\t",
        ):
            self.assertIn(key, stats_text)
        self.assertIn("z_gc\t", stats_text)
        self.assertIn("codon_dist\t", stats_text)
        self.assertIn("kmer_js\t", stats_text)

        # Histogram n_flags (0..3) phai cong lai dung bang tong so trinh tu.
        hist_section = stats_text.split("n_flags\tcount")[1].split("\n\nmeasure")[0]
        total = sum(
            int(line.split("\t")[1]) for line in hist_section.strip().splitlines() if line.strip()
        )
        self.assertEqual(total, 13)

    def test_outliers_rejects_stdin_profile(self):
        with self.assertRaises(SystemExit):
            cs.main(
                [
                    "outliers",
                    "--profile",
                    "-",
                    "--out",
                    self.path("o.tsv"),
                    "--stats",
                    self.path("s.tsv"),
                ]
            )


# ---------------------------------------------------------------------------
# report (qua CLI, main())
# ---------------------------------------------------------------------------


class TestReportCommand(TempDirMixin, unittest.TestCase):
    def _write_outliers(self, path, rows):
        lines = ["\t".join(cs.OUTLIERS_HEADER)]
        for r in rows:
            lines.append("\t".join(str(r[k]) for k in cs.OUTLIERS_HEADER))
        write_text(path, "\n".join(lines) + "\n")

    def test_report_has_warning_top_rows_and_blank_explanation_column(self):
        outliers_path = self.path("outliers.tsv")
        out_path = self.path("report.md")
        rows = [
            {
                "seq_id": "s{}".format(i),
                "gene": "g{}".format(i),
                "len": 300,
                "gc": 0.5,
                "gc3": 0.5,
                "z_gc": 0.1 * i,
                "z_gc3": 0.1 * i,
                "codon_dist": float(i),
                "kmer_js": 0.01 * i,
                "n_flags": (2 if i >= 3 else 0),
            }
            for i in range(5)
        ]
        self._write_outliers(outliers_path, rows)

        rc = cs.main(["report", "--outliers", outliers_path, "--top", "2", "--out", out_path])
        self.assertEqual(rc, 0)

        report = read_text(out_path)
        # Canh bao bat buoc + thu tu kha nang giai thich + buoc kiem tiep theo.
        self.assertIn("CANH BAO BAT BUOC", report)
        self.assertIn("1. **Loi lap rap", report)
        self.assertIn("2. **Vung lap", report)
        self.assertIn("3. **HGT", report)
        self.assertIn("4. Chi khi da loai het", report)
        self.assertIn("BLAST", report)
        self.assertIn("DIAMOND", report)
        self.assertIn("giai_thich_kha_di", report)

        # Top 2 theo n_flags giam dan roi kmer_js giam dan: s4 (n_flags=2,
        # kmer_js=0.04) truoc s3 (n_flags=2, kmer_js=0.03).
        pos_s4 = report.index("| s4 |")
        pos_s3 = report.index("| s3 |")
        self.assertLess(pos_s4, pos_s3)
        self.assertNotIn("| s0 |", report)  # ngoai top 2

    def test_report_empty_outliers_raises(self):
        outliers_path = self.path("empty.tsv")
        write_text(outliers_path, "")
        with self.assertRaises(SystemExit):
            cs.main(
                ["report", "--outliers", outliers_path, "--out", self.path("report.md")]
            )


# ---------------------------------------------------------------------------
# --help (top-level va tung lenh con)
# ---------------------------------------------------------------------------


class TestHelp(unittest.TestCase):
    def _assert_help_exits_zero(self, argv):
        with self.assertRaises(SystemExit) as ctx:
            cs.main(argv)
        self.assertEqual(ctx.exception.code, 0)

    def test_top_level_help(self):
        self._assert_help_exits_zero(["--help"])

    def test_profile_help(self):
        self._assert_help_exits_zero(["profile", "--help"])

    def test_outliers_help(self):
        self._assert_help_exits_zero(["outliers", "--help"])

    def test_report_help(self):
        self._assert_help_exits_zero(["report", "--help"])


if __name__ == "__main__":
    unittest.main()
