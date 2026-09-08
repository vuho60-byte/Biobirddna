# T-C2 — locus-c (tiếp tục): hoàn tất 20 locus, viết báo cáo 04

Repo: `D:\BIRDBIODNA project`. Phiên trước teammate locus-c bị ngắt giữa chừng (phiên Claude tắt), chưa ghi báo cáo và handoff. Đọc brief gốc `research/briefs/T-C-locus-c.md` (luật, format, giới hạn giữ nguyên) rồi tiếp tục từ trạng thái hiện có — **không làm lại từ đầu**.

## Trạng thái đã có (kiểm trước khi làm)
- `pipeline/p03_asr/fetch_coords.py`, `pipeline/p03_asr/extract_locus.py` — đọc để hiểu cách dùng; chạy `--help`.
- `data/c_loci/<GENE>/` đã có cho 10 gene: ADCYAP1, ASIP, BMP4, CALM1, CREB1, CRY4, FOXP2, KITLG, MLPH, NPAS2. Với mỗi thư mục: kiểm có `<GENE>.cds363.fa` (363 hàng, có `Pycnonotus_jocosus`) và `<GENE>.blocks.tsv` chưa; thiếu gì thì chạy bổ sung.
- `data/c_loci/loci_galGal4.tsv` có thể đã có một phần — bổ sung các gene còn thiếu.

## Việc
1. Hoàn tất 10 gene còn lại theo danh sách brief gốc (mục 1): MC1R, TYR, SLC45A2, PMEL, TYRP1, SOX10, OCA2, CLOCK, DRD4, SLC6A4, SHH (chọn đủ 10; gene không có trên galGal4 → thay bằng gene khác trong registry `research/synthesis/00-tong-hop-vong-1.md` mục 5, ghi lý do).
2. Kiểm nhanh 3 gene (mục 4 brief gốc). Tổng `data/c_loci` < 400 MB; RAM: xử lý theo luồng; `MSYS_NO_PATHCONV=1` trước `docker run`; chỉ đọc bigMaf theo vùng.
3. Viết `research/synthesis/04-locus-c-v0.md` theo mục 5 brief gốc; thêm 1 dòng `tasks/primordial-dna-handoff.md`.

## Cấm
Pull image · tải file > 50 MB · Perplexity · sửa file ngoài `data/c_loci/**`, `pipeline/p03_asr/**`, `research/synthesis/04-locus-c-v0.md`, 1 dòng handoff.

## Trả về ≤10 dòng
số gene có tọa độ / 20 · số gene rút xong · tổng bp CDS · % loài có dữ liệu trung bình · % gap chào mào trung bình · dung lượng `data/c_loci` · DONE/BLOCKED · đường dẫn.
