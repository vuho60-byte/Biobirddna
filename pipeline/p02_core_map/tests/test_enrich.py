"""Unit test cho lenh con 'enrich' (kiem dinh gene giau vung loi so voi nen
+ doi chung am accelerated) trong conserved_to_bulbul.py -- unittest thuan,
du lieu nhung ngay trong file (khong doc/ghi ngoai thu muc tam cua test).

Dac ta: research/briefs/X5-enrichment-null-model.md +
research/raw/A2-antigravity-null-model.md.

Chay: python -B -m unittest discover -s pipeline/p02_core_map/tests -v
"""

import os
import shutil
import sys
import tempfile
import unittest

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
        self.tmp = tempfile.mkdtemp(prefix="c2b_enrich_test_")
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def path(self, name):
        return os.path.join(self.tmp, name)


# ---------------------------------------------------------------------------
# benjamini_hochberg: ham thuan tuy, kiem doc lap voi p-value dat san
# ---------------------------------------------------------------------------


class TestBenjaminiHochberg(unittest.TestCase):
    def test_matches_hand_calculation(self):
        # Vi du tay: p=[0.01,0.02,0.03,0.5], m=4.
        # q(rank1..4) = 0.04,0.04,0.04,0.5 (tinh tay: p*m/rank roi lay min
        # luy tich tu rank lon ve rank nho).
        pvalues = [0.01, 0.02, 0.03, 0.5]
        q = c2b.benjamini_hochberg(pvalues)
        expected = [0.04, 0.04, 0.04, 0.5]
        for got, want in zip(q, expected):
            self.assertAlmostEqual(got, want, places=6)

    def test_order_matches_hand_calculation_unsorted_input(self):
        # Dau vao KHONG sap: p=[0.2, 0.001, 0.05, 0.9, 0.01], m=5.
        # Tay tinh (sap tang dan 0.001,0.01,0.05,0.2,0.9 -> rank1..5, q=p*5/rank,
        # roi min luy tich tu rank5 ve rank1):
        #   rank5 p=0.9  -> 0.9
        #   rank4 p=0.2  -> 0.25          -> min(0.9,0.25)=0.25
        #   rank3 p=0.05 -> 0.083333...   -> min(0.25,0.083333)=0.083333
        #   rank2 p=0.01 -> 0.025         -> min(0.083333,0.025)=0.025
        #   rank1 p=0.001-> 0.005         -> min(0.025,0.005)=0.005
        # tra ve dung VI TRI dau vao (khong sap lai):
        pvalues = [0.2, 0.001, 0.05, 0.9, 0.01]
        q = c2b.benjamini_hochberg(pvalues)
        expected = [0.25, 0.005, 0.05 * 5 / 3, 0.9, 0.025]
        self.assertEqual(len(q), len(pvalues))
        for got, want in zip(q, expected):
            self.assertAlmostEqual(got, want, places=6)
        # q phai khong giam dan khi xet theo thu tu p tang dan (buoc step-up).
        order = sorted(range(len(pvalues)), key=lambda i: pvalues[i])
        q_in_p_order = [q[i] for i in order]
        self.assertEqual(q_in_p_order, sorted(q_in_p_order))

    def test_empty_input(self):
        self.assertEqual(c2b.benjamini_hochberg([]), [])


# ---------------------------------------------------------------------------
# enrich: kich ban chinh -- P0 tu --genome-size, fold/p-value/BH/loc gene
# ---------------------------------------------------------------------------

# 4 gene tren 1 scaffold, khong chong toa do:
#   gene-EXP    [0,100000)     len=100000  bp_obs=1000  -> fold=1 (dung ky vong)
#   gene-RICH   [200000,250000) len=50000  bp_obs=5000  -> fold=10 (giau ro ret)
#   gene-TINY   [300000,300500) len=500    bp_obs=300   -> bi loc (gene_len<1000)
#   gene-LOWBP  [400000,420000) len=20000  bp_obs=50    -> bi loc (bp_obs<200)
# + 1 dong intergenic dem cho tong bp loi toan cuc = 10000 (P0 = 10000/1e6 = 0.01)
BASIC_GFF = (
    "##gff-version 3\n"
    "scaf1\tRefSeq\tgene\t1\t100000\t.\t+\t.\tID=gene-EXP;Name=ExpectedGene\n"
    "scaf1\tRefSeq\tgene\t200001\t250000\t.\t+\t.\tID=gene-RICH;Name=RichGene\n"
    "scaf1\tRefSeq\tgene\t300001\t300500\t.\t+\t.\tID=gene-TINY;Name=TinyGene\n"
    "scaf1\tRefSeq\tgene\t400001\t420000\t.\t+\t.\tID=gene-LOWBP;Name=LowBpGene\n"
)
BASIC_ANNOT_ROWS = [
    ("scaf1", 0, 1000, "intron", "gene-EXP", "ExpectedGene"),
    ("scaf1", 200000, 205000, "intron", "gene-RICH", "RichGene"),
    ("scaf1", 300000, 300300, "intron", "gene-TINY", "TinyGene"),
    ("scaf1", 400000, 400050, "intron", "gene-LOWBP", "LowBpGene"),
    ("scaf1", 600000, 603650, "intergenic", "", ""),  # dem: tong bp loi = 10000
]


class TestEnrichBasic(TempDirMixin, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.gff_path = self.path("genomic.gff")
        write_text(self.gff_path, BASIC_GFF)
        self.annot_path = self.path("core_annot.tsv")
        write_text(
            self.annot_path,
            "\n".join("\t".join(str(x) for x in row) for row in BASIC_ANNOT_ROWS) + "\n",
        )

    def run_enrich(self, extra_args=None):
        out_path = self.path("gene_enrichment.tsv")
        stats_path = self.path("enrich_stats.tsv")
        argv = [
            "enrich",
            "--annot", self.annot_path,
            "--gff", self.gff_path,
            "--genome-size", "1000000",
            "--out", out_path,
            "--stats", stats_path,
        ]
        if extra_args:
            argv += extra_args
        rc = c2b.main(argv)
        self.assertEqual(rc, 0)
        return out_path, stats_path

    @staticmethod
    def _rows_by_gene(out_path):
        lines = read_text(out_path).splitlines()
        header = lines[0].split("\t")
        rows = {}
        for line in lines[1:]:
            fields = line.split("\t")
            rows[fields[0]] = dict(zip(header, fields))
        return rows

    def test_default_filters_fold_and_pvalue_and_bh(self):
        out_path, stats_path = self.run_enrich()
        rows = self._rows_by_gene(out_path)

        # gene-TINY (gene_len 500 < 1000) va gene-LOWBP (bp_obs 50 < 200) bi loc.
        self.assertEqual(set(rows.keys()), {"gene-EXP", "gene-RICH"})

        exp = rows["gene-EXP"]
        self.assertEqual(int(exp["bp_obs"]), 1000)
        self.assertEqual(int(exp["gene_len"]), 100000)
        self.assertAlmostEqual(float(exp["fold"]), 1.0, places=6)
        # bp_obs dung bang ky vong -> rank_score_p gan 0.5 (xap xi chuan +
        # hieu chinh lien tuc lech nhe ve phia > 0.5, xem README).
        self.assertAlmostEqual(float(exp["rank_score_p"]), 0.5, delta=0.03)
        self.assertEqual(int(exp["signif_flag"]), 0)
        self.assertEqual(int(exp["approx_warn"]), 0)

        rich = rows["gene-RICH"]
        self.assertEqual(int(rich["bp_obs"]), 5000)
        self.assertAlmostEqual(float(rich["fold"]), 10.0, places=6)
        self.assertLess(float(rich["rank_score_p"]), 1e-6)
        self.assertEqual(int(rich["signif_flag"]), 1)  # qua nguong sau BH
        self.assertEqual(int(rich["approx_warn"]), 0)

        stats = read_text(stats_path)
        self.assertIn("p0\t0.01", stats)
        self.assertIn("total_core_bp\t10000", stats)
        self.assertIn("total_space\t1000000", stats)
        self.assertIn("genes_tested\t2", stats)
        self.assertIn("genes_pass_fdr\t1", stats)

    def test_output_header_and_sorted_by_fold_descending(self):
        out_path, _ = self.run_enrich()
        lines = read_text(out_path).splitlines()
        self.assertEqual(
            lines[0].split("\t"),
            [
                "gene_id", "gene_name", "bp_obs", "gene_len", "bp_exp", "fold",
                "rank_score_p", "bh_q", "signif_flag", "approx_warn",
            ],
        )
        gene_ids = [line.split("\t")[0] for line in lines[1:]]
        self.assertEqual(gene_ids, ["gene-RICH", "gene-EXP"])  # fold 10 > 1

    def test_min_gene_len_and_min_bp_filters_can_be_loosened(self):
        # Mac dinh gene-TINY/gene-LOWBP bi loc (test tren); ha nguong thi phai
        # xuat hien -> xac nhan --min-gene-len/--min-bp thuc su co hieu luc.
        out_path, _ = self.run_enrich(extra_args=["--min-gene-len", "100", "--min-bp", "10"])
        rows = self._rows_by_gene(out_path)
        self.assertIn("gene-TINY", rows)
        self.assertIn("gene-LOWBP", rows)

    def test_genome_size_and_chrom_sizes_give_same_p0(self):
        _out_gs, stats_gs = self.run_enrich()

        chrom_sizes_path = self.path("chrom.sizes")
        write_text(chrom_sizes_path, "scaf1\t600000\nscaf2\t400000\n")  # tong = 1,000,000
        out_path2 = self.path("gene_enrichment2.tsv")
        stats_path2 = self.path("enrich_stats2.tsv")
        rc = c2b.main(
            [
                "enrich",
                "--annot", self.annot_path,
                "--gff", self.gff_path,
                "--chrom-sizes", chrom_sizes_path,
                "--out", out_path2,
                "--stats", stats_path2,
            ]
        )
        self.assertEqual(rc, 0)
        stats2 = read_text(stats_path2)
        self.assertIn("p0\t0.01", stats2)
        self.assertIn("total_space\t1000000", stats2)
        # Cung annot/gff, cung tong khong gian (600000+400000=1000000) ->
        # toan bo thong ke phai giong het nhau du lay tu --genome-size hay
        # --chrom-sizes.
        self.assertEqual(read_text(stats_gs), stats2)

    def test_enrich_help_exits_zero(self):
        with self.assertRaises(SystemExit) as ctx:
            c2b.main(["enrich", "--help"])
        self.assertEqual(ctx.exception.code, 0)


# ---------------------------------------------------------------------------
# enrich: approx_warn khi gene_len x P0 < 10
# ---------------------------------------------------------------------------


class TestEnrichApproxWarn(TempDirMixin, unittest.TestCase):
    def test_approx_warn_flags_when_gene_len_times_p0_below_10(self):
        gff_path = self.path("small.gff")
        write_text(
            gff_path,
            "##gff-version 3\n"
            "scafW\tRefSeq\tgene\t1\t500\t.\t+\t.\tID=gene-SMALL;Name=SmallGene\n",
        )
        annot_path = self.path("small_annot.tsv")
        # 1 dong duy nhat: toan bo 50bp la cua chinh gene nay -> total_core_bp=50.
        write_text(annot_path, "scafW\t0\t50\tintron\tgene-SMALL\tSmallGene\n")

        out_path = self.path("out.tsv")
        rc = c2b.main(
            [
                "enrich",
                "--annot", annot_path,
                "--gff", gff_path,
                "--genome-size", "10000",
                "--out", out_path,
                "--min-gene-len", "400",
                "--min-bp", "1",
            ]
        )
        self.assertEqual(rc, 0)
        lines = read_text(out_path).splitlines()
        row = dict(zip(lines[0].split("\t"), lines[1].split("\t")))
        self.assertEqual(row["gene_id"], "gene-SMALL")
        # P0 = 50/10000 = 0.005; gene_len x P0 = 500 x 0.005 = 2.5 < 10 -> canh bao.
        self.assertEqual(int(row["approx_warn"]), 1)

    def test_approx_warn_off_for_well_powered_gene(self):
        # Doi chung: gene du lon (gene_len x P0 >= 10) thi KHONG bat canh bao.
        gff_path = self.path("big.gff")
        write_text(
            gff_path,
            "##gff-version 3\n"
            "scafW\tRefSeq\tgene\t1\t2000\t.\t+\t.\tID=gene-BIG;Name=BigGene\n",
        )
        annot_path = self.path("big_annot.tsv")
        write_text(annot_path, "scafW\t0\t50\tintron\tgene-BIG\tBigGene\n")
        out_path = self.path("out.tsv")
        rc = c2b.main(
            [
                "enrich",
                "--annot", annot_path,
                "--gff", gff_path,
                "--genome-size", "10000",
                "--out", out_path,
                "--min-gene-len", "400",
                "--min-bp", "1",
            ]
        )
        self.assertEqual(rc, 0)
        lines = read_text(out_path).splitlines()
        row = dict(zip(lines[0].split("\t"), lines[1].split("\t")))
        # P0 = 50/10000 = 0.005; gene_len x P0 = 2000 x 0.005 = 10 -> khong < 10.
        self.assertEqual(int(row["approx_warn"]), 0)


# ---------------------------------------------------------------------------
# enrich: --annot-accel -> accel_bp/accel_fold/ca_ratio (doi chung am)
# ---------------------------------------------------------------------------


class TestEnrichAccelCaRatio(TempDirMixin, unittest.TestCase):
    # 3 gene cung do dai (10000bp), cung bp loi conserved (2000bp -> fold
    # nhu nhau ~33.33 het) de moi khac biet ca_ratio chi den tu phia accel:
    #   gene-RICH2  accel_bp=0     -> ca_ratio = inf
    #   gene-SPEC   accel_bp=20    -> ca_ratio cao nhung huu han (=100.0)
    #   gene-ART    accel_bp=2000  -> giau ca 2 phia nhu nhau -> ca_ratio = 1.0
    GFF = (
        "##gff-version 3\n"
        "scafX\tRefSeq\tgene\t1\t10000\t.\t+\t.\tID=gene-RICH2;Name=Rich2\n"
        "scafX\tRefSeq\tgene\t20001\t30000\t.\t+\t.\tID=gene-SPEC;Name=Spec\n"
        "scafX\tRefSeq\tgene\t40001\t50000\t.\t+\t.\tID=gene-ART;Name=Art\n"
    )

    def setUp(self):
        super().setUp()
        self.gff_path = self.path("ca.gff")
        write_text(self.gff_path, self.GFF)

        conserved_rows = [
            ("scafX", 0, 2000, "intron", "gene-RICH2", "Rich2"),
            ("scafX", 20000, 22000, "intron", "gene-SPEC", "Spec"),
            ("scafX", 40000, 42000, "intron", "gene-ART", "Art"),
        ]
        self.annot_path = self.path("conserved_annot.tsv")
        write_text(
            self.annot_path,
            "\n".join("\t".join(str(x) for x in r) for r in conserved_rows) + "\n",
        )

        accel_rows = [
            # gene-RICH2 co chu y KHONG xuat hien o day -> accel_bp=0.
            ("scafX", 20000, 20020, "intron", "gene-SPEC", "Spec"),  # 20bp
            ("scafX", 40000, 42000, "intron", "gene-ART", "Art"),  # 2000bp
            # dem ngoai moi gene de tong accel bp = 6000 (P0_accel = 0.006,
            # bang P0 conserved = 6000/1000000, de gene-ART ra ca_ratio dung 1.0).
            ("scafX", 900000, 903980, "intergenic", "", ""),  # 3980bp
        ]
        self.accel_path = self.path("accel_annot.tsv")
        write_text(
            self.accel_path,
            "\n".join("\t".join(str(x) for x in r) for r in accel_rows) + "\n",
        )

    def test_ca_ratio_three_behaviours(self):
        out_path = self.path("gene_enrichment.tsv")
        stats_path = self.path("enrich_stats.tsv")
        rc = c2b.main(
            [
                "enrich",
                "--annot", self.annot_path,
                "--annot-accel", self.accel_path,
                "--gff", self.gff_path,
                "--genome-size", "1000000",
                "--out", out_path,
                "--stats", stats_path,
            ]
        )
        self.assertEqual(rc, 0)

        lines = read_text(out_path).splitlines()
        header = lines[0].split("\t")
        self.assertEqual(header[-3:], ["accel_bp", "accel_fold", "ca_ratio"])
        rows = {}
        for line in lines[1:]:
            fields = line.split("\t")
            rows[fields[0]] = dict(zip(header, fields))

        rich2 = rows["gene-RICH2"]
        self.assertEqual(int(rich2["accel_bp"]), 0)
        self.assertEqual(rich2["ca_ratio"], "inf")

        spec = rows["gene-SPEC"]
        self.assertEqual(int(spec["accel_bp"]), 20)
        self.assertAlmostEqual(float(spec["ca_ratio"]), 100.0, places=3)

        art = rows["gene-ART"]
        self.assertEqual(int(art["accel_bp"]), 2000)
        self.assertAlmostEqual(float(art["ca_ratio"]), 1.0, places=3)

        # Bang "top 20 theo ca_ratio" trong stats phai xep inf len dau.
        stats = read_text(stats_path)
        self.assertIn("# top 20 theo ca_ratio", stats)
        ca_section = stats.split("# top 20 theo ca_ratio")[1]
        ca_lines = [l for l in ca_section.splitlines() if l.strip()]
        self.assertTrue(ca_lines[1].startswith("gene-RICH2"))


if __name__ == "__main__":
    unittest.main()
