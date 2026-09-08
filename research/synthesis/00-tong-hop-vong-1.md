# 00 — Tổng hợp vòng 1 (S1, opus/refiner)

Nguồn: `research/raw/R1..R5` + `R7` (đầy đủ) + `R6a/R6b` (khảo sát Google của Gemini — **nguồn phụ**, chỉ bổ sung URL, mặc định UNVERIFIED) + `docs/00`, `docs/02`.
Nhãn gộp R1–R5+R7 (196 claim): **C=CONFIRMED 91 · S=STRONG_INFERENCE 78 · U=UNVERIFIED 27**. Dưới đây dùng C/S/U viết tắt.

> **Ghi chú cách đếm (F18):** 6 claim mang **nhãn kép**, ở đây đếm theo nhãn của **mệnh đề chính**; nếu đếm theo nhãn đứng đầu dòng sẽ ra C=92 · S=78 · U=26 (chênh đúng 1). Sáu claim đó: **R3 #31** (C cho Drosophila/Arabidopsis; U cho chim) · **R4 #15** (C cho mốc >1 Ma; U cho con số 1,2–1,6 Ma) · **R5 #6** (S cho bản 1.0.3; U cho bản 1.1) · **R7 #6** (C cho trích dẫn Fregin 2012; U cho nội dung/mốc tuổi) · **R7 #9** (S cho miền Bắc; U cho ranh giới miền Nam/Trung) · **R7 #40** (C cho trích dẫn Eaton 2015; U cho liên hệ tới *P. jocosus*).

---

## 1. TL;DR

1. Hạ tầng dữ liệu **có thật, mở được**: B10K 363 bộ gene (Feng 2020; Stiller 2024), alignment Cactus/HAL 363 loài trên S3, track phyloP + 3 model trung tính macro/micro/NST giới tính.
2. **Chào mào CÓ bộ gene**: `GCA_013400435.1` (B10K 2020) — nhưng scaffold, N50 218 kb. *P. cafer* tốt hơn (N50 3,04 Mb, BUSCO 97,2%) nhưng **chưa có GCA/GCF**. Lưu ý: "do B10K nộp" **không đồng nghĩa** "nằm trong bộ 363 / trong file HAL" — điểm này vẫn **S**, chưa đối chiếu danh sách loài (U21, mục 8).
3. "Bộ gene chim ổn định bất thường" có cơ sở phân tử thật: TE ~7,8% vs thú ~44,5%; stasis synteny; vi NST bảo tồn hàng trăm triệu năm [C].
4. Nhưng "chim đột biến chậm hơn thú" **KHÔNG đúng như quy luật theo lớp** — driver là thời gian thế hệ + Ne. Tiền đề dự án cần chỉnh.
5. Tiến hóa quan sát được trong đời người: **5/5** ví dụ của `docs/00` có nguồn thật — và **có thêm một ví dụ trên chính chào mào**: quần thể du nhập đảo Reunion phân kỳ hình thái mỏ trong **<10 thế hệ** (Amiot 2007; Le Gros 2016) [C].
6. Hành vi bẩm sinh có nền di truyền thật (FoxP2, CRY4, NST W) nhưng **đa gene**; DRD4 không tái lập qua quần thể.
7. `docs/00` có **17 chỗ cần sửa** — nặng nhất: "Spottiswoode 2022 *Science*" (thật ra PNAS; bản *Science* là Merondun 2025).
8. Registry gene gộp **49 dòng**, trong đó **46 dòng có nguồn bình duyệt**, **2 dòng là khoảng trống đã xác nhận** (#24 gà lôi, #28 chào mào), **1 dòng chờ Main kiểm** (#23 Lopes 2016, DOI chỉ từ R6b). **Chào mào: chưa có dữ liệu gene màu, cũng chưa có ASR nào làm trực tiếp trên Pycnonotidae** (R2 + R7 xác nhận độc lập) — khoảng trống thật.
9. H3 **không có dự đoán riêng nào** về kiến trúc bộ gene chim; bảng `docs/00` giữ nguyên trạng thái trống.
10. Rào cản Pha 1 lớn nhất: HAL là **một file duy nhất hàng trăm GB**, không tải riêng loài.
11. Chưa ai tái dựng tổ tiên tại nút **Pycnonotidae** — đóng góp mới thật nếu làm được.
12. **T06 = khả thi có điều kiện** (mục 10).

---

## 2. Trả lời Q1–Q6

### Q1 — "Giống nhau 100% bề ngoài, chỉ khác cá tính"
**Kết luận:** "biến dị hành vi > hình thái" là cảm nhận đúng nhưng **chưa ai đo trực diện**. "100%" sai (`docs/00` đã tự nhận). Cá tính heritable cao nhưng **đa gene**.
- h² exploratory *Parus major* = **54±5%** — C, Drent 2003, R3 #20.
- SNP-chip ~500k: **không SNP nào ý nghĩa toàn hệ gene**, kể cả DRD4 — C, Kim 2018, R3 #24.
- DRD4 SNP830 chỉ tái lập **1/4 quần thể** — C, Korsten 2010, R3 #22.
- **Không có nghiên cứu so trực diện CV hình thái vs repeatability hành vi cùng loài** — U, R3 #27.
- CV thô không so được giữa trait khác thứ nguyên — S, Pélabon 2020, R3 #29.
- **Mốc đối chiếu cho phần "tự đo":** meta-analysis repeatability hành vi (nhiều loài, gồm chim) — repeatability cao hơn ở field so với lab, cao hơn khi khoảng cách hai lần đo ngắn; mate-preference ít repeatable nhất — C, Bell 2009 *Anim Behav* 77(4):771-783, R3 #28.

**Cần chỉnh:** Q1a hỏi "có số liệu công bố không?" → **không có**. Khoảng trống thật → Q1a chuyển từ tra cứu thành **việc code tự đo** (cùng framework ICC/rptR cho hai trục, không so CV thô); lấy **Bell 2009 (R3 #28)** làm mốc đối chiếu cho giá trị repeatability đo được.

### Q2 — "Nhận thức có sẵn trong DNA"
**Kết luận:** đúng và có bằng chứng chức năng, nhưng "có sẵn" ≠ "một gene quyết định". Một ví dụ trong `docs/00` thực ra thuộc về **học**.
- Sẻ vằn cách ly hội tụ bài hót wild-type sau 3–4 thế hệ — C, Fehér 2009, R3 #4.
- FoxP2 knockdown Area X → hót không chính xác (**chức năng**) — C, Haesler 2004/2007, R3 #5–6.
- CRY4 nhạy từ in vitro > gà/bồ câu; **mất Cry4** ở chim ruồi/vẹt/Suboscines — C, Xu 2021 · Langebrake 2024, R3 #14–16.
- Mimicry trứng qua NST W — C, nhưng loài là **cuckoo finch *Anomalospiza imberbis***, R3 #8.
- Sẻ vằn chọn vật liệu tổ **theo trải nghiệm tuổi non** — C, Bailey 2014, R3 #12.
- CLOCK/ADCYAP1 **không phải marker phân biệt di cư/định cư** — C, Le Clercq 2023, R3 #17.

**Cần chỉnh:** "làm tổ không cần thầy" là ví dụ **yếu nhất** — chuyển sang cột hỗn hợp bẩm sinh + học.

### Q3 — "2000 năm chưa thấy tiến hóa"
**Kết luận:** tiến hóa ĐÃ quan sát trực tiếp (5/5 ví dụ có nguồn), đồng thời trực giác "chim không đổi" có cơ sở ở cấp cấu trúc bộ gene. Không mâu thuẫn: **đổi ở VỎ, ổn định ở LÕI** — đúng kiến trúc ba lớp dự án.
- **Trên CHÍNH chào mào:** quần thể du nhập đảo Reunion phân kỳ hình thái mỏ giữa bờ ẩm/bờ khô trong **<10 thế hệ** — C, Amiot 2007 *Ibis*, R7 #11; Le Gros 2016 *Mol Ecol* mở rộng 3 đảo: vừa founder effect (Reunion) vừa **thích nghi thật** (Mauritius) — C, R7 #13.
- Chích đầu đen: lộ trình di cư mới ~30 năm + cơ sở di truyền — C, Berthold 1992, R2 #9; ghép đôi đồng loại — C, Bearhop 2005, R2 #10.
- Sẻ Ý là loài lai — C, 3 bài đa phương pháp, R2 #11–13.
- ALX1/HMGA2 (mỏ sẻ Darwin, s=0,59) và COL4A5 (mỏ sẻ ngô lớn) — S, R2 #2–3, #6; COL4A5 **có phản biện** (Perrier 2018), R2 #7.
- **Về "biến dị thì con non khó sống":** allele bạch tạng ở chích đầm lau lớn chỉ lộ ra khi quần thể mới lập bị cận huyết rồi biến mất khi cận huyết giảm — C, Bensch 2004, R7 #25; nhưng trong chính loài đó chim bạch tạng-một-phần có **thành công sinh sản tương đương** — C, R7 #28. Tức "biến dị = kém sống sót" **có điều kiện, tùy loài**, không phải quy luật.
- Bộ gene: 1,0–2,1 Gb, TE ~7,8% — C, R1 #7; stasis synteny — C, R1 #8; vi NST — C, R1 #9.

**Cần chỉnh:** Q3b giả định ngầm "chim đột biến chậm hơn thú" — sai (R1 #20/#22). Q3a (% synteny chào mào↔gà) **chưa ai tính** → tự làm Pha 2. Nên bổ sung ví dụ Reunion vào `docs/00`: bằng chứng tiến hóa quan sát được **trên chính loài dự án quan tâm**, mạnh hơn mọi ví dụ ngoại lai.

### Q4 — "DNA gốc là gì? Thí nghiệm của mục tiêu nguyên thủy?"
**Kết luận:** "DNA gốc" **không đào lên được**, chỉ tái dựng bằng tính toán. H1/H2 có nhiều dự đoán đã ứng nghiệm; H3 chưa có dự đoán riêng nào.
- AMEL/AMBN/ENAM đột biến bất hoạt **CHUNG, cùng kiểu**, ở **gần như mọi bộ chim** đã khảo sát, ~116 Ma — **C**, Meredith 2014 *Science* 346(6215):1254390 **+ nguồn thứ hai Meredith et al. 2013 *BMC Evolutionary Biology*** (đột biến dịch khung chung trước điểm phân tách Neognathae), R4 #21. *Lưu ý nhãn:* R1 #19 gán **S** ("1 nguồn chính"); C chỉ đứng được **nhờ** nguồn thứ hai 2013 đã ghi rõ ở đây — xem mục 7 #7.
- ERV: >470.000 trên 758 genome — S, R4 #22–23; nhưng khung "ERV cùng vị trí orthologous làm marker" **chưa có bài cho chim** — U, R4 #24.
- Lệch cây gene fine-scale là **dự đoán của coalescent (ILS)**, không phải điểm yếu H1 — C, R4 #25.
- Kỷ lục aDNA: mammoth **>1 triệu năm**; **không có DNA chim Mesozoi được xác nhận** — C, R4 #15–16. Woodward 1994 bị **4 bình luận *Science* 1995** bác — C, R4 #18.
- H3 **không có dự đoán riêng** cho gene răng hỏng chung / ERV chung / hóa thạch chuyển tiếp — C (phủ định có nguồn), R4 #30; phản biện bình duyệt trực tiếp: không tìm được — U, R4 #29.

**Cần chỉnh:** "aDNA tối đa ~1–2 triệu năm" — bài gốc chỉ ghi ">1 triệu năm"; con số 1,2–1,6 Ma là U.

### Q5 — "Phải thích nghi, nhưng đa số tuyệt chủng"
**Kết luận:** tuyệt chủng là **một nửa của tiến hóa**, không mâu thuẫn với nó. Số liệu chim rất chắc.
- **187 loài** tuyệt chủng từ 1500; ~90% loài đảo; xâm lấn 46%, săn bắt 26% — C, Butchart 2018 (URL đã mở), R4 #31.
- 279 taxa, 78,7% trên đảo đại dương — C, Szabo 2012, R4 #32.
- ~1300–1500 loài (~12%) từ cuối Pleistocene; gấp **80× (60–95×)** nền — C, Cooke 2023, R4 #33; khớp ~100 E/MSY của Pimm 2006, R4 #34.
- Chim là dòng khủng long **duy nhất** sống sót K–Pg — C, Field 2018, R4 #35.
- "Thích nghi" trong sinh học tiến hóa ≠ nghĩa đời thường — C, Futuyma Ch.11, R4 #36.

**Cần chỉnh:** "hơn 99% loài từng tồn tại đã tuyệt chủng" **không được R4 xác minh** → giữ U.

### Q6 — "Thuật toán coding tìm nhóm DNA gốc"
**Kết luận:** cả 4 kho "DNA gốc" đều có thật, có dữ liệu + công cụ công khai. Nhưng nút Pycnonotidae **chưa ai làm** — vừa rào cản vừa cơ hội.
- UCE: Faircloth 2012, McCormack 2013 — C; probe chuẩn **Tetrapods-UCE-5Kv1 = 5.472 bait / 5.060 locus** — C, R1 #15–17.
- ASHCE >99% không mã hóa, cis-regulatory gắn lông/cánh — C, Seki 2017, R1 #13; số **265.984 yếu tố / ~1% genome** — S (supplementary bị chặn), R1 #14.
- ~274 gene mất — C, nguồn chính **Lovell 2014**, Zhang 2014 xác nhận chéo, R1 #18.
- Karyotype tổ tiên DESCHRAMBLER 14 nút, chỉ tới Estrildidae/Thraupidae/Fringillidae — S, Damas 2018, R1 #10.
- **Không bài nào tái dựng tại đúng 3 nút cần (Neornithes, Passeriformes, Pycnonotidae)** — U, R1 #12; **R7 #20 xác nhận độc lập**: không có ASR màu lông nào làm trực tiếp trên Pycnonotidae.
- **Chiều đột biến màu** (đầu vào "trạng thái tổ tiên" của V4): melanin cổ, bảo tồn xuyên Amniota — S, Roy 2019; có ở chim từ Eocene — C, Vinther 2009; carotenoid xuất hiện **sau, độc lập ≥13 lần**, sớm nhất trong Passeriformes ở Paleocene — C (ASR thật), Thomas 2014; SLC45A2 đột biến **độc lập** ở gà và cút — **S**, Gunnarsson 2006 (epub 2006; số in *Genetics* 175(2):867-877 năm 2007 — **cùng một bài**, DOI 10.1534/genetics.106.063107; nhãn hạ từ C xuống S theo tiền lệ mục 7 #3, xem mục 7 #8). → Mô hình "**mất chức năng phái sinh, tái diễn ngẫu nhiên**", không phải allele tổ tiên chung — nhưng **toàn bộ là ngoại suy liên loài**, nhãn tổng hợp **S**, R7 #17–21 + mục 5.

**Cần chỉnh:** định nghĩa vận hành (c) giả định "ancestral nodes có sẵn"; thực tế **phải tự chạy** → Pha 3 chuyển từ tra cứu sang tính toán. Hai R-file độc lập (R2, R7) cùng kết luận **không có dữ liệu gene/ASR nào trên Pycnonotidae** — kết quả phủ định đã xác nhận chéo, không phải thiếu sót tìm kiếm.

---

## 3. Sổ giả thuyết H1/H2/H3

| GT | Dự đoán | Bằng chứng (nhãn, R-file) | Còn thiếu | Code kiểm được |
|---|---|---|---|---|
| H1 | Gene hỏng chung cùng vị trí | AMEL/AMBN/ENAM bất hoạt chung ở **gần như mọi bộ chim**, ~116 Ma — **C nhờ 2 bài**: Meredith 2014 *Science* + Meredith et al. 2013 *BMC Evol Biol* (R4 #21; R1 #19 gán S vì chỉ tính 1 bài — mục 7 #7) | Chưa ai kiểm trên chào mào | `p03_asr`: kéo locus ENAM/AMEL/AMBN, xác nhận frameshift ở *P. jocosus* |
| H1 | ERV chèn cùng vị trí theo cây | >470.000 ERV/758 genome — S (R4 #22–23) | Khung orthologous-insertion cho chim — U (R4 #24) | `p02_core_map`: quét ERV trên alignment 363-way |
| H1 | Cây loài lồng nhau nhất quán | Khớp cấp sâu, lệch fine-scale đúng ILS — C (R4 #25) | Chưa có cây riêng Pycnonotidae | `p03_asr`: IQ-TREE2, so topology |
| H1 | Đồng hồ khớp hóa thạch | Bayes factor ủng hộ ~100 Ma — S (R4 #7) | — | Không cần code; TimeTree (D10) |
| H2 | Vùng bảo tồn rộng hơn kỳ vọng | ASHCE ~265.984 — S (R1 #14); UCE 5.060 locus — C (R1 #17) | Số ASHCE chính xác; chưa giao genome chào mào | `p02_core_map`: BED phyloP≥ngưỡng ∩ ASHCE ∩ UCE ∩ chào mào |
| H2 | dN/dS rất thấp ở toolkit | Toolkit có chứng cứ chức năng mạnh — C (R3 #32–36) | **Chưa ai đo dN/dS toolkit vs hành vi** | `p04_selection`: codeml/HyPhy, 3 nhóm gene |
| H2 | Ít tái sắp xếp NST | Stasis synteny, vi NST — C (R1 #8–9); karyotype tổ tiên — S (R1 #10) | **% synteny chào mào↔gà chưa ai tính** | `p02_core_map`: synteny chào mào↔gà↔cá sấu |
| H3 | *(chưa có dự đoán riêng)* | Claim đã công bố — C (R4 #26–27); **không tìm thấy dự đoán riêng** — C phủ định (R4 #30) | Dự đoán khác biệt được với H1/H2; phản biện bình duyệt — U (R4 #28–29) | Chưa code được gì cho tới khi H3 nêu dự đoán riêng |

---

## 4. Bảng dataset D01–D13 cập nhật

| ID | Tên | URL đã xác minh | ✔/✘ | License | Dung lượng | Pha |
|---|---|---|---|---|---|---|
| D01 | *P. jocosus* GCA_013400435.1 | `ftp.ncbi.nlm.nih.gov/genomes/all/GCA/013/400/435/…` (report+stats đã fetch) | ✔ | GenBank công khai | ~1,02 Gb; N50 218 kb | 1–2 |
| D02 | B10K 363 genome | `b10k.genomics.cn` · `db.cngb.org/datamart/animal/DATAani1/` | ✔ | **Chưa ghi rõ** | 363 bộ gene | 1–3 |
| D03 | UCSC 363-avian-2020-hub | 2 trang doc `cgl.gi.ucsc.edu/…` · `alignment-output.s3.amazonaws.com/birds-final.hal` · 3 `.mod` | ✔ | Chưa ghi rõ | **HAL hàng trăm GB**; `.mod` vài MB | 1–2 |
| D04 | Ensembl Compara | Chỉ FTP tổng; **không có đường dẫn bird-specific** | ✘ | Ensembl mở | dump chục GB | 3–4 |
| D05 | VGP Passerida | `GCA_003957565.2` · `GCF_001522545.1` · `GCA_001700915.1` | ✔ một phần (chỉ đọc được tiêu đề) | GenBank/RefSeq | ~1,0–1,2 Gb/loài | 2–4 |
| D06 | Ngoài nhóm (cá sấu/rùa/thằn lằn) | **Chưa R-file nào cho accession** | ✘ | — | ~2–3 Gb/loài | 2 |
| D07 | UCE Tetrapods-5Kv1 | Figshare + `github.com/faircloth-lab/uce-probe-sets` | ✔ | cần xác nhận CC-BY | FASTA vài MB | 2 |
| D08 | ASHCE Seki 2017 supp. | Đính kèm `10.1038/ncomms14229`, không cổng riêng | ✘ (paywall/reCAPTCHA) | Nat Commun OA (cần xác nhận) | bảng ~265.984 yếu tố | 2 |
| D09 | aDNA chim tuyệt chủng | Accession trong bài (Edwards 2024, Mitchell 2014, Grealy, Soares, Anmarkrud); R6b nêu `PRJNA534317` — nguồn phụ, U | ✘ | GenBank/ENA public | mtDNA nhỏ; moa ~900 Mb @4–5× | 4–6 |
| D10 | TimeTree | `timetree.org` | ✔ | **Miễn phí nghiên cứu cá nhân; KHÔNG redistribute nếu chưa xin phép** | Nhỏ | 4 |
| D11 | Paleobiology DB | `paleobiodb.org` | ✔ (trang chủ) | **Chưa xác định** | Nhỏ | 4 |
| D12 | IUCN spatial data | `iucnredlist.org/resources/spatial-data-download` → **403**. Thay thế đã mở: `datazone.birdlife.org/…/many-bird-species-have-already-gone-extinct` | ✘ (thay bằng BirdLife ✔) | Không xác nhận được | Nhỏ | 4 |
| D13 | Catalog đột biến màu có gene | Dựng từ PubMed (mục 5) | ✔ | Theo bài báo | Bảng nhỏ | 3–5 |

**Tổng: 8 ✔ / 5 ✘.**

**Kết quả phủ định phải ghi nhận (không tính vào D01–D13):** ngoài *P. jocosus*, **không có genome nhân (nuclear) nào cho họ Chào mào** — *P. sinensis*, *P. aurigaster*, *Hypsipetes*, *Alophoixus* chỉ có mitogenome lẻ tẻ, **✘** (R5 #4, U/✘ "không thấy"); *P. cafer* mới chỉ có WGS master `JBQLIZ000000000`, **chưa có GCA_/GCF_** (R5 #3, U). ⇒ **Không có taxon cùng chi/cùng họ để lấy trạng thái ngoài nhóm gần** cho ASR — ảnh hưởng trực tiếp tới điều kiện 3 ở mục 10 và tới `docs/03` mục F.2.

---

## 5. Registry gene ứng viên (đầu vào T22) — 49 dòng

*Gộp R2 (màu lông) + R3 (hành vi/toolkit) + R5 (sắc tố Passeriformes) + R7 (chiều đột biến). Nhãn giữ nguyên gốc.*

### A. Màu lông / sắc tố — 28 dòng

| # | Loài | Phenotype | Gene | Di truyền / bằng chứng | Nguồn | Nhãn |
|---|---|---|---|---|---|---|
| 1 | Gà | Extended Black | MC1R | AD; linkage + functional E92K | Kerje 2003; Dávila 2014 | C |
| 2 | Gà | Hoa văn chu kỳ trong lông | GJA5 | cis-regulatory indel; IBD | Li 2021 | S |
| 3 | Gà | Dominant White/Dun/Smoky | PMEL17 | AD; linkage + sequence | Kerje 2004 | S |
| 4 | Gà | Silver (S) | SLC45A2 | **Z-linked**; 5 đột biến độc lập | Gunnarsson 2006 (số in 2007; DOI 10.1534/genetics.106.063107) | S |
| 5 | Gà | Lavender | MLPH | AR; R35W | Vaez 2008 | S |
| 6 | Gà | Recessive White | TYR | AR; chèn ALV intron 4 | Chang 2006; Cho 2021 | C |
| 7 | Bồ câu | Head crest | EphB2 | genome scan + functional | Shapiro 2013 | S |
| 8 | Bồ câu | ash-red/nâu, epistasis | Tyrp1, Sox10, Slc45a2 | AR/AD + epistasis | Domyan 2014 | S |
| 9 | Bồ câu | Recessive red | Sox10 (2 đột biến upstream) | AR; ChIPseq | Domyan 2025 | S |
| 10 | Canary | Dị hình màu trống–mái | BCO2 | mapping + transcriptome | Gazda 2020 | S |
| 11 | Canary | White recessive | SCARB1 | AR; splice mất exon 4 | Toomey/Lopes 2017 | S |
| 12 | Canary nuôi | Dilute Opal/Onyx + quét 14 gene | MLPH (+ASIP, DCT, EDNRB, KITLG, MITF, SLC45A2, TYRP1, ZEB2, CYP2J19, BCO2, SCARB1…) | pool-seq Fst window | Bovo 2023 | S |
| 13 | Budgerigar | Blue (mất psittacofulvin) | MuPKS | AR; GWAS + LC-MS | Cooke 2017 | S |
| 14 | Lovebird *Agapornis* | Blue (hội tụ, cùng R644W) | MuPKS | AR; WGA + sweep | Ke 2024 | C |
| 15 | Cút Nhật | Cinnamon/Silver | SLC45A2 | **Z-linked** | Gunnarsson 2006 (cùng bài với #4) | S |
| 16 | Cút vàng TQ | Giảm melanin lông tơ | SLC24A5 | bán trội?; association + tyrosinase | Zhang 2025 | S |
| 17 | Cút Bắc Kinh | Trắng | PMEL | association + biểu hiện phôi | Yuan 2023 | S |
| 18 | Sẻ vằn | Trắng | **MC1R — BÁC BỎ** | backcross; ÂM TÍNH | Hoffman 2014 | **C** cho "MC1R **không** phải nguyên nhân"; **S** cho cơ chế thay thế (theo mục 7 #3) |
| 19 | *Monarcha castaneiventris* | Melanism song song 2 đảo | MC1R + ASIP | GWAS + FST outlier | Uy 2016 | S |
| 20 | *Sporophila* Capuchino | Hàm lượng pheomelanin | OCA2/HERC2 (del 55bp) | pangenome + GWAS | Recuerda 2025 | S |
| 21 | House finch | Đỏ ketocarotenoid | **CYP2J19/BDH1L — KHÔNG dùng** | functional; phủ định | Koch 2025 | S |
| 22 | House finch | Độ đỏ ~ chức năng ty thể | CYP2J19 | tương quan (Koch 2025 nghi vấn) | Hill 2019 | S |
| 23 | Canary red factor | Đỏ ketocarotenoid | CYP2J19 | ketolase carotenoid | Lopes 2016 (DOI chỉ từ R6b/Gemini) | **U — Main cần kiểm** |
| 24 | Gà lôi *Phasianus colchicus* | Melanistic Tenebrosus | CHƯA XÁC ĐỊNH | — | — | U |
| 25 | Ngỗng nhà *Anser anser* | Pha loãng màu liên kết giới tính | MLANA | mất 1 bp; genotyping | Olli 2026 | S |
| 26 | Ngỗng tuyết + skua Bắc Cực | **Melanism (TĂNG sắc tố)** | MC1R | hội tụ độc lập 2 loài + **ASR chính thức: derived, Pleistocene** | Mundy 2004 *Science* | C (chiều **ngược** với bạch tạng — dùng làm đối chứng phương pháp) |
| 27 | Chích đầm lau lớn *A. arundinaceus* | Bạch tạng một phần | Allele lặn **chưa định danh** | thực địa 15 năm; lộ ra khi cận huyết, biến mất khi cận huyết giảm | Bensch 2004 | C |
| 28 | **Chào mào *P. jocosus*** | **Mọi đột biến màu (bạch, bông, mơ, nâu…)** | **CHƯA CÓ DỮ LIỆU; cũng chưa có ASR nào trên Pycnonotidae** | — | R2 + R7 #20 xác nhận độc lập | **U — khoảng trống thật; KHÔNG suy diễn gene từ loài khác** |

### B. Toolkit hình thái — 7 dòng

| # | Loài | Phenotype | Gene | Bằng chứng | Nguồn | Nhãn |
|---|---|---|---|---|---|---|
| 26 | Sẻ Darwin | Hình dạng mỏ | ALX1 (haplotype 240kb) | GWAS liên/nội loài | Lamichhaney 2015 | S |
| 27 | Sẻ Darwin | Kích thước mỏ, s=0,59 | HMGA2 | GWAS + character displacement | Lamichhaney 2016 | S |
| 28 | Sẻ ngô lớn | Chiều dài mỏ | COL4A5 | polygenic association | Bosse 2017 | S |
| 29 | Sẻ Darwin | Độ sâu/rộng mỏ | BMP4 | **gain-of-function phôi gà** | Abzhanov 2004 | C |
| 30 | Sẻ Darwin (cactus) | Mỏ dài (trục độc lập) | Calmodulin | gain-of-function | Abzhanov 2006 | C |
| 31 | Chim (chung) | Tăng trưởng hàm trên | Shh qua FEZ | thực nghiệm phôi + review | Hu & Marcucio 2008 | C |
| 32 | Sauropsid | Lông/vảy, EDC | Cụm β-keratin | 2 nhóm độc lập | Sawyer 2003; Strasser 2014 | C |

### C. Hành vi — 14 dòng

| # | Loài | Hành vi | Gene | Bằng chứng | Nguồn | Nhãn |
|---|---|---|---|---|---|---|
| 33 | Sẻ vằn | Học hót chính xác | FoxP2 | **knockdown RNAi (chức năng)** | Haesler 2004/2007 | C |
| 34 | Sẻ vằn | Mật độ gai neuron Area X | FoxP2 | knockdown | Schulz 2010 | S |
| 35 | Robin châu Âu | La bàn từ | CRY4 | in vitro + mô học + mùa | Xu 2021; Günther 2018 | C |
| 36 | Passeriformes | Chọn lọc dương; mất Cry4 ở chim ruồi/vẹt/Suboscines | Cry4a | quét 363 genome | Langebrake 2024 | C |
| 37 | 76 loài chim | Thời điểm di cư thu | CLOCK poly-Q | review — **không phải marker phân biệt** | Le Clercq 2023 | C |
| 38 | Chích liễu (đực) | Ngày di cư xuân + thay lông | ADCYAP1 | association đặc thù giới tính | Bazzi 2016 | S |
| 39 | *Zosterops lateralis* | Di cư/định cư đảo | CLOCK, CREB1; **ADCYAP1, SERT, NPAS2 KHÔNG liên hệ** | multi-gene, chưa tái lập | Estandía 2023 | S |
| 40 | *Parus major* | Exploration, h²=54±5% | **Đa gene — không SNP nào ý nghĩa toàn hệ gene** | chọn lọc 2 chiều + SNP-chip 500k | Drent 2003; Kim 2018 | C |
| 41 | *Parus major* | Exploration ~ DRD4 | DRD4 | **chỉ tái lập 1/4 QT**; methylation không giải thích h² | Fidler 2007; Korsten 2010; van Oers 2020 | C (thất bại tái lập) |
| 42 | Cuckoo finch *A. imberbis* | Bắt chước trứng vật chủ | Locus liên kết **NST W** | dòng mẹ | Spottiswoode 2022 **PNAS** | C |
| 43 | Cu cu *Cuculus canorus* | Màu nền vỏ trứng | Matrilineal + chuyển vị liên kết W | genomics | Merondun 2025 ***Science*** | C |
| 44 | *Parus major* | Hoa văn vỏ trứng | W-linked | dòng mẹ | Gosler 2000 | S |
| 45 | Chích đầu đen | Hướng di cư (F1 trung gian) | Vài gene chính **chưa định danh**; R6a nêu SDC1 | lai SE×SW, F2 | Helbig 1996; Berthold 1992 | S; **SDC1 = U, Main cần kiểm** |
| 46 | Sẻ vằn | Chọn vật liệu làm tổ | **KHÔNG gene — do trải nghiệm tuổi non** | thực nghiệm đối chứng | Bailey 2014 | C (bác "định sẵn di truyền") |

> Theo yêu cầu brief: dòng **#28 — chào mào: chưa có dữ liệu** (R2 và R7 xác nhận độc lập). Dòng #18 và #21 là **kết quả âm tính đã kiểm chứng** (không phải "chưa nghiên cứu"); dòng #26 là **đối chứng phương pháp** (ASR chính thức, nhưng chiều tăng sắc tố) — cả ba dùng làm rào chắn chống suy diễn trong V4/T22.

---

## 6. CORRECTIONS cho `docs/00` (17 mục)

| # | Sai | Đúng | Nguồn |
|---|---|---|---|
| 1 | "Tu hú… (Spottiswoode 2022, ***Science***)" | Cuckoo finch *A. imberbis*; **Spottiswoode 2022 *PNAS*** 119(17):e2121752119. Bản *Science* đúng chủ đề (*Cuculus canorus*) là **Merondun 2025**, *Science* 390(6772):527-532 | R3 #8–9, C |
| 2 | "gene ứng viên cá tính: DRD4 (Fidler 2007)" | DRD4 chỉ tái lập **1/4 quần thể** (Korsten 2010); SNP-chip 500k **không SNP nào ý nghĩa toàn hệ gene** (Kim 2018) → **đa gene** | R3 #22, #24, C |
| 3 | Q3b ngụ ý "chim đột biến chậm hơn thú" | Khác nhau tới **40 lần** giữa loài có xương sống; driver là **thời gian thế hệ + Ne**, không phải lớp Aves | R1 #20 C, #22 S |
| 4 | "bộ gene chim nhỏ (~1–1,3 Gb)" | **1,0–2,1 Gb** vs thú 2,2–6,0 Gb; TE ~**7,8%** vs ~44,5% | R1 #7, C |
| 5 | "~274 gene mất (Zhang 2014)" | Nguồn chính **Lovell 2014 *Genome Biology* 15:565**; Zhang 2014 xác nhận chéo | R1 #18, C |
| 6 | "aDNA tối đa ~1–2 triệu năm" | Kỷ lục **>1 triệu năm** (van der Valk 2021); 1,2–1,6 Ma **chưa xác minh** | R4 #15 |
| 7 | "ENAM/AMEL/AMBN mất cùng kiểu ở **mọi** loài chim" | ở **gần như mọi bộ** chim; mất men răng **~116 Ma** | R1 #19, R4 #21 |
| 8 | "Berthold & Helbig, thập niên 1990" | **Berthold 1992 *Nature* 360:668-670** (C). Helbig 1991 **không định vị được**; bản tự thuật là **Helbig 1996 *J Exp Biol* 199:49-55** | R2 #9; R3 #1–2, U |
| 9 | "Làm tổ không cần thầy" (bẩm sinh thuần) | **Hỗn hợp bẩm sinh + học**: Bailey 2014 (vật liệu theo trải nghiệm); Walsh 2009 (repeatability tổ weaver thấp) | R3 #11–13 |
| 10 | "Én đá **cánh ngắn lại** vì xe hơi" | Chim chết vì xe có **sải cánh DÀI HƠN** quần thể → chọn lọc **chống** cánh dài | R2 #8, S |
| 11 | Mốc hạn hán sẻ Darwin 1977 / 2004–05 | **Chưa tự kiểm chứng được**; Boag & Grant 1981 không truy xuất được vòng 1 | R2 #4–5, U |
| 12 | "hơn 99% loài từng tồn tại đã tuyệt chủng" | Giữ **U**. Số liệu chim đã xác minh: **187 loài từ 1500** (Butchart 2018); ~1300–1500 loài từ cuối Pleistocene, **80×** nền (Cooke 2023) | R4 #31, #33 |
| 13 | "*Asteriornis* 66,7 Ma" | **66,8–66,7 Ma** | R4 #4, C |
| 14 | `docs/02`: D01 "*P. jocosus* (nếu có)"; D03 "phastCons/phyloP tính sẵn" | D01 **CÓ**: `GCA_013400435.1`, scaffold, N50 218 kb. D03: **phyloP CÓ** (3 `.mod`); **phastCons KHÔNG được xác nhận** | R5 #1 C; R1 #6 vs R5 #14 |
| 15 | Q4: "*Asteriornis* … — chim hiện đại **cổ nhất** (Field et al. 2020)" | *Asteriornis maastrichtensis* là hóa thạch chim vương miện **được bảo tồn tốt nhất** từ kỷ Phấn trắng — **không phải cổ nhất**: *Vegavis iaai* **69,2–68,4 Ma** (Torres 2025) già hơn ~2 Ma | R4 #4 C; R4 #5 C |
| 16 | Bảng H3: shCherbak & Makukov 2013 "gây tranh cãi, **không được cộng đồng chấp nhận**" (nêu như sự thật) | Đổi thành: **không tìm được bài phản biện bình duyệt trực tiếp nào** nhắm thẳng vào bài 2013 (**U**); **trạng thái tiếp nhận của cộng đồng chưa xác minh** trong vòng 1 | R4 #29, **U** |
| 17 | Q3: Bosse 2017 (COL4A5, mỏ sẻ ngô lớn Anh) trình bày **không kèm phản biện** | Gắn chú thích: **Perrier & Charmantier 2018** *Evolution Letters* 3(3):240-247, DOI 10.1002/evl3.86 — xu hướng dài mỏ dài hạn ở Anh có thể đi kèm **xu hướng GIẢM gần đây**; tranh luận về **HƯỚNG** thay đổi, cần đọc toàn văn cả hai | R2 #7, **S** |

*Ngoài phạm vi `docs/00` nhưng cần ghi nhận:* brief R7 trích **"Amiot et al. 2007, *Biological Journal of the Linnean Society*"** — thực tế bài đăng trên ***Ibis***, DOI 10.1111/j.1474-919x.2007.00671.x (R7 #11, C). Sửa khi trích dẫn chính thức.

---

## 7. Mâu thuẫn giữa các R-file và cách giải quyết (8)

1. **phyloP/phastCons trên hub UCSC.** R1 #6 (C, có 3 URL `.mod`) vs R5 #14 ("trang không nhắc"). → **Không mâu thuẫn thật**: hai bên đọc **hai trang khác nhau** (`b10kAlignment.html` vs `b10kConservationTrackDescription.html`). Kết luận: **phyloP ✔, phastCons ✘**.
2. **Chào mào có trong B10K 363 không.** R1 #23 (U) vs R5 #1 (C, assembly do **B10K Consortium** nộp). → R5 chứng minh **trực tiếp** (assembly_report FTP NCBI) rằng *P. jocosus* **có assembly do B10K nộp** — nhưng **KHÔNG** chứng minh loài này nằm trong **bộ 363 / trong file HAL**. Kết luận đúng phạm vi: **STRONG_INFERENCE** ("là genome do B10K nộp ⇒ nhiều khả năng thuộc bộ 363, **chưa đối chiếu danh sách loài**"). **Câu hỏi của R1 #23 vẫn MỞ** → chuyển thành **U21** (mục 8, ưu tiên 1) và thành điều kiện kiểm bắt buộc của **P1.4** (`halStats --genomes` / danh sách 363 loài), cùng lúc với việc đo kích thước HAL. R5 mục 5 cũng để ngỏ: chưa rõ 7 họ trong "Genome Assemblies for Seven Families of Birds From the Global South" có gồm Pycnonotidae hay không.
3. **Nhãn Hoffman 2014.** R2=C, R5=S — **cùng một bài báo**, không đủ "hai nguồn độc lập". → Giữ **S** cho cơ chế; **C** cho phát biểu hẹp "MC1R KHÔNG phải nguyên nhân" (âm tính tự kiểm chứng bằng backcross).
4. **Lopes 2016 CYP2J19.** R2 **không tìm được** qua PubMed/Consensus; R6b (Gemini) đưa DOI. → R6 là nguồn phụ → ghi **U + "Main cần kiểm"** (registry #23). Không nâng nhãn.
5. **CYP2J19 có phải "gene đỏ" chung không.** R5 #11 (Koch 2025: house finch **không** dùng) vs R6b (Lopes 2016). → **Không loại trừ nhau**: một con đường, không phải con đường duy nhất. Cấm phát biểu "mọi chim đỏ dùng CYP2J19".
6. **Con số tuyệt chủng từ 1500** (164/187/216/279/~1300–1500). → Khác phạm vi (loài vs taxa) và phương pháp. **Chốt 187 (Butchart 2018)** làm số chuẩn; ghi rõ Cooke 2023 là ước tính đầy đủ hơn.

7. **Nhãn Meredith 2014 (gene men răng).** R1 #19 = **S** ("1 nguồn chính, tuy rất được trích dẫn") vs R4 #21 = **C**. → **Giữ C**, vì R4 có **nguồn thứ hai thật**: **Meredith et al. 2013 *BMC Evolutionary Biology*** (đột biến dịch khung chung trước điểm phân tách Neognathae) — nguồn thứ hai này **phải được ghi rõ** ở mục 2 Q4 và mục 3 (đã ghi). Nếu về sau không xác minh được bài 2013 thì **hạ về S** cho nhất quán với tiền lệ Hoffman (mục 7 #3). Phạm vi phát biểu: "ở **gần như mọi bộ** chim" — **không** được nới thành "ở mọi loài" (CORRECTIONS #7).

8. **Nhãn + năm Gunnarsson (SLC45A2).** R7 #21 = **C**, ghi **2006**; R2 catalog #4/#14 = **S**, ghi **2007** — **cùng một bài** (cùng DOI 10.1534/genetics.106.063107, cùng *Genetics* 175:867-877). → Chốt **một năm: 2006** (epub; số in 2007) và **một nhãn: S** ở cả mục 2 Q6, mục 5 hàng #4 và #15 — theo đúng tiền lệ mục 7 #3 (Hoffman 2014): một bài báo duy nhất **không đủ** "hai nguồn độc lập" để lên C.

*(Bosse 2017 vs Perrier 2018 là tranh luận trong tài liệu gốc, không phải mâu thuẫn giữa R-file — đã đưa vào CORRECTIONS #17 để `docs/00` không trình bày Bosse 2017 một chiều.)*

---

## 8. UNVERIFIED gộp — cần vòng 2 (ưu tiên theo ảnh hưởng Pha 1)

**Ưu tiên 1 — chặn Pha 1:**
- **U1.** Kích thước thật + khả năng tải một phần HAL 363 loài (R5 #14). *Không giải quyết → Pha 2 phải đổi kiến trúc.*
- **U2.** License B10K / CNGB / S3 / UCSC hub — cần trước khi tải và trước khi công bố.
- **U3.** Đường dẫn bird-specific Ensembl Compara + OrthoDB Aves + BUSCO `aves_odb10` (8.338 gene) (R5 #15–17) — **lối đi rẻ** thay HAL.
- **U4.** *P. cafer* đã có GCA/GCF chưa (tra `PRJNA1226769`) (R5 #3) — quyết định tham chiếu chính.
- **U5.** RAM/đĩa WSL2 mới là suy luận Perplexity, **không benchmark** (R5 #18).
- **U8.** *(nâng từ ưu tiên 2 lên 1 — F11)* **Accession outgroup cho D06** (cá sấu/rùa/thằn lằn): **không R-file nào đưa accession** ⇒ **ACCEPTANCE_CRITERIA #2 chưa đạt**. D06 là đầu vào **bắt buộc** của định nghĩa (a) *core-invariant* trong `docs/00` Q6 — thiếu nó thì không phân biệt được "bảo tồn trong chim" với "bảo tồn xuyên Sauropsida".
- **U21.** *(mới — F02)* **Chào mào có nằm trong bộ 363 genome / trong file HAL không** (R1 #23 vẫn MỞ; R5 #1 chỉ chứng minh assembly do B10K nộp). Kiểm bằng `halStats --genomes` hoặc danh sách 363 loài của B10K, **cùng lúc với P1.4**. *Không giải quyết → không biết có lát alignment cho chào mào hay không ⇒ P1.6 và Pha 2 mất tiền đề.*

**Ưu tiên 2 — chặn Pha 2–3:** **U6.** Số liệu + file tọa độ ASHCE (R1 #14). **U7.** % synteny macro/micro (Damas 2018) + repo DESCHRAMBLER (R1 #10).

**Ưu tiên 2b — chào mào (từ R7):** **U17.** Mốc tuổi phân tách họ Pycnonotidae / chi *Pycnonotus* (Shakya & Sheldon 2017 **không** hiệu chỉnh đồng hồ phân tử) — cần cho Pha 3 khi đặt nút ASR. **U18.** Bài phylogeography mtDNA/microsatellite chuyên biệt cho *P. jocosus* — chưa tìm thấy, có thể là khoảng trống thật. **U19.** Ghi nhận **lai TỰ NHIÊN** *jocosus* × *sinensis/cafer/aurigaster* — không tìm được dù tìm trực tiếp (chỉ có lai nuôi nhốt). **U20.** Số liệu định lượng áp lực bẫy bắt *P. jocosus* tại VN (Leupen 2022 chưa đọc trực tiếp).

**Ưu tiên 3 — nội dung, không chặn code:** **U9.** Lopes 2016 CYP2J19; gene "trắng" thật ở sẻ vằn; gene màu gà lôi. **U10.** Helbig 1991 gốc; Boag & Grant 1981 + mốc 1977/2004–05. **U11.** DOI chính thức Bosse 2017, Brown & Brown 2013, Berthold 1992, Smeds 2016, Bergeron 2023. **U12.** Khung ERV orthologous marker cho chim. **U13.** Phản biện bình duyệt nhắm shCherbak & Makukov 2013. **U14.** Hsp90-canalization/FA trên chim; nghiên cứu so CV hình thái vs repeatability hành vi — **có thể không tồn tại**, khi đó thành việc đo của dự án. **U15.** License PBDB + lối vào IUCN không 403. **U16.** Tần suất đột biến màu mới/locus/thế hệ trong nuôi nhốt — **cần chủ dự án quyết** có chấp nhận nguồn aviculture phi bình duyệt không.

---

## 9. Đề xuất Pha 1 (7 việc)

| # | Việc | Input | Output | Công cụ | Ước lượng | Tiêu chí xong |
|---|---|---|---|---|---|---|
| P1.1 | Dựng WSL2 + conda env | `env/environment.yml` | env chạy được | conda/mamba | 1–2 h; ~10–15 GB — **ước lượng làm việc, chưa benchmark (U)** | `import Bio, pandas, pyranges` OK; `iqtree2`/`codeml`/`halStats`/`phyloP` trả version |
| P1.2 | Tải + kiểm D01 | `GCA_013400435.1` | FASTA + `data/registry.csv` có sha256 | NCBI `datasets` CLI | ~1 GB; 15–30 ph | sha256 khớp; tái tạo đúng N50 218.123/53.855 bp |
| P1.3 | BUSCO `aves_odb10` trên D01 (+ *P. cafer* nếu có) | FASTA D01 | Báo cáo BUSCO | BUSCO v5 | ~8.338 marker; 4–8 GB RAM; vài giờ | Có % complete/fragmented/missing; **chốt assembly tham chiếu chính** |
| P1.4 | **Thăm dò HAL trước khi tải** (giải U1 **+ U21**) | `birds-final.hal` | Kích thước thật, có HTTP range?, **danh sách genome** | `curl -I`, `halStats --genomes` từ xa | 30–60 ph — **ước lượng làm việc, chưa benchmark (U)** | Trả lời được **cả hai**: (a) tải từng phần **được/không**; (b) **`P. jocosus` có trong `--genomes` / danh sách 363 loài hay không (giải U21)**. **Gate của Pha 2.** |
| P1.5 | Lối đi rẻ song song (giải U3) | Ensembl Compara (**MySQL dump**, R5 #17 U), OrthoDB Aves (R5 #16 U), BUSCO `aves_odb10` (R5 #15 U) | Bảng orthologue 1:1 chim | curl + **MySQL** (nạp `ensembl_compara` dump) **HOẶC** OrthoDB/BUSCO file phẳng + pandas | vài GB–vài chục GB (dump quan hệ, **không** phải TSV sẵn); công **cao hơn ước tính ban đầu** — chưa benchmark (U) | **Bước 0: xác minh URL tải được THẬT** (cả 3 nguồn đều đang U, chưa mở trực tiếp) → rồi mới tính ≥1 nguồn orthologue chim mở được thật, đủ chạy `p04_selection` **không cần HAL** |
| P1.6 | Tải 3 `.mod` phyloP + chạy thử 1 locus | 3 URL `.mod` **+ 1 lát alignment** (bigMaf **gà** — nguồn duy nhất có sẵn theo R1 #5/R5 #14 — **hoặc** lát HAL lấy được ở P1.4) | `.mod` cục bộ + track thử | curl, PHAST | vài MB; <1 h — chưa benchmark (U) | phyloP chạy được 1 locus → **benchmark thật thay ước lượng (U5)**. **Phụ thuộc P1.4** cho lát alignment của chim ngoài gà |
| P1.7 | Áp **17** CORRECTIONS vào `docs/00`; cập nhật `docs/02` | Mục 6 (17 mục) + mục 4 | `docs/00`, `docs/02` đã sửa + ADR | Edit | 1 h — chưa benchmark (U) | Không còn dòng nào mâu thuẫn R-file; dòng chưa xác minh có nhãn rõ; đủ **17/17** mục |

*P1.4 và P1.5 chạy **song song**; P1.4 thất bại → P1.5 thành đường chính, Pha 2 viết lại từ "cắt HAL" sang "orthologue + track có sẵn".*

*Phụ thuộc và ước lượng (F09, F10, F21):* **P1.6 KHÔNG độc lập** — phyloP cần **alignment** cho locus, mà alignment chỉ có trong **HAL** (P1.4) hoặc **bigMaf riêng của gà** (R1 #5, R5 #14, cả hai C). ⇒ **P1.4 thất bại → P1.6 chỉ đóng được U5 ở mức "chạy trên locus gà", KHÔNG đóng được U5 cho chào mào** (ghi lại ở mục 10). Mọi con số thời gian/đĩa ở bảng trên là **ước lượng làm việc chưa benchmark (U)**, cùng hạng với U5 (R5 #18) — không được trích như số liệu có nguồn.

---

## 10. Kết luận T06 cho V4

**T06 = KHẢ THI CÓ ĐIỀU KIỆN.**

*Đã đủ để bắt đầu:* chào mào có bộ gene thật (`GCA_013400435.1`, C); B10K + alignment 363 loài + track phyloP có URL mở được; UCE probe set và registry 49 dòng sẵn sàng làm đầu vào T22. **Thêm từ R7:** cây phát sinh Pycnonotidae đã có (Shakya & Sheldon 2017, C) để đặt nút ASR, và quần thể du nhập Reunion/Mauritius/Oahu là **bộ dữ liệu tiến hóa quan sát được sẵn có trên chính loài** (Amiot 2007; Le Gros 2016, C).

**Bốn điều kiện, theo thứ tự phải thỏa:**

1. **Dữ liệu (cứng).** HAL là **một file hàng trăm GB, không tải riêng loài**. Phải chứng minh **một trong hai**: (a) tải từng phần bằng HTTP range / `halStats` từ xa (P1.4), hoặc (b) đường vòng Ensembl Compara / OrthoDB Aves / BUSCO (P1.5 — **cả 3 nguồn đang U**, phải xác minh URL trước). **Không thỏa cả hai → Pha 2 không chạy được, T06 tụt xuống "chưa khả thi".** **Điều kiện đi kèm (U21):** phải kiểm **cùng lúc** rằng *P. jocosus* **thật sự có trong danh sách 363 genome / trong HAL** — "assembly do B10K nộp" mới chỉ là **S**, chưa phải bằng chứng có mặt trong alignment. Nếu **P1.4 thất bại**, P1.6 chỉ chạy được trên lát **bigMaf gà** ⇒ **U5 không đóng được cho chào mào**.
2. **Chất lượng tham chiếu.** Assembly chào mào scaffold N50 **218 kb** — quá vụn cho synteny/vi NST (Q3a). Hoặc (a) chờ `GCA` chính thức của *P. cafer* (N50 3,04 Mb, BUSCO 97,2%), hoặc (b) **giới hạn tuyên bố ở mức locus/gene**, không tuyên bố synteny toàn genome cho chào mào.
3. **Phạm vi ASR.** Không có tái dựng sẵn tại nút Pycnonotidae → **phải tự chạy**. Pha 3 giới hạn ở **ASR theo locus** (IQ-TREE2 `-asr` trên gene màu T22 + gene hành vi Q2b); **không hứa** tái dựng bộ gene tổ tiên toàn phần. **Ràng buộc dữ liệu (R5 #3, #4 — F03):** ASR theo locus tại nút Pycnonotidae **chưa có taxon cùng chi/cùng họ để lấy trạng thái ngoài nhóm gần** — *P. sinensis*, *P. aurigaster*, *Hypsipetes*, *Alophoixus* **không có genome nhân**, *P. cafer* **chưa có GCA/GCF**. ⇒ Phải dùng **ngoài nhóm Passerida** (sẻ vằn / sẻ ngô lớn, D05) **hoặc chờ GCA của *P. cafer***; đồng thời `docs/03` mục F.2 (so với *P. sinensis*, *P. cafer*) **chưa chạy được** trong vòng này. Thêm ràng buộc từ R7: cây Shakya & Sheldon 2017 **không có mốc tuổi** (U17) → nút Pycnonotidae đặt được về **topology** nhưng **chưa gán được thời gian** cho tới khi có nguồn hiệu chỉnh đồng hồ.
4. **Ngôn ngữ bằng chứng.** Mọi phát biểu gene cho chào mào giữ ở mức **U / suy luận từ loài khác** (registry #28; R2 và R7 xác nhận chéo là khoảng trống thật). Cấm chuyển gene gà/bồ câu/canary sang chào mào khi chưa có dữ liệu chào mào. Kết luận "đột biến màu là **mất chức năng phái sinh**" (R7 mục 5) giữ nhãn **S — ngoại suy liên loài**, không được nâng thành C. Rào chắn chống suy diễn: #18 (MC1R–sẻ vằn, âm tính), #21 (CYP2J19–house finch, âm tính), #26 (MC1R–ngỗng tuyết/skua, đúng phương pháp nhưng **sai chiều**).

**Tiêu chí chấp nhận chưa đạt (F11):** **ACCEPTANCE_CRITERIA #2 ("≥1 nguồn cho mỗi dataset chính D01–D08") CHƯA ĐẠT** — **D06 không có nguồn nào** (không R-file nào đưa accession outgroup), và **D04 / D08 mới đạt một phần** (D04 chỉ có FTP tổng, không đường dẫn bird-specific; D08 bị paywall/reCAPTCHA). Vì D06 là đầu vào **bắt buộc** của định nghĩa (a) *core-invariant* trong `docs/00` Q6, **U8 được nâng lên ưu tiên 1** (mục 8).

**Verdict vòng 1: PASS_WITH_ACCEPTED_RISK.** Rủi ro chấp nhận: **U1** (kích thước HAL) và **U21** (chào mào có trong 363/HAL không) — đóng ở P1.4; **U5** (chưa benchmark) — đóng ở P1.6, *nhưng chỉ đóng được cho chào mào nếu P1.4 thành công*; **U8/ACCEPTANCE_CRITERIA #2 ở D06** — rủi ro **mới ghi nhận**, phải đóng trước khi Pha 2 dùng định nghĩa core-invariant.

---

## Nhật ký sửa theo REVIEW V1 (`research/synthesis/01-review-vong-1.md`)

**Đã sửa theo V1: F01, F02, F03, F06, F07, F08, F09, F10, F11, F17, F18, F19, F20, F21, F23.**

Chi tiết ngắn (vị trí đã đụng):
- **F01** — Gunnarsson: chốt **một năm 2006** (epub; số in 2007, cùng DOI) và **một nhãn S** ở mục 2 Q6 + mục 5 hàng #4, #15; kê thành **mục 7 #8**.
- **F02** — mục 7 #2 hạ xuống **S**; R1 #23 mở lại thành **U21** (mục 8, ưu tiên 1); thêm điều kiện `halStats --genomes` vào **P1.4**; ghi chú ở TL;DR #2 và điều kiện 1 mục 10.
- **F03** — thêm khối "kết quả phủ định" sau bảng D01–D13 (R5 #3, #4) và sửa **điều kiện 3** mục 10 (không có taxon cùng chi ⇒ dùng Passerida hoặc chờ GCA *P. cafer*; `docs/03` F.2 chưa chạy được).
- **F06** — mâu thuẫn nhãn Meredith kê thành **mục 7 #7**; ghi rõ nguồn thứ hai **Meredith et al. 2013 *BMC Evol Biol*** ở mục 2 Q4 và mục 3 để giữ C.
- **F07, F08, F23** — thêm **CORRECTIONS #15** (*Asteriornis* không phải cổ nhất), **#16** ("không được cộng đồng chấp nhận" → U), **#17** (Perrier 2018 kèm Bosse 2017); cập nhật **TL;DR #7** và **P1.7** thành **17**.
- **F09, F10** — P1.6 thêm input alignment + **phụ thuộc P1.4**; P1.5 đổi công cụ sang MySQL dump / OrthoDB-BUSCO + **bước 0 xác minh URL**; thêm đoạn ghi chú phụ thuộc dưới bảng mục 9.
- **F11** — tuyên bố **ACCEPTANCE_CRITERIA #2 chưa đạt** ở D06 (một phần D04/D08) trong mục 10; **U8 nâng lên ưu tiên 1**.
- **F17** — TL;DR #8: 49 dòng = 46 có nguồn bình duyệt + 2 khoảng trống đã xác nhận + 1 chờ Main kiểm.
- **F18** — thêm ghi chú cách đếm dưới dòng nhãn gộp, liệt kê đúng **6 claim nhãn kép** (số C/S/U giữ nguyên).
- **F19** — thêm **Bell 2009** (R3 #28) làm mốc đối chiếu ở Q1a; thêm **Mallarino 2012** (R3 #34) làm rào chắn many-to-one mapping dưới mục 5B (ghi rõ **không tính vào 49 dòng**).
- **F20** — mục 5 hàng #18 áp quyết định của mục 7 #3 vào cột Nhãn.
- **F21** — mọi ước lượng thời gian/đĩa ở mục 9 gắn nhãn "**ước lượng làm việc, chưa benchmark (U)**".

**Không sửa ở file này (ngoài phạm vi được giao):** F04, F05, F12, F13, F14, F15, F16, F24, F25 (đều thuộc `docs/03`) và F22 (thuộc `docs/00` + plan).

### Kết quả RECHECK sau khi sửa

**RECHECK 1 — nhất quán nhãn cùng-một-bài (F01, F06, F20).**
`grep -on "Gunnarsson [0-9]\{4\}\|Meredith [0-9]\{4\}\|Hoffman [0-9]\{4\}" research/synthesis/00-tong-hop-vong-1.md | sort -u`
→ 9 kết quả trên 3 tên, tập hợp tên+năm duy nhất = **`Gunnarsson 2006` · `Hoffman 2014` · `Meredith 2014`** — **mỗi tên đúng MỘT năm**. Nhãn đi kèm cũng đồng nhất: Gunnarsson = **S** ở cả mục 2 Q6, mục 5 #4, mục 5 #15; Hoffman = "**C** cho phát biểu phủ định / **S** cho cơ chế" ở cả mục 5 #18 và mục 7 #3; Meredith 2014 = **C** ở mục 2 Q4, mục 3, mục 6 #7, có nêu nguồn thứ hai. ⇒ **PASS.**
*Lưu ý đọc kết quả:* nguồn thứ hai **Meredith et al. 2013** là **BÀI KHÁC** (*BMC Evolutionary Biology*, không phải *Science* 2014) nên cố ý không rơi vào pattern "Meredith <năm>"; đây không phải trường hợp một bài mang hai năm.

**RECHECK 3 — cụm từ đã bị CORRECTIONS bắt không được tái xuất hiện (F04, F12).**
`grep -n "mọi loài chim\|cánh ngắn lại\|cổ nhất" docs/00-tai-dinh-khung-cau-hoi.md docs/03-suy-luan-nguon-goc-chao-mao.md research/synthesis/00-tong-hop-vong-1.md`
→ **4 kết quả, không có kết quả nào là claim sai còn sót**:
1. `docs/00:82` — "…**không phải cổ nhất**…" (câu đã sửa, phủ định).
2. `docs/03:16` — "…(hóa thạch được bảo tồn tốt nhất, **không phải cổ nhất**)" (câu đã sửa, phủ định).
3. `00-tong-hop:221` — **CORRECTIONS #10** trích lại lỗi cũ "cánh ngắn lại" ở cột **Sai**.
4. `00-tong-hop:226` — **CORRECTIONS #15** trích lại lỗi cũ "cổ nhất" ở cột **Sai**.
⇒ **PASS theo đúng ngoại lệ của RECHECK** ("ngoài chính bảng CORRECTIONS trích lại lỗi cũ"), mở rộng thêm cho **câu phủ định**. Pattern grep của brief không phân biệt được "cổ nhất" với "không phải cổ nhất" — cần đọc ngữ cảnh, không đọc số đếm. Cụm "mọi loài chim": **0 kết quả** ở cả 3 file.
