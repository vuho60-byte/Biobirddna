# X5 — Lệnh `enrich`: kiểm định gene giàu lõi so với nền, và đối chứng âm bằng bộ accelerated

Chỉ sửa/tạo trong `pipeline/p02_core_map/**`. **Không có bất kỳ lệnh xóa nào** trong code hay script (luật project). Không chạy docker. Python 3.11 **stdlib** (được dùng `math`, `statistics`; không numpy/scipy).

## Vì sao
Hiện xếp hạng gene theo tổng bp lõi và theo mật độ bp/kb. Cả hai chưa trả lời được câu "gene này giàu lõi **hơn mong đợi** hay không". Đặc tả lấy từ `research/raw/A2-antigravity-null-model.md` (đọc trước, mục 1 và 2):
- Kiểm định tỷ lệ nền: so tỷ lệ bp lõi của gene với xác suất nền P₀ = tổng bp lõi / tổng bp không gian xét.
- Đối chứng âm: gene chịu ràng buộc thật phải giàu vùng **conserved** nhưng KHÔNG giàu vùng **accelerated**. Gene giàu cả hai là dấu hiệu artifact (locus khổng lồ, điểm nóng tái tổ hợp).

## Việc
Thêm lệnh con `enrich` vào `pipeline/p02_core_map/conserved_to_bulbul.py`:

```
enrich --annot core_annot.tsv [--annot-accel core_annot_accel.tsv]
       --gff genomic.gff.gz --genome-size N | --chrom-sizes FILE
       --out gene_enrichment.tsv [--stats enrich_stats.tsv]
       [--min-gene-len 1000] [--min-bp 200] [--fdr 0.05]
```

Yêu cầu tính:
1. **P₀** = (tổng bp lõi trong `--annot`) / (tổng bp không gian). Không gian lấy từ `--genome-size` hoặc tổng cột 2 của `--chrom-sizes`. Ghi P₀ vào stats.
2. Cho mỗi gene có `gene_len ≥ --min-gene-len` và `bp ≥ --min-bp`:
   - `bp_obs` (bp lõi rơi vào gene), `gene_len`, `bp_exp = P₀ × gene_len`, `fold = bp_obs / bp_exp`.
   - **p-value một phía (giàu hơn nền)** theo mô hình nhị thức: số "thành công" = `bp_obs`, số phép thử = `gene_len`, xác suất = P₀. Vì `gene_len` lớn (10⁴–10⁶), tính chính xác bằng tổng nhị thức là không khả thi → dùng **xấp xỉ chuẩn có hiệu chỉnh liên tục** (`statistics.NormalDist`), và ghi rõ trong README rằng đây là xấp xỉ; nếu `gene_len × P₀ < 10` thì đánh dấu cột `approx_warn=1`.
   - Ghi chú quan trọng phải nêu trong README: các base trong một vùng lõi **không độc lập** nên p-value nhị thức là *chống chỉ định về mặt thống kê chặt*; nó chỉ dùng để **xếp hạng**, không dùng để tuyên bố ý nghĩa thống kê. Đặt tên cột là `rank_score_p` chứ không phải `pvalue` để không gây hiểu nhầm.
3. **Hiệu chỉnh đa kiểm định** Benjamini–Hochberg trên `rank_score_p` → cột `bh_q`. Cột `signif_flag` = 1 nếu `bh_q < --fdr` (kèm cảnh báo ở README như trên).
4. Nếu có `--annot-accel` (bảng chú giải chạy trên bộ **accelerated**): thêm `accel_bp`, `accel_fold`, và `ca_ratio = fold / accel_fold` (khi `accel_fold > 0`; nếu `accel_bp = 0` ghi `inf`). Xếp hạng phụ theo `ca_ratio`.
5. `--stats` xuất: P₀, tổng bp lõi, tổng bp không gian, số gene xét, số gene qua ngưỡng FDR, top 20 theo `fold`, top 20 theo `ca_ratio` (nếu có).

Đầu ra `--out` là TSV có header: `gene_id gene_name bp_obs gene_len bp_exp fold rank_score_p bh_q signif_flag approx_warn [accel_bp accel_fold ca_ratio]`, sắp theo `fold` giảm dần.

## Test (`tests/test_enrich.py`, unittest thuần, dữ liệu nhúng)
- P₀ tính đúng từ `--genome-size` và từ `--chrom-sizes`.
- Gene có `bp_obs` đúng bằng kỳ vọng → `fold ≈ 1`, `rank_score_p` gần 0,5, không qua ngưỡng.
- Gene giàu rõ rệt → `fold > 1`, `rank_score_p` nhỏ, qua ngưỡng sau BH.
- BH đúng thứ tự: kiểm bằng bộ p-value đặt sẵn (so với giá trị tính tay).
- Lọc theo `--min-gene-len` / `--min-bp` hoạt động.
- `ca_ratio`: gene giàu conserved nhưng nghèo accelerated có `ca_ratio` cao; gene giàu cả hai có `ca_ratio ≈ 1`; `accel_bp = 0` cho `inf`.
- `approx_warn` bật khi `gene_len × P₀ < 10`.

## Tiêu chí xong
- `python -B -m unittest discover -s pipeline/p02_core_map/tests -v` sạch (26+ test, gồm 22 test cũ vẫn PASS).
- `--help` của `enrich` thoát 0.
- README `pipeline/p02_core_map/README.md` thêm mục "Kiểm định giàu lõi so với nền": cách chạy, ý nghĩa cột, **và ba cảnh báo** (base không độc lập; nearest-gene fallacy; bảo tồn tổ tiên ≠ đặc thù chào mào — lấy từ A2 mục 3).
- Thêm đúng 1 dòng `tasks/primordial-dna-handoff.md`.

## Trả về ≤10 dòng
file sửa · dòng tổng kết unittest · xác nhận không lệnh xóa · tên cột đầu ra · giả định.
