"""Test cho phep chuan hoa mat do loi (bp tren moi kb chieu dai gene) trong annotate.

Ly do co test nay: xep hang gene theo TONG bp thien vi gene dai; canh bao tu
research/raw/A1-antigravity-gene-interpretation.md muc 5. Bang thu hai trong
annot_stats phai xep theo mat do va phai loc gene qua ngan / qua it bp.

Chay: python -B -m unittest discover -s pipeline/p02_core_map/tests -v
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import conserved_to_bulbul as c2b  # noqa: E402


GFF = """##gff-version 3
scaf1\tRefSeq\tgene\t1\t100000\t.\t+\t.\tID=gene-LONG;Name=LongGene
scaf1\tRefSeq\tmRNA\t1\t100000\t.\t+\t.\tID=rna-LONG;Parent=gene-LONG
scaf1\tRefSeq\texon\t1\t500\t.\t+\t.\tID=ex1;Parent=rna-LONG
scaf1\tRefSeq\tCDS\t1\t500\t.\t+\t0\tID=cds1;Parent=rna-LONG
scaf2\tRefSeq\tgene\t1\t4000\t.\t+\t.\tID=gene-SHORT;Name=ShortGene
scaf2\tRefSeq\tmRNA\t1\t4000\t.\t+\t.\tID=rna-SHORT;Parent=gene-SHORT
scaf2\tRefSeq\texon\t1\t300\t.\t+\t.\tID=ex2;Parent=rna-SHORT
scaf2\tRefSeq\tCDS\t1\t300\t.\t+\t0\tID=cds2;Parent=rna-SHORT
"""

# LongGene: 3 vung x 400 bp = 1200 bp tren locus 100 kb -> 12 bp/kb
# ShortGene: 2 vung x 400 bp = 800 bp tren locus 4 kb   -> 200 bp/kb
BED = "\n".join(
    [
        "scaf1\t1000\t1400\tq1\t950\t+",
        "scaf1\t5000\t5400\tq2\t950\t+",
        "scaf1\t9000\t9400\tq3\t950\t+",
        "scaf2\t1000\t1400\tq4\t950\t+",
        "scaf2\t2000\t2400\tq5\t950\t+",
    ]
) + "\n"


def parse_density_table(text):
    """Tra ve list (gene_name, bp, gene_len, bp_per_kb) tu bang xep theo mat do."""
    rows = []
    started = False
    for line in text.splitlines():
        if line.startswith("# xep theo mat do"):
            started = True
            continue
        if not started:
            continue
        if line.startswith("gene_id\t") or not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) == 5:
            rows.append((parts[1], int(parts[2]), int(parts[3]), float(parts[4])))
    return rows


class TestDensityRanking(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.gff = os.path.join(self.tmp, "ann.gff")
        self.bed = os.path.join(self.tmp, "core.bed")
        self.out = os.path.join(self.tmp, "annot.tsv")
        self.stats = os.path.join(self.tmp, "stats.tsv")
        with open(self.gff, "w", encoding="utf-8", newline="\n") as f:
            f.write(GFF)
        with open(self.bed, "w", encoding="utf-8", newline="\n") as f:
            f.write(BED)

    def run_annotate(self):
        rc = c2b.main(
            [
                "annotate",
                "--bed", self.bed,
                "--gff", self.gff,
                "--out", self.out,
                "--stats", self.stats,
            ]
        )
        self.assertEqual(rc, 0)
        with open(self.stats, encoding="utf-8") as f:
            return f.read()

    def test_bp_table_has_gene_len_and_density_columns(self):
        text = self.run_annotate()
        self.assertIn("gene_id\tgene_name\tbp\tgene_len\tbp_per_kb", text)

    def test_density_table_ranks_short_dense_gene_first(self):
        text = self.run_annotate()
        rows = parse_density_table(text)
        self.assertTrue(rows, "khong co bang xep theo mat do")
        # Gene ngan nhung dac (200 bp/kb) phai dung truoc gene dai (12 bp/kb),
        # nguoc voi xep hang theo tong bp (LongGene 1200 > ShortGene 800).
        self.assertEqual(rows[0][0], "ShortGene")
        self.assertAlmostEqual(rows[0][3], 200.0, places=1)
        names = [r[0] for r in rows]
        self.assertIn("LongGene", names)
        self.assertLess(names.index("ShortGene"), names.index("LongGene"))
        long_row = rows[names.index("LongGene")]
        self.assertAlmostEqual(long_row[3], 12.0, places=1)

    def test_density_table_filters_tiny_genes(self):
        # Nang nguong loc len tren chieu dai ca hai gene -> bang mat do rong.
        old_len, old_bp = c2b.MIN_GENE_LEN_FOR_DENSITY, c2b.MIN_BP_FOR_DENSITY
        try:
            c2b.MIN_GENE_LEN_FOR_DENSITY = 200000
            text = self.run_annotate()
            self.assertEqual(parse_density_table(text), [])
        finally:
            c2b.MIN_GENE_LEN_FOR_DENSITY, c2b.MIN_BP_FOR_DENSITY = old_len, old_bp

    def test_total_bp_ranking_still_puts_long_gene_first(self):
        # Bang dau tien (theo tong bp) van giu thu tu cu -> hai bang bo sung nhau.
        text = self.run_annotate()
        head = text.split("# xep theo mat do")[0]
        gene_lines = [l for l in head.splitlines() if l.startswith("gene-")]
        self.assertTrue(gene_lines)
        self.assertTrue(gene_lines[0].startswith("gene-LONG"), gene_lines[:2])


if __name__ == "__main__":
    unittest.main()
