# S1 — Tổng hợp vòng 1 (opus/refiner)

Vai trò: refiner phân tích cho Main. Đọc TOÀN BỘ: `docs/00-tai-dinh-khung-cau-hoi.md`, `docs/02-nguon-du-lieu-va-cong-cu.md`, `research/raw/R1-*.md` … `R5-*.md`, và `research/raw/R6a-*.md`, `R6b-*.md` nếu file không rỗng (khảo sát Google của Gemini — nguồn phụ, chỉ dùng để bổ sung URL, không dùng làm nguồn duy nhất cho claim).

Output: `research/synthesis/00-tong-hop-vong-1.md` (tiếng Việt, ≤3500 từ, đúng 10 mục, đúng thứ tự):

```
## 1. TL;DR (≤12 dòng)
## 2. Trả lời từng câu hỏi Q1–Q6
   Mỗi câu: kết luận 2–3 dòng · 3–6 bằng chứng chính (mỗi bằng chứng: nhãn + nguồn ngắn + R-file nguồn) · chỗ nào tiền đề của chủ dự án cần chỉnh, nói thẳng nhưng tôn trọng
## 3. Sổ giả thuyết H1/H2/H3
   Bảng: dự đoán | bằng chứng đã tìm được (nhãn, R-file) | còn thiếu gì | code nào kiểm được (module pipeline/README.md)
## 4. Bảng dataset D01–D13 cập nhật
   ID | tên | URL đã xác minh | ✔/✘ | license | dung lượng ước lượng | dùng ở pha nào
## 5. Registry gene ứng viên (đầu vào tracker T22 của V4)
   loài | phenotype hoặc hành vi | gene | kiểu di truyền / loại bằng chứng | nguồn | nhãn — gộp từ R2 (màu lông) + R3 (hành vi). Ghi rõ dòng "chào mào: chưa có dữ liệu" nếu đúng vậy.
## 6. CORRECTIONS cho docs/00
   Mọi trích dẫn/số liệu trong docs/00 mà R-file cho thấy sai hoặc không xác minh được (ví dụ R3: "Spottiswoode 2022 Science" thực ra là PNAS; bản Science đúng chủ đề là Merondun 2025). Format: dòng sai → dòng đúng → nguồn.
## 7. Mâu thuẫn giữa các R-file và cách giải quyết
## 8. UNVERIFIED gộp — cần vòng 2 (ưu tiên theo mức ảnh hưởng tới Pha 1)
## 9. Đề xuất Pha 1 cụ thể (5–8 việc)
   Mỗi việc: input | output | công cụ | dung lượng/thời gian ước lượng (từ R5) | tiêu chí xong
## 10. Kết luận T06 cho V4
   khả thi / khả thi có điều kiện / chưa khả thi — điều kiện cụ thể là gì
```

## Luật
- KHÔNG thêm claim mới ngoài nội dung R-file; nếu buộc phải thêm từ kiến thức riêng → nhãn UNVERIFIED + ghi "Main cần kiểm".
- Giữ nguyên nhãn bằng chứng của R-file; không nâng. Hai R-file cùng xác nhận độc lập thì được nâng STRONG_INFERENCE → CONFIRMED, phải ghi rõ hai nguồn.
- Không kể chuyện quá trình. Không sửa file nào khác ngoài output và MỘT dòng thêm vào `tasks/primordial-dna-handoff.md`.
- Không dùng Perplexity, không tìm kiếm mới; đây là bước tổng hợp.

## Khi xong
Trả lời Main ≤10 dòng: số claim gộp theo nhãn · số dataset ✔/✘ · số dòng registry gene · số CORRECTIONS · số mâu thuẫn · số việc Pha 1 · kết luận T06 · đường dẫn file.
