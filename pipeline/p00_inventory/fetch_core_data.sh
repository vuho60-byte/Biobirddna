#!/usr/bin/env bash
# Tải lại dữ liệu lõi theo data/registry.csv (idempotent: bỏ qua file đã đủ byte). Không xóa gì.
set -uo pipefail
cd "/d/BIRDBIODNA project" || exit 1
HUB="https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020-hub"
NCBI="https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/013/400/435/GCA_013400435.1_ASM1340043v1"
A="GCA_013400435.1_ASM1340043v1"
mkdir -p data/ucsc data/models data/ncbi/GCA_013400435.1 data/a2
get(){ url="$1"; out="$2"; want="${3:-0}"
  have=$(stat -c %s "$out" 2>/dev/null || echo 0)
  if [ "$want" != "0" ] && [ "$have" = "$want" ]; then echo "SKIP $(basename "$out") ($have)"; return 0; fi
  for i in 1 2 3 4 5 6; do
    curl -sS -L -C - --retry 3 --retry-delay 5 --max-time 900 -o "$out" "$url" || true
    have=$(stat -c %s "$out" 2>/dev/null || echo 0)
    [ "$want" = "0" ] && { echo "GOT  $(basename "$out") ($have)"; return 0; }
    [ "$have" = "$want" ] && { echo "OK   $(basename "$out") ($have)"; return 0; }
    echo "..   $(basename "$out") $have/$want (lượt $i)"
  done
  echo "FAIL $(basename "$out") $have/$want"; return 1
}
echo "FETCH_START $(date '+%F %T')"
get "$HUB/Gallus_gallus/ancRep_separate_models_rev.bw.conserved.bb"   data/ucsc/ancRep_separate_models_rev.bw.conserved.bb   345031105
get "$HUB/Gallus_gallus/ancRep_separate_models_rev.bw.accelerated.bb" data/ucsc/ancRep_separate_models_rev.bw.accelerated.bb 329399456
get "$HUB/Gallus_gallus/Gallus_gallus.2bit"                           data/ucsc/Gallus_gallus.2bit                          265935614
get "$HUB/Gallus_gallus/chrom.sizes"                                  data/ucsc/Gallus_gallus.chrom.sizes                   388228
get "$HUB/Pycnonotus_jocosus/chrom.sizes"                             data/ucsc/Pycnonotus_jocosus.chrom.sizes              2719075
for m in macros micros sex; do get "$HUB/b10k_model_363_${m}.mod" "data/models/b10k_model_363_${m}.mod" 0; done
get "$NCBI/${A}_genomic.fna.gz"          "data/ncbi/GCA_013400435.1/${A}_genomic.fna.gz"          324574462
get "$NCBI/${A}_genomic.gff.gz"          "data/ncbi/GCA_013400435.1/${A}_genomic.gff.gz"          6289035
get "$NCBI/${A}_protein.faa.gz"          "data/ncbi/GCA_013400435.1/${A}_protein.faa.gz"          3691101
get "$NCBI/${A}_cds_from_genomic.fna.gz" "data/ncbi/GCA_013400435.1/${A}_cds_from_genomic.fna.gz" 7745482
get "$NCBI/md5checksums.txt"             "data/ncbi/GCA_013400435.1/md5checksums.txt"             0
get "$NCBI/${A}_assembly_report.txt"     "data/ncbi/GCA_013400435.1/${A}_assembly_report.txt"     0
echo "== md5 NCBI =="; (cd data/ncbi/GCA_013400435.1 && md5sum -c md5checksums.txt 2>/dev/null | grep -E "genomic.fna.gz|gff.gz|protein.faa.gz|cds_from")
echo "FETCH_EXIT=$?"
