# V2 — Review chéo bài A1 của Antigravity (nhãn bằng chứng + nguồn)

Đối tượng: `research/raw/A1-antigravity-gene-interpretation.md` (Antigravity viết, 29 KB).
Bạn là reviewer độc lập của Claude team. Việc của bạn là **kiểm nhãn và nguồn**, không viết lại bài.

## Bối cảnh luật nhãn (project)
`CLAUDE.md` quy định: **C (CONFIRMED)** = ≥2 nguồn độc lập hoặc 1 nguồn đã đọc trực tiếp có thiết kế tự kiểm chứng; **S (STRONG_INFERENCE)** = 1 nguồn tốt; **U (UNVERIFIED)** = chưa có nguồn, phải nói rõ. Vòng 1 đã có tiền lệ: cùng một bài báo không đủ làm "hai nguồn độc lập" (xem `research/synthesis/01-review-vong-1.md` finding F01/F06).

## Số liệu đáng nghi (Main đếm trước)
Bài có **62 nhãn [C]**, **17 nhãn [S]**, **0 nhãn [U]**, nhưng chỉ liệt kê **22 URL** ở mục 6. Nghi vấn: nâng nhãn hàng loạt.

## Kiểm (mỗi mục PASS/FAIL + trích dòng cụ thể)
- K1 **Tỉ lệ nhãn**: đếm lại chính xác số [C]/[S]/[U]; với mỗi [C], truy xem bài có dẫn ≥2 nguồn phân biệt cho đúng claim đó không (không tính hai lần cùng một bài, không tính "kiến thức chung"). Liệt kê các [C] không đủ căn cứ → phải hạ xuống [S] hoặc [U].
- K2 **URL**: mở từng URL trong mục 6 (WebFetch). Ghi rõ: mở được / hỏng / chuyển hướng; nội dung có đúng chủ đề được viện dẫn không. URL bịa hoặc không khớp nội dung là finding HIGH.
- K3 **Claim không nguồn**: câu nào mang số liệu hoặc khẳng định cơ chế mà không có URL/tên bài nào phía sau → phải là [U].
- K4 **Đối chiếu số liệu dự án**: bài trích các con số của dự án (531.189 phần tử; 39.826 ánh xạ; 22,6% CDS; 10,5% intron; 66,9% liên gene; danh sách 10 gene và bp). So với `docs/04-ke-hoach-tach-adn-goc.md` mục 10b — có chép sai không.
- K5 **Trung lập H1/H2**: mục 4 có nghiêng về một giả thuyết mà thiếu căn cứ không; có nêu đủ giới hạn không.
- K6 **Giá trị dùng được**: ba cảnh báo phương pháp ở mục 5 (hiệu ứng chiều dài gene, gán vùng liên gene cho gene gần nhất, chất lượng annotation) — có đúng và có áp dụng được vào code của dự án không? Đề xuất cụ thể: cần thêm phép chuẩn hóa nào vào `pipeline/p02_core_map/summarize_a2.py` (ví dụ mật độ base lõi trên mỗi kb chiều dài gene, so với phân phối nền).

## Output
Ghi `research/synthesis/06-review-A1.md`:
```
STATUS: PASS | NEEDS_FIX | BLOCKED
BẢNG NHÃN: | # | claim (trích ngắn) | nhãn bài ghi | nhãn đúng | lý do |
BẢNG URL:  | # | URL | mở được? | khớp nội dung? |
FINDINGS:  | # | K | mức (BLOCKER/HIGH/MEDIUM/LOW) | vấn đề | sửa thế nào |
KẾT LUẬN DÙNG ĐƯỢC GÌ: phần nào của A1 dùng được ngay cho báo cáo LÕI v0, phần nào phải hạ nhãn trước khi dùng
ĐỀ XUẤT CODE: phép chuẩn hóa cần thêm (mục K6), viết dưới dạng đặc tả ngắn cho lập trình viên
```
Thêm đúng 1 dòng vào `tasks/primordial-dna-handoff.md`. Không sửa `research/raw/A1-*.md` (luật: raw không sửa tay). Không sửa file khác.

## Giới hạn
Được dùng WebFetch để mở URL trong bài; **không** dùng Perplexity; không tìm nguồn mới ngoài việc xác minh URL đã có.

## Trả về ≤10 dòng
STATUS · số [C] phải hạ nhãn · số URL hỏng/không khớp · số finding theo mức · phần dùng được ngay · đường dẫn file.
