#!/usr/bin/env bash
# Chay A2 tren TOAN BO genome voi tham so da chot (docs/04 muc 10b).
#
# Idempotent: run_a2.sh tu bo qua buoc da chay dung tham so VA dung input
# (co che .params + input_id, sua 2026-09-08). Chay lai an toan.
# Khong co lenh xoa nao trong file nay (luat project sau su co 2026-09-08).
#
# Dung: bash pipeline/p02_core_map/launch_full.sh [--threads N]
set -uo pipefail
cd "/d/BIRDBIODNA project" || exit 1

THREADS="${2:-2}"
CHUNK_BASES=90000000
MM_EXTRA="-k 13 -w 5 -s 30 -m 20 -n 2 -K 10M -f 0.001"

echo "RUN_START $(date '+%F %T')"
bash pipeline/p00_inventory/check_resources.sh || exit 2

# Buoc 1-5: merge -> twoBitToFa -> chia manh -> minimap2 theo manh -> paf2bed (cov 0,8) -> annotate
time bash pipeline/p02_core_map/run_a2.sh \
  --threads "$THREADS" \
  --chunk-bases "$CHUNK_BASES" \
  --mm-extra "$MM_EXTRA" \
  --clean-chunks
rc=$?

if [ "$rc" -eq 0 ]; then
  # Bo thu hai voi nguong coverage thap hon (0,5) de do do nhay cua nguong.
  echo "[$(date '+%F %T')] STEP paf2bed_cov50 START"
  python -B pipeline/p02_core_map/conserved_to_bulbul.py paf2bed \
    --paf data/a2/elements.paf \
    --out data/a2/bulbul_core.cov50.bed \
    --unmapped data/a2/unmapped.cov50.txt \
    --stats data/a2/map_stats.cov50.tsv \
    --min-identity 0.70 --min-coverage 0.50 \
    --query-list data/a2/elements.bed
  echo "[$(date '+%F %T')] STEP paf2bed_cov50 END"

  echo "[$(date '+%F %T')] STEP annotate_cov50 START"
  python -B pipeline/p02_core_map/conserved_to_bulbul.py annotate \
    --bed data/a2/bulbul_core.cov50.bed \
    --gff data/ncbi/GCA_013400435.1/GCA_013400435.1_ASM1340043v1_genomic.gff.gz \
    --out data/a2/core_annot.cov50.tsv \
    --stats data/a2/annot_stats.cov50.tsv
  echo "[$(date '+%F %T')] STEP annotate_cov50 END"

  echo "[$(date '+%F %T')] STEP summary START"
  python -B pipeline/p02_core_map/summarize_a2.py --dir data/a2 --label "(toan genome, $(date '+%F'))" \
    > data/a2/SUMMARY.md
  echo "[$(date '+%F %T')] STEP summary END"

  echo "[$(date '+%F %T')] STEP sha256 START"
  ( cd data/a2 && sha256sum bulbul_core.bed bulbul_core.cov50.bed elements.paf elements.bed > SHA256SUMS.txt )
  echo "[$(date '+%F %T')] STEP sha256 END"
fi

echo "BENCH_EXIT=$rc"
