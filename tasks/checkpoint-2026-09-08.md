# Checkpoint cuối ngày 2026-09-08 — đọc trước khi làm tiếp

## Đã xong hôm nay
1. **Khôi phục project** sau sự cố xóa ổ D (Codex): tái tạo 66 file từ transcript, git init, nay có 10 commit. Codex bị CẤM cho tới khi chủ dự án duyệt lại.
2. **Đội hình mới**: Claude team + Antigravity gọi qua **team MCP** (session `6cb4eb5c-9bf5-4551-a469-f936c1bd34b6`, gọi lại được). teamai đã gỡ khỏi settings.json (backup `.bak-*`).
3. **Vá 2 lỗi gốc**: `.params` nay gồm danh tính input (lỗi khiến kết quả toàn genome 07/09 giữ số liệu chr1); `check_resources.sh` dừng hẳn khi Docker không chạy.
4. **KẾT QUẢ CHÍNH — A2 toàn bộ bộ gene** (20 phút 40 giây, RAM đỉnh 49% trần 1,86 GB):
   - 2.947.588 phần tử bảo tồn → **248.461 ánh xạ (8,43%), 62,49 Mb = 6,10% bộ gene chào mào** (ngưỡng phủ 0,8)
   - nới ngưỡng 0,5: 411.275 phần tử, 88,42 Mb = 8,63%
   - phân bố: CDS 24,3% · intron 11,0% · liên gene 64,7%
   - top theo tổng bp: Znf521, Sox6, Foxp1, Vps13b, Klhl29
   - **top theo mật độ bp/kb: Hoxa5, Hoxa11, Hoxa3, Gpr19, Dolk, Nipbl** (>2.000 bp/kb) — cụm HOX, gene quy định trục cơ thể
   - file: `data/a2/SUMMARY.md`, `map_stats*.tsv`, `annot_stats*.tsv`, `SHA256SUMS.txt`
5. **`enrich`** (kiểm định giàu lõi so với nền, binomial + BH + tỉ số conserved/accelerated): code + test xong, 33 test PASS. README còn dở.
6. **Bộ căn LAST** cho phần tử <100 bp: code + 14 test xong, **chưa chạy thật**.
7. **Review V2 → BLOCKED bài A1 của Antigravity**: 11/22 URL sai chủ đề, 1 URL 404; 53/62 nhãn C phải hạ. Không được dùng A1 trong báo cáo. Chi tiết `research/synthesis/06-review-A1.md`.

## Việc đầu tiên ngày mai (theo thứ tự)
1. Mở Docker Desktop trước (pipeline cần).
2. Hoàn tất README mục "Kiểm định giàu lõi so với nền" (đang dở), rồi **chạy `enrich` thật**:
   - cần chú giải bộ **accelerated** làm đối chứng âm → chạy lại pipeline A2 với `conserved.bb` thay bằng `accelerated.bb` (hoặc thêm cờ), xuất `core_annot_accel.tsv`
   - rồi `enrich --annot core_annot.tsv --annot-accel core_annot_accel.tsv --chrom-sizes data/ucsc/Pycnonotus_jocosus.chrom.sizes`
3. **Viết báo cáo LÕI v0** theo `research/briefs/S3-bao-cao-loi-chao-mao-v0.md` (agent S3 bị dừng trước khi viết). Nhớ: KHÔNG dùng nội dung A1 chưa qua review.
4. Chạy LAST cho nhóm <100 bp (`pipeline/p02b_last/run_last.sh`), gộp BED, cập nhật báo cáo.
5. Chạy lại sản phẩm C (20 locus) — `data/c_loci` mất trong sự cố.

## Ràng buộc còn hiệu lực
- Codex: cấm cho tới khi được duyệt. Không giao thao tác xóa cho bất kỳ agent nào.
- Model ngoài (Antigravity): mọi bài phải qua reviewer mở từng URL trước khi dùng.
- Docker VM 2 GB; minimap2 chạy theo 12 mảnh 90 Mbp, `-k 13 -w 5 -s 30 -m 20 -n 2 -K 10M -f 0.001`, 2 luồng.
- Commit sau mỗi bước có kết quả.
