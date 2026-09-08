#!/usr/bin/env bash
# run_a2.sh -- wrapper loi A2: vung bao ton 363 loai chim -> toa do chao mao.
# Chay tren Git Bash Windows. Thu tu:
#   bigBedToBed (docker, stdout) | merge (python)
#   -> twoBitToFa -bed=elements.bed (docker)
#   -> split_fasta.py (python, chia bo gene chao mao thanh manh <=chunk-bases)
#   -> minimap2 -x asm20 (docker, 1 lan / manh, noi PAF lai)
#   -> paf2bed (python, chon hit tot nhat qua CA CAC MANH)
#   -> annotate (python)
#
# KHONG ghi all.bed 1,4 GB trung gian: bigBedToBed pipe thang vao
# `conserved_to_bulbul.py merge --in -` qua stdout/stdin.
#
# Moi buoc ghi START/END/SKIP vao data/a2/run.log. Bo qua buoc da co du
# output VA tham so lan truoc khong doi (moi buoc co 1 file "<output>.params"
# canh no; --force bo qua ca 2 dieu kien, luon chay lai). --chrom X loc
# all.bed theo NST X truoc merge de benchmark (khong tao file all.bed, loc
# ngay tren pipe).
#
# Lich su: ban dau chay minimap2 1 lan tren toan bo genome chao mao voi
# `-I <size>` de chia index thanh lo (VM Docker ~2GB RAM). Da OOM (exit 137)
# ngay ca voi `-I 200M`/4 thread khi xay lo index thu 2 (xem docs/04 muc 9).
# Mac dinh moi (docs/04 muc 10): chia FILE FASTA thanh manh <=180 Mbp bang
# split_fasta.py TRUOC (moi manh index nguyen khoi, khong dung -I nua), map
# tung manh rieng roi noi PAF - khong OOM, 6 manh chay het 38s. Tham so seed
# `-k 13 -w 5 -s 30 -m 20 -n 2` (thay vi asm20 mac dinh `-k19 -w10 -s200`) vi
# thi nghiem 15.000 phan tu cho thay asm20 mac dinh chi can 0,92% (do nhay
# seed qua thap voi phan tu ngan sau merge), con bo tham so nay dat 84,3% o
# bin 200-499bp (xem docs/04 muc 10 bang thi nghiem day du).
#
# Cac docker image (tag dung nguyen van, xem research/briefs/X1-*.md):
#   quay.io/biocontainers/ucsc-bigbedtobed:482--h0b57e2e_0
#   quay.io/biocontainers/ucsc-twobittofa:482--hdc0a859_0
#   quay.io/biocontainers/minimap2:2.30--h577a1d6_0
set -euo pipefail

usage() {
  cat <<'EOF'
Dung: run_a2.sh [tuy chon]

Tuy chon:
  --chrom CHROM         Chi chay tren 1 NST ga (vd chr1) de benchmark; loc
                         ngay tren pipe bigBedToBed, khong ghi all.bed.
  --force                Chay lai moi buoc du output (va tham so) da khop.
  --threads N             So luong thread minimap2 (mac dinh: so CPU - 2,
                         hoac 12 neu khong doc duoc so CPU).
  --chunk-bases N         So base toi da moi manh khi chia bo gene chao mao
                         bang split_fasta.py (mac dinh 180000000 = 180 Mbp;
                         xem docs/04 muc 9-10: tranh OOM tren VM Docker ~2GB).
  --mm-extra "CHUOI"      Tham so seed minimap2 them vao sau `-x asm20`, ap
                         dung cho MOI manh (mac dinh "-k 13 -w 5 -s 30 -m 20
                         -n 2", ket qua thi nghiem tot nhat trong docs/04
                         muc 10). Vi du: --mm-extra "-k 15 -w 7 -s 30 -m 20 -n 2".
  --clean-chunks          Xoa thu muc manh genome (data/a2/genome_chunks) sau
                         khi map xong toan bo cac manh (tiet kiem dia; lan
                         chay sau se phai chia manh lai).
  --min-identity F       Nguong identity cho paf2bed (mac dinh 0.70).
  --min-coverage F       Nguong coverage cho paf2bed (mac dinh 0.80).
  --gap N                --gap cho lenh merge (mac dinh 10).
  --min-len N             --min-len cho lenh merge (mac dinh 20).
  --data-dir DIR          Thu muc data/ (mac dinh <repo>/data).
  -h, --help              In huong dan nay va thoat (khong dung docker).
EOF
}

CHROM=""
FORCE=0
THREADS="${THREADS:-}"
CHUNK_BASES="${CHUNK_BASES:-180000000}"
MM_EXTRA="${MM_EXTRA:-"-k 13 -w 5 -s 30 -m 20 -n 2"}"
CLEAN_CHUNKS=0
MIN_IDENTITY="${MIN_IDENTITY:-0.70}"
MIN_COVERAGE="${MIN_COVERAGE:-0.80}"
GAP="${GAP:-10}"
MIN_LEN="${MIN_LEN:-20}"
DATA_DIR_OVERRIDE=""

while [ $# -gt 0 ]; do
  case "$1" in
    --chrom) CHROM="$2"; shift 2 ;;
    --force) FORCE=1; shift ;;
    --threads) THREADS="$2"; shift 2 ;;
    --chunk-bases) CHUNK_BASES="$2"; shift 2 ;;
    --mm-extra) MM_EXTRA="$2"; shift 2 ;;
    --clean-chunks) CLEAN_CHUNKS=1; shift ;;
    --min-identity) MIN_IDENTITY="$2"; shift 2 ;;
    --min-coverage) MIN_COVERAGE="$2"; shift 2 ;;
    --gap) GAP="$2"; shift 2 ;;
    --min-len) MIN_LEN="$2"; shift 2 ;;
    --data-dir) DATA_DIR_OVERRIDE="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "run_a2.sh: tuy chon khong biet: $1" >&2; usage >&2; exit 2 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA_DIR="${DATA_DIR_OVERRIDE:-$PROJECT_DIR/data}"
OUT_DIR="$DATA_DIR/a2"
LOG="$OUT_DIR/run.log"
PY="$SCRIPT_DIR/conserved_to_bulbul.py"
SPLIT_PY="$SCRIPT_DIR/split_fasta.py"

CONSERVED_BB="/data/ucsc/ancRep_separate_models_rev.bw.conserved.bb"
CHICKEN_2BIT="/data/ucsc/Gallus_gallus.2bit"
BULBUL_FNA_HOST="$DATA_DIR/ncbi/GCA_013400435.1/GCA_013400435.1_ASM1340043v1_genomic.fna.gz"
BULBUL_GFF_HOST="$DATA_DIR/ncbi/GCA_013400435.1/GCA_013400435.1_ASM1340043v1_genomic.gff.gz"

IMG_BIGBEDTOBED="quay.io/biocontainers/ucsc-bigbedtobed:482--h0b57e2e_0"
IMG_TWOBITTOFA="quay.io/biocontainers/ucsc-twobittofa:482--hdc0a859_0"
IMG_MINIMAP2="quay.io/biocontainers/minimap2:2.30--h577a1d6_0"

mkdir -p "$OUT_DIR"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"
}

params_file_for() {
  # params_file_for FILE -> ten file ".params" canh FILE, noi step_needed/
  # save_params doc-ghi tham so da dung o lan chay gan nhat cua buoc do.
  echo "${1}.params"
}

step_needed() {
  # step_needed PARAMS_FILE PARAMS_STR FILE...  -> "true" (return 0, can
  # chay) neu FORCE=1, thieu 1 FILE bat ky, HOAC tham so PARAMS_STR khac lan
  # chay truoc (doc tu PARAMS_FILE). Chi doc, KHONG tu ghi PARAMS_FILE - goi
  # save_params sau khi buoc chay xong thanh cong (tranh danh dau "da chay
  # dung tham so" khi buoc bi loi giua chung, vd docker crash).
  local pf="$1" ps="$2"
  shift 2
  if [ "$FORCE" -eq 1 ]; then
    return 0
  fi
  for f in "$@"; do
    [ -f "$f" ] || return 0
  done
  if [ -f "$pf" ] && [ "$(cat "$pf")" = "$ps" ]; then
    return 1
  fi
  return 0
}

save_params() {
  # save_params PARAMS_FILE PARAMS_STR -> ghi tham so dung o lan chay nay.
  printf '%s' "$2" > "$1"
}

win_path() {
  # Chuyen duong dan POSIX (git bash) sang duong dan Windows that su, dung
  # cho ve trai cua -v khi da tat auto-convert bang MSYS_NO_PATHCONV=1.
  if command -v cygpath >/dev/null 2>&1; then
    cygpath -w "$1"
  else
    echo "run_a2.sh: khong tim thay cygpath (can Git Bash / MSYS2) de doi duong dan cho docker -v" >&2
    exit 3
  fi
}

WIN_DATA_DIR="$(win_path "$DATA_DIR")"

CPU_COUNT="$(nproc 2>/dev/null || echo 0)"
if [ "$CPU_COUNT" -gt 2 ] 2>/dev/null; then
  DEFAULT_THREADS=$((CPU_COUNT - 2))
else
  DEFAULT_THREADS=12
fi
THREADS="${THREADS:-$DEFAULT_THREADS}"

ELEMENTS_BED="$OUT_DIR/elements.bed"
MERGE_STATS="$OUT_DIR/merge_stats.tsv"
ELEMENTS_FA="$OUT_DIR/elements.fa"
ELEMENTS_PAF="$OUT_DIR/elements.paf"
GENOME_CHUNKS_DIR="$OUT_DIR/genome_chunks"
SPLIT_MARKER="$GENOME_CHUNKS_DIR/.split_done"
BULBUL_CORE_BED="$OUT_DIR/bulbul_core.bed"
UNMAPPED_TXT="$OUT_DIR/unmapped.txt"
MAP_STATS="$OUT_DIR/map_stats.tsv"
CORE_ANNOT_TSV="$OUT_DIR/core_annot.tsv"
ANNOT_STATS="$OUT_DIR/annot_stats.tsv"

log "=== run_a2.sh bat dau (chrom=${CHROM:-ALL} force=$FORCE threads=$THREADS chunk-bases=$CHUNK_BASES mm-extra=\"$MM_EXTRA\") ==="

# --- Buoc 1: bigBedToBed | (loc --chrom) | merge ---------------------------
MERGE_PARAMS_FILE="$(params_file_for "$ELEMENTS_BED")"
MERGE_PARAMS_STR="gap=$GAP min_len=$MIN_LEN chrom=${CHROM:-ALL}"
if step_needed "$MERGE_PARAMS_FILE" "$MERGE_PARAMS_STR" "$ELEMENTS_BED" "$MERGE_STATS"; then
  log "STEP bigbedtobed_merge START"
  if [ -n "$CHROM" ]; then
    MSYS_NO_PATHCONV=1 docker run --rm -v "${WIN_DATA_DIR}:/data" "$IMG_BIGBEDTOBED" \
        bigBedToBed "$CONSERVED_BB" stdout \
      | awk -F'\t' -v c="$CHROM" 'BEGIN{OFS="\t"} $1==c' \
      | python -B "$PY" merge --in - --out "$ELEMENTS_BED" --gap "$GAP" --min-len "$MIN_LEN" --stats "$MERGE_STATS"
  else
    MSYS_NO_PATHCONV=1 docker run --rm -v "${WIN_DATA_DIR}:/data" "$IMG_BIGBEDTOBED" \
        bigBedToBed "$CONSERVED_BB" stdout \
      | python -B "$PY" merge --in - --out "$ELEMENTS_BED" --gap "$GAP" --min-len "$MIN_LEN" --stats "$MERGE_STATS"
  fi
  save_params "$MERGE_PARAMS_FILE" "$MERGE_PARAMS_STR"
  log "STEP bigbedtobed_merge END"
else
  log "STEP bigbedtobed_merge SKIP (output + tham so da khop; dung --force de chay lai)"
fi

# --- Buoc 2: twoBitToFa -bed=elements.bed -----------------------------------
TWOBIT_PARAMS_FILE="$(params_file_for "$ELEMENTS_FA")"
TWOBIT_PARAMS_STR="fixed"
if step_needed "$TWOBIT_PARAMS_FILE" "$TWOBIT_PARAMS_STR" "$ELEMENTS_FA"; then
  log "STEP twobittofa START"
  MSYS_NO_PATHCONV=1 docker run --rm -v "${WIN_DATA_DIR}:/data" "$IMG_TWOBITTOFA" \
    twoBitToFa "$CHICKEN_2BIT" "/data/a2/elements.fa" -bed="/data/a2/elements.bed"
  save_params "$TWOBIT_PARAMS_FILE" "$TWOBIT_PARAMS_STR"
  log "STEP twobittofa END"
else
  log "STEP twobittofa SKIP (output da ton tai; dung --force de chay lai)"
fi

# --- Buoc 3: chia bo gene chao mao thanh manh, minimap2 tung manh, noi PAF --
# Khong con dung `-I <size>` (OOM tren VM ~2GB RAM voi genome nguyen khoi -
# xem docs/04 muc 9). Mac dinh moi: split_fasta.py chia truoc thanh manh
# <=chunk-bases, moi manh index nguyen khoi roi map, noi PAF lai. paf2bed van
# tu chon hit tot nhat qua CAC MANH (co che best[qname] hien co, khong doi).
SPLIT_PARAMS_FILE="$(params_file_for "$SPLIT_MARKER")"
SPLIT_PARAMS_STR="chunk_bases=$CHUNK_BASES"
if step_needed "$SPLIT_PARAMS_FILE" "$SPLIT_PARAMS_STR" "$SPLIT_MARKER"; then
  log "STEP split_genome START (chunk-bases=$CHUNK_BASES)"
  rm -rf "$GENOME_CHUNKS_DIR"
  mkdir -p "$GENOME_CHUNKS_DIR"
  python -B "$SPLIT_PY" --in "$BULBUL_FNA_HOST" --out-dir "$GENOME_CHUNKS_DIR" --max-bases "$CHUNK_BASES" 2>&1 | tee -a "$LOG"
  touch "$SPLIT_MARKER"
  save_params "$SPLIT_PARAMS_FILE" "$SPLIT_PARAMS_STR"
  log "STEP split_genome END"
else
  log "STEP split_genome SKIP (da co manh voi cung chunk-bases; dung --force de chia lai)"
fi

PAF_PARAMS_FILE="$(params_file_for "$ELEMENTS_PAF")"
PAF_PARAMS_STR="chunk_bases=$CHUNK_BASES mm_extra=$MM_EXTRA threads=$THREADS"
if step_needed "$PAF_PARAMS_FILE" "$PAF_PARAMS_STR" "$ELEMENTS_PAF"; then
  log "STEP minimap2_chunks START (threads=$THREADS mm-extra=\"$MM_EXTRA\")"
  PAF_TMP="$ELEMENTS_PAF.tmp"
  : > "$PAF_TMP"
  shopt -s nullglob
  chunks=("$GENOME_CHUNKS_DIR"/chunk_*.fa)
  shopt -u nullglob
  if [ "${#chunks[@]}" -eq 0 ]; then
    echo "run_a2.sh: khong tim thay manh nao trong $GENOME_CHUNKS_DIR (split_genome that bai?)" >&2
    exit 4
  fi
  for chunk in "${chunks[@]}"; do
    cb="$(basename "$chunk")"
    t0=$(date +%s)
    log "CHUNK $cb START"
    MSYS_NO_PATHCONV=1 docker run --rm -v "${WIN_DATA_DIR}:/data" "$IMG_MINIMAP2" \
        minimap2 -x asm20 $MM_EXTRA -t "$THREADS" --secondary=no -c \
        "/data/a2/genome_chunks/$cb" "/data/a2/elements.fa" >> "$PAF_TMP"
    t1=$(date +%s)
    log "CHUNK $cb END elapsed=$((t1 - t0))s lines=$(wc -l < "$PAF_TMP")"
  done
  mv -f "$PAF_TMP" "$ELEMENTS_PAF"
  save_params "$PAF_PARAMS_FILE" "$PAF_PARAMS_STR"
  log "STEP minimap2_chunks END lines=$(wc -l < "$ELEMENTS_PAF")"

  if [ "$CLEAN_CHUNKS" -eq 1 ]; then
    rm -rf "$GENOME_CHUNKS_DIR"
    rm -f "$SPLIT_PARAMS_FILE"
    log "STEP minimap2_chunks: --clean-chunks da xoa $GENOME_CHUNKS_DIR (lan chay sau se chia manh lai)"
  fi
else
  log "STEP minimap2_chunks SKIP (output + tham so da khop; dung --force de chay lai)"
fi

# --- Buoc 4: paf2bed --------------------------------------------------------
PAF2BED_PARAMS_FILE="$(params_file_for "$BULBUL_CORE_BED")"
PAF2BED_PARAMS_STR="min_identity=$MIN_IDENTITY min_coverage=$MIN_COVERAGE"
if step_needed "$PAF2BED_PARAMS_FILE" "$PAF2BED_PARAMS_STR" "$BULBUL_CORE_BED" "$UNMAPPED_TXT" "$MAP_STATS"; then
  log "STEP paf2bed START"
  python -B "$PY" paf2bed --paf "$ELEMENTS_PAF" --out "$BULBUL_CORE_BED" \
    --unmapped "$UNMAPPED_TXT" --stats "$MAP_STATS" \
    --min-identity "$MIN_IDENTITY" --min-coverage "$MIN_COVERAGE" \
    --query-list "$ELEMENTS_BED"
  save_params "$PAF2BED_PARAMS_FILE" "$PAF2BED_PARAMS_STR"
  log "STEP paf2bed END"
else
  log "STEP paf2bed SKIP (output + tham so da khop; dung --force de chay lai)"
fi

# --- Buoc 5: annotate --------------------------------------------------------
ANNOT_PARAMS_FILE="$(params_file_for "$CORE_ANNOT_TSV")"
ANNOT_PARAMS_STR="fixed"
if step_needed "$ANNOT_PARAMS_FILE" "$ANNOT_PARAMS_STR" "$CORE_ANNOT_TSV" "$ANNOT_STATS"; then
  log "STEP annotate START"
  python -B "$PY" annotate --bed "$BULBUL_CORE_BED" --gff "$BULBUL_GFF_HOST" \
    --out "$CORE_ANNOT_TSV" --stats "$ANNOT_STATS"
  save_params "$ANNOT_PARAMS_FILE" "$ANNOT_PARAMS_STR"
  log "STEP annotate END"
else
  log "STEP annotate SKIP (output da ton tai; dung --force de chay lai)"
fi

log "=== run_a2.sh xong. Dau ra chinh: $BULBUL_CORE_BED , $CORE_ANNOT_TSV ==="
