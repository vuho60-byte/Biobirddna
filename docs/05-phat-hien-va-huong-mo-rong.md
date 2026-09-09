# 05 — Mô tả phát hiện và hướng mở rộng

Ngày 2026-09-09. Mọi số trong tài liệu này tái lập được từ `data/a2/`, `data/a2_accel/`, `data/anomaly/`.

---

## PHẦN A — Mô tả kỹ ba kết quả đã có

### A1. Đối chứng âm: quy trình phân biệt được vùng chịu ràng buộc với vùng tự do biến đổi

**Thiết kế.** Chạy **cùng một quy trình, cùng tham số, cùng ngày** trên hai bộ dữ liệu đối lập, đều lấy từ phép đo phyloP trên alignment 363 loài chim:
- bộ **conserved**: vùng thay thế base **chậm hơn** mô hình trung tính (FDR < 5%);
- bộ **accelerated**: vùng thay thế base **nhanh hơn** mô hình trung tính (cùng FDR).

Hai bộ khác nhau đúng một điều: dấu của độ lệch so với trung tính. Mọi thứ khác giống hệt.

**Kết quả.**

| | Bảo tồn | Tiến hóa nhanh |
|---|---|---|
| Phần tử đưa vào | 2.947.588 | 4.054.556 |
| Base gốc trên bộ gene gà | 134.568.082 (12,85%) | 89.349.479 (8,53%) |
| Ánh xạ được sang chào mào | **248.461** | **1.133** |
| Tỉ lệ ánh xạ | **8,43%** | **0,03%** |

Chênh **281 lần**, dù bộ tiến hóa nhanh có **nhiều phần tử hơn** (4,05 so với 2,95 triệu).

**Ý nghĩa — nói cho đúng.** Đây **không phải phát hiện sinh học mới**. Đây là **kiểm chứng phương pháp**, và nó đóng lại nghi ngờ lớn nhất về toàn bộ kết quả: rằng 6% bộ gene tìm được chỉ là thứ công cụ căn trình tự tình cờ khớp. Nếu vậy, bộ tiến hóa nhanh cũng phải khớp tương đương. Nó không.

Kết quả này đồng thời là một **thang đo** cho mọi kết quả về sau: bất kỳ tập vùng nào ánh xạ được ở mức gần 0,03% là nhiễu; gần 8% là tín hiệu thật.

**Giới hạn.** Vì gần như không gene nào có vùng tiến hóa nhanh ánh xạ được, **không** tính được tỉ số bảo tồn/tăng tốc theo từng gene như dự tính ban đầu. Đối chứng âm này có giá trị ở cấp **toàn quy trình**, không ở cấp gene. Muốn xếp hạng gene vẫn phải dùng xáo trộn vị trí ngẫu nhiên (chưa làm).

### A2. Bản đồ lõi bất biến đầu tiên cho họ Chào mào

- 248.461 vùng, **61,50 Mb sau khi gộp trùng lặp = 6,00% bộ gene chào mào**.
- **59,8%** toàn bộ vùng mã hóa protein của chào mào nằm trong lõi; làm giàu **9,96 lần** so với rải ngẫu nhiên (giao base-level).
- Phân bố lõi: 19,2% trong vùng mã hóa, 33,3% trong thân gene (gồm intron), phần còn lại ở vùng giữa các gene.
- Xếp gene theo **mật độ** lõi trên mỗi kb locus đưa **cụm Hoxa** (Hoxa3, Hoxa5, Hoxa6, Hoxa11) lên đầu, trên 1.800 base lõi mỗi kb. Xếp theo tổng base thì đứng đầu là gene dài (Znf521, Sox6, Foxp1) — hai bảng không giao nhau một gene nào.

**Tính mới:** bảo tồn sâu ở vùng mã hóa và ở cụm Hox là kiến thức chuẩn. Cái mới là **bộ dữ liệu cho chính họ Pycnonotidae**, chưa từng được công bố, tái lập được bằng mã trong repo.

### A3. Không có dấu vết đoạn DNA ngoại lai trong vùng mã hóa

Quét 14.003 vùng mã hóa bằng ba thước đo thành phần độc lập (GC/GC3, cách dùng codon, phổ 4-mer):

| Số cờ | Số trình tự |
|---|---|
| 3 cờ (nghi ngờ mạnh) | **0** |
| 2 cờ | 27 |
| 1 cờ | 89 |
| 0 cờ | 13.887 (99,17%) |

27 trình tự hai cờ đều ngắn (324–549 bp), tỉ lệ GC bình thường, chỉ lệch ở phổ 4-mer — chữ ký của **trình tự ngắn thống kê kém tin cậy hoặc vùng lặp**, không phải của DNA khác dòng dõi. Kết quả **âm tính**, và âm tính ở đây là kết quả có giá trị: nó thu hẹp không gian giả thuyết bằng số liệu.

---

## PHẦN B — Mười hướng mở rộng, xếp theo chi phí và giá trị

### Nhóm 1 — Hoàn thiện cái đang dở (rẻ, làm được ngay)

**B1. Căn đoạn ngắn bằng LAST.** Hiện nhóm dưới 100 bp chiếm ~78% số phần tử nhưng chỉ ánh xạ được 0,25–4,7%. Mã đã viết, 14 phép thử đạt, chưa chạy. Kỳ vọng nâng độ phủ từ 6% lên có thể 8–10% bộ gene và **sửa được thiên lệch** hiện tại (bức tranh đang nghiêng về vùng mã hóa vì đoạn dài dễ căn hơn).
*Chi phí: một buổi chạy. Giá trị: cao — nó quyết định con số phân bố có tin được không.*

**B2. Kiểm định nền bằng xáo trộn vị trí.** Viết bộ xáo trộn ngẫu nhiên bằng Python thuần: giữ nguyên số lượng và phân bố độ dài phần tử lõi, rải lại ngẫu nhiên trên bộ gene (tránh khoảng trống lắp ráp), lặp 1.000 lần, so số base lõi thật của từng gene với phân phối ngẫu nhiên. Đây mới là phép kiểm đúng cho câu "gene này giàu lõi hơn mong đợi".
*Chi phí: một ngày viết + vài giờ chạy. Giá trị: cao — biến bảng xếp hạng thành phát biểu có kiểm định.*

**B3. Tái dựng trình tự tổ tiên cho 20 locus.** Sản phẩm C đã lên kế hoạch, dữ liệu mất trong sự cố, cần chạy lại. Cho ra trình tự tổ tiên tại ba mốc và bảng vị trí khác biệt giữa tổ tiên và chào mào hiện đại.
*Chi phí: nửa ngày. Giá trị: cao — đây là "DNA gốc" theo nghĩa đen nhất mà tính toán cho được.*

### Nhóm 2 — Câu hỏi khoa học mới, khả thi với dữ liệu đang có

**B4. Vùng tăng tốc riêng của nhánh chào mào.** Dữ liệu UCSC đo tăng tốc trên **toàn cây chim**. Chúng ta có ba mô hình trung tính và có alignment chứa chào mào, nên chạy được phyloP ở chế độ so **một nhánh riêng** để tìm vùng bảo tồn ở mọi loài chim **nhưng thay đổi nhanh riêng ở nhánh chào mào**. Đây chính là phương pháp đã tạo ra khái niệm vùng tăng tốc ở người.
*Trả lời câu: **cái gì làm chào mào khác các loài chim khác?** Chưa ai làm cho họ này.*
*Chi phí: cần công cụ PHAST trong Docker và một cây loài; hai đến ba ngày. Giá trị: cao nhất trong danh sách về tính mới.*

**B5. Phép thử gene răng hỏng.** Vòng nghiên cứu trước đã xác nhận năm gene men răng không còn bản ghi nào ở gà. Quét chúng trong bộ gene chào mào bằng cách so protein cá sấu và rùa lên bộ gene. Nếu tìm thấy mảnh vỡ mang **cùng kiểu hỏng** như ở các bộ chim khác, đó là bằng chứng trực tiếp cho tổ tiên chung, kiểm được trên chính loài của bạn.
*Chi phí: cần công cụ tìm kiếm trình tự và bộ gene ngoài nhóm (đã có accession); hai ngày. Giá trị: cao — đây là phép thử phân biệt giả thuyết, không chỉ mô tả.*

**B6. So sánh lõi giữa các loài chim hót.** Chạy đúng quy trình này cho sẻ vằn và sẻ ngô lớn (bộ gene chất lượng cao hơn nhiều), rồi so ba bản đồ. Phần chung là lõi của chim hót; phần chỉ có ở chào mào là ứng viên cho đặc trưng riêng.
*Chi phí: mỗi loài một lần chạy, khoảng nửa ngày. Giá trị: trung bình cao; cũng là phép kiểm chéo cho chất lượng bộ gene chào mào vốn còn vụn.*

### Nhóm 3 — Nối thẳng vào việc nuôi chim

**B7. Lõi ở các gene sắc tố.** Kiểm xem MC1R, TYR, SLC45A2, OCA2, MLPH và vùng điều hòa quanh chúng được lõi phủ tới đâu. Gene bị phủ dày nghĩa là ít dung thứ đột biến, nên đột biến ở đó thường gây hậu quả nặng; gene phủ thưa thì dễ sinh biến thể sống được. Đây là cơ sở để đoán **loại đột biến màu nào khả dĩ xuất hiện** ở chào mào.
*Chi phí: vài giờ, dữ liệu đã có. Giá trị: cao cho ứng dụng thực tế, nối thẳng vào công cụ di truyền màu lông.*

**B8. Lõi ở gene liên quan tiếng hót.** Cùng cách làm với FoxP2 và các gene học hót. Trả lời câu hỏi thứ hai của bạn từ đầu dự án: phần "có sẵn trong DNA" của tiếng hót nằm ở đâu và bảo tồn tới mức nào.
*Chi phí: vài giờ. Giá trị: cao về mặt câu chuyện, và đo được.*

### Nhóm 4 — Dài hơi

**B9. Công bố bộ dữ liệu.** Bản đồ lõi đầu tiên cho họ Chào mào, kèm mã và mã băm, đủ chuẩn cho một bài dạng công bố dữ liệu. Cần hoàn thành B1, B2 và bổ sung đánh giá chất lượng bộ gene trước.

**B10. Bổ sung bộ gene chất lượng cao cho chào mào.** Hạn chế lớn nhất hiện nay là bộ gene chào mào ở mức scaffold, đoạn trung vị 218 kb. Mọi kết luận về trật tự gene và về vùng điều hòa xa đều bị chặn bởi điều này. Cách gỡ: chờ bộ gene mới, hoặc hợp tác với nhóm có mẫu.

---

## PHẦN C — Đề xuất thứ tự

1. **B1** (đoạn ngắn) — vì nó sửa thiên lệch của mọi con số hiện có.
2. **B7 + B8** (gene sắc tố và tiếng hót) — rẻ, trả lời đúng câu hỏi gốc của dự án, dùng được ngay.
3. **B2** (kiểm định nền) — biến bảng xếp hạng thành phát biểu có kiểm định.
4. **B5** (gene răng) — phép thử phân biệt giả thuyết đầu tiên thực sự chạy được.
5. **B4** (vùng tăng tốc riêng chào mào) — hướng có tính mới cao nhất, làm khi ba việc trên xong.

Ba việc đầu nằm gọn trong hai ngày làm việc với tài nguyên hiện tại.
