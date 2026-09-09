# Thư gửi Anthropic — bản nháp 2026-09-09

Hai bản: tiếng Anh để gửi, tiếng Việt để bạn kiểm nội dung.
Địa chỉ gợi ý: `support@anthropic.com` (hỗ trợ tài khoản/hạn mức) và biểu mẫu tại `anthropic.com/contact-sales` nếu muốn xin gói nghiên cứu.
Tất cả số liệu trong thư đều kiểm được trong repo công khai; không có câu nào nói quá.

---

## BẢN TIẾNG ANH (để gửi)

**Subject:** Independent avian comparative-genomics project built with Claude Code — request for research access

Hello Anthropic team,

I am a bird keeper and independent researcher in Vietnam. Over the past three days I used Claude Code to build a working comparative-genomics pipeline for the red-whiskered bulbul (*Pycnonotus jocosus*), a songbird I breed and study. Everything runs on one consumer laptop with a 2 GB Docker memory ceiling. The repository is public:

**https://github.com/vuho60-byte/Biobirddna**

**What the project does.** It identifies the regions of the bulbul genome that have stayed nearly unchanged across the avian lineage. It takes the UCSC 363-bird phyloP conserved set, merges 70.4 million significant sites into 2.95 million elements on the chicken assembly, aligns them onto the bulbul genome in chunks, and annotates them against the NCBI gene set.

**Measured results (reproducible from the repo).**
- 248,461 conserved elements mapped, covering 61.5 Mb after merging overlaps — 6.00% of the bulbul genome.
- 59.8% of all bulbul coding sequence falls inside these conserved regions, a 9.96-fold enrichment over random expectation. (Base-level intersection; a first pass using per-region classification inflated this to 76.8% / 12.6-fold and a reviewer caught it.)
- Ranking genes by core density rather than total base count puts the Hoxa cluster on top (Hoxa3, Hoxa5, Hoxa6, Hoxa11, over 1,800 conserved bp per kb of locus).
- Whole run: 20 minutes 40 seconds, peak container memory 49% of a 1.86 GB limit.

I want to be precise about novelty: deep conservation of coding sequence and of Hox clusters is textbook biology, not a discovery. What is unusual here is that a hobbyist with no institutional compute reproduced it end-to-end, with tests, checksums and an audit trail — and that the same pipeline is now positioned to answer questions nobody has asked for this species, since no ancestral-state reconstruction or pigmentation-gene study exists for the family Pycnonotidae.

**Where Claude Code mattered most.** Three things I did not expect:
1. *Cross-checking caught fabricated citations.* I had an external model write a gene-function summary. A separate Claude reviewer opened all cited URLs and found 11 of 22 pointed to real but completely unrelated papers — a "Haesler 2007 FoxP2" citation was actually a malaria paper. 53 of 62 confidence labels had to be downgraded and the document was blocked from the report. Without that adversarial review step, my report would have rested on invented sources.
2. *A methodological correction I would have missed.* The external model pointed out that ranking genes by total conserved base pairs is biased toward long genes. Claude turned that into code — a density metric with four unit tests — and the corrected ranking is what surfaced the Hox cluster.
3. *Recovery from a destructive accident.* A coding agent I was using issued a malformed cleanup command that deleted the project directory and about 16 GB from the drive. Claude Code rebuilt all 66 project files from its own session transcripts, verified them against the test suite, and committed to git within minutes.

**My request.** I am doing this without funding or institutional access, on a personal plan. Access to a stronger model, or a higher usage allowance for this project, would let me finish the parts that are currently blocked by cost and time: aligning short conserved elements, running the statistical null model, and reconstructing ancestral sequences at three phylogenetic nodes. If you have a research-access, non-profit, or case-study program that fits, I would be glad to apply and to document my workflow publicly for other independent researchers.

Thank you for building tools that let someone like me do this at all.

Best regards,
Vũ Hồ — vuho60@gmail.com
Repository: https://github.com/vuho60-byte/Biobirddna

---

## BẢN TIẾNG VIỆT (để bạn kiểm nội dung)

**Tiêu đề:** Dự án gene chim độc lập làm bằng Claude Code — xin quyền truy cập phục vụ nghiên cứu

Chào đội ngũ Anthropic,

Tôi là người nuôi chim và nghiên cứu độc lập ở Việt Nam. Ba ngày qua tôi dùng Claude Code dựng một quy trình phân tích gene so sánh cho chào mào má đỏ, loài tôi nuôi và theo dõi. Mọi thứ chạy trên một máy tính cá nhân với trần bộ nhớ 2 GB. Repo công khai: https://github.com/vuho60-byte/Biobirddna

**Dự án làm gì.** Tìm những vùng trong bộ gene chào mào gần như không đổi suốt lịch sử lớp chim: lấy tập vùng bảo tồn của 363 loài chim từ UCSC, gộp 70,4 triệu điểm thành 2,95 triệu phần tử trên bộ gene gà, căn sang bộ gene chào mào theo mảnh, rồi đối chiếu với chú giải gene của NCBI.

**Kết quả đo được (tái lập từ repo).**
- 248.461 phần tử ánh xạ được, phủ 61,5 triệu base sau khi gộp trùng lặp — 6,00% bộ gene chào mào.
- 59,8% vùng mã hóa protein của chào mào nằm trong vùng bảo tồn, giàu gấp 9,96 lần so với rải ngẫu nhiên. (Tính giao base-level; lần đầu dùng bảng phân loại theo vùng cho ra 76,8% / 12,6 lần, reviewer đã bắt được.)
- Xếp gene theo mật độ lõi thay vì tổng số base đưa cụm Hoxa lên đầu (Hoxa3, Hoxa5, Hoxa6, Hoxa11, hơn 1.800 base lõi mỗi kb).
- Toàn bộ lần chạy: 20 phút 40 giây, bộ nhớ đỉnh 49% trần 1,86 GB.

Tôi nói rõ về tính mới: bảo tồn sâu ở vùng mã hóa và cụm Hox là kiến thức sách giáo khoa, không phải khám phá. Điều khác thường là một người nghiệp dư không có máy tính của viện nghiên cứu đã tái lập được trọn vẹn, có test, có mã băm, có nhật ký kiểm chứng — và cùng quy trình đó nay sẵn sàng trả lời những câu chưa ai hỏi cho loài này, vì chưa có nghiên cứu tái dựng tổ tiên hay gene sắc tố nào cho họ Chào mào.

**Chỗ Claude Code có ích nhất.** Ba điều tôi không ngờ:
1. *Kiểm chéo bắt được trích dẫn bịa.* Tôi nhờ một model ngoài viết phần diễn giải chức năng gene. Một Claude khác đóng vai người review mở toàn bộ đường dẫn và phát hiện 11 trên 22 nguồn trỏ tới bài thật nhưng sai hoàn toàn chủ đề — nguồn ghi là "Haesler 2007 về FoxP2" hóa ra là bài về sốt rét. 53 trên 62 nhãn tin cậy phải hạ, tài liệu bị chặn khỏi báo cáo.
2. *Một chỉnh sửa phương pháp tôi sẽ bỏ sót.* Model ngoài chỉ ra rằng xếp gene theo tổng số base bảo tồn thiên vị gene dài. Claude biến nhận xét đó thành code kèm bốn phép thử, và chính bảng đã sửa mới làm cụm Hox lộ ra.
3. *Khôi phục sau tai nạn xóa dữ liệu.* Một agent lập trình tôi dùng chạy lệnh dọn dẹp sai cú pháp, xóa mất thư mục dự án và khoảng 16 GB trên ổ đĩa. Claude Code dựng lại toàn bộ 66 tệp từ chính nhật ký phiên làm việc, kiểm bằng bộ test rồi đưa vào git trong vài phút.

**Đề nghị của tôi.** Tôi làm việc này không có tài trợ, không có tài nguyên của viện, đang dùng gói cá nhân. Được dùng model mạnh hơn, hoặc được nới hạn mức cho dự án này, sẽ giúp tôi hoàn thành những phần đang tắc vì chi phí và thời gian: căn các phần tử bảo tồn ngắn, chạy kiểm định thống kê, và tái dựng trình tự tổ tiên tại ba nút phát sinh loài. Nếu quý công ty có chương trình hỗ trợ nghiên cứu, phi lợi nhuận, hoặc nghiên cứu điển hình phù hợp, tôi sẵn sàng nộp hồ sơ và ghi lại công khai cách làm để những người nghiên cứu độc lập khác dùng lại.

Cảm ơn vì đã làm ra công cụ để một người như tôi làm được việc này.

Trân trọng,
Vũ Hồ — vuho60@gmail.com

---

## Ghi chú khi gửi

- Mọi con số trong thư đều lấy từ `data/a2/SUMMARY.md` và `annot_stats.tsv`, tái lập được bằng `pipeline/p02_core_map/launch_full.sh`.
- Không nên dùng từ "khám phá" hay "phát hiện mới" cho phần sinh học; điểm mạnh của thư là quy trình và tính minh bạch.
- Nếu muốn tăng sức thuyết phục: đợi chạy xong kiểm định thống kê và bộ căn đoạn ngắn rồi hãy gửi, khi đó phần "đang tắc" chuyển thành "đã làm được", và có thể nêu con số mới cho họ đọc.
- Anthropic hiếm khi cấp model riêng qua email hỗ trợ. Đường thực tế hơn: hỏi về nâng gói hoặc hạn mức, và hỏi thẳng xem có chương trình nghiên cứu độc lập nào không.


---

## Cập nhật 2026-09-09 — đã sửa số trong bản nháp Gmail

Bản nháp trong Gmail đã cập nhật: số đúng là **59,8%** và **9,96 lần** (tính bằng
`pipeline/p02_core_map/overlap_stats.py`, giao từng base, có gộp trùng lặp).
Thư cũng thêm một mục thứ ba trong phần "Claude Code có ích": chính agent review
của Claude đã bắt lỗi trong số liệu do Claude tạo ra — đó là điểm mạnh nên kể.
