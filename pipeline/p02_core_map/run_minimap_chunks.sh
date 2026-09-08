#!/usr/bin/env bash
# Map elements.fa lên từng mảnh genome (index nguyên khối mỗi mảnh) để ở dưới trần RAM 2 GB, nối PAF.
# Dùng: bash run_minimap_chunks.sh [threads]   (mặc định 4). Sau đó chạy run_a2.sh (bước minimap2 sẽ SKIP vì đã có PAF).
set -euo pipefail
T=${1:-4}; ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; DATA="$ROOT/data"; WIN="$(cygpath -w "$DATA")"
IMG="quay.io/biocontainers/minimap2:2.30--h577a1d6_0"; OUT="$DATA/a2/elements.paf"; TMP="$OUT.tmp"; : > "$TMP"
for c in "$DATA"/a2/genome_chunks/chunk_*.fa; do
  b=$(basename "$c"); echo "[$(date '+%F %T')] CHUNK $b START" 
  MSYS_NO_PATHCONV=1 docker run --rm -v "$WIN:/data" "$IMG" minimap2 -x asm20 -t "$T" --secondary=no -c "/data/a2/genome_chunks/$b" /data/a2/elements.fa >> "$TMP"
  echo "[$(date '+%F %T')] CHUNK $b END lines=$(wc -l < "$TMP")"
done
mv -f "$TMP" "$OUT"; echo "[$(date '+%F %T')] PAF DONE lines=$(wc -l < "$OUT")"
