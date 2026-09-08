# A2 — Antigravity: mô hình nền, đối chứng âm, sai lầm khi công bố

Nguồn: team MCP `ask_antigravity`, session `6cb4eb5c-9bf5-4551-a469-f936c1bd34b6`, run `run_22d9a5b8-a7c1-4a54-8494-00e7a1d62a96`, 2026-09-08, 61 giây. Tiếp nối `A1-antigravity-gene-interpretation.md`.
Câu hỏi của Main: (1) mô hình nền chuẩn ngành để nói "gene X giàu vùng bảo tồn hơn mong đợi", khả thi với dữ liệu đang có; (2) dùng bộ accelerated làm đối chứng âm thế nào; (3) sai lầm phổ biến khi công bố.

---

### 1. Phép so sánh NỀN (null model) chuẩn ngành

Để khẳng định gene X giàu CNE vượt mong đợi ngẫu nhiên (với BED gà, GFF chào mào), 2 cách khả thi và chuẩn ngành gồm:

- **Xáo trộn khoảng không gian (interval permutation / shuffling) [C]:** dùng `bedtools shuffle` xáo trộn các đoạn CNE 1.000–5.000 lần trên không gian nhiễm sắc thể 1 chào mào (loại trừ khoảng trống lắp ráp `N`), giữ nguyên số lượng và phân bố độ dài CNE **[C]**. So sánh số bp thực tế của gene X với phân phối ngẫu nhiên để tính *p-value thực nghiệm* và *fold enrichment* **[C]**.
- **Kiểm định tỷ lệ nền (binomial / Fisher's exact test) [C]:** so sánh tỷ lệ bp CNE của gene X với xác suất nền toàn nhiễm sắc thể 1 (P₀ = tổng bp CNE / tổng bp nhiễm sắc thể) **[C]**. Bộ BED và GFF hiện tại chạy được ngay mà không cần dữ liệu phyloP theo từng base **[S]**.

### 2. Dùng bộ "accelerated" làm đối chứng âm đúng cách

- **Kiểm tra tính đặc hiệu (specificity test) [C]:** gene thực sự chịu ràng buộc bảo tồn sâu (H2) phải giàu CNE nhưng cạn kiệt (depleted) hoặc ở mức ngẫu nhiên với vùng accelerated **[C]**. Nếu gene X gom lượng lớn cả CNE lẫn accelerated, đó là hiện tượng sai lệch (*artifact*) do kích thước locus khổng lồ hoặc điểm nóng tái tổ hợp/đột biến, không phải chọn lọc bảo tồn **[C]**.
- **Tỷ số C/A (conserved-to-accelerated ratio) [S]:** xếp hạng gene theo tỷ số CNE/accelerated đối chiếu với phân phối nền **[S]**. *Lưu ý:* gBGC (*GC-biased gene conversion* do tái tổ hợp) ở chim thường tạo tín hiệu accelerated giả; cần kiểm soát thiên lệch này trước khi kết luận **[C]**.

### 3. Sai lầm phổ biến khi công bố cần tránh

- **Bẫy gán gene gần nhất (*nearest-gene fallacy*) [C]:** 66,9% CNE nằm ngoài gene; trong cấu trúc chất nhiễm sắc 3D (TAD), enhancer thường nhảy cóc qua gene lân cận để tác động lên promoter ở xa **[C]**. Tự ý tuyên bố "CNE liên gene này điều hòa gene X" chỉ theo khoảng cách tuyến tính là sai lầm kinh điển dễ bị phản biện bác bỏ **[C]**.
- **Nhầm bảo tồn tổ tiên với đặc thù chào mào [C]:** CNE trên 363 loài chim phản ánh áp lực bảo tồn khung phát triển chung của tổ tiên có màng ối (*ancestral constraint*), không thể suy diễn thành "đặc trưng kiểu hình riêng của chào mào" **[C]**.

---

**Ghi chú của Main (không phải lời Antigravity):** nhãn [C] trong bài này chưa qua review chéo; A1 đang bị nghi nâng nhãn (62 [C] / 22 nguồn), xem `research/synthesis/06-review-A1.md`. Dùng nội dung A2 làm **đặc tả kỹ thuật** để viết code kiểm định, không trích như tài liệu tham khảo cho tới khi có review.
