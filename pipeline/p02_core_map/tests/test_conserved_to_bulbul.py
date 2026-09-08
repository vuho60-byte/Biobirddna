"""Unit test cho conserved_to_bulbul.py -- unittest thuan, khong pytest,
du lieu nhung ngay trong file (khong doc/ghi ngoai thu muc tam cua test).

Chay: python -B -m unittest discover -s pipeline/p02_core_map/tests -v
"""

import gzip
import io
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import conserved_to_bulbul as c2b  # noqa: E402


def read_text(path):
    with open(path, "r", newline="", encoding="utf-8") as f:
        return f.read()


def write_text(path, content):
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(content)


class TempDirMixin:
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="c2b_test_")
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def path(self, name):
        return os.path.join(self.tmp, name)


# ---------------------------------------------------------------------------
# merge
# ---------------------------------------------------------------------------


class TestMerge(TempDirMixin, unittest.TestCase):
    INPUT_ROWS = [
        ("chr1", 0, 10),
        ("chr1", 15, 30),  # gap=5 <= 10 -> gop voi khoang truoc thanh 0-30
        ("chr1", 1000, 1010),
        ("chr1", 1015, 1020),  # gap=5 <= 10 -> gop thanh 1000-1020 (len 20)
        ("chr2", 0, 5),  # len 5 < min-len 20 -> bi loai
        ("chr2", 50, 90),  # len 40 -> giu
    ]

    def _write_input(self, rows):
        lines = "\n".join("{}\t{}\t{}".format(c, s, e) for c, s, e in rows) + "\n"
        in_path = self.path("all.bed")
        write_text(in_path, lines)
        return in_path

    def test_merge_gap_minlen_and_stats(self):
        in_path = self._write_input(self.INPUT_ROWS)
        out_path = self.path("elements.bed")
        stats_path = self.path("merge_stats.tsv")

        rc = c2b.main(
            [
                "merge",
                "--in",
                in_path,
                "--out",
                out_path,
                "--gap",
                "10",
                "--min-len",
                "20",
                "--stats",
                stats_path,
            ]
        )
        self.assertEqual(rc, 0)

        out_lines = read_text(out_path).splitlines()
        self.assertEqual(
            out_lines,
            [
                "chr1\t0\t30\tchr1:0-30",
                "chr1\t1000\t1020\tchr1:1000-1020",
                "chr2\t50\t90\tchr2:50-90",
            ],
        )

        stats = read_text(stats_path)
        self.assertIn("intervals_in\t6", stats)
        self.assertIn("elements_out\t3", stats)
        self.assertIn("bp_in\t85", stats)
        self.assertIn("bp_out\t90", stats)
        self.assertIn("length_20_49\t3", stats)
        self.assertIn("chr1\t2", stats)
        self.assertIn("chr2\t1", stats)

    def test_merge_stdin_pipe(self):
        in_lines = "chr1\t0\t10\nchr1\t5\t25\n"
        out_path = self.path("elements.bed")
        with mock.patch("sys.stdin", io.StringIO(in_lines)):
            rc = c2b.main(["merge", "--in", "-", "--out", out_path, "--gap", "10", "--min-len", "5"])
        self.assertEqual(rc, 0)
        self.assertEqual(read_text(out_path).splitlines(), ["chr1\t0\t25\tchr1:0-25"])

    def test_merge_rejects_unsorted_start(self):
        in_path = self._write_input([("chr1", 10, 20), ("chr1", 5, 8)])
        out_path = self.path("elements.bed")
        with self.assertRaises(SystemExit):
            c2b.main(["merge", "--in", in_path, "--out", out_path])

    def test_merge_rejects_regrouped_chrom(self):
        in_path = self._write_input([("chr1", 0, 10), ("chr2", 0, 10), ("chr1", 20, 30)])
        out_path = self.path("elements.bed")
        with self.assertRaises(SystemExit):
            c2b.main(["merge", "--in", in_path, "--out", out_path])

    def test_merge_rejects_bad_columns(self):
        in_path = self.path("bad.bed")
        write_text(in_path, "chr1\t0\n")
        out_path = self.path("elements.bed")
        with self.assertRaises(SystemExit):
            c2b.main(["merge", "--in", in_path, "--out", out_path])

    def test_merge_empty_input(self):
        in_path = self.path("empty.bed")
        write_text(in_path, "")
        out_path = self.path("elements.bed")
        stats_path = self.path("stats.tsv")
        rc = c2b.main(["merge", "--in", in_path, "--out", out_path, "--stats", stats_path])
        self.assertEqual(rc, 0)
        self.assertEqual(read_text(out_path), "")
        self.assertIn("intervals_in\t0", read_text(stats_path))


# ---------------------------------------------------------------------------
# paf2bed
# ---------------------------------------------------------------------------


class TestPaf2Bed(TempDirMixin, unittest.TestCase):
    def _paf_line(self, qname, qlen, qstart, qend, strand, tname, tlen, tstart, tend, nmatch, alnlen, mapq):
        return "\t".join(
            str(x)
            for x in (qname, qlen, qstart, qend, strand, tname, tlen, tstart, tend, nmatch, alnlen, mapq)
        )

    def test_best_hit_threshold_and_no_hit(self):
        paf_lines = [
            # q1: 2 hit -> chon theo mapq truoc (60 > 10), du hit thu 2 co nmatch/alnlen cao hon
            self._paf_line("q1", 100, 0, 100, "+", "scafA", 5000, 200, 300, 95, 100, 60),
            self._paf_line("q1", 100, 0, 100, "+", "scafA", 5000, 900, 1000, 100, 100, 10),
            # q2: identity 30/50=0.60 < nguong 0.70 -> low_identity
            self._paf_line("q2", 50, 0, 50, "+", "scafA", 5000, 10, 60, 30, 50, 40),
            # q3: identity 38/40=0.95 dat, nhung coverage 20/40=0.5 < 0.80 -> low_coverage
            self._paf_line("q3", 40, 0, 20, "+", "scafB", 3000, 5, 45, 38, 40, 50),
        ]
        paf_path = self.path("elements.paf")
        write_text(paf_path, "\n".join(paf_lines) + "\n")

        query_list_path = self.path("elements.bed")
        write_text(
            query_list_path,
            "\n".join(
                [
                    "chrA\t0\t100\tq1",
                    "chrA\t100\t150\tq2",
                    "chrB\t0\t40\tq3",
                    "chrB\t100\t140\tq4",  # khong co dong nao trong PAF -> no_hit
                ]
            )
            + "\n",
        )

        out_path = self.path("bulbul_core.bed")
        unmapped_path = self.path("unmapped.txt")
        stats_path = self.path("map_stats.tsv")

        rc = c2b.main(
            [
                "paf2bed",
                "--paf",
                paf_path,
                "--out",
                out_path,
                "--unmapped",
                unmapped_path,
                "--stats",
                stats_path,
                "--min-identity",
                "0.70",
                "--min-coverage",
                "0.80",
                "--query-list",
                query_list_path,
            ]
        )
        self.assertEqual(rc, 0)

        out_lines = read_text(out_path).splitlines()
        self.assertEqual(len(out_lines), 1)
        fields = out_lines[0].split("\t")
        self.assertEqual(fields[0], "scafA")
        self.assertEqual(fields[1], "200")
        self.assertEqual(fields[2], "300")
        self.assertEqual(fields[3], "q1")
        self.assertEqual(fields[4], "950")  # identity 0.95 -> 950/1000
        self.assertEqual(fields[5], "+")
        self.assertEqual(fields[6], "100")
        self.assertEqual(fields[7], "1.0000")
        self.assertEqual(fields[8], "60")

        unmapped_text = read_text(unmapped_path)
        self.assertIn("q2\tlow_identity\tidentity=0.6000", unmapped_text)
        self.assertIn("q3\tlow_coverage\tcoverage=0.5000", unmapped_text)
        self.assertIn("q4\tno_hit\t", unmapped_text)

        stats = read_text(stats_path)
        self.assertIn("total_queries\t4", stats)
        self.assertIn("mapped\t1", stats)
        self.assertIn("mapped_pct\t25.00", stats)
        self.assertIn("unmapped\t3", stats)
        self.assertIn("second_hit_queries\t1", stats)
        # bang moi: mapped_pct theo qlen_bin (mapped/total MOI bin, total ke
        # ca q4 no_hit qua length_hint tu --query-list elements.bed).
        # q3 (qlen=40) + q4 (length_hint=140-100=40) -> bin 20_49, ca 2 deu
        # khong mapped -> 0/2. q2 (qlen=50) -> bin 50_99, khong mapped -> 0/1.
        # q1 (qlen=100) -> bin 100_199, mapped -> 1/1 = 100%.
        self.assertIn("qlen_bin\tmapped\ttotal\tmapped_pct", stats)
        self.assertIn("20_49\t0\t2\t0.00", stats)
        self.assertIn("50_99\t0\t1\t0.00", stats)
        self.assertIn("100_199\t1\t1\t100.00", stats)

    def test_best_hit_tiebreak_nmatch_then_alnlen(self):
        # Finding #3 (05-review-code-x1.md): rank_key = (mapq, nmatch, alnlen)
        # nhung test cu chi khoa duoc tang mapq. O day khoa rieng tang nmatch
        # (mapq bang nhau) va tang alnlen (mapq+nmatch bang nhau).
        paf_lines = [
            # q1: mapq bang nhau (50) -> chon nmatch lon hon (95 > 80)
            self._paf_line("q1", 100, 0, 100, "+", "scafA", 5000, 0, 100, 80, 100, 50),
            self._paf_line("q1", 100, 0, 100, "+", "scafA", 5000, 500, 600, 95, 100, 50),
            # q2: mapq (50) va nmatch (90) bang nhau -> chon alnlen lon hon (120 > 100)
            self._paf_line("q2", 100, 0, 100, "+", "scafB", 5000, 0, 100, 90, 100, 50),
            self._paf_line("q2", 100, 0, 100, "+", "scafB", 5000, 700, 820, 90, 120, 50),
        ]
        paf_path = self.path("tiebreak.paf")
        write_text(paf_path, "\n".join(paf_lines) + "\n")
        out_path = self.path("out.bed")
        unmapped_path = self.path("unmapped.txt")

        rc = c2b.main(
            [
                "paf2bed",
                "--paf",
                paf_path,
                "--out",
                out_path,
                "--unmapped",
                unmapped_path,
                "--min-identity",
                "0.0",
                "--min-coverage",
                "0.0",
            ]
        )
        self.assertEqual(rc, 0)

        rows = {}
        for line in read_text(out_path).splitlines():
            fields = line.split("\t")
            rows[fields[3]] = fields
        self.assertEqual(rows["q1"][1], "500")  # dong nmatch=95 duoc chon
        self.assertEqual(rows["q2"][1], "700")  # dong alnlen=120 duoc chon

    def test_no_query_list_falls_back_to_paf_queries(self):
        paf_lines = [
            self._paf_line("qa", 30, 0, 30, "+", "scafA", 1000, 0, 30, 30, 30, 60),
        ]
        paf_path = self.path("a.paf")
        write_text(paf_path, "\n".join(paf_lines) + "\n")
        out_path = self.path("out.bed")
        unmapped_path = self.path("unmapped.txt")
        rc = c2b.main(
            ["paf2bed", "--paf", paf_path, "--out", out_path, "--unmapped", unmapped_path]
        )
        self.assertEqual(rc, 0)
        self.assertEqual(len(read_text(out_path).splitlines()), 1)
        # khong co --query-list nen khong the phat hien no_hit; chi 1 dong header
        self.assertEqual(len(read_text(unmapped_path).splitlines()), 1)

    def test_paf_bad_column_count_errors(self):
        paf_path = self.path("bad.paf")
        write_text(paf_path, "q1\t100\t0\t100\n")
        with self.assertRaises(SystemExit):
            c2b.main(
                [
                    "paf2bed",
                    "--paf",
                    paf_path,
                    "--out",
                    self.path("out.bed"),
                    "--unmapped",
                    self.path("unmapped.txt"),
                ]
            )


# ---------------------------------------------------------------------------
# annotate
# ---------------------------------------------------------------------------


GFF_CONTENT = """##gff-version 3
scafA\tRefSeq\tgene\t1000\t2000\t.\t+\t.\tID=gene-G1;Name=GENE1
scafA\tRefSeq\tmRNA\t1000\t2000\t.\t+\t.\tID=rna-R1;Parent=gene-G1
scafA\tRefSeq\texon\t1000\t1200\t.\t+\t.\tID=exon-R1-1;Parent=rna-R1
scafA\tRefSeq\tCDS\t1050\t1150\t.\t+\t0\tID=cds-R1;Parent=rna-R1
scafA\tRefSeq\texon\t1500\t1600\t.\t+\t.\tID=exon-R1-2;Parent=rna-R1
scafB\tRefSeq\tgene\t10\t50\t.\t+\t.\tID=gene-G2;Name=GENE2
scafC\tRefSeq\tgene\t1000\t2000\t.\t+\t.\tID=gene-G3;Name=GENE3
scafC\tRefSeq\tmRNA\t1000\t2000\t.\t+\t.\tID=rna-R3;Parent=gene-G3
scafC\tRefSeq\texon\t1000\t1100\t.\t+\t.\tID=exon-R3-1;Parent=rna-R3
scafC\tRefSeq\tgene\t1500\t2500\t.\t-\t.\tID=gene-G4;Name=GENE4
scafC\tRefSeq\tmRNA\t1500\t2500\t.\t-\t.\tID=rna-R4;Parent=gene-G4
scafC\tRefSeq\texon\t2400\t2500\t.\t-\t.\tID=exon-R4-1;Parent=rna-R4
scafD\tRefSeq\tpseudogene\t3000\t3200\t.\t+\t.\tID=gene-P1;Name=PSEUDO1;pseudo=true
scafD\tRefSeq\tmRNA\t3000\t3200\t.\t+\t.\tID=rna-P1;Parent=gene-P1;pseudo=true
scafD\tRefSeq\texon\t3000\t3050\t.\t+\t.\tID=exon-P1-1;Parent=rna-P1
scafD\tRefSeq\tpseudogene\t3300\t3400\t.\t+\t.\tID=gene-P2
"""


class TestAnnotate(TempDirMixin, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.gff_path = self.path("genomic.gff.gz")
        with gzip.open(self.gff_path, "wt", encoding="utf-8") as f:
            f.write(GFF_CONTENT)

    def test_classification_cds_exon_intron_intergenic_multi_scaffold(self):
        bed_rows = [
            ("scafA", 1060, 1080, "r1"),  # trong CDS 1049-1150 (0-based)
            ("scafA", 1520, 1550, "r2"),  # trong exon2 1499-1600, ngoai CDS
            ("scafA", 1300, 1350, "r3"),  # trong gene 999-2000, ngoai moi exon -> intron
            ("scafA", 5000, 5050, "r4"),  # ngoai gene -> intergenic
            ("scafB", 20, 30, "r5"),  # trong gene2 9-50, gene2 khong co exon nao -> intron
        ]
        bed_path = self.path("bulbul_core.bed")
        write_text(
            bed_path,
            "\n".join("{}\t{}\t{}\t{}".format(c, s, e, n) for c, s, e, n in bed_rows) + "\n",
        )

        out_path = self.path("core_annot.tsv")
        stats_path = self.path("annot_stats.tsv")

        rc = c2b.main(
            [
                "annotate",
                "--bed",
                bed_path,
                "--gff",
                self.gff_path,
                "--out",
                out_path,
                "--stats",
                stats_path,
            ]
        )
        self.assertEqual(rc, 0)

        rows = [line.split("\t") for line in read_text(out_path).splitlines()]
        by_name = {r[3]: r for r in rows}

        self.assertEqual(by_name["r1"][4:7], ["CDS", "gene-G1", "GENE1"])
        self.assertEqual(by_name["r2"][4:7], ["exon_noncoding", "gene-G1", "GENE1"])
        self.assertEqual(by_name["r3"][4:7], ["intron", "gene-G1", "GENE1"])
        self.assertEqual(by_name["r4"][4:7], ["intergenic", "", ""])
        self.assertEqual(by_name["r5"][4:7], ["intron", "gene-G2", "GENE2"])

        stats = read_text(stats_path)
        self.assertIn("CDS\t1\t20", stats)
        self.assertIn("exon_noncoding\t1\t30", stats)
        self.assertIn("intron\t2\t60", stats)
        self.assertIn("intergenic\t1\t50", stats)
        self.assertIn("gene-G1\tGENE1\t100", stats)
        self.assertIn("gene-G2\tGENE2\t10", stats)

    def test_annotate_overlapping_genes_same_scaffold_picks_larger_overlap(self):
        # Finding #2 (05-review-code-x1.md): gene-G3 [999,2000) va gene-G4
        # [1499,2500) chong toa do tren cung scafC (khac mach). Vung BED
        # [1900,2100) giao ca 2 gene nhung ngoai moi exon: giao G3 = 100bp,
        # giao G4 = 200bp -> phai chon G4 (giao lon hon), class "intron".
        bed_path = self.path("overlap.bed")
        write_text(bed_path, "scafC\t1900\t2100\to1\n")
        out_path = self.path("overlap_annot.tsv")

        rc = c2b.main(
            ["annotate", "--bed", bed_path, "--gff", self.gff_path, "--out", out_path]
        )
        self.assertEqual(rc, 0)

        rows = [line.split("\t") for line in read_text(out_path).splitlines()]
        by_name = {r[3]: r for r in rows}
        self.assertEqual(by_name["o1"][4:7], ["intron", "gene-G4", "GENE4"])

    def test_annotate_pseudogene_body_and_name_fallback(self):
        # REQUIRED_FIX #1 (05-review-code-x1.md Finding #1): than pseudogene
        # ngoai exon phai ra "intron" (khong phai "intergenic"); gene_name lay
        # Name/gene attribute, fallback ve ID neu khong co ca hai.
        bed_rows = [
            ("scafD", 3010, 3030, "p1"),  # trong exon cua pseudogene P1 (co Name)
            ("scafD", 3100, 3150, "p2"),  # trong than P1, ngoai exon -> intron
            ("scafD", 3320, 3350, "p3"),  # pseudogene P2, khong Name/gene -> fallback ID
        ]
        bed_path = self.path("pseudo.bed")
        write_text(
            bed_path,
            "\n".join("{}\t{}\t{}\t{}".format(c, s, e, n) for c, s, e, n in bed_rows) + "\n",
        )
        out_path = self.path("pseudo_annot.tsv")

        rc = c2b.main(
            ["annotate", "--bed", bed_path, "--gff", self.gff_path, "--out", out_path]
        )
        self.assertEqual(rc, 0)

        rows = [line.split("\t") for line in read_text(out_path).splitlines()]
        by_name = {r[3]: r for r in rows}
        self.assertEqual(by_name["p1"][4:7], ["exon_noncoding", "gene-P1", "PSEUDO1"])
        self.assertEqual(by_name["p2"][4:7], ["intron", "gene-P1", "PSEUDO1"])
        self.assertEqual(by_name["p3"][4:7], ["intron", "gene-P2", "gene-P2"])

    def test_annotate_bad_bed_errors(self):
        bed_path = self.path("bad.bed")
        write_text(bed_path, "scafA\tnotanumber\t100\n")
        with self.assertRaises(SystemExit):
            c2b.main(
                [
                    "annotate",
                    "--bed",
                    bed_path,
                    "--gff",
                    self.gff_path,
                    "--out",
                    self.path("out.tsv"),
                ]
            )


# ---------------------------------------------------------------------------
# --help (top-level va tung lenh con)
# ---------------------------------------------------------------------------


class TestHelp(unittest.TestCase):
    def _assert_help_exits_zero(self, argv):
        with self.assertRaises(SystemExit) as ctx:
            c2b.main(argv)
        self.assertEqual(ctx.exception.code, 0)

    def test_top_level_help(self):
        self._assert_help_exits_zero(["--help"])

    def test_merge_help(self):
        self._assert_help_exits_zero(["merge", "--help"])

    def test_paf2bed_help(self):
        self._assert_help_exits_zero(["paf2bed", "--help"])

    def test_annotate_help(self):
        self._assert_help_exits_zero(["annotate", "--help"])


if __name__ == "__main__":
    unittest.main()
