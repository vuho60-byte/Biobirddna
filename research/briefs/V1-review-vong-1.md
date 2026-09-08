# V1 — REVIEW độc lập bản tổng hợp vòng 1 (fresh context)

Vai trò: reviewer chưa từng thấy quá trình. Mục tiêu: tìm chỗ bản tổng hợp nói SAI, nói QUÁ, hoặc BỎ SÓT so với nguồn thô — không viết lại bản tổng hợp.

## Đọc
1. `research/synthesis/00-tong-hop-vong-1.md` (đối tượng review)
2. `research/raw/R1-*.md` … `R5-*.md`, `R6a-*.md`, `R6b-*.md` (nguồn thô — sự thật nằm ở đây)
3. `docs/00-tai-dinh-khung-cau-hoi.md` (để kiểm mục CORRECTIONS có đủ không)
4. `tasks/primordial-dna-plan.md` mục ACCEPTANCE_CRITERIA
5. `docs/03-suy-luan-nguon-goc-chao-mao.md` (đối tượng review thứ hai) đối chiếu `research/raw/R7-*.md`, `R2-*.md`, `R4-*.md`

## Kiểm (mỗi mục ghi PASS/FAIL + bằng chứng dòng cụ thể)
- K1 Nâng nhãn trái phép: claim nào trong tổng hợp mang nhãn cao hơn nhãn trong R-file gốc (trừ khi ghi rõ 2 nguồn độc lập từ 2 R-file).
- K2 Claim không có trong R-file nào và không đánh UNVERIFIED + "Main cần kiểm".
- K3 Số liệu/tên/năm/tạp chí chép sai so với R-file (lấy 10 claim ngẫu nhiên ở mục 2 và 5 dòng ở mục 5 để đối chiếu).
- K4 Bỏ sót: điểm quan trọng trong R-file (đặc biệt R5 mục 1 assembly, R2 mục 7 catalog, R3 mục 6–7 gene, R4 mục 4 H3) không xuất hiện trong tổng hợp.
- K5 Mục 6 CORRECTIONS có bắt hết lỗi trong docs/00 mà R-file đã chỉ ra không (tối thiểu: Spottiswoode 2022 tạp chí; kiểm thêm các trích dẫn khác trong docs/00 Q3/Q4 đối chiếu R2/R4).
- K6 Mục 9 Pha 1: mỗi việc có input/output/công cụ/tiêu chí xong; có việc nào bất khả thi theo R5 không.
- K7 Mâu thuẫn nội bộ trong bản tổng hợp (mục 2 nói A, mục 3 nói B).
- K8 Tiêu chí chấp nhận trong plan: đạt/không đạt từng dòng.
- K9 docs/03: mọi claim có nhãn C/S/U có đúng nhãn và đúng nội dung so với R7/R2/R4 không; mục E (giả thuyết H3) có trung lập không (không mỉa mai, không bênh); có claim nào không truy được về R-file mà thiếu nhãn U không; lập luận mục C và D có mâu thuẫn nội bộ không.

## Output
Ghi `research/synthesis/01-review-vong-1.md`:
```
STATUS: PASS | NEEDS_FIX | BLOCKED
FINDINGS: bảng | # | K | Mức (BLOCKER/HIGH/MEDIUM/LOW) | Vị trí (file:mục) | Vấn đề | Bằng chứng từ R-file | Sửa thế nào |
REQUIRED_FIX: danh sách sửa bắt buộc (BLOCKER/HIGH) để đạt PASS
RECHECK: cách kiểm lại sau khi sửa
```
Thêm đúng 1 dòng vào `tasks/primordial-dna-handoff.md`. Không sửa file nào khác. Không tìm kiếm mới.

Trả lời Main ≤10 dòng: STATUS (tổng hợp) · STATUS (docs/03) · số finding theo mức · K nào FAIL · đường dẫn file.
