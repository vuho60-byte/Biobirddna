#!/usr/bin/env bash
# Thăm dò kích thước + hỗ trợ range của các file dữ liệu từ xa (HEAD, không tải).
# Chạy: bash pipeline/p00_inventory/probe_remote.sh > data/probe-$(date +%F).tsv
HUB="https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020-hub"
NCBI="https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/013/400/435/GCA_013400435.1_ASM1340043v1"
URLS=(
 "https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020.hal"
 "$HUB/Gallus_gallus/ancRep_separate_models_rev.bw.conserved.bb"
 "$HUB/Gallus_gallus/ancRep_separate_models_rev.bw.accelerated.bb"
 "$HUB/Gallus_gallus/ancRep_separate_models_rev.bw"
 "$HUB/Gallus_gallus/chicken.bigMaf.bb"
 "$HUB/Pycnonotus_jocosus/Pycnonotus_jocosus.2bit"
 "$HUB/Pycnonotus_jocosus/Pycnonotus_jocosus.genes.bb"
 "$NCBI/GCA_013400435.1_ASM1340043v1_genomic.fna.gz"
 "$NCBI/GCA_013400435.1_ASM1340043v1_genomic.gff.gz"
 "$NCBI/GCA_013400435.1_ASM1340043v1_protein.faa.gz"
)
printf "date\thttp\tbytes\tranges\turl\n"
for u in "${URLS[@]}"; do
  h=$(curl -sI -L --max-time 30 "$u" | tr -d '\r')
  code=$(printf "%s" "$h" | grep -iE "^HTTP/" | tail -1 | awk '{print $2}')
  len=$(printf "%s" "$h" | grep -i "^content-length" | tail -1 | awk '{print $2}')
  rng=$(printf "%s" "$h" | grep -i "^accept-ranges" | tail -1 | awk '{print $2}')
  printf "%s\t%s\t%s\t%s\t%s\n" "$(date +%F)" "${code:-ERR}" "${len:-?}" "${rng:-none}" "$u"
done
