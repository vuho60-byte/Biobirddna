# X2 — Sửa A2 sau review + tích hợp map theo mảnh và tham số nhạy

Chỉ sửa trong `pipeline/p02_core_map/**`. Đọc trước: `research/synthesis/05-review-code-x1.md` (REQUIRED_FIX), `docs/04-ke-hoach-tach-adn-goc.md` mục 10 (số liệu benchmark), `pipeline/p02_core_map/run_minimap_chunks.sh` và `split_fasta.py` (Main viết tạm, được phép tích hợp/thay).

## Việc
1. Áp toàn bộ REQUIRED_FIX của review: `annotate` xử lý feature `pseudogene` (thân pseudogene ngoài exon → `intron`; gene_name lấy `Name`/`gene` attribute, fallback ID); thêm test gene chồng tọa độ cùng scaffold; test tie-break `nmatch`/`alnlen` cho paf2bed; `step_needed` ghi tham số vào file `.params` cạnh output và chạy lại khi tham số đổi.
2. `run_a2.sh`: bỏ đường `-I` làm mặc định; mặc định mới = chia genome thành mảnh `--chunk-bases 180000000` bằng `split_fasta.py` (bỏ qua nếu đã có mảnh), map từng mảnh với **`minimap2 -x asm20 -k 13 -w 5 -s 30 -m 20 -n 2 -t <T> --secondary=no -c`**, nối PAF (giữ hành vi `paf2bed` chọn hit tốt nhất qua các mảnh). Tham số `-k/-w/-s/-m/-n` cấu hình được qua `--mm-extra "<chuỗi>"`. Giữ `--chrom`, `--force`, log thời gian từng mảnh. Xóa mảnh sau khi xong nếu `--clean-chunks`.
3. `paf2bed --stats`: thêm bảng `mapped_pct theo qlen_bin` (mapped/total mỗi bin) — hiện chỉ có count của hit.
4. Cập nhật README (tham số mới, lý do: OOM với `-I` ở VM 2 GB; kết quả thí nghiệm). Chạy unittest sạch; `bash -n run_a2.sh`.

## Cấm
Không chạy docker/minimap2 thật trong bước này (Main chạy). Không sửa file ngoài thư mục. Không dependency ngoài stdlib.

## Trả về ≤8 dòng
file sửa/tạo · dòng tổng kết unittest · xác nhận từng mục 1–4 · giả định.
