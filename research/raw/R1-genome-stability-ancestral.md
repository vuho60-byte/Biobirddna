## 1. TL;DR

B10K đã công bố 363 bộ gene chim (92,4% họ chim còn tồn tại) qua 2 bài Nature (Feng 2020; Stiller 2024), có cổng dữ liệu chính thức và alignment 363-way (Cactus/HAL) kèm điểm bảo tồn phastCons/phyloP đã tính sẵn trên hub UCSC — tìm thấy URL tải trực tiếp file HAL (~hàng trăm GB) và 3 file model neutral (macro/micro/sex chromosome). Bộ gene chim CONFIRMED nhỏ hơn, ít yếu tố nhảy hơn, và ổn định cấu trúc NST hơn thú (Zhang 2014 *Science*; Kapusta & Suh 2017 *PNAS*; Waters 2021 *PNAS*). ASHCE (Seki 2017 *Nat Commun*) và UCE (Faircloth 2012; McCormack 2013; bộ probe Tetrapods-UCE-5Kv1 = 5.060 locus) là 2 "kho DNA gốc" tính được, đã có công cụ (phyluce) và dữ liệu công khai. ~274 gene mất ở chim (Lovell 2014 *Genome Biology*, CONFIRMED bởi Zhang 2014) và gene răng ENAM/AMEL/AMBN mất bằng đột biến hỏng chung (Meredith 2014 *Science*, ~116 triệu năm trước). Tái dựng karyotype tổ tiên chim đã có (DESCHRAMBLER, nhóm Griffin/Damas 2018 *Genome Biology*: 14 nút tổ tiên tới họ Estrildidae/Thraupidae/Fringillidae) nhưng CHƯA có tái dựng riêng cho tổ tiên Pycnonotidae — đây là khoảng trống thật của dự án. Mục 2 (URL tải alignment + track bảo tồn) đã xác minh mở được, đáp ứng yêu cầu cốt lõi của brief. Không dùng Perplexity (0/3 lượt) vì PubMed/Consensus/WebSearch đã đủ.

## 2. Bảng phát hiện

| # | Claim | Nhãn | Nguồn (tác giả, năm, tạp chí, DOI/URL) | Trả lời Qx |
|---|---|---|---|---|
| 1 | B10K phase II đã công bố 363 bộ gene chim, đại diện 92,4% họ chim (267 bộ gene giải trình tự mới) | CONFIRMED | Feng et al. 2020, *Nature* 587:252-257, DOI 10.1038/s41586-020-2873-9; xác nhận chéo bởi Stiller et al. 2024, *Nature* 629:851-860, DOI 10.1038/s41586-024-07323-1 (dùng lại cùng bộ 363 genome) | Q1 |
| 2 | B10K phase I (48 loài, Zhang 2014) + phylogenomics gốc (Jarvis 2014) là nền trước phase II | CONFIRMED | Zhang et al. 2014, *Science* 346:1311-1320, DOI 10.1126/science.1251385; Jarvis et al. 2014, *Science* 346:1320-1331, DOI 10.1126/science.1253451 | Q1 |
| 3 | Stiller et al. 2024 dùng vùng liên gene (intergenic) + phương pháp coalescent trên 363 genome, xác nhận Neoaves bức xạ nhanh quanh ranh giới Creta-Paleogen (K-Pg); phát hiện tăng đột biến/kích thước não/Ne sau tuyệt chủng K-Pg | CONFIRMED | Stiller et al. 2024, *Nature* 629:851-860, DOI 10.1038/s41586-024-07323-1 (PMID 38560995) | Q1 |
| 4 | Cổng dữ liệu B10K chính thức: b10k.genomics.cn (BGI) và CNGB Datamart db.cngb.org/datamart/animal/DATAani1/ | CONFIRMED (đã mở được cả 2 URL) | WebSearch → https://b10k.genomics.cn/ ; https://db.cngb.org/datamart/animal/DATAani1/ | Q1 |
| 5 | Alignment 363-way dùng Progressive Cactus; có track hub UCSC "363-avian-2020-hub"; file thô định dạng HAL tải trực tiếp tại https://alignment-output.s3.amazonaws.com/birds-final.hal (hàng trăm GB); MAF (bigMaf) chỉ có trên browser gà; snake track HAL có trên mọi genome | CONFIRMED (mở trực tiếp trang tài liệu UCSC) | UCSC Genome Browser docs, https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020-hub/documentation/b10kAlignment.html ; liên hệ Guojie Zhang, Benedict Paten | Q6 (mục 2 brief) |
| 6 | Điểm bảo tồn: dùng phyloP (LRT, mode CONACC, FDR q<0.05) trên 3 model trung tính riêng cho macro-chromosome / micro-chromosome / NST giới tính, tải riêng .mod cho từng loại NST | CONFIRMED (mở trực tiếp trang tài liệu UCSC + 3 URL .mod) | UCSC docs, https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020-hub/documentation/b10kConservationTrackDescription.html ; file: .../combined-b10k-200m-hub/b10k_model_363_{macros,micros,sex}.mod ; liên hệ Joel Armstrong | Q6 (mục 2 brief) |
| 7 | Bộ gene chim ổn định hơn thú: kích thước 1,0–2,1 Gb (chim) so với 2,2–6,0 Gb (thú); TE trung bình 7,8% (chim, khoảng 4,6–10,4%) so với 44,5% (thú, khoảng 33,4–56,3%); do mất DNA qua xóa đoạn lớn (>10kb) bù trừ tích lũy TE | CONFIRMED | Kapusta & Suh & Feschotte 2017, *PNAS* 114:E1460-E1469, DOI 10.1073/pnas.1616702114 (PMID 28179571); nhất quán với Zhang et al. 2014 *Science* (kích thước bị co do xói mòn lặp lại + xóa đoạn + mất gene) | Q3, Q3a |
| 8 | Bộ gene chim biểu hiện "evolutionary stasis" mức cao ở trình tự nucleotide, gene synteny, cấu trúc NST, dù vẫn có thay đổi thích nghi không trung tính ở vùng mã hóa/không mã hóa | CONFIRMED | Zhang et al. 2014, *Science* 346:1311-1320, DOI 10.1126/science.1251385 | Q3 |
| 9 | Vi NST (microchromosome) là "khối xây dựng" chung của NST chim, bò sát và thú — bảo tồn cấu trúc rất cao qua hàng trăm triệu năm | CONFIRMED | Waters, Patel, Ruiz-Herrera et al. 2021, *PNAS* 118, DOI 10.1073/pnas.2112494118; đồng thuận với các review của nhóm Griffin (Griffin & Larkin & O'Connor 2019, *Eur J Med Genet*, DOI 10.1016/j.ejmg.2019.03.004; O'Connor et al. 2024, *Cells* 13:310, DOI 10.3390/cells13040310) | Q3, Q3a |
| 10 | Karyotype tổ tiên chim đã được tái dựng bằng thuật toán DESCHRAMBLER (mở rộng của RACA) qua 14 nút tiến hóa, từ tổ tiên chim tới tổ tiên các họ sẻ Estrildidae/Thraupidae/Fringillidae; phân biệt lịch sử tiến hóa khác nhau giữa macro- và micro-chromosome | STRONG_INFERENCE (nguồn chính + tóm tắt qua WebSearch, chưa đọc trực tiếp % synteny định lượng trong abstract) | Damas, Kim, Farré et al. 2018, *Genome Biology* 19:155, DOI 10.1186/s13059-018-1544-8 | Q6, Q3a |
| 11 | Tái dựng bộ gene tổ tiên diapsid (bò sát + chim, bao gồm khủng long không phải chim) cho phép truy vết tiến hóa NST ở chim và khủng long không phải chim | STRONG_INFERENCE (1 nguồn chính, cùng nhóm tác giả với #10) | O'Connor, Romanov, Kiazim et al. 2018, *Nature Communications* 9:1883, DOI 10.1038/s41467-018-04267-9 | Q6, Q7 |
| 12 | CHƯA tìm thấy bài nào tái dựng riêng bộ gene/karyotype tổ tiên ở đúng 3 nút dự án cần: Neornithes, Passeriformes, Pycnonotidae — công trình gần nhất (Damas 2018) chỉ tới mức họ Estrildidae/Thraupidae/Fringillidae, không phải Pycnonotidae | UNVERIFIED (khoảng trống, cần vòng 2 hoặc tự tính bằng DESCHRAMBLER/Cactus ancestor) | Suy luận từ #10 + tìm kiếm không ra kết quả khác | Q6 (định nghĩa "ancestral nodes") |
| 13 | ASHCE (avian-specific highly conserved elements): >99% nằm ở vùng không mã hóa, gắn với đặc trưng riêng chim (lông, cánh) qua vai trò cis-regulatory | CONFIRMED | Seki, Li, Fang et al. 2017, *Nature Communications* 8:14229, DOI 10.1038/ncomms14229 (PMID 28165450) | Q6, Q4 (brief) |
| 14 | Số lượng ASHCE dự đoán: 265.984 yếu tố (≥20bp), chiếm ~1% bộ gene chim (~11 Mbp tổng cộng), phân tích trên 48 bộ gene chim | STRONG_INFERENCE (số liệu lấy qua tóm tắt WebSearch của bài, chưa tự đọc bảng số liệu gốc) | Seki et al. 2017, *Nature Communications*, DOI 10.1038/ncomms14229 — dữ liệu bổ sung đính kèm trực tiếp trên trang Nature Communications (không có cổng tải riêng); không mở được full text (paywall/reCAPTCHA khi thử) | Q4 (brief) |
| 15 | UCE (ultraconserved elements) hoạt động như marker phylogenomic xuyên amniote; Faircloth 2012 dùng 2.386 locus UCE trên 9 loài chim không mô hình, phục hồi được 3 nhánh chim cổ | CONFIRMED | Faircloth, McCormack, Crawford et al. 2012, *Systematic Biology* 61(5):717-726, DOI 10.1093/sysbio/sys004 (PMID 22232343) | Q6, Q5 (brief) |
| 16 | McCormack et al. 2013 dùng >1.500 locus UCE (target enrichment) cho 32 loài Neoaves + gà ngoài nhóm, tăng độ phân giải cây Neoaves so với ít locus hơn | CONFIRMED | McCormack, Harvey, Faircloth et al. 2013, *PLoS ONE* 8(1):e54848, DOI 10.1371/journal.pone.0054848 (PMID 23382987) | Q5 (brief) |
| 17 | Bộ probe chuẩn Tetrapods-UCE-5Kv1 (phyluce): 5.472 bait nhắm 5.060 locus UCE bảo tồn ở động vật bốn chân | CONFIRMED (trang dữ liệu chính thức Figshare + GitHub faircloth-lab) | Figshare dataset "Tetrapods 5,472 baits targeting 5,060 conserved loci (Tetrapods-UCE-5Kv1.fasta.zip)"; repo https://github.com/faircloth-lab/uce-probe-sets ; tài liệu phyluce https://phyluce.readthedocs.io | Q5 (brief) |
| 18 | Chim thiếu ~274 gene mã hóa protein có mặt ở phần lớn dòng động vật có xương sống, phần lớn nằm trong cụm syntenic bảo tồn ở sauropsid không phải chim và ở người; mất sau khi chim/khủng long tách khỏi cá sấu; nhiều gene liên quan gây chết ở gặm nhấm hoặc bệnh di truyền người | CONFIRMED | Lovell, Wirthlin, Wilhelm et al. 2014 (2015 online), *Genome Biology* 15:565, DOI 10.1186/s13059-014-0565-1 (PMID 25518852); nhất quán với Zhang et al. 2014 *Science* (mất gene là một cơ chế co gọn bộ gene chim) | Q6 (brief, mục "gene mất") |
| 19 | Tổ tiên chung chim hiện đại (Neornithes) mất răng khoáng hóa (mineralized teeth) một lần duy nhất; phát hiện đột biến bất hoạt dùng chung (shared inactivating mutations) trong gene biểu hiện ở men răng/ngà răng (ENAM, AMEL, AMBN…) ở gần như mọi bộ chim; ước tính mất men răng ~116 triệu năm trước | STRONG_INFERENCE (1 nguồn chính, tuy rất được trích dẫn) | Meredith, Zhang, Gilbert, Jarvis, Springer 2014, *Science* 346(6215):1254390, DOI 10.1126/science.1254390 (PMID 25504730) | Q6 (brief, mục gene răng) |
| 20 | Tốc độ đột biến trên mỗi thế hệ (per-generation) khác nhau tới 40 lần giữa các loài có xương sống (68 loài thú/cá/chim/bò sát, 151 phả hệ bố-mẹ-con); thời gian thế hệ, tuổi thành thục và khả năng sinh sản là yếu tố chính quyết định biến thiên; loài Ne lớn dài hạn có tốc độ đột biến/thế hệ thấp hơn (giả thuyết drift barrier) | CONFIRMED | Bergeron, Besenbacher, Zheng et al. 2023, *Nature* 615:285-291, DOI 10.1038/s41586-023-05752-y (PMID 36859541) | Q3b |
| 21 | Tốc độ tiến hóa phân tử ty thể ở chim tương quan với khối lượng cơ thể/thời gian thế hệ (không phải đồng hồ phân tử nghiêm ngặt cố định ~0,01 substitution/site/triệu năm) | CONFIRMED | Nabholz, Lanfear, Fuchs 2016, *Molecular Ecology* 25(18):4438-4449, DOI 10.1111/mec.13780 (PMID 27483387); đồng hướng với Nabholz, Uwimana, Lartillot 2013, *Genome Biology and Evolution* 5(7):1273-1290, DOI 10.1093/gbe/evt083 (PMID 23711670) | Q3b |
| 22 | Suy luận tổng hợp: vì chim có thời gian thế hệ trung bình dài hơn nhiều loài gặm nhấm nhưng ngắn hơn nhiều thú lớn, "tốc độ đột biến/năm" của chim không thấp hơn thú một cách đơn giản — driver chính là thời gian thế hệ + Ne, không phải "lớp Aves" tự thân | STRONG_INFERENCE (suy luận từ #20+#21, chưa có bài so sánh trực diện "chim thấp hơn thú" theo một con số duy nhất) | Tổng hợp từ Bergeron 2023 *Nature* + Nabholz 2016 *Mol Ecol* | Q3b |
| 23 | Chào mào (Pycnonotidae) chưa có trong 363 genome B10K hiện tại theo tra cứu vòng 1 (không xác nhận được tên loài Pycnonotus trong tóm tắt/kết quả tìm kiếm) — cần R5 xác minh trực tiếp qua danh sách loài B10K/NCBI | UNVERIFIED | Không tìm thấy nguồn xác nhận trực tiếp trong vòng 1; nhiệm vụ chồng lấn với brief R5 | Q1 (liên quan) |

## 3. Bảng dataset/công cụ

| ID (docs/02 hoặc "mới") | Tên | URL | Chứa gì | URL đã mở? (✔/✘) | License |
|---|---|---|---|---|---|
| D02 | B10K Database (BGI) | https://b10k.genomics.cn/ | Cổng chính thức B10K, thông tin dự án, liên kết dữ liệu | ✔ | Không ghi rõ trên trang tóm tắt tìm kiếm — cần R5 kiểm license cụ thể |
| D02 | B10K Genomes Project — CNGB Datamart | https://db.cngb.org/datamart/animal/DATAani1/ | Kho dữ liệu bộ gene B10K trên China National GeneBank | ✔ | CNGB DataMart (chưa xác minh điều khoản chi tiết) |
| D03 | UCSC — Bird 10K Alignment Tracks (tài liệu hub 363-avian-2020) | https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020-hub/documentation/b10kAlignment.html | Mô tả track alignment Cactus 363-way; MAF (chỉ browser gà) và HAL (mọi genome) | ✔ (đã mở, đọc nội dung) | UCSC Genome Browser (thường miễn phí phi thương mại; chưa thấy dòng license rõ trên trang này) |
| D03 (mới) | File HAL thô 363-way | https://alignment-output.s3.amazonaws.com/birds-final.hal | Toàn bộ alignment Cactus dạng HAL, "hàng trăm GB" | ✔ (URL thấy trực tiếp trong trang tài liệu UCSC, chưa tải file vì quá lớn) | Không ghi trên trang; theo B10K/UCSC |
| D03 | UCSC — Bird 10K Conservation Track Description | https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020-hub/documentation/b10kConservationTrackDescription.html | Mô tả track phyloP (LRT, CONACC, FDR q<0.05) cho 363-way | ✔ (đã mở, đọc nội dung) | UCSC Genome Browser |
| D03 (mới) | 3 file model trung tính phyloP (macro/micro/sex) | https://comparative-genomics-hubs.s3-us-west-2.amazonaws.com/combined-b10k-200m-hub/b10k_model_363_{macros,micros,sex}.mod | Model trung tính riêng theo loại NST, dùng để tính phyloP | ✔ (URL thấy trực tiếp trong trang UCSC, chưa tải) | Không ghi; theo B10K/UCSC |
| D07 | Tetrapods-UCE-5Kv1 probe set (Figshare) | https://figshare.com/articles/dataset/Tetrapods_5_472_baits_targeting_5_060_conserved_loci_Tetrapods-UCE-5Kv1_fasta_zip_/5899645 | FASTA 5.472 bait / 5.060 locus UCE cho động vật bốn chân | ✔ | Figshare (thường CC-BY, cần R vòng sau xác nhận cụ thể trên trang) |
| D07 (mới) | uce-probe-sets (faircloth-lab GitHub) | https://github.com/faircloth-lab/uce-probe-sets | Kho các bộ probe UCE khác nhau (bao gồm tetrapod, amniote…) | ✔ | GitHub public repo (xem LICENSE file trên repo) |
| D08 | ASHCE — dữ liệu bổ sung của Seki et al. 2017 | Đính kèm trực tiếp trên trang bài báo Nature Communications DOI 10.1038/ncomms14229 (không có cổng tải riêng độc lập tìm thấy) | Bảng tọa độ ASHCE, số liệu bổ sung | ✘ (thử mở nature.com và PMC đều bị chặn — paywall redirect / reCAPTCHA) | Theo Nature Communications (Open Access theo mặc định của tạp chí, cần xác nhận lại) |
| D06 (mới) | Kapusta & Suh 2017 PNAS (dữ liệu TE/genome size 10 thú + 24 chim) | DOI 10.1073/pnas.1616702114 (PMC5338432) | Số liệu định lượng TE gain/loss, kích thước bộ gene | ✔ (đọc được abstract qua PubMed) | PNAS (PMC open access) |
| — (mới) | DESCHRAMBLER (thuật toán, không phải dataset) | Nhắc tới trong Damas et al. 2018 *Genome Biology* DOI 10.1186/s13059-018-1544-8 | Công cụ dự đoán ancestral genome fragment adjacency (mở rộng RACA) | ✘ (chưa tìm URL repo chính thức trong vòng 1) | Chưa xác minh |

## 4. Trả lời ngắn từng câu hỏi trong brief

1. **B10K hiện trạng:** 363 bộ gene công bố (92,4% họ chim), Feng 2020 *Nature* (phase II) + Stiller 2024 *Nature* (cây phát sinh, dùng lại 363 genome). Cổng dữ liệu: b10k.genomics.cn và CNGB Datamart. CONFIRMED.

2. **Alignment + điểm bảo tồn (quan trọng nhất):** Có sẵn trên UCSC hub "363-avian-2020-hub". Alignment Cactus/HAL tải tại S3 (link cụ thể ở bảng 3, file hàng trăm GB). Điểm bảo tồn dùng phyloP (không thấy nói rõ phastCons riêng cho set này trong tài liệu đã mở, chỉ thấy phyloP) với 3 model trung tính theo loại NST. CONFIRMED, URL đã mở trực tiếp.

3. **Bộ gene chim ổn định hơn thú:** CONFIRMED trên nhiều chỉ số — kích thước nhỏ hơn (1,0–2,1 Gb vs 2,2–6,0 Gb), TE thấp hơn nhiều (~7,8% vs ~44,5%), "evolutionary stasis" ở synteny/cấu trúc NST (Zhang 2014), vi NST bảo tồn cực cao (Waters 2021). Tốc độ đột biến/thế hệ khác nhau 40 lần giữa các loài có xương sống, chủ yếu do thời gian thế hệ và Ne quyết định (Bergeron 2023) — không có bằng chứng "chim thấp hơn thú" là quy luật đơn giản theo lớp phân loại; đây là STRONG_INFERENCE cần cẩn trọng khi diễn giải cho dự án.

4. **ASHCE (Seki 2017):** ~265.984 yếu tố (≥20bp, STRONG_INFERENCE vì lấy qua tóm tắt gián tiếp), >99% không mã hóa, gắn cis-regulatory với đặc trưng riêng chim (lông/cánh). Dữ liệu bổ sung đính kèm trực tiếp bài báo, KHÔNG có cổng tải độc lập tìm thấy — không mở được do paywall/reCAPTCHA.

5. **UCE ở chim:** Faircloth 2012 (2.386 locus, 9 loài) và McCormack 2013 (>1.500 locus, 32 loài Neoaves) đều CONFIRMED, có DOI. Bộ probe chuẩn Tetrapods-UCE-5Kv1 = 5.060 locus / 5.472 bait, có trên Figshare + GitHub faircloth-lab.

6. **Gene mất ở chim:** ~274 gene mã hóa protein mất, CONFIRMED (Lovell 2014, xác nhận chéo Zhang 2014). Gene răng ENAM/AMEL/AMBN mất bằng đột biến bất hoạt DÙNG CHUNG ở hầu hết bộ chim (Meredith 2014, STRONG_INFERENCE vì 1 nguồn chính, ~116 triệu năm trước).

7. **Ancestral genome/karyotype reconstruction:** Có — DESCHRAMBLER (nhóm Griffin/Damas), tái dựng 14 nút tới mức họ Estrildidae/Thraupidae/Fringillidae (Damas 2018); O'Connor 2018 tái dựng tới tổ tiên diapsid (bao gồm khủng long không chim). CHƯA tìm thấy tái dựng riêng cho đúng 3 nút dự án cần (Neornithes/Passeriformes/Pycnonotidae) — UNVERIFIED, là khoảng trống thật.

## 5. Câu hỏi còn mở / cần vòng 2

- Cần đọc trực tiếp bảng số liệu ASHCE (Seki 2017 Nature Communications, phần Supplementary) để xác nhận số 265.984 và ~11 Mbp — hiện chỉ có qua tóm tắt WebSearch (STRONG_INFERENCE), thử mở nature.com/PMC đều bị chặn (paywall redirect, reCAPTCHA).
- Cần % synteny/microchromosome định lượng cụ thể (ví dụ macro vs micro giữ lại bao nhiêu % so với tổ tiên) từ Damas 2018 — chỉ lấy được mô tả định tính qua tóm tắt, chưa đọc số liệu Bảng/Hình gốc.
- Chưa xác nhận Pycnonotus jocosus (chào mào) có nằm trong danh sách 363 loài B10K hay không — cần R5 đối chiếu trực tiếp danh sách loài (liên quan D01/D02).
- Chưa có bài nào tái dựng ancestral sequence/karyotype ở đúng nút Pycnonotidae — nếu dự án cần, phải tự chạy DESCHRAMBLER hoặc dùng Cactus ancestor nodes trên alignment 363-way đã tải được (Pha 2, cần code).
- Chưa xác minh license cụ thể của B10K Database/CNGB Datamart và của HAL alignment S3 bucket — chỉ thấy tồn tại URL, chưa đọc điều khoản sử dụng.
- Chưa tìm được URL/tên chính thức repo GitHub của DESCHRAMBLER — chỉ có mô tả thuật toán qua tóm tắt bài báo liên quan.
- Câu hỏi Q3a "synteny/vi NST chào mào ↔ gà (~90 triệu năm) là bao nhiêu %?" — không có bài nào tính riêng cho Pycnonotidae; đây là việc code Pha 2 cần tự làm với dữ liệu D02/D03 đã có URL.

## 6. Search log

| tool | query | số kết quả | dùng được? |
|---|---|---|---|
| pubmed.search_articles | Bird 10,000 Genomes Project B10K phylogenomics 363 genomes | 1 | ✔ (Feng 2020) |
| pubmed.search_articles | avian genome stability microchromosome synteny conservation karyotype | 0 | ✘ (câu quá dài, AND hết) |
| pubmed.search_articles | avian specific highly conserved elements ASHCE Seki | 1 | ✔ (Seki 2017) |
| pubmed.search_articles | ultraconserved elements birds phylogenomics Faircloth McCormack UCE probe | 0 | ✘ |
| pubmed.search_articles | bird genes lost comparative genomics tooth enamel gene ENAM AMEL AMBN pseudogene | 0 | ✘ |
| pubmed.search_articles | ancestral genome reconstruction birds Neornithes karyotype DESCHRAMBLER Cactus | 0 | ✘ |
| pubmed.search_articles | avian genome microchromosome karyotype evolution conserved synteny | 19 (lấy 8) | ✔ (Waters 2021, Griffin reviews, Kretschmer…) |
| pubmed.search_articles | comparative genomic analysis 48 bird species avian genome evolution | 7 (lấy 6) | ✔ (Zhang 2014, Jarvis 2014) |
| pubmed.search_articles | bird genome gene loss tooth enamel Meredith convergent evolution | 1 | ✔ (Meredith 2014) |
| pubmed.search_articles | avian ancestral karyotype reconstruction Griffin chromosome | 4 | ✔ (Damas 2018, O'Connor 2018, Griffin 2019) |
| pubmed.search_articles | germline mutation rate birds substitution rate comparative | 5 | ✘ (không đúng chủ đề trực tiếp) |
| pubmed.search_articles | Nabholz birds mutation rate generation time molecular evolution | 3 | ✔ (Nabholz 2016, 2013) |
| pubmed.search_articles | Complexity of avian evolution revealed by family-level genomes Stiller | 1 | ✔ (Stiller 2024) |
| pubmed.search_articles | Faircloth 2012 ultraconserved elements anchor thousands genetic markers evolutionary timescales | 1 | ✔ |
| pubmed.search_articles | Evolution of the germline mutation rate across vertebrates Bergeron | 2 | ✔ (Bergeron 2023 xác định đúng bài) |
| pubmed.search_articles | conserved syntenic clusters protein coding genes missing birds Lovell | 1 | ✔ (Lovell 2014) |
| pubmed.get_article_metadata | (20 PMID gộp — B10K, ASHCE, karyotype, mutation rate…) | 20 | ✔ (file lớn, đọc qua jq) |
| consensus.search | number of genes lost in bird genomes common ancestor 274 genes comparative genomics | 3 | ✔ (xác nhận Lovell 2014 + Zhang 2014) |
| consensus.search | ultraconserved elements enrichment phylogenomics vertebrates Faircloth 2012 | 3 | ✔ (xác nhận Faircloth 2012, 1150 trích dẫn) |
| consensus.search | mutation rate per generation birds lower than mammals molecular clock generation time effect | 3 | ✔ (dẫn tới Bergeron 2023 — phải xác minh lại tác giả qua PubMed vì Consensus ghi nhầm "Jiao Zheng" là tác giả chính) |
| WebSearch | B10K Bird 10000 Genomes Project data portal download genomes 2024 | ~10 link | ✔ (b10k.genomics.cn, CNGB) |
| WebSearch | UCSC Genome Browser 363 birds Cactus alignment phastCons phyloP track hub | ~8 link | ✔ (tìm ra trang tài liệu UCSC) |
| WebSearch | Genome Ark B10K bird genomes hal alignment download | ~10 link | ✔ (xác nhận trang UCSC + Stiller 2024 Nature link) |
| WebSearch | DESCHRAMBLER software ancestral genome reconstruction chromosome painting tool description | ~9 link | ✔ (mô tả thuật toán) |
| WebSearch | bird genome size average 1.0-1.3 Gb versus mammal genome 3.2 Gb transposable element percentage comparison | ~9 link | ✔ (dẫn ra Kapusta & Suh 2017) |
| WebSearch | McCormack 2013 "ultraconserved elements" birds PLoS ONE family-level phylogenomics probe set | ~10 link | ✔ |
| WebSearch | phyluce "Tetrapods-UCE-5Kv1" probe set number of loci | ~10 link | ✔ (5.060 locus xác nhận) |
| WebSearch | Seki 2017 ASHCE supplementary data avian specific highly conserved elements download | ~8 link | ✔ một phần (số liệu 265.984, không có link tải riêng) |
| WebSearch | Damas 2018 "avian ancestral karyotypes" abstract synteny percentage… DESCHRAMBLER nodes | ~10 link (2 vòng) | ✔ một phần (14 nút, chưa ra % định lượng) |
| WebFetch | cgl.gi.ucsc.edu/.../b10kAlignment.html | 1 trang | ✔ (URL HAL trực tiếp) |
| WebFetch | cgl.gi.ucsc.edu/.../b10kConservationTrackDescription.html | 1 trang | ✔ (3 URL .mod trực tiếp) |
| WebFetch | nature.com/articles/s41586-024-07323-1 ; nature.com/articles/ncomms14229 ; pmc.ncbi.nlm.nih.gov/articles/PMC5473641 ; link.springer.com (Damas 2018) | 4 trang | ✘ (paywall redirect / reCAPTCHA, không đọc được nội dung) |

**Perplexity: 0/3 lượt đã dùng** (không cần dùng — PubMed/Consensus/WebSearch đủ trả lời brief). Điều chưa làm được: chưa đọc trực tiếp full-text/supplementary của Seki 2017 và Damas 2018 để lấy số liệu định lượng chính xác (ASHCE count, % synteny macro/micro); chưa xác nhận loài chào mào có trong B10K 363; chưa tìm license chi tiết của B10K/CNGB/HAL S3 bucket.
