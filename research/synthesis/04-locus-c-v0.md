# 04 — Sản phẩm C phiên bản 0: 20 locus, tọa độ galGal4, alignment CDS 363 loài

Nhãn: **đây là dữ liệu trung gian (alignment thô theo bigMaf, neo tọa độ trên gà)**, không phải kết luận sinh học. Không claim nào về tiến hóa/chức năng được rút ra ở đây; dùng làm đầu vào cho Pha 3 (ASR) và T22 (registry gene ứng viên).

Việc do teammate `locus-c` thực hiện qua 2 phiên (phiên 1 bị ngắt giữa chừng khi Claude tắt, chưa ghi báo cáo; phiên 2 `locus-c2` kiểm trạng thái, xác nhận 18/20 gene đã trích xong từ phiên 1, hoàn tất kiểm nhanh 3 gene + viết báo cáo này — không phải trích lại).

## 1. Kết quả tổng quan

| Chỉ số | Giá trị |
|---|---|
| Số gene có tọa độ galGal4 | 20/20 |
| Số gene rút alignment CDS xong (DONE) | 18/20 |
| Số gene BLOCKED (không có block MAF nào, đã kiểm độc lập ≥4 điểm) | 2/20 (CLOCK, DRD4) |
| Tổng bp CDS (cds_bp, 18 gene DONE) | 26.649 bp (thiết kế theo exon window); 26.045 bp (gallus_nongap_bp thực nhận — NPAS2 hụt 604 bp do một số window trả gap toàn phần cho gà) |
| % loài có ≥50% vị trí CDS không gap, trung bình 18 gene | 93,1% (thấp nhất PMEL 14,0%, cao nhất SOX10/FOXP2/NPAS2/SLC6A4/CREB1/CALM1 100%) |
| % gap tại Pycnonotus jocosus, trung bình 18 gene | 7,4% (thấp nhất 0% ở TYR/SLC45A2/TYRP1/SOX10/ASIP/CREB1/CALM1, cao nhất PMEL 85,0%, NPAS2 29,7%) |
| Tổng thời gian chạy (elapsed_sec cộng dồn 18 gene) | 515,5 s (~8,6 phút; mỗi gene gọi bigBedToBed theo từng cửa sổ exon, đọc từ xa, không tải file) |
| Dung lượng `data/c_loci/` | 9,5 MB (< 400 MB giới hạn) |
| Hàng `Pycnonotus_jocosus` có mặt trong FASTA | Có, cả 18/18 gene DONE (363 hàng loài mỗi file) |

## 2. Bảng 20 gene (tọa độ galGal4, số exon, bp CDS, độ phủ loài, gap chào mào)

Cột "số loài ≥50%" = số loài trong 363 có ≥50% vị trí CDS không phải gap (n_species_ge50pct trong `<GENE>.blocks.tsv`). Cột "% gap chào mào" = tỷ lệ vị trí gap (`-`) trong chuỗi CDS đã ghép của Pycnonotus_jocosus.

| Gene | Chrom (galGal4) | Strand | Số exon CDS | Tổng bp CDS | Số loài ≥50% (/363) | % gap chào mào | Thời gian | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| TYR | chr1 | - | 5 | 1590 | 362 (99,7%) | 0,00% | 30,8 s | DONE |
| SLC45A2 | chrZ | - | 7 | 1632 | 358 (98,6%) | 0,00% | 29,7 s | DONE |
| MLPH | chr7 | - | 17 | 2052 | 362 (99,7%) | 2,39% | 50,7 s | DONE |
| PMEL | chrUn_JH375501 | - | 12 | 2223 | 51 (14,0%) | 84,98% | 16,8 s | DONE (scaffold chưa xếp NST, độ phủ 363-way thấp) |
| TYRP1 | chrZ | - | 8 | 1611 | 356 (98,1%) | 0,00% | 27,0 s | DONE |
| SOX10 | chr1 | + | 4 | 1386 | 363 (100,0%) | 0,00% | 12,7 s | DONE |
| OCA2 | chr1 | + | 23 | 2556 | 361 (99,4%) | 0,43% | 67,1 s | DONE |
| ASIP | chr20 | - | 4 | 393 | 359 (98,9%) | 0,00% | 12,9 s | DONE |
| BMP4 | chr5 | - | 3 | 1215 | 355 (97,8%) | 0,25% | 11,3 s | DONE |
| KITLG | chr1 | - | 10 | 864 | 359 (98,9%) | 1,74% | 37,6 s | DONE (thay MC1R lần 2 — xem mục 3) |
| FOXP2 | chr1 | - | 16 | 2076 | 363 (100,0%) | 0,34% | 44,4 s | DONE |
| CRY4 | chr26 | - | 10 | 1590 | 321 (88,4%) | 8,87% | 18,1 s | DONE (ký hiệu gà là LOC395100) |
| CLOCK | chr4 | + | 20 | — | — | — | — | **BLOCKED** — 0 dòng block MAF ở cả 4 điểm dò độc lập rải khắp gene; xem mục 3 |
| NPAS2 | chr1 | + | 20 | 2448 (thiết kế) / 1844 (thực nhận) | 363 (100,0%) | 29,66% | 60,3 s | DONE |
| ADCYAP1 | chr2 | - | 2 | 290 | 318 (87,6%) | 0,00% | 9,4 s | DONE |
| DRD4 | chr5 | - | 5 | — | — | — | — | **BLOCKED** — 0 dòng block MAF ở cả 5 cửa sổ exon-CDS + vùng lân cận; xem mục 3 |
| SLC6A4 | chr19 | - | 13 | 2013 | 363 (100,0%) | 0,30% | 25,8 s | DONE |
| CREB1 | chr7 | - | 8 | 984 | 363 (100,0%) | 0,00% | 26,4 s | DONE |
| CALM1 | chr5 | + | 5 | 448 | 363 (100,0%) | 0,00% | 17,9 s | DONE |
| SHH | chr2 | - | 3 | 1278 | 345 (95,0%) | 3,68% | 16,6 s | DONE |

Nguồn tọa độ: UCSC REST `track=refGene` galGal4 cho 19/20 gene; riêng OCA2 không có ở `refGene`, lấy từ `ensGene` (`ENSGALT00000027021.4`) — ghi trong `data/c_loci/loci_galGal4.tsv` cột `nguon`/`track`.

## 3. Các thay thế/loại bỏ gene và lý do (đã kiểm chứng, không suy đoán)

- **MC1R → (thử DCT, thất bại) → KITLG**: MC1R nằm trên chr11 — toàn bộ chr11 vắng mặt khỏi `chicken.bigMaf.bb` của hub này (xác nhận qua `bigBedInfo -chroms` ở phiên P1.1). Thay bằng DCT (chr1:~145,7 Mb) nhưng dò 4 điểm độc lập quanh 145,6–146,0 Mb đều 0 block (chỉ 1 điểm ở 145,60–145,61 Mb có 2044 dòng nhưng nằm ngoài CDS DCT). Thay lần 2 bằng KITLG (chr1:42,86 Mb), xác nhận có dữ liệu qua probe trước khi chạy full extraction — có trong registry `00-tong-hop-vong-1.md` mục 5A #12.
- **CLOCK — giữ nguyên, đánh dấu BLOCKED**: dò 4 điểm độc lập rải khắp 20 cửa sổ exon-CDS (64.696.006-53bp, 64.701.467-557bp, 64.710.324-414bp, 64.717.216-393bp) đều trả về 0 dòng block MAF → vùng này không được `chicken.bigMaf.bb` của hub này bao phủ. Không có gene circadian thay thế đúng nghĩa trong registry mục 5C (CRY4 đã dùng; CRY1/CRY2 không có trong 49 dòng registry). Không bịa trình tự.
- **DRD4 — giữ nguyên, đánh dấu BLOCKED**: cả 5 cửa sổ exon-CDS + vùng lân cận (chr5:600.000–610.000) đều 0 dòng block MAF. Registry mục 5C #43-44 chỉ nêu DRD4, không có gene cá tính/hành vi đơn lẻ khác để thay. Không bịa trình tự.
- Kết quả: 20 gene mục tiêu ban đầu (10 từ 5A/5B, 10 từ 5C/5B) → sau 2 lần thay thế còn nguyên 20 dòng tọa độ trong `loci_galGal4.tsv`, trong đó 18 rút alignment thành công, 2 BLOCKED có ghi chú xác minh đầy đủ.

## 4. Kiểm nhanh (dịch mã gà, kiểm codon dừng sớm)

Không fetch thêm dữ liệu (không vi phạm giới hạn tải/pull); kiểm bằng cách dịch trực tiếp chuỗi CDS Gallus_gallus (đã bỏ gap) sang protein bằng bảng mã chuẩn, kiểm độ dài chia hết cho 3, có đúng 1 codon dừng và nằm ở cuối (không có codon dừng sớm giữa chuỗi). Chọn 3 gene đại diện 2 nhóm (sắc tố + toolkit hành vi):

| Gene | bp CDS (gà, không gap) | Số codon | Chia hết cho 3 | Codon dừng sớm | Kết thúc bằng stop | Kết luận |
|---|---|---|---|---|---|---|
| TYR | 1590 | 530 | Có | 0 | Có | OK — không có bất thường |
| SOX10 | 1386 | 462 | Có | 0 | Có | OK — không có bất thường |
| FOXP2 | 2076 | 692 | Có | 0 | Có | OK — không có bất thường |

Không so trực tiếp với chuỗi protein NCBI/UCSC tham chiếu (brief cho phép bỏ qua nếu không có sẵn — không thực hiện fetch mới ngoài phạm vi được duyệt). Kết quả trên chỉ xác nhận khung đọc gà hợp lệ, KHÔNG xác nhận chức năng hay tính đúng của alignment 362 loài còn lại.

## 5. Giới hạn (bắt buộc đọc trước khi dùng dữ liệu này)

1. **Neo trên galGal4, không phải GRCg6a/7b**: mọi tọa độ exon/CDS lấy từ track `refGene`/`ensGene` của galGal4 (bản build cũ hơn). Không nội suy sang genome gà mới hơn.
2. **Tọa độ của 362 loài còn lại trong bigMaf là GIẢ** (ví dụ `Alca_torda.1 1 1 + 6000`) — chỉ trình tự là thật (theo đúng kiến trúc hub `363-avian-2020-hub`, docs/04 mục 8). Tuyệt đối không dùng cột tọa độ loài khác để suy vị trí trên bộ gene của loài đó.
3. **Chỉ vị trí không-gap của Gallus_gallus được giữ**: alignment ghép theo đúng cấu trúc block MAF của hub, nên các vị trí mà gà có gap bị loại khỏi CDS ghép (khác với alignment toàn cục theo mọi loài).
4. **9 nhiễm sắc thể vắng mặt khỏi `chicken.bigMaf.bb`**: chr9, chr11, chr12, chr14, chr16, chr18, chr24, chr27, chr32 (xác nhận bằng `bigBedInfo -chroms` ở P1.1) — mọi gene nằm trên các NST này không thể rút được bằng lối này (đây là lý do MC1R phải thay).
5. **PMEL có độ phủ loài rất thấp** (chỉ 51/363 loài ≥50% vị trí, gap chào mào 85%) vì nằm trên scaffold chưa xếp NST (`chrUn_JH375501`) — độ tin cậy 363-way alignment ở locus này thấp hơn hẳn các gene khác, cần cân nhắc loại khỏi Pha 3 (ASR) hoặc gắn nhãn UNVERIFIED riêng nếu dùng.
6. **NPAS2** có chênh lệch cds_bp thiết kế (2448 bp theo exon window) và gallus_nongap_bp thực nhận (1844 bp, gap chào mào 29,7%) — một số cửa sổ exon trả về block nhưng gà có gap ở phần lớn vị trí đó; cần xem lại từng block trước khi dùng cho ASR.
7. **2/20 gene BLOCKED hoàn toàn** (CLOCK, DRD4) — không có dữ liệu, không suy diễn thay thế.
8. Đây là **dữ liệu trung gian**: chưa alignment lại bằng MAFFT/PRANK, chưa loại trùng lặp/chuẩn hoá tên loài ngoài danh sách `species_363.txt`, chưa ASR.

## 6. Bước tiếp theo

- **IQ-TREE2 `-asr`** trên các file `<GENE>.cds363.fa` để tái dựng tổ tiên tại 3 nút (Neornithes, Passeriformes, Pycnonotidae) theo Pha 3 của `docs/04-ke-hoach-tach-adn-goc.md` — **cần duyệt pull image** (chưa có image IQ-TREE2 trong môi trường hiện tại).
- Trước khi ASR: cân nhắc loại PMEL (độ phủ 14%) hoặc chạy riêng với cây con ít loài hơn; kiểm lại các block NPAS2 gap cao.
- CLOCK/DRD4: nếu cần dữ liệu circadian/hành vi bổ sung, phải quay lại registry mở rộng (ngoài phạm vi 49 dòng hiện có) hoặc dùng nguồn khác ngoài bigMaf 363-avian.

## 7. Tệp liên quan

- `data/c_loci/loci_galGal4.tsv` — tọa độ 20 gene + ghi chú thay thế/BLOCKED.
- `data/c_loci/<GENE>/<GENE>.cds363.fa` + `<GENE>.blocks.tsv` — 18 gene DONE.
- `data/c_loci/species_363.txt` — danh sách 363 loài dùng làm khung tên hàng FASTA.
- `pipeline/p03_asr/fetch_coords.py`, `pipeline/p03_asr/extract_locus.py` — script tra tọa độ UCSC REST và rút alignment theo exon-CDS.
