# THINK — primordial-dna (2026-09-07)

REAL_OBJECTIVE:
  Biến 6 câu hỏi trực giác của người nuôi chim (ổn định hình thái, hành vi bẩm sinh, "không thấy tiến hóa", "DNA gốc", tuyệt chủng, "dùng code mổ xẻ") thành một dự án tính toán có đích: xác định LÕI bất biến của bộ gene chim, tái dựng trình tự tổ tiên cho locus đã chọn, và nối kết quả vào V4 (tracker T06/T22). Không phải viết bài tranh luận triết học.

KNOWN_FACTS:
  - V4 = skill biobirddna-genetics v0.4.0: quyết định di truyền màu lông; tracker 27 chủ đề gần như toàn bộ evidence: missing; T06 (bộ gene chào mào) và T22 (gene ứng viên) chưa bắt đầu.
  - Thư mục project rỗng (chỉ .claude). Máy: Python 3.14 không Biopython/pandas; không MAFFT/IQ-TREE/samtools; Node 24; ACPX 0.13 có agent antigravity-gemini-high; Board CLI hoạt động.
  - Perplexity: Pro 78, Deep Research 17. Một thread cũ 2026-07-29 về gene sắc tố lông (có thể tái dùng).
  - Công cụ bio có sẵn: PubMed, Consensus, bioRxiv MCP.

ASSUMPTIONS:
  - Chủ dự án muốn hướng khoa học kiểm chứng được, chấp nhận việc một số tiền đề bị chỉnh (mốc 2000 năm, "100% giống nhau").
  - Alignment 363 loài chim + điểm bảo tồn của B10K/UCSC có thể tải, không cần tự align (nếu sai → chi phí tính toán tăng mạnh).
  - Có ít nhất một assembly Pycnonotus ở NCBI (nếu không → dùng loài họ hàng gần trong Passerida).

UNKNOWN_BLOCKERS:
  - Trạng thái assembly P. jocosus; license/quyền dùng dữ liệu B10K.
  - Dung lượng tải và máy tính có đủ (HAL 363 loài rất lớn).

RISKS:
  - Bịa trích dẫn khi tổng hợp nhanh → bắt buộc nhãn CONFIRMED/STRONG_INFERENCE/UNVERIFIED và search log.
  - Trôi mục tiêu sang tranh luận H3 (thiết kế) thay vì đo đạc → sổ giả thuyết ép mỗi H nêu dự đoán kiểm được.
  - Quá tay: viết pipeline khi chưa có dữ liệu → pha này chỉ skeleton + README.

RECOMMENDED_DIRECTION:
  Vòng 1 = tái định khung (xong) + khung xương (xong) + 6 nhánh tìm kiếm song song (R1–R6) → tổng hợp → quyết định Pha 1 (môi trường + inventory dữ liệu).
