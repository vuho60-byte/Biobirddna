#!/usr/bin/env bash
# Chạy A2 toàn genome: lưu kết quả chr1 sang data/a2_chr1, dọn output dở, chạy run_a2.sh với mặc định đã chốt (docs/04 mục 10b).
cd "/d/BIRDBIODNA project" || exit 1
echo "RUN_START $(date '+%F %T')"
mkdir -p data/a2_chr1
: # cp -f data/a2/bulbul_core*.bed data/a2/map_stats*.tsv data/a2/annot_stats.tsv data/a2/core_annot.tsv data/a2/unmapped*.txt data/a2/merge_stats.tsv data/a2/elements.paf data/a2/run.log data/a2/bench-chr1* data/a2_chr1/ 2>/dev/null
echo "a2_chr1 files: $(ls data/a2_chr1 | wc -l)"
: # (chi lan dau) rm -f data/a2/elements.bed data/a2/elements.bed.params data/a2/elements.fa data/a2/elements.fa.params data/a2/elements.paf.tmp
bash pipeline/p00_inventory/check_resources.sh || exit 2
time bash pipeline/p02_core_map/run_a2.sh --threads 2 --chunk-bases 90000000 --mm-extra "-k 13 -w 5 -s 30 -m 20 -n 2 -K 10M -f 0.001" --clean-chunks
echo "BENCH_EXIT=$?"
