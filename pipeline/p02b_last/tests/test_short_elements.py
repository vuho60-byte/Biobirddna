"""Unit test cho short_elements.py -- unittest thuan, khong pytest, du lieu
nhung ngay trong file (khong doc/ghi ngoai thu muc tam cua test).

Chay: python -B -m unittest discover -s pipeline/p02b_last/tests -v
"""

import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import short_elements as se  # noqa: E402


def read_text(path):
    with open(path, "r", newline="", encoding="utf-8") as f:
        return f.read()


def write_text(path, content):
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(content)


class TempDirMixin:
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="se_test_")
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def path(self, name):
        return os.path.join(self.tmp, name)


def fasta_record(header, seq, wrap=None):
    """Dung FASTA text cho 1 record, tuy chon xuong dong moi `wrap` ky tu
    (mac dinh: ca chuoi tren 1 dong) - dung de test _iter_fasta xu ly duoc
    sequence nhieu dong."""
    lines = [">" + header]
    if wrap:
        for i in range(0, len(seq), wrap):
            lines.append(seq[i : i + wrap])
    else:
        lines.append(seq)
    return "\n".join(lines) + "\n"


def make_texts(length, mismatches):
    """Tra ve (target_text, query_text) dai `length`, giong het nhau tru
    dung `mismatches` vi tri DAU TIEN bi doi ky tu (A -> C). Dung de kiem
    soat chinh xac so base khop (matches = length - mismatches) ma khong
    phai dem tay tung ky tu trong chuoi align."""
    target = "A" * length
    query_chars = list(target)
    for i in range(mismatches):
        query_chars[i] = "C"
    return target, "".join(query_chars)


def maf_block(score, t_name, t_start, t_size, t_strand, t_src_size, t_text,
              q_name, q_start, q_size, q_strand, q_src_size, q_text):
    """Dung 1 khoi MAF hop le (dong 'a score=' + 2 dong 's': target roi
    query, dung thu tu LAST that su xuat ra khi chay `lastal <db-tu-genome>
    <query.fa>`)."""
    return "a score={}\ns {} {} {} {} {} {}\ns {} {} {} {} {} {}\n".format(
        score,
        t_name, t_start, t_size, t_strand, t_src_size, t_text,
        q_name, q_start, q_size, q_strand, q_src_size, q_text,
    )


# ---------------------------------------------------------------------------
# filter
# ---------------------------------------------------------------------------


class TestFilter(TempDirMixin, unittest.TestCase):
    def test_filter_keeps_within_range_and_stats(self):
        bed = (
            "chr1\t0\t15\ts_short\n"       # do dai 15 < min-len 20 -> loai
            "chr1\t100\t130\ts_ok30\n"     # do dai 30 -> giu, 1 dong seq
            "chr1\t200\t260\ts_ok60\n"     # do dai 60 -> giu, seq 2 dong
            "chr1\t300\t450\ts_long\n"     # do dai 150 > max-len 99 -> loai
        )
        fa = (
            fasta_record("s_short", "A" * 15)
            + fasta_record("s_ok30", "C" * 30)
            + fasta_record("s_ok60 mo ta them", "G" * 60, wrap=30)
            + fasta_record("s_long", "T" * 150)
        )
        bed_path = self.path("elements.bed")
        fa_path = self.path("elements.fa")
        write_text(bed_path, bed)
        write_text(fa_path, fa)

        out_path = self.path("short.fa")
        stats_path = self.path("filter_stats.tsv")

        rc = se.main(
            [
                "filter",
                "--in-fa", fa_path,
                "--in-bed", bed_path,
                "--out", out_path,
                "--max-len", "99",
                "--stats", stats_path,
            ]
        )
        self.assertEqual(rc, 0)

        out_text = read_text(out_path)
        self.assertEqual(
            out_text,
            fasta_record("s_ok30", "C" * 30) + fasta_record("s_ok60 mo ta them", "G" * 60, wrap=30),
        )

        stats = read_text(stats_path)
        self.assertIn("total_in_bed\t4", stats)
        self.assertIn("total_in_fasta\t4", stats)
        self.assertIn("kept\t2", stats)
        self.assertIn("excluded_too_long\t1", stats)
        self.assertIn("excluded_too_short\t1", stats)
        self.assertIn("bp_kept\t90", stats)

    def test_filter_id_in_fasta_missing_from_bed_raises(self):
        bed_path = self.path("elements.bed")
        fa_path = self.path("elements.fa")
        write_text(bed_path, "chr1\t0\t30\tknown\n")
        write_text(fa_path, fasta_record("ghost", "A" * 30))

        with self.assertRaises(SystemExit):
            se.main(
                [
                    "filter",
                    "--in-fa", fa_path,
                    "--in-bed", bed_path,
                    "--out", self.path("short.fa"),
                    "--max-len", "99",
                ]
            )


# ---------------------------------------------------------------------------
# maf2bed
# ---------------------------------------------------------------------------


class TestMaf2Bed(TempDirMixin, unittest.TestCase):
    def test_best_hit_thresholds_and_no_hit(self):
        # q1: 2 khoi cung query, score cao hon thang (80 > 50) du ca 2 deu
        # match hoan toan - dung dung tieu chi "uu tien score" truoc tien.
        t1, q1t = make_texts(20, 0)
        t2, q2t = make_texts(20, 0)
        block_q1_low = maf_block(50, "scafA", 100, 20, "+", 5000, t1, "q1", 0, 20, "+", 20, q1t)
        block_q1_high = maf_block(80, "scafA", 900, 20, "+", 5000, t2, "q1", 0, 20, "+", 20, q2t)

        # q2: identity 10/20 = 0.50 < nguong 0.70 mac dinh -> low_identity
        t3, q3t = make_texts(20, 10)
        block_q2 = maf_block(20, "scafA", 2000, 20, "+", 5000, t3, "q2", 0, 20, "+", 20, q3t)

        # q3: identity 1.0 (dat), nhung coverage 35/50 = 0.70 < nguong 0.80 -> low_coverage
        t4, q4t = make_texts(35, 0)
        block_q3 = maf_block(30, "scafB", 500, 35, "+", 3000, t4, "q3", 0, 35, "+", 50, q4t)

        maf_text = "\n".join([block_q1_low, block_q1_high, block_q2, block_q3])
        maf_path = self.path("aln.maf")
        write_text(maf_path, maf_text)

        query_list_path = self.path("elements.bed")
        write_text(
            query_list_path,
            "chrA\t0\t20\tq1\nchrA\t100\t120\tq2\nchrB\t0\t50\tq3\nchrX\t0\t25\tq4\n",
        )

        out_path = self.path("bulbul_short.bed")
        unmapped_path = self.path("unmapped_short.txt")
        stats_path = self.path("map_stats_short.tsv")

        rc = se.main(
            [
                "maf2bed",
                "--maf", maf_path,
                "--out", out_path,
                "--unmapped", unmapped_path,
                "--stats", stats_path,
                "--min-identity", "0.70",
                "--min-coverage", "0.80",
                "--query-list", query_list_path,
            ]
        )
        self.assertEqual(rc, 0)

        out_lines = read_text(out_path).splitlines()
        self.assertEqual(out_lines, ["scafA\t900\t920\tq1\t1000\t+\t20\t1.0000\t80"])

        unmapped_text = read_text(unmapped_path)
        self.assertIn("q2\tlow_identity\tidentity=0.5000", unmapped_text)
        self.assertIn("q3\tlow_coverage\tcoverage=0.7000", unmapped_text)
        self.assertIn("q4\tno_hit\t", unmapped_text)

        stats = read_text(stats_path)
        self.assertIn("total_queries\t4", stats)
        self.assertIn("mapped\t1", stats)
        self.assertIn("mapped_pct\t25.00", stats)
        self.assertIn("unmapped\t3", stats)
        self.assertIn("second_hit_queries\t1", stats)
        self.assertIn("qlen_bin\tmapped\ttotal\tmapped_pct", stats)
        self.assertIn("20_49\t1\t3\t33.33", stats)
        self.assertIn("50_99\t0\t1\t0.00", stats)

    def test_tiebreak_matches_then_alnlen(self):
        # score bang nhau (50) -> chon so base khop lon hon (18 > 15)
        t1, qt1 = make_texts(20, 5)
        t2, qt2 = make_texts(20, 2)
        maf_text = "\n".join(
            [
                maf_block(50, "scafT1", 0, 20, "+", 1000, t1, "qA", 0, 20, "+", 20, qt1),
                maf_block(50, "scafT2", 0, 20, "+", 1000, t2, "qA", 0, 20, "+", 20, qt2),
            ]
        )
        maf_path = self.path("tie1.maf")
        write_text(maf_path, maf_text)
        out_path = self.path("out.bed")

        rc = se.main(
            [
                "maf2bed",
                "--maf", maf_path,
                "--out", out_path,
                "--unmapped", self.path("unmapped.txt"),
                "--min-identity", "0.0",
                "--min-coverage", "0.0",
            ]
        )
        self.assertEqual(rc, 0)
        fields = read_text(out_path).splitlines()[0].split("\t")
        self.assertEqual(fields[0], "scafT2")

    def test_tiebreak_alnlen_when_score_and_matches_equal(self):
        # score (50) va so base khop (15) bang nhau -> chon do dai align lon hon (20 > 15)
        t1, qt1 = make_texts(15, 0)  # matches=15, alnlen=15
        t2, qt2 = make_texts(20, 5)  # matches=15, alnlen=20
        maf_text = "\n".join(
            [
                maf_block(50, "scafU1", 0, 15, "+", 1000, t1, "qB", 0, 15, "+", 15, qt1),
                maf_block(50, "scafU2", 0, 20, "+", 1000, t2, "qB", 0, 20, "+", 20, qt2),
            ]
        )
        maf_path = self.path("tie2.maf")
        write_text(maf_path, maf_text)
        out_path = self.path("out.bed")

        rc = se.main(
            [
                "maf2bed",
                "--maf", maf_path,
                "--out", out_path,
                "--unmapped", self.path("unmapped.txt"),
                "--min-identity", "0.0",
                "--min-coverage", "0.0",
            ]
        )
        self.assertEqual(rc, 0)
        fields = read_text(out_path).splitlines()[0].split("\t")
        self.assertEqual(fields[0], "scafU2")

    def test_target_strand_minus_coordinate_and_relative_strand(self):
        # qneg1: target '-' / query '+' -> mach tuong doi '-'; toa do doi
        # sang mach '+' cua target: start=100,size=10,src_size=1000 ->
        # end=1000-100=900, begin=900-10=890.
        t1, qt1 = make_texts(10, 0)
        block1 = maf_block(90, "scafNeg", 100, 10, "-", 1000, t1, "qneg1", 0, 10, "+", 10, qt1)
        # qneg2: target '-' / query '-' (cung mach) -> mach tuong doi '+'.
        t2, qt2 = make_texts(10, 0)
        block2 = maf_block(70, "scafW", 50, 10, "-", 200, t2, "qneg2", 0, 10, "-", 10, qt2)

        maf_path = self.path("strand.maf")
        write_text(maf_path, "\n".join([block1, block2]))
        out_path = self.path("out.bed")

        rc = se.main(
            [
                "maf2bed",
                "--maf", maf_path,
                "--out", out_path,
                "--unmapped", self.path("unmapped.txt"),
                "--min-identity", "0.0",
                "--min-coverage", "0.0",
            ]
        )
        self.assertEqual(rc, 0)
        rows = {line.split("\t")[3]: line.split("\t") for line in read_text(out_path).splitlines()}
        self.assertEqual(rows["qneg1"][:3], ["scafNeg", "890", "900"])
        self.assertEqual(rows["qneg1"][5], "-")
        self.assertEqual(rows["qneg2"][:3], ["scafW", "140", "150"])
        self.assertEqual(rows["qneg2"][5], "+")

    def test_malformed_blocks_are_skipped_not_crashed(self):
        # 1 khoi tot (qgood) + 3 kieu khoi hong: thieu dong 's' thu 2, thieu
        # 'score=', va 2 chuoi align khac do dai. Ca 3 khoi hong phai bi bo
        # qua (khong crash) va duoc dem dung ly do trong stats; qms/qtlm co
        # trong --query-list nen phai ra no_hit (khoi duy nhat cua chung bi
        # loai) thay vi bi bo lo hoan toan.
        t_good, q_good = make_texts(20, 0)
        good_block = maf_block(99, "scafGood", 0, 20, "+", 1000, t_good, "qgood", 0, 20, "+", 20, q_good)

        maf_text = (
            good_block
            + "\n"
            + "a score=77\n"
            + "s scafX 0 10 + 100 AAAAAAAAAA\n"  # thieu dong 's' thu 2
            + "\n"
            + "a\n"  # thieu score=
            + "s scafY 0 15 + 200 AAAAAAAAAAAAAAA\n"
            + "s qms 0 15 + 15 AAAAAAAAAAAAAAA\n"
            + "\n"
            + "a score=55\n"
            + "s scafZ 0 12 + 300 AAAAAAAAAAAA\n"  # 12 ky tu
            + "s qtlm 0 10 + 10 AAAAAAAAAA\n"  # 10 ky tu -> khac do dai
        )
        maf_path = self.path("bad.maf")
        write_text(maf_path, maf_text)

        query_list_path = self.path("elements.bed")
        write_text(query_list_path, "chrG\t0\t20\tqgood\nchrM\t0\t15\tqms\nchrT\t0\t10\tqtlm\n")

        out_path = self.path("out.bed")
        unmapped_path = self.path("unmapped.txt")
        stats_path = self.path("stats.tsv")

        rc = se.main(
            [
                "maf2bed",
                "--maf", maf_path,
                "--out", out_path,
                "--unmapped", unmapped_path,
                "--stats", stats_path,
                "--query-list", query_list_path,
            ]
        )
        self.assertEqual(rc, 0)

        out_lines = read_text(out_path).splitlines()
        self.assertEqual(len(out_lines), 1)
        self.assertTrue(out_lines[0].startswith("scafGood\t0\t20\tqgood\t"))

        unmapped_text = read_text(unmapped_path)
        self.assertIn("qms\tno_hit\t", unmapped_text)
        self.assertIn("qtlm\tno_hit\t", unmapped_text)

        stats = read_text(stats_path)
        self.assertIn("blocks_total\t4", stats)
        self.assertIn("blocks_bad\t3", stats)
        self.assertIn("wrong_s_count\t1", stats)
        self.assertIn("missing_score\t1", stats)
        self.assertIn("text_len_mismatch\t1", stats)

    def test_maf_bad_column_count_errors(self):
        # Dong 's' du 7 truong nhung field so khong phai so nguyen van phai
        # bi coi la khoi hong (khong crash) - khac voi paf2bed (PAF sai cot
        # thi dung chuong trinh) vi MAF la dau ra cong cu ngoai, co the co
        # khoi le te; o day chi kiem tra rc=0 va khong co dong nao duoc map.
        maf_path = self.path("bad.maf")
        write_text(maf_path, "a score=10\ns scafA notanumber 10 + 100 AAAAAAAAAA\ns q1 0 10 + 10 AAAAAAAAAA\n")
        out_path = self.path("out.bed")
        rc = se.main(
            [
                "maf2bed",
                "--maf", maf_path,
                "--out", out_path,
                "--unmapped", self.path("unmapped.txt"),
            ]
        )
        self.assertEqual(rc, 0)
        self.assertEqual(read_text(out_path), "")


# ---------------------------------------------------------------------------
# merge-beds
# ---------------------------------------------------------------------------


class TestMergeBeds(TempDirMixin, unittest.TestCase):
    def test_merge_dedup_keeps_higher_score(self):
        file1 = (
            "scafLOW\t0\t20\tid_a\t900\t+\t20\t1.0000\t50\n"
            "scafB\t0\t20\tid_b\t800\t+\t20\t1.0000\t40\n"
        )
        file2 = (
            "scafHIGH\t0\t20\tid_a\t950\t+\t20\t1.0000\t60\n"
            "scafD\t0\t20\tid_c\t700\t+\t20\t1.0000\t30\n"
        )
        path1 = self.path("bulbul_core.bed")
        path2 = self.path("bulbul_short.bed")
        write_text(path1, file1)
        write_text(path2, file2)

        out_path = self.path("bulbul_core_all.bed")
        stats_path = self.path("merge_beds_stats.tsv")

        rc = se.main(
            [
                "merge-beds",
                "--in", path1,
                "--in", path2,
                "--out", out_path,
                "--stats", stats_path,
            ]
        )
        self.assertEqual(rc, 0)

        out_lines = read_text(out_path).splitlines()
        self.assertEqual(
            out_lines,
            [
                "scafB\t0\t20\tid_b\t800\t+\t20\t1.0000\t40",
                "scafD\t0\t20\tid_c\t700\t+\t20\t1.0000\t30",
                "scafHIGH\t0\t20\tid_a\t950\t+\t20\t1.0000\t60",
            ],
        )

        stats = read_text(stats_path)
        self.assertIn("inputs\t2", stats)
        self.assertIn("total_rows_in\t4", stats)
        self.assertIn("unique_ids_out\t3", stats)
        self.assertIn("duplicate_ids\t1", stats)

    def test_merge_bad_columns_errors(self):
        path1 = self.path("bad.bed")
        write_text(path1, "scafA\t0\t20\tid_a\n")  # chi 4 cot, thieu score/strand
        with self.assertRaises(SystemExit):
            se.main(["merge-beds", "--in", path1, "--out", self.path("out.bed")])


# ---------------------------------------------------------------------------
# --help (top-level va tung lenh con)
# ---------------------------------------------------------------------------


class TestHelp(unittest.TestCase):
    def _assert_help_exits_zero(self, argv):
        with self.assertRaises(SystemExit) as ctx:
            se.main(argv)
        self.assertEqual(ctx.exception.code, 0)

    def test_top_level_help(self):
        self._assert_help_exits_zero(["--help"])

    def test_filter_help(self):
        self._assert_help_exits_zero(["filter", "--help"])

    def test_maf2bed_help(self):
        self._assert_help_exits_zero(["maf2bed", "--help"])

    def test_merge_beds_help(self):
        self._assert_help_exits_zero(["merge-beds", "--help"])


if __name__ == "__main__":
    unittest.main()
