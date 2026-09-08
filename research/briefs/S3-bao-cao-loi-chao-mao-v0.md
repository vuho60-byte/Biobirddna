# S3 — Viết báo cáo "LÕI chào mào v0" (sản phẩm A + B)

Output: `research/synthesis/03-loi-chao-mao-v0.md` (tiếng Việt). Thêm đúng 1 dòng `tasks/primordial-dna-handoff.md`. Không sửa file khác. **Không chạy lại pipeline** — chỉ đọc kết quả đã có.

## Đọc trước
- `data/a2/SUMMARY.md` (tóm tắt tự sinh), `data/a2/merge_stats.tsv`, `data/a2/map_stats.tsv`, `data/a2/map_stats.cov50.tsv`, `data/a2/annot_stats.tsv`, `data/a2/annot_stats.cov50.tsv`, `data/a2/SHA256SUMS.txt`.
- `docs/04-ke-hoach-tach-adn-goc.md` mục 1 (định nghĩa sản phẩm A/B/C), mục 8, 10, 10b (kết quả chr1 để so sánh).
- `research/raw/A1-antigravity-gene-interpretation.md` **và** `research/synthesis/06-review-A1.md` (review chéo) — chỉ dùng phần review cho phép dùng, giữ đúng nhãn sau review.
- `pipeline/p02_core_map/README.md` mục "Chuẩn hóa mật độ lõi" — bắt buộc đọc **cả hai** bảng gene.

## Cấu trúc bắt buộc (8 mục)
```
## 1. TL;DR (≤10 dòng, có số)
## 2. Cách làm (5–8 dòng: dữ liệu nguồn, công cụ, tham số, phiên bản; dẫn sha256)
## 3. Kết quả A — LÕI-363 trên tọa độ gà
   số khoảng vào, số phần tử sau gộp, tổng bp, phân bố độ dài
## 4. Kết quả B — LÕI trên bộ gene chào mào
   bảng: coverage 0,8 và 0,5 × (số phần tử ánh xạ, %, bp, % bộ gene chào mào 1,02 Gb)
   bảng % ánh xạ theo nhóm độ dài; nhận xét vì sao nhóm ngắn thấp
## 5. LÕI nằm ở đâu trong bộ gene
   bảng feature_class (CDS / exon không mã hóa / intron / liên gene): số vùng, bp, %
   so sánh với kỳ vọng nếu rải ngẫu nhiên (nêu rõ đây là so sánh thô, chưa có mô hình nền)
## 6. Gene chứa nhiều lõi nhất — HAI bảng
   6a. theo tổng bp (top 15)   6b. theo mật độ bp/kb (top 15)
   Nêu rõ hai bảng khác nhau thế nào và vì sao (thiên vị gene dài).
   Nếu review A1 cho phép, thêm 1–2 câu diễn giải chức năng cho gene đứng đầu, giữ nhãn.
## 7. Giới hạn (bắt buộc, mỗi mục 1–2 dòng)
   neo trên gà galGal4 nên mất vùng không align được với gà; nhóm <100 bp gần như chưa ánh xạ;
   assembly chào mào mức scaffold N50 218 kb; gán vùng liên gene cho gene giao nhiều nhất là xấp xỉ;
   chưa có mô hình nền để kiểm định thống kê; chưa dùng bộ accelerated làm đối chứng.
## 8. Việc tiếp theo (5 gạch đầu dòng, mỗi gạch có tiêu chí xong)
```

## Luật
- Mọi con số phải lấy trực tiếp từ file kết quả; **không** làm tròn sai lệch, không tự tính lại theo trí nhớ. Nếu một con số không có trong file, ghi "chưa đo".
- Nhãn bằng chứng C/S/U theo `CLAUDE.md`. Kết quả tính toán của chính dự án ghi là **[đo được]**, không phải C/S/U (nhãn C/S/U dành cho claim lấy từ tài liệu).
- Không dùng cụm "DNA khủng long còn nguyên"; gọi đúng: vùng chịu chọn lọc lọc, bảo tồn từ tổ tiên chung.
- Không kết luận H1/H2/H3 thắng thua; chỉ nêu dữ liệu này phù hợp/không phù hợp dự đoán nào, kèm giới hạn.

## Trả về Main ≤10 dòng
số phần tử lõi · % bộ gene chào mào (2 ngưỡng) · phân bố feature_class · top 3 gene mỗi bảng · số giới hạn đã nêu · đường dẫn file.
