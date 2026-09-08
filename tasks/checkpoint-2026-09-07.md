# Checkpoint cuối ngày 2026-09-07 (23:40) — đọc file này trước khi làm tiếp

## Đang chạy nền khi tạm ngưng (không cần can thiệp)
- A2 toàn genome (pid bash 31180, `pipeline/p02_core_map/launch_full.sh`): đã qua mảnh 7/12 lúc 23:39, ~30 s/mảnh; sau map sẽ tự chạy paf2bed + annotate và xóa `data/a2/genome_chunks`. Log: `data/a2_full.log`, `data/a2_full.err`; dòng cuối phải là `BENCH_EXIT=0`. Output: `data/a2/bulbul_core.bed`, `map_stats.tsv`, `annot_stats.tsv`, `core_annot.tsv`, `unmapped.txt`, `elements.paf`.
- Teammate locus-c (Sonnet, sản phẩm C): ghi `data/c_loci/**`, `pipeline/p03_asr/**`, `research/synthesis/04-locus-c-v0.md`, 1 dòng handoff. Nếu chưa có file → chưa xong hoặc thất bại; kiểm handoff.

## Việc đầu tiên ngày mai
1. `tail -3 data/a2_full.log` → nếu `BENCH_EXIT=0`: chạy `python -B pipeline/p02_core_map/summarize_a2.py --dir data/a2 --label "(toàn genome)"` và `paf2bed --min-coverage 0.5` như đã làm cho chr1 (lệnh trong docs/04 mục 10b) → viết `research/synthesis/03-loi-chao-mao-v0.md` (sản phẩm A+B v0). Nếu 137: thử `-K 5M` hoặc đề nghị nâng `.wslconfig memory=6GB`.
2. Đọc `research/synthesis/04-locus-c-v0.md` nếu có → quyết định pull image IQ-TREE (cần duyệt) cho ASR.
3. Xin duyệt pull image `last` (bioconda) cho phần tử <100 bp (80 % số phần tử, ~41 % base chưa ánh xạ).
4. Cập nhật registry.csv cho output A2 (sha256), Board FINDING, todo.

## Số liệu chốt hôm nay (chr1 gà, docs/04 mục 10–10b)
531.189 phần tử; căn được 39.826 (cov ≥0,8) / 66.799 (cov ≥0,5); 9,8–14,0 Mb trên chào mào; identity p50 0,90; annotation 22 % CDS / 10 % intron / 67 % liên gene; top gene Tenm4, Syn3, Sema3a, Pdzrn4, Celf2, Pcca, Reln, Dlg2, Foxp2, Taf3. Toàn genome: 2.947.588 phần tử, 134,6 Mb base bảo tồn.

## Ràng buộc còn hiệu lực
VM Docker 2 GB (`.wslconfig`), map theo mảnh 90 Mbp, `-k13 -w5 -s30 -m20 -n2 -K 10M -f 0.001`, 2 thread; Codex hết quota tới 12/09; không tải HAL/bigMaf; hook chặn `rm`/Remove-Item trong lệnh PowerShell.
