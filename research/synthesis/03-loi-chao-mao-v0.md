# 03 — LÕI chào mào v0 (sản phẩm A + B)

Ngày 2026-09-09. Tác giả: root/S3 (opus/refiner). Brief: `research/briefs/S3-bao-cao-loi-chao-mao-v0.md`.
Nguồn số: `data/a2/` (chạy 2026-09-08 22:55–23:17, lệnh `enrich` 2026-09-09 07:57). Không chạy lại pipeline khi viết báo cáo này.

Quy ước nhãn: kết quả tính toán của chính dự án ghi **[đo được]**; nhãn C/S/U chỉ dùng cho claim lấy từ tài liệu ngoài.
Gọi tên đúng: đây là **vùng chịu chọn lọc lọc, bảo tồn từ tổ tiên chung của lớp chim**, không phải "DNA khủng long còn nguyên".

---

## 1. TL;DR

- LÕI-363 trên tọa độ gà: 70.370.065 khoảng vào → **2.947.588 phần tử** sau gộp (gap ≤10 bp, giữ ≥20 bp); 134.568.082 bp bảo tồn thật, span sau gộp 239.658.099 bp. **[đo được]**
- Ánh xạ sang bộ gene chào mào (minimap2 asm20): **248.461 phần tử (8,43%) = 62.491.397 bp = 6,10% bộ gene 1,02 Gb** ở ngưỡng coverage ≥0,8; **411.275 phần tử (13,95%) = 88.415.707 bp = 8,63%** ở ngưỡng ≥0,5. **[đo được]**
- Tỉ lệ ánh xạ phụ thuộc mạnh vào độ dài: 0,25% ở nhóm 20–49 bp, 74,03% ở nhóm ≥500 bp (cov ≥0,8). 60,05% số phần tử nằm ở nhóm 20–49 bp — phần lớn LÕI hiện **chưa** được ánh xạ. **[đo được]**
- Lõi đã ánh xạ nằm ở: **CDS 24,3%** (15.182.650 bp) · **intron 11,0%** (6.905.274 bp) · **liên gene 64,7%** (40.403.473 bp) · exon không mã hóa 0,0% (do GFF assembly này không có exon ngoài CDS). **[đo được]**
- Vùng mã hóa chỉ chiếm **1,93%** bộ gene chào mào (19.763.303 bp CDS hợp nhất từ GFF) nhưng chứa **24,3%** lõi → **giàu gấp 12,6 lần** so với rải ngẫu nhiên; tương đương **76,8% toàn bộ CDS của chào mào nằm trong lõi** (đây là **giới hạn trên**, xem mục 5 và 7). **[đo được]**
- Hai bảng gene cho **hai danh sách hoàn toàn không trùng nhau**: theo tổng bp là Znf521/Sox6/Foxp1 (gene dài 160–224 kb), theo mật độ bp/kb là Hoxa5/Hoxa11/Hoxa3 (gene 2–3 kb). Chỉ đọc bảng tổng bp là sai phương pháp. **[đo được]**
- Lệnh `enrich` báo **8.450/10.729 gene "qua ngưỡng FDR"** — con số này **KHÔNG** được dùng để tuyên bố ý nghĩa thống kê (base trong một vùng lõi không độc lập), chỉ dùng để **xếp hạng**. **[đo được, diễn giải hạn chế]**
- Đối chứng âm (bộ **accelerated**, `pipeline/p02_core_map/launch_accel.sh` → `data/a2_accel/`) **đang chạy, chưa có kết quả**; tại thời điểm viết `data/a2_accel/` chưa tồn tại nên chưa có cột `accel_fold`/`ca_ratio`.
- Chưa có mô hình nền (permutation khớp %GC) → mọi so sánh "giàu/nghèo" ở mục 5 là **so sánh thô**, không phải kiểm định.

---

## 2. Cách làm

- Đầu vào A: `ancRep_separate_models_rev.bw.conserved.bb` (UCSC B10K 363-avian-2020, tọa độ gà galGal4), sha256 `9a5a5d17…3fe1fd83`, đã ghi `data/registry.csv`.
- Đầu vào B: bộ gene chào mào NCBI **GCA_013400435.1 / ASM1340043v1** — `genomic.fna.gz` sha256 `c88a4b31…d9245c09`, `genomic.gff.gz` sha256 `aaf14098…0659b77c`; tọa độ tham chiếu gà từ `Gallus_gallus.2bit`.
- Công cụ (Docker): kent `bigBedToBed` + `twoBitToFa`; **minimap2 `-x asm20`** với `-k 13 -w 5 -s 30 -m 20 -n 2 -K 10M -f 0.001`, 2 luồng, bộ gene chia mảnh ≤90.000.000 bp (12 mảnh, 60.582 sequence, 1.024.591.993 base — `data/a2/run.log`).
- Code: `pipeline/p02_core_map/conserved_to_bulbul.py` (stdlib, streaming) — `merge --gap 10 --min-len 20` → `paf2bed --min-identity 0.70 --min-coverage 0.80` (và bản `--min-coverage 0.50`) → `annotate` (GFF) → `enrich --chrom-sizes` (`P₀ = 0,0603613`, `total_space = 1.035.289.814`).
- Đầu ra + sha256 (`data/a2/SHA256SUMS.txt`): `bulbul_core.bed` `3c30352b…4ee67a68` · `bulbul_core.cov50.bed` `2d2424bd…12b4dbbb` · `elements.paf` `64def027…dfadc660` · `elements.bed` `3c5cbb5e…01733249`.
- Lưu ý phiên bản không gian: `run.log` đếm **1.024.591.993 bp** từ FASTA NCBI (dùng làm mẫu số "% bộ gene" trong báo cáo này), còn `enrich` dùng `Pycnonotus_jocosus.chrom.sizes` của UCSC hub = **1.035.289.814 bp**; chênh ~1,0% giữa hai nguồn, đã ghi để người đọc sau không nhầm.

---

## 3. Kết quả A — LÕI-363 trên tọa độ gà

| Chỉ số | Giá trị | Nguồn |
|---|---|---|
| Khoảng vào (mục bigBed, phần lớn 1 bp) | 70.370.065 | `merge_stats.tsv: intervals_in` |
| Phần tử sau gộp (gap ≤10 bp, ≥20 bp) | **2.947.588** | `merge_stats.tsv: elements_out` |
| bp bảo tồn thật (trước gộp) | 134.568.082 | `merge_stats.tsv: bp_in` |
| bp span sau gộp (gồm khe ≤10 bp) | 239.658.099 | `merge_stats.tsv: bp_out` |

`bp_out > bp_in` là đúng theo thiết kế: gộp khe ≤10 bp nên span nuốt cả phần khe không bảo tồn. Con số dùng để nói "LÕI-363 lớn bao nhiêu trên gà" là **134.568.082 bp** (≈12,9% genome gà galGal4, khớp `docs/04` mục 8). **[đo được]**

Phân bố độ dài phần tử:

| Nhóm bp | Số phần tử | % tổng phần tử |
|---|---|---|
| 20–49 | 1.770.154 | 60,05 |
| 50–99 | 541.134 | 18,36 |
| 100–199 | 358.412 | 12,16 |
| 200–499 | 239.442 | 8,12 |
| ≥500 | 38.446 | 1,30 |
| **Tổng** | **2.947.588** | **100** |

Phân bố theo NST gà (top, `merge_stats.tsv`): chr1 531.189 · chr2 405.941 · chr3 321.931 · chr4 266.803 · chrZ 200.397 · chr5 197.042. **[đo được]**

---

## 4. Kết quả B — LÕI trên bộ gene chào mào

| Ngưỡng coverage | Phần tử ánh xạ | % trong 2.947.588 | bp trên chào mào | % bộ gene (1.024.591.993 bp) |
|---|---|---|---|---|
| ≥0,8 (bộ chính) | 248.461 | 8,43 | 62.491.397 | **6,10** |
| ≥0,5 (bộ nới) | 411.275 | 13,95 | 88.415.707 | **8,63** |

Bộ lọc chung: `--min-identity 0.70`, 1 hit tốt nhất/query tính qua cả 12 mảnh; 8.505 query có hit thứ hai. Phân bố độ tương đồng của các hit đạt identity ≥0,70 (461.655 hit, giống nhau ở cả hai bộ): <0,70 = 97 · 0,70–0,80 = 4.776 · 0,80–0,90 = 194.776 · 0,90–0,95 = 194.294 · 0,95–1,00 = 59.837 · =1,00 = 7.875. **[đo được]**

% ánh xạ theo nhóm độ dài:

| Nhóm bp | Tổng phần tử | Ánh xạ cov ≥0,8 | % | Ánh xạ cov ≥0,5 | % |
|---|---|---|---|---|---|
| 20–49 | 1.770.154 | 4.362 | **0,25** | 5.436 | **0,31** |
| 50–99 | 541.134 | 25.616 | 4,73 | 44.415 | 8,21 |
| 100–199 | 358.412 | 88.449 | 24,68 | 147.510 | 41,16 |
| 200–499 | 239.442 | 101.573 | 42,42 | 177.603 | 74,17 |
| ≥500 | 38.446 | 28.461 | **74,03** | 36.311 | **94,45** |

**Vì sao nhóm ngắn thấp:** minimap2 `-x asm20` là bộ căn dựa trên minimizer chuỗi hạt giống — một phần tử 20–49 bp có quá ít minimizer để vừa vượt ngưỡng điểm (`-s 30`, `-m 20`) vừa đạt `min-coverage` trên toàn chiều dài; đồng thời chuỗi ngắn khớp ngẫu nhiên nhiều nơi nên bị bộ lọc hit tốt nhất/`-f 0.001` loại. Nới coverage 0,8 → 0,5 gần như **không** cứu được nhóm này (0,25% → 0,31%), tức nút thắt là **giai đoạn tìm hạt giống**, không phải ngưỡng coverage. Hệ quả: 60,05% số phần tử (nhóm 20–49 bp) hiện gần như vắng mặt trong bản đồ B — đây là lý do bộ căn LAST (`pipeline/p02b_last/`, đã viết, chưa chạy) là việc tiếp theo bắt buộc. **[đo được + suy luận kỹ thuật]**

---

## 5. LÕI nằm ở đâu trong bộ gene

**Bộ chính (coverage ≥0,8)** — `annot_stats.tsv`:

| Lớp | Số vùng | bp | % bp lõi |
|---|---|---|---|
| CDS | 68.295 | 15.182.650 | **24,3** |
| exon không mã hóa | 0 | 0 | 0,0 |
| intron | 26.669 | 6.905.274 | 11,0 |
| liên gene | 153.497 | 40.403.473 | 64,7 |
| **Tổng** | **248.461** | **62.491.397** | **100** |

**Bộ nới (coverage ≥0,5)** — `annot_stats.cov50.tsv`: CDS 90.162 vùng / 18.231.781 bp / 20,6% · intron 51.153 / 10.862.455 / 12,3% · liên gene 269.960 / 59.321.471 / 67,1% · exon không mã hóa 0. Nới ngưỡng làm tỉ trọng CDS **giảm** (24,3% → 20,6%) — phù hợp với việc phần tử thêm vào chủ yếu là các hit yếu hơn nằm ngoài vùng mã hóa. **[đo được]**

**So sánh thô với kỳ vọng nếu rải ngẫu nhiên** (mẫu số: hợp nhất khoảng từ GFF `GCA_013400435.1`, tính trong phiên này — CDS 19.763.303 bp; thân gene/pseudogene 221.939.072 bp; còn lại 802.652.921 bp):

| Lớp | % không gian bộ gene | % lõi quan sát (cov ≥0,8) | Tỉ số thô |
|---|---|---|---|
| CDS | 1,93 | 24,3 | **×12,6** |
| Thân gene ngoài CDS | 19,73 | 11,0 | ×0,56 |
| Liên gene | 78,34 | 64,7 | ×0,83 |

Nói cách khác: **15.182.650 / 19.763.303 = 76,8% tổng CDS của chào mào được gán vào lõi**. **[đo được]**

Ba điều kiện phải đọc kèm con số 12,6 lần và 76,8%:
1. **Đây là so sánh thô, chưa có mô hình nền.** Không có permutation khớp %GC/khoảng cách gene, không có kiểm định. Không được viết "p < 0,05" cho bất kỳ dòng nào ở trên.
2. **76,8% là giới hạn trên.** `annotate --stats` cộng **toàn bộ chiều dài vùng BED** được gán lớp CDS, không cắt theo phần giao thực tế với CDS (README `p02_core_map`, mục Giới hạn). Một vùng lõi 300 bp chỉ chồng CDS 80 bp vẫn được tính đủ 300 bp.
3. **Thiên vị ánh xạ đi cùng chiều với kết luận.** Phần tử dài ánh xạ tốt hơn (74,03% ở ≥500 bp so với 0,25% ở 20–49 bp) và vùng mã hóa bảo tồn hơn nên phần tử trong CDS vừa dài hơn vừa dễ căn hơn. Một phần của "×12,6" là hệ quả của bộ căn, chưa tách được khỏi tín hiệu sinh học thật.

Ngoài ra `exon_noncoding = 0` **không** có nghĩa chào mào không có exon không mã hóa: GFF của assembly này có tập exon **trùng khít** tập CDS (19.763.303 bp cho cả hai) — annotation thiếu UTR/exon không mã hóa. Vì vậy một phần "liên gene" và "intron" thực chất là UTR. **[đo được]**

---

## 6. Gene chứa nhiều lõi nhất — HAI bảng

### 6a. Theo TỔNG bp lõi (CHƯA chuẩn hóa chiều dài) — top 15, bộ cov ≥0,8

| # | Gene | bp lõi | Chiều dài gene (bp) | bp/kb |
|---|---|---|---|---|
| 1 | Znf521 | 55.291 | 180.037 | 307,11 |
| 2 | Sox6 | 51.612 | 224.302 | 230,10 |
| 3 | Foxp1 | 47.957 | 160.237 | 299,29 |
| 4 | Vps13b | 46.555 | 361.573 | 128,76 |
| 5 | Klhl29 | 45.938 | 319.949 | 143,58 |
| 6 | Zfhx4 | 44.501 | 122.682 | 362,73 |
| 7 | Zfpm2 | 43.177 | 248.776 | 173,56 |
| 8 | Znf407 | 42.888 | 202.086 | 212,23 |
| 9 | Pappa | 39.162 | 174.142 | 224,89 |
| 10 | Pard3 | 37.592 | 293.833 | 127,94 |
| 11 | Gmds | 37.466 | 253.233 | 147,95 |
| 12 | Auts2 | 37.343 | 168.002 | 222,28 |
| 13 | Znf423 | 37.306 | 158.879 | 234,81 |
| 14 | Arid1b | 35.385 | 241.893 | 146,28 |
| 15 | PYCJOC_R07429 | 35.046 | 313.774 | 111,69 |

### 6b. Theo MẬT ĐỘ bp lõi/kb (lọc `gene_len ≥ 1000`, `bp ≥ 200`) — top 15, bộ cov ≥0,8

| # | Gene | bp/kb | bp lõi | Chiều dài gene (bp) |
|---|---|---|---|---|
| 1 | Gpr19_1 | 2.687,50 | 2.967 | 1.104 |
| 2 | Dolk | 2.514,16 | 3.907 | 1.554 |
| 3 | Nipbl_5 | 2.479,01 | 2.717 | 1.096 |
| 4 | **Hoxa5** | 2.475,73 | 4.845 | 1.957 |
| 5 | **Hoxa11** | 2.326,53 | 5.586 | 2.401 |
| 6 | Rbm12 | 2.207,81 | 5.822 | 2.637 |
| 7 | **Hoxa3** | 2.124,41 | 5.806 | 2.733 |
| 8 | Gpr173 | 1.974,56 | 2.251 | 1.140 |
| 9 | Hoxa6 | 1.850,48 | 3.849 | 2.080 |
| 10 | Arhgap5_1 | 1.839,60 | 3.819 | 2.076 |
| 11 | Gpr85 | 1.808,11 | 2.007 | 1.110 |
| 12 | Lrrtm2 | 1.757,11 | 2.720 | 1.548 |
| 13 | Slitrk4 | 1.697,74 | 3.387 | 1.995 |
| 14 | Fam110b | 1.681,08 | 1.866 | 1.110 |
| 15 | Kcnj12 | 1.616,96 | 1.659 | 1.026 |

### Hai bảng khác nhau thế nào và vì sao

**Giao nhau của hai top 15 = 0 gene.** Không một gene nào có mặt ở cả hai bảng. **[đo được]**

- Bảng 6a **thiên vị gene dài**: mọi gene trong đó dài 122–362 kb. Xếp theo tổng bp thì "mega-gene" luôn thắng chỉ vì có nhiều bp để chứa lõi, bất kể mật độ. Ví dụ rõ nhất là Dlg2: 21.828 bp lõi (đủ vào top 50 theo tổng bp) nhưng chiều dài 587.588 bp nên mật độ chỉ **37,15 bp/kb** — thấp hơn Gpr19_1 khoảng 72 lần.
- Bảng 6b chuẩn hóa theo chiều dài locus (`bp_per_kb = 1000 × bp lõi / gene_len`) và lọc `gene_len ≥ 1000`, `bp ≥ 200` để loại nhiễu gene tí hon. Kết quả là các gene 1–3 kb gần như **phủ kín** bởi lõi: Hoxa5 4.845 bp lõi trên locus 1.957 bp — con số vượt chiều dài gene vì `annotate` cộng nguyên chiều dài vùng BED chứ không cắt theo phần giao (xem mục 5, điều kiện 2). Không đọc bp/kb như "tỉ lệ phần trăm phủ".
- Cảnh báo này đến từ mục 5 bài A1 của Antigravity và đã được code hóa trong `annotate` từ commit `73cba7f` (README `p02_core_map`, mục "Chuẩn hóa mật độ lõi"). **Chỉ dùng bảng 6a là sai phương pháp.**
- Bảng 6b và cột `fold` của `gene_enrichment.tsv` là **cùng một thứ tự** (fold = bp_per_kb / 1000 / P₀; ví dụ Gpr19_1: 2.687,50/1000/0,0603613 = 44,52 = cột `fold`). Không nên trình bày như hai bằng chứng độc lập.

### Về con số "8.450/10.729 gene qua ngưỡng FDR"

`enrich_stats.tsv` ghi `genes_tested = 10.729`, `genes_pass_fdr = 8.450` (`--fdr 0.05`). **Con số này KHÔNG được dùng để tuyên bố ý nghĩa thống kê.** Mô hình nhị thức phía sau `rank_score_p` giả định mỗi base là một phép thử Bernoulli độc lập; các base trong cùng một vùng lõi là **một khối liền, không độc lập**, nên p-value và `bh_q`/`signif_flag` bị thổi phồng có hệ thống — tỉ lệ 79% gene "có ý nghĩa" chính là triệu chứng của vi phạm giả định đó, không phải phát hiện sinh học. Ba cột này **chỉ dùng để xếp hạng tương đối** (README `p02_core_map`, cảnh báo #1). **Đối chứng âm (bộ accelerated) đang chạy, chưa có kết quả** — khi có, cột `ca_ratio` (= `fold` / `accel_fold`) mới là chỉ báo đặc hiệu đáng tin hơn `bh_q`.

### Diễn giải chức năng gene đứng đầu

**Không đưa vào.** `research/synthesis/06-review-A1.md` kết luận **BLOCKED** cho bài A1: 11/22 URL trỏ tới bài báo có thật nhưng hoàn toàn sai chủ đề, 53/62 nhãn [C] phải hạ (~44 xuống [U]). Toàn bộ nội dung sinh học của A1 không được dùng ở báo cáo này. Ba thứ **được** dùng từ A1 là ba cảnh báo phương pháp ở mục 5 của bài đó — chúng là **suy luận phương pháp luận trên chính thiết kế pipeline của dự án, không mang nhãn [C]**, và đã được ghi lại ở mục 5 và mục 7 dưới đây: (i) thiên vị gene dài khi xếp theo tổng bp; (ii) bẫy gán vùng liên gene cho gene giao nhiều nhất; (iii) annotation thiếu UTR nên một phần "liên gene" thực ra là UTR/intron.

Chức năng của Znf521/Sox6/Foxp1 và cụm Hoxa hiện là **[U]** trong dự án này cho tới khi có một brief sourcing riêng làm lại. Không dùng làm đầu vào tracker T06/T22 ở mức [C]/[S].

---

## 7. Giới hạn

1. **Neo trên gà galGal4.** LÕI-363 chỉ tồn tại ở những vùng chào mào còn align được với gà; vùng đặc hữu của chào mào (hoặc phân kỳ quá mức so với gà) không bao giờ xuất hiện trong đầu vào. Đây là thiếu hụt **một chiều**, chưa định lượng được.
2. **Nhóm <100 bp gần như chưa ánh xạ.** 0,25% (20–49 bp) và 4,73% (50–99 bp) ở cov ≥0,8; hai nhóm này chiếm 78,4% tổng số phần tử. Bản đồ B hiện là bản đồ của các phần tử **dài**, không phải của toàn bộ LÕI.
3. **Assembly chào mào ở mức scaffold.** GCA_013400435.1 gồm **60.582 scaffold, N50 scaffold 218.123 bp** (`run.log` của phiên này ghi 60.582 sequence; số N50 lấy từ `research/raw/R5-…`, nhãn CONFIRMED) — không xếp theo NST, nên không nói được gì về phân bố lõi theo macro/micro-chromosome, và các vùng bắc cầu qua đầu mút scaffold bị mất.
4. **Gán vùng liên gene là xấp xỉ.** `annotate` gán vùng lớp intron cho gene giao nhiều bp nhất; vùng lớp liên gene **không** được gán gene nào. Enhancer thật có thể điều khiển promoter cách 500 kb, "nhảy cóc" qua gene gần hơn — không được suy "lõi liên gene gần gene X thì điều hòa gene X" (cảnh báo #2 của README, kế thừa A1 mục 5).
5. **Annotation thiếu UTR.** Tập exon của GFF trùng khít tập CDS (cả hai = 19.763.303 bp), nên `exon_noncoding = 0` là **giả tạo**; một phần "liên gene"/"intron" thực chất là UTR (cảnh báo #3 của README, kế thừa A1 mục 5).
6. **Chưa có mô hình nền để kiểm định thống kê.** `bh_q`/`signif_flag`/"8.450 gene qua FDR" chỉ để xếp hạng, không phải kết luận thống kê. Cần permutation khớp %GC + khoảng cách gene (đặc tả §2 của `06-review-A1.md`).
7. **Chưa dùng bộ accelerated làm đối chứng.** `launch_accel.sh` đang chạy, `data/a2_accel/` chưa có; chưa có `accel_fold`/`ca_ratio`. Trước khi có đối chứng này, không phân biệt được "gene giàu lõi vì chịu ràng buộc" với "gene nằm ở vùng bộ gene dễ căn/dễ gọi tín hiệu".
8. **bp lõi theo gene là giới hạn trên.** Cộng nguyên chiều dài vùng BED, không cắt theo phần giao thực tế — ảnh hưởng trực tiếp tới 24,3%, 76,8%, ×12,6 và mọi giá trị bp/kb.
9. **Bảo tồn tổ tiên ≠ đặc thù chào mào.** Tín hiệu bắt nguồn từ mức bảo tồn qua 363 loài chim trên tọa độ gà — phản ánh khung phát triển chung của tổ tiên, không tự nó nói gì về kiểu hình riêng của chào mào (cảnh báo #3 của `enrich`).

**Về H1/H2/H3:** dữ liệu này chưa phân biệt được ba giả thuyết. "×12,6 ở CDS" và "76,8% CDS nằm trong lõi" là dự đoán chung của **cả** H1 (tiến hóa chuẩn: chọn lọc thanh lọc mạnh trên vùng mã hóa) **và** H2 (ràng buộc mạnh) — không có giả thuyết nào bị loại bởi con số này, và không có tiên đoán riêng nào của H3 được kiểm ở đây. Câu hỏi đúng cho vòng sau vẫn là: **dữ liệu nào phân biệt được?** — ứng viên gần nhất là tỉ số conserved/accelerated theo gene (`ca_ratio`) trên nền permutation, vì ba giả thuyết cho các kỳ vọng khác nhau về **hình dạng phân phối** ràng buộc, không chỉ về mức trung bình.

---

## 8. Việc tiếp theo

- **Chạy xong đối chứng âm accelerated** (`pipeline/p02_core_map/launch_accel.sh` → `data/a2_accel/`). *Xong khi:* `data/a2_accel/core_annot.tsv` tồn tại, `enrich_stats.tsv` có `p0_accel`/`total_accel_bp`, `gene_enrichment.tsv` có 3 cột `accel_bp`/`accel_fold`/`ca_ratio`, và có bảng top 20 theo `ca_ratio`; sha256 ghi vào `SHA256SUMS.txt`.
- **Chạy LAST cho nhóm phần tử <100 bp** (`pipeline/p02b_last/run_last.sh`, đã viết + 14 test PASS, chưa chạy thật) rồi gộp BED với bộ minimap2. *Xong khi:* `map_stats_short.tsv` có `mapped > 0` ở cả bin 20_49 và 50_99, BED gộp có sha256 trong registry, và mục 4 của báo cáo này được cập nhật bằng số mới.
- **Dựng mô hình nền permutation khớp %GC** (đặc tả `06-review-A1.md` §2): N ≥ 100 lần xáo trộn giữ nguyên độ dài + số phần tử/scaffold. *Xong khi:* `gene_enrichment.tsv` có cột `p_empirical` và `enrichment` so với nền xáo trộn, và mọi câu "giàu gấp N lần" trong báo cáo này được thay bằng giá trị có khoảng tin cậy.
- **Tính bp lõi cắt theo phần giao thực tế** (clip vùng BED vào CDS/exon/gene) và **sửa bug hiển thị `summarize_a2.py`** (F10: hàm `section()` gộp lẫn hai bảng gene rồi cắt `[:10]` nên không bao giờ in bảng mật độ). *Xong khi:* `annot_stats.tsv` có cột bp đã cắt, tỉ lệ "76,8% CDS" được tính lại thành số thật thay vì giới hạn trên, và `SUMMARY.md` in đủ **cả hai** dòng "Top 10 theo TỔNG bp" và "Top 10 theo MẬT ĐỘ" (kèm 1 unit test PASS).
- **Brief sourcing lại chức năng gene** cho top 6a + 6b, thay thế bài A1 đã BLOCKED. *Xong khi:* mỗi gene được giữ nhãn có ≥2 URL độc lập đã được reviewer mở trực tiếp và xác nhận đúng chủ đề (theo tiền lệ F01 và bài học `feedback-external-model-citations`), và bảng kết quả đủ điều kiện nộp vào tracker T22 của V4.
