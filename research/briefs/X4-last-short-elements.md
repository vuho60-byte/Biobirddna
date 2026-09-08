# X4 — Bộ căn LAST cho phần tử bảo tồn ngắn (<100 bp)

Repo: `D:\BIRDBIODNA project`. Chỉ được tạo/sửa trong `pipeline/p02b_last/**`. **Không sửa file ngoài thư mục đó. Không chạy docker/LAST thật trong bước này. Không có bất kỳ lệnh xóa nào trong script bạn viết** (luật project, xem `CLAUDE.md`).

## Vì sao cần
minimap2 (kể cả `-k 13 -w 5 -s 30 -m 20 -n 2`) chỉ căn được 0,3% phần tử 20–49 bp và 7,8% phần tử 50–99 bp từ gà sang chào mào (số đo thật, `docs/04` mục 10b). Nhóm này chiếm ~80% số phần tử và ~41% tổng base bảo tồn, nên hiện đang mất. LAST là công cụ chuẩn cho căn trình tự ngắn giữa loài xa nhau.

## Môi trường (đã có sẵn)
- Image đã pull: `quay.io/biocontainers/last:1654--h5814d7d_1` (có `lastdb`, `lastal`, `last-split`, `maf-convert`).
- Docker VM chỉ **2 GB RAM** → phải chia bộ gene chào mào thành mảnh (dùng lại `pipeline/p02_core_map/split_fasta.py`, mặc định `--chunk-bases 90000000`).
- Git Bash: **luôn** `MSYS_NO_PATHCONV=1` trước `docker run`; mount `-v "<đường dẫn Windows>:/data"`; đường dẫn trong container là `/data/...`.
- Đầu vào có sẵn sau khi pipeline A2 chạy: `data/a2/elements.bed` (BED 4 cột, cột 4 = id `chr:start-end`), `data/a2/elements.fa` (FASTA, tên = id).

## Việc
1. `pipeline/p02b_last/short_elements.py` (Python 3.11 **stdlib**), 3 lệnh con:
   - `filter --in-fa elements.fa --in-bed elements.bed --out short.fa --max-len 99 [--min-len 20] --stats filter_stats.tsv` — lọc phần tử ngắn ra FASTA riêng.
   - `maf2bed --maf aln.maf --out bulbul_short.bed --unmapped unmapped_short.txt --stats map_stats_short.tsv --min-identity 0.70 --min-coverage 0.80 --query-list elements.bed` — đọc MAF của LAST (khối `a score=...` + hai dòng `s`), chọn **một** hit tốt nhất mỗi query (ưu tiên score, rồi số base khớp, rồi độ dài align), tính identity = base khớp / độ dài align, coverage = phần query được phủ; xuất BED 6+ **cùng định dạng cột với `pipeline/p02_core_map` (`conserved_to_bulbul.py paf2bed`)** để hai bộ kết quả ghép được với nhau; thống kê có bảng `qlen_bin mapped total mapped_pct`.
   - `merge-beds --in bulbul_core.bed --in bulbul_short.bed --out bulbul_core_all.bed --stats merge_beds_stats.tsv` — gộp hai bộ, loại trùng theo id query (giữ bản có identity cao hơn), báo số trùng.
2. `pipeline/p02b_last/run_last.sh` — quy trình: `filter` → chia mảnh genome (dùng `split_fasta.py`, bỏ qua nếu đã có) → với mỗi mảnh: `lastdb -P <T> -uNEAR <db> <chunk.fa>` rồi `lastal -P <T> -D1e6 <db> short.fa | last-split` → nối MAF → `maf2bed` → `merge-beds`. Tham số cấu hình được: `--threads`, `--chunk-bases`, `--max-len`, `--lastdb-extra`, `--lastal-extra`, `--force`. Ghi log thời gian từng mảnh giống `run_a2.sh`. Áp cùng cơ chế `.params` **có danh tính input** như `run_a2.sh` (xem hàm `input_id` trong file đó — đọc để dùng lại đúng cách).
   Lưu ý bộ nhớ: `lastdb` cho mảnh 90 Mbp với `-uNEAR` có thể vượt 2 GB → thêm tùy chọn `--chunk-bases` nhỏ hơn và ghi rõ trong README rằng nếu container bị giết (exit 137) thì giảm xuống 45000000.
3. `pipeline/p02b_last/tests/test_short_elements.py` — unittest thuần, dữ liệu nhúng: lọc theo độ dài, phân tích MAF (gồm khối nhiều dòng, strand `-`, trường hợp thiếu), chọn hit tốt nhất, ngưỡng identity/coverage, gộp BED loại trùng. Chạy: `python -B -m unittest discover -s pipeline/p02b_last/tests -v`.
4. `pipeline/p02b_last/README.md`: cách chạy, ý nghĩa cột, giới hạn (LAST chậm hơn; phần tử 20–49 bp vẫn có thể mơ hồ; cảnh báo RAM).

## Tiêu chí xong
- unittest sạch; `bash -n run_last.sh` sạch; `--help` của mọi lệnh con thoát 0.
- Không dependency ngoài stdlib; không ghi ra ngoài đường dẫn nhận từ tham số.
- Thêm đúng 1 dòng vào `tasks/primordial-dna-handoff.md`.

## Trả về ≤10 dòng
file tạo · dòng tổng kết unittest · xác nhận không có lệnh xóa trong script · giả định/giới hạn.
