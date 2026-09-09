#!/usr/bin/env bash
# Doi chung am: chay A2 tren bo vung TIEN HOA NHANH (accelerated) thay vi bao ton.
# Ket qua vao data/a2_accel/ (khong dung chung voi data/a2). Khong co lenh xoa.
# Gene chiu rang buoc that phai giau conserved nhung KHONG giau accelerated
# (dac ta: research/raw/A2-antigravity-null-model.md muc 2).
set -uo pipefail
cd "/d/BIRDBIODNA project" || exit 1
echo "RUN_START $(date '+%F %T')"
bash pipeline/p00_inventory/check_resources.sh || exit 2

time bash pipeline/p02_core_map/run_a2.sh \
  --conserved-bb /data/ucsc/ancRep_separate_models_rev.bw.accelerated.bb \
  --out-dir "/d/BIRDBIODNA project/data/a2_accel" \
  --threads 2 --chunk-bases 90000000 \
  --mm-extra "-k 13 -w 5 -s 30 -m 20 -n 2 -K 10M -f 0.001"
rc=$?

if [ "$rc" -eq 0 ]; then
  echo "[$(date '+%F %T')] STEP enrich START"
  python -B pipeline/p02_core_map/conserved_to_bulbul.py enrich \
    --annot data/a2/core_annot.tsv \
    --annot-accel data/a2_accel/core_annot.tsv \
    --gff data/ncbi/GCA_013400435.1/GCA_013400435.1_ASM1340043v1_genomic.gff.gz \
    --chrom-sizes data/ucsc/Pycnonotus_jocosus.chrom.sizes \
    --out data/a2/gene_enrichment.tsv \
    --stats data/a2/enrich_stats.tsv
  echo "[$(date '+%F %T')] STEP enrich END"
fi
echo "BENCH_EXIT=$rc"
