# A1 — Antigravity: diễn giải sinh học nhóm gene chứa nhiều "lõi bất biến" nhất

Bạn là nhà nghiên cứu cộng tác trong dự án BIRDBIODNA (tách "DNA gốc" của chim chào mào bằng tính toán). Viết bằng **tiếng Việt**, giữ tên gene và tên bài báo bằng tiếng Anh. Dùng Google Search để tra cứu; **chỉ ghi URL bạn thực sự thấy trong kết quả tìm kiếm**, không bịa DOI.

## Bối cảnh (dữ liệu thật của dự án, đo ngày 2026-09-07)
Chúng tôi lấy các vùng bảo tồn có ý nghĩa (phyloP, FDR < 5%) trên alignment 363 loài chim, gộp thành phần tử, rồi ánh xạ sang bộ gene chào mào *Pycnonotus jocosus*. Trên nhiễm sắc thể 1 của gà (làm mốc thử nghiệm):
- 531.189 phần tử bảo tồn, 39.826 phần tử ánh xạ được (9,8 Mb trên chào mào).
- Phân bố: 22,6% base nằm trong CDS (vùng mã hóa), 10,5% trong intron, 66,9% ở vùng liên gene.
- 10 gene chứa nhiều base lõi nhất (bp): Tenm4 (29.055), Syn3 (26.283), Sema3a (25.576), Pdzrn4 (24.817), Celf2 (23.976), Pcca (23.947), Reln (22.294), Dlg2 (21.758), Foxp2 (21.710), Taf3 (20.469).

## Câu hỏi phải trả lời
1. **Từng gene trong 10 gene trên làm gì?** Một đoạn ngắn mỗi gene: chức năng chính, mô/cơ quan biểu hiện, bệnh hoặc kiểu hình khi hỏng (ở chim nếu có, nếu không thì ở động vật có xương sống khác). Có nguồn.
2. **Nhóm này có thiên lệch về chức năng nào không?** Kiểm giả thuyết: phần lớn là gene phát triển thần kinh/khớp nối thần kinh (Tenm4, Syn3, Sema3a, Reln, Dlg2, Foxp2 đều liên quan thần kinh). Nếu đúng, giải thích tại sao gene thần kinh lại giàu vùng điều hòa bảo tồn (dẫn tài liệu về "conserved non-coding elements clustered around developmental and neural genes", ví dụ các nghiên cứu về gene desert, GRB — genomic regulatory blocks).
3. **Foxp2 ở chim:** vai trò trong học hót; điều gì đã biết về vùng điều hòa của nó; có nghiên cứu nào về CNE quanh FoxP2 ở chim hót không.
4. **Điều này nói gì về hai giả thuyết đang so sánh trong dự án:**
   - H2 (tiến hóa + ràng buộc mạnh): dự đoán vùng bảo tồn cực cao tập trung quanh gene phát triển, và chọn lọc lọc rất mạnh ở nhóm toolkit.
   - H1 (tiến hóa chuẩn): cũng dự đoán bảo tồn nhưng không nhất thiết tập trung như vậy.
   Kết quả trên ủng hộ/không ủng hộ điều gì? Viết trung lập, nêu rõ giới hạn (mới chỉ 1 nhiễm sắc thể, mới chỉ phần ánh xạ được).
5. **Cảnh báo phương pháp:** những cách hiểu sai có thể mắc khi xếp hạng gene theo "số base lõi" (gene dài thì nhiều base hơn; vùng liên gene gán cho gene gần nhất; annotation của assembly scaffold chưa hoàn chỉnh). Nêu cách chuẩn hóa đúng (ví dụ chuẩn hóa theo chiều dài gene, so với phân phối nền).

## Định dạng đầu ra
In thẳng ra câu trả lời cuối, Markdown, không ghi file, không chạy lệnh. Cấu trúc:
```
## 1. Mười gene: chức năng
## 2. Thiên lệch chức năng của nhóm
## 3. Foxp2 và học hót
## 4. Ý nghĩa cho H1/H2 (trung lập, có giới hạn)
## 5. Cảnh báo phương pháp + cách chuẩn hóa
## 6. Nguồn (danh sách URL đã mở)
```
Mỗi khẳng định gắn nhãn: **[C]** nếu có ít nhất 2 nguồn độc lập, **[S]** nếu 1 nguồn tốt, **[U]** nếu chưa tìm được nguồn. Không nâng nhãn.
