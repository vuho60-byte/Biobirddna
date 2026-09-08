# X3 — Codex: sửa lỗi bỏ-qua-bước của A2, tái tạo output toàn genome, tóm tắt

Repo: `D:\BIRDBIODNA project` (Windows; Git Bash + Docker Desktop; VM Docker 2 GB RAM). Chỉ được ghi trong `pipeline/p02_core_map/**` và `data/a2/**`. Không đụng `data/a2_chr1/` (kết quả chr1 đã lưu), không đụng file khác. Không tải file mới, không pull image.

## Bối cảnh
- `pipeline/p02_core_map/run_a2.sh` có cơ chế `step_needed`/`save_params` ghi file `<output>.params` để bỏ qua bước đã chạy. **Lỗi:** chuỗi tham số không chứa danh tính của INPUT (kích thước/mtime hoặc sha), nên khi input đổi (chạy chr1 rồi chạy toàn genome trong cùng `data/a2`) các bước `paf2bed`/`annotate` bị SKIP và output cũ của chr1 còn nguyên. Xem `data/a2_full.log` dòng cuối: `STEP annotate SKIP (output da ton tai...)`.
- Toàn genome đã có: `data/a2/elements.bed` (2.947.588 phần tử, `merge_stats.tsv` đúng), `elements.fa`, `elements.paf` (map 12 mảnh, ~420k+ dòng). Cần xác minh từng output còn lại là của toàn genome hay của chr1 (chr1 có `total_queries=531189`).
- Đọc `pipeline/p02_core_map/README.md` và `docs/04-ke-hoach-tach-adn-goc.md` mục 10–10b để biết tham số đã chốt.

## Việc
1. Sửa `step_needed`/`save_params`: chuỗi params của mỗi bước phải gồm (a) tham số CLI liên quan bước đó, (b) với MỖI input file: đường dẫn + kích thước byte + mtime (hoặc sha256 nếu < 50 MB). Input đổi → chạy lại. Thêm unittest cho hàm này (tách logic ra Python hoặc test bash bằng file tạm — tùy, nhưng phải có test chạy được bằng `python -B -m unittest discover -s pipeline/p02_core_map/tests -v`).
2. Trong `data/a2`: xác định output nào cũ (so `total_queries`, số dòng, mtime với `elements.paf`). Tái tạo bằng lệnh con Python trực tiếp (không cần docker): `paf2bed` (coverage 0,8 → `bulbul_core.bed`, `map_stats.tsv`, `unmapped.txt`; và coverage 0,5 → `bulbul_core.cov50.bed`, `map_stats.cov50.tsv`, `unmapped.cov50.txt`), rồi `annotate` cho cả hai bộ (`core_annot.tsv`/`annot_stats.tsv` và `core_annot.cov50.tsv`/`annot_stats.cov50.tsv`). Dùng `--query-list data/a2/elements.bed`. Ghi `.params` mới đúng chuẩn.
3. Chạy `python -B pipeline/p02_core_map/summarize_a2.py --dir data/a2 --label "(toàn genome, 2026-09-08)"` và lưu kết quả vào `data/a2/SUMMARY.md`; mở rộng `summarize_a2.py` để in thêm bộ cov50 annotation nếu có file `annot_stats.cov50.tsv`.
4. Tính sha256 cho `bulbul_core.bed`, `bulbul_core.cov50.bed`, `elements.paf` → `data/a2/SHA256SUMS.txt`.
5. Xóa các file benchmark chr1 còn sót trong `data/a2` (`bench-chr1*`, thư mục `exp/`) — chúng đã có bản sao ở `data/a2_chr1` (kiểm tồn tại trước khi xóa; `exp/` chỉ xóa nếu `data/a2_chr1/exp` không tồn tại thì di chuyển sang đó thay vì xóa).

## Tiêu chí xong
- unittest sạch (số test ≥ 18 + test mới); `bash -n run_a2.sh` sạch.
- `data/a2/map_stats.tsv` có `total_queries 2947588`; `SUMMARY.md` có bảng % theo nhóm độ dài cho cả hai coverage; `annot_stats.tsv` phản ánh toàn genome.
- Báo cáo ≤10 dòng: file sửa · unittest · số phần tử căn được (cov 0,8 / 0,5) và bp · top 10 gene · sha256 8 ký tự của 2 BED.
