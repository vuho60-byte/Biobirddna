# R5 — Bộ gene chào mào / Pycnonotidae + khả thi pipeline (T06 của V4)

## 1. TL;DR

- *Pycnonotus jocosus* (chào mào má đỏ) **CÓ** assembly thật ở NCBI: **GCA_013400435.1** (ASM1340043v1), do **B10K Consortium** nộp 2020-07-10, mức **scaffold**, dùng SOAPdenovo v2.04, N50 scaffold chỉ **218,123 bp**, N50 contig **53,855 bp**, tổng 1,024,591,993 bp, 60,582 scaffold, GC 41.5%. Đây là bản cũ, chất lượng thấp (short-read), KHÔNG phải chromosome-level.
- Loài chị em cùng chi **P. cafer** (chào mào bụng đỏ, "Red-vented Bulbul") vừa có genome mới, tốt hơn hẳn: N50 scaffold 3.04 Mb, BUSCO 97.2%, 15,533 gene (Puthumana et al. 2025, *DNA Research*), nhưng **chưa thấy GCA_/GCF_** chính thức — chỉ có WGS master accession JBQLIZ000000000.
- Không tìm được genome nhân (nuclear) cho *P. sinensis*, *P. aurigaster*, *Hypsipetes*, *Alophoixus* — chỉ có mitogenome lẻ tẻ. Ghi ✘.
- Tham chiếu Passerida chất lượng cao: sẻ vằn bTaeGut1.4.pri (VGP) = GCA_003957565.2; sẻ ngô lớn (Parus major) = GCF_001522545.1 (bản cũ hơn Parus_major1.1 cũng tồn tại nhưng chưa chốt được GCF mới); sẻ nhà (Passer domesticus) = GCA_001700915.1 (1 nguồn, chưa verify chéo).
- Gene sắc tố ở Passeriformes (không gà/bồ câu) có nhiều case tốt: MC1R/ASIP (Monarcha flycatcher), OCA2/HERC2 (Sporophila), MC1R (âm tính ở sẻ vằn), CYP2J19/BDH1L (house finch — có cả bằng chứng ủng hộ và bằng chứng phủ định), MLPH + loạt gene khác (chim hoàng yến nuôi).
- HAL 363-loài B10K là 1 file duy nhất "hàng trăm GB" trên S3, KHÔNG có tùy chọn tải riêng từng loài — mâu thuẫn với giả định D03 trong docs/02 rằng có phastCons/phyloP tính sẵn (trang UCSC không nhắc tới phyloP/phastCons, chỉ có snake track HAL + 1 bigMaf trên trình duyệt gà).
- BUSCO `aves_odb10` ≈ 8,338 gene (1 nguồn, chưa mở trực tiếp trang BUSCO).
- Ước lượng tài nguyên WSL2 (Perplexity, tổng hợp, chưa có benchmark thực đo): (a) chỉ dùng track sẵn ~12–24GB RAM; (b) ASR 50 locus×50 loài ~8–16GB RAM/họ locus; (c) dN/dS 500 gene×50 loài ~4–8GB RAM. Cả 4 công cụ (halTools, PHAST, IQ-TREE2, PAML/codeml) được cho là cài được qua conda/bioconda trên WSL2 Ubuntu.
- **Kết luận T06: khả thi có điều kiện** (xem mục 4, câu 1 và mục 5).

## 2. Bảng phát hiện

| # | Claim | Nhãn | Nguồn (tác giả, năm, tạp chí, DOI/URL) | Trả lời Qx |
|---|---|---|---|---|
| 1 | *Pycnonotus jocosus* có assembly GCA_013400435.1 (ASM1340043v1), submitter B10K Consortium, ngày nộp 2020-07-10, mức scaffold, phương pháp SOAPdenovo v2.04, N50 scaffold 218,123 bp, N50 contig 53,855 bp, tổng 1,024,591,993 bp, 60,582 scaffold, 99,384 contig, GC 41.5% | CONFIRMED | NCBI Assembly (GCA_013400435.1) — `assembly_report.txt` + `assembly_stats.txt` chính thức (https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/013/400/435/GCA_013400435.1_ASM1340043v1/) đối chiếu độc lập với Puthumana et al. 2025 *DNA Research* 32(6):dsaf027 (bài dẫn lại chính accession này khi so sánh) | Q1 |
| 2 | *Pycnonotus cafer* (Red-vented Bulbul) có genome mới: 1.03 Gb, N50 scaffold 3.04 Mb, BUSCO genome 97.2% / gene set 96.5%, 15,533 gene mã hoá protein, mức "scaffold — reference standard"; nộp bởi MetaBioSys Group, IISER Bhopal; WGS accession JBQLIZ000000000 (v1: JBQLIZ010000000), BioProject PRJNA1226769, BioSample SAMN46958819 | CONFIRMED | Puthumana MA, Bisht MS, Singh M, Sharma VK (2025). "Genome assembly and insights into globally invasive Red-vented Bulbul (*Pycnonotus cafer*)". *DNA Research* 32(6):dsaf027. DOI 10.1093/dnares/dsaf027 (PMID 41063535, PMC12666379) — đối chiếu trực tiếp nội dung PMC + tóm tắt WebSearch độc lập | Q1, Q2 |
| 3 | Chưa tìm được accession dạng GCA_/GCF_ chính thức cho *P. cafer* tại thời điểm tra cứu (chỉ có WGS master JBQLIZ000000000, chưa thấy trang NCBI Assembly riêng) | UNVERIFIED | Không tìm thấy trang `ncbi.nlm.nih.gov/assembly/` cho JBQLIZ000000000 trong phiên này — ghi ✘ theo luật "không đoán accession" | Q1 |
| 4 | Không tìm thấy genome NHÂN (nuclear) công bố cho *P. sinensis*, *P. aurigaster*, *Hypsipetes*, *Alophoixus*; chỉ có mitogenome đơn lẻ (vd. *P. sinensis hainanus* mitogenome, *P. melanicterus* mitogenome) | UNVERIFIED (✘ không thấy) | WebSearch nhiều truy vấn khác nhau trên NCBI/PubMed, không ra kết quả genome nhân | Q1 |
| 5 | Sẻ vằn (*Taeniopygia guttata*) — assembly tham chiếu VGP bTaeGut1.4.pri, GenBank GCA_003957565.2, trở thành reference chính thức năm 2021, dựng bằng PacBio CLR + 10x Genomics + Bionano + Hi-C (cá thể Black17) | STRONG_INFERENCE | Trang NCBI Assembly https://www.ncbi.nlm.nih.gov/assembly/10005361 (tiêu đề xác nhận tên assembly) + tóm tắt WebSearch dẫn cùng accession từ nguồn khác | Q3 |
| 6 | Sẻ ngô lớn (*Parus major*) — RefSeq GCF_001522545.1, tên assembly Parus_major1.0.3; có bản mới hơn Parus_major1.1 (NCBI assembly ID 763951) nhưng chưa xác định được số GCF mới trong phiên này | STRONG_INFERENCE (bản 1.0.3); UNVERIFIED (bản 1.1, chưa có GCF) | https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_001522545.1/ ; https://www.ncbi.nlm.nih.gov/assembly/763951 | Q3 |
| 7 | Sẻ nhà (*Passer domesticus*) — GCA_001700915.1 | STRONG_INFERENCE (1 nguồn, chưa mở trực tiếp trang NCBI Assembly) | Bài "Whole Genome Sequencing and Assembly of the House Sparrow, *Passer domesticus*" (PMC12308067 / bioRxiv 10.1101/2023.11.04.565608) — qua tóm tắt WebSearch | Q3 |
| 8 | MC1R và ASIP là gene ứng viên gây "parallel melanism" (đen toàn thân) hội tụ độc lập ở hai đảo khác nhau của chim chích Solomon *Monarcha castaneiventris*, xác nhận bằng GWAS kiểm soát cấu trúc quần thể + FST outlier | STRONG_INFERENCE (1 nguồn, nhưng thiết kế GWAS + FST mạnh) | Uy JAC et al. (2016). "Mutations in different pigmentation genes are associated with parallel melanism in island flycatchers". *Proc Biol Sci* 283(1834). DOI 10.1098/rspb.2016.0731 (PMID 27412275, PMC4947890) | Q4 |
| 9 | Một deletion 55bp gần OCA2/HERC2 liên quan hàm lượng pheomelanin ở lông chim *Sporophila* (Capuchino seedeaters); phân kỳ loài chủ yếu do SNP/indel nhỏ ở vùng không mã hoá của gene liên quan melanin, không phải SV lớn | STRONG_INFERENCE (1 nguồn, pangenome + GWAS) | Recuerda M et al. (2025). "A pangenomic approach reveals the sources of genetic variation fueling the rapid radiation of Capuchino Seedeaters". *Evolution* 79(12):2739-2755. DOI 10.1093/evolut/qpaf188 (PMID 40985593) | Q4 |
| 10 | MC1R KHÔNG liên quan thật sự tới màu lông (trắng/hoang dã) ở sẻ vằn nuôi nhốt — liên kết ban đầu là do cấu trúc quần thile (artefact), phép lai kiểm chứng không cho kết quả có ý nghĩa | STRONG_INFERENCE (1 nguồn, có thiết kế lai kiểm chứng) | Hoffman JI et al. (2014). "MC1R genotype and plumage colouration in the zebra finch (*Taeniopygia guttata*): population structure generates artefactual associations". *PLoS ONE* 9(1):e86519. DOI 10.1371/journal.pone.0086519 (PMID 24489736, PMC3906038) | Q4 |
| 11 | Ở chim sẻ nhà đỏ (house finch, *Haemorhous mexicanus*), CYP2J19/BDH1L KHÔNG xúc tác tạo sắc tố đỏ 3-OH-echinenone chính của loài này (bác bỏ giả định trước đây rằng mọi chim màu đỏ ketocarotenoid đều dùng chung con đường CYP2J19/BDH1L) | STRONG_INFERENCE (1 nguồn, có thực nghiệm chức năng + biểu hiện gene) | Koch RE et al. (2025). "Multiple Pathways to Red Carotenoid Coloration: House Finches (*Haemorhous mexicanus*) Do Not Use CYP2J19 to Produce Red Plumage". *Mol Ecol* 34(9):e17744. DOI 10.1111/mec.17744 (PMID 40167337, PMC12010460) | Q4 |
| 12 | CYP2J19 liên quan chức năng ty thể gan ở house finch đang thay lông — độ đỏ lông tương quan hiệu suất ty thể (nghiên cứu trước Koch 2025, sau này bị Koch 2025 đặt lại nghi vấn về cơ chế cụ thể ở loài này) | STRONG_INFERENCE (1 nguồn, đã bị nghiên cứu sau làm phức tạp thêm — xem claim #11) | Hill GE et al. (2019). "Plumage redness signals mitochondrial function in the house finch". *Proc Biol Sci* 286(1911):20191354. DOI 10.1098/rspb.2019.1354 (PMID 31551059, PMC6784716) | Q4 |
| 13 | Ở chim hoàng yến nuôi (*Serinus canaria*), tín hiệu chọn lọc trùng với các gene carotenoid (CYP2J19, EDC, BCO2, SCARB1) và gene melanin (AGRP, ASIP, DCT, EDNRB, KITLG, MITF, MLPH, SLC45A2, TYRP1, ZEB2); 2 đột biến ứng viên trong MLPH giải thích biến thể "dilute" Opal và Onyx | STRONG_INFERENCE (1 nguồn, WGS pool-seq + phân tích Fst-window) | Bovo S et al. (2023). "Whole genome sequencing identifies candidate genes and mutations that can explain diluted and other colour varieties of domestic canaries (*Serinus canaria*)". *Anim Genet* 54(4):510-525. DOI 10.1111/age.13331 (PMID 37194440) | Q4 |
| 14 | Alignment Cactus 363 loài chim (B10K) chỉ có DUY NHẤT 1 file HAL khổng lồ ("hundreds of gigabytes"), tải tại `https://alignment-output.s3.amazonaws.com/birds-final.hal`; không có tuỳ chọn tải riêng từng loài/track; snake track (đọc HAL) có trên mọi genome ở UCSC nhưng chậm, khuyến nghị ≤5 snake track cùng lúc và vùng xem ≤100kb; bigMaf chỉ có trên trình duyệt gà; trang tài liệu KHÔNG nhắc tới phyloP/phastCons tính sẵn | CONFIRMED (fetch trực tiếp trang tài liệu chính thức UCSC/CGL, đối chiếu nội dung URL S3 nêu trong cùng trang) | UCSC/CGL "Bird 10K Alignment Tracks" — https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020-hub/documentation/b10kAlignment.html (liên hệ tác giả: Guojie Zhang, Benedict Paten) | Q5, Q6 |
| 15 | BUSCO lineage `aves_odb10` có 8,338 gene marker (OrthoDB) | UNVERIFIED (1 nguồn gián tiếp, chưa mở trực tiếp busco.ezlab.org) | Tóm tắt WebSearch dẫn OrthoDB/BUSCO v5 docs — chưa fetch trực tiếp trang gốc để xác nhận số liệu | Q7 |
| 16 | OrthoDB cung cấp tải theo phân nhóm phân loại (bao gồm Aves) qua `orthodb.org/?page=filelist`; có bản BUSCO/OrthoDB đã chia theo clade tại `bioinf.uni-greifswald.de/bioinf/partitioned_odb11/` | UNVERIFIED (chưa mở trực tiếp URL, chỉ có qua tóm tắt WebSearch) | WebSearch tổng hợp OrthoDB v11 userguide (ezlab.org) | Q6, Q7 |
| 17 | Ensembl lưu toàn bộ dữ liệu so sánh (GeneTree, orthologue/paralogue) trong CSDL `ensembl_compara`, tải được qua FTP dạng MySQL dump theo từng release; KHÔNG xác định được đường dẫn TSV cụ thể cho orthologue chim trong phiên này | UNVERIFIED (đường dẫn chính xác chưa xác minh) | Ensembl Compara resources paper, DOI 10.1093/database/bav096 (qua tóm tắt WebSearch) | Q6 |
| 18 | Ước lượng tài nguyên WSL2 (không phải benchmark thực đo, là tổng hợp suy luận): (a) chỉ dùng track bảo tồn có sẵn ~12–24GB RAM, đĩa vài chục–vài trăm MB; (b) IQ-TREE2 ASR 50 locus×50 loài ~8–16GB RAM/họ locus, đĩa 1–5GB; (c) codeml dN/dS 500 gene×50 loài ~4–8GB RAM, đĩa vài–vài chục GB; cả halTools, PHAST, IQ-TREE2, PAML/codeml được cho là cài/chạy được qua conda/bioconda trên WSL2 Ubuntu | UNVERIFIED (Perplexity tổng hợp, không có benchmark cụ thể trích dẫn, độ chính xác thấp) | Perplexity smart_query (intent=standard), lượt 1/3, nguồn tham chiếu gồm nhiều bài Bioinformatics/GBE không đọc trực tiếp | Q5 |

## 3. Bảng dataset/công cụ

| ID (docs/02 hoặc "mới") | Tên | URL | Chứa gì | URL đã mở? (✔/✘) | License |
|---|---|---|---|---|---|
| D01 | NCBI Assembly GCA_013400435.1 (*P. jocosus*) | https://www.ncbi.nlm.nih.gov/assembly/GCA_013400435.1 (+ FTP: https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/013/400/435/GCA_013400435.1_ASM1340043v1/) | Assembly report + assembly stats (scaffold-level, SOAPdenovo) | ✔ (fetch trực tiếp file report + stats) | NCBI GenBank — công khai, không ghi license riêng |
| mới | GenBank WGS *P. cafer* JBQLIZ000000000 (via PMC12666379) | https://pmc.ncbi.nlm.nih.gov/articles/PMC12666379/ | Bài báo genome + BioProject PRJNA1226769 / BioSample SAMN46958819 | ✔ (đọc nội dung bài qua fetch) | Bài mở (PMC), dữ liệu NCBI SRA công khai |
| D05 | NCBI Assembly bTaeGut1.4.pri (*Taeniopygia guttata*, VGP) | https://www.ncbi.nlm.nih.gov/assembly/10005361 | Trang assembly GCA_003957565.2 | ✔ (chỉ đọc được tiêu đề, không phải nội dung đầy đủ) | NCBI GenBank |
| mới | NCBI Datasets GCF_001522545.1 (*Parus major*) | https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_001522545.1/ | Trang assembly RefSeq Parus_major1.0.3 | ✔ (chỉ tiêu đề) | NCBI RefSeq |
| mới | *Passer domesticus* genome paper (PMC12308067) | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12308067/ | Bài công bố GCA_001700915.1 | ✘ (chỉ thấy qua tóm tắt WebSearch, chưa fetch trực tiếp) | — |
| D03 | UCSC/GenomeArk "Bird 10K Alignment Tracks" (363-loài Cactus HAL) | https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020-hub/documentation/b10kAlignment.html (HAL thô: https://alignment-output.s3.amazonaws.com/birds-final.hal) | Snake track HAL toàn bộ genome, bigMaf (chỉ browser gà); KHÔNG có phyloP/phastCons ghi rõ trên trang | ✔ (fetch toàn bộ nội dung trang) | Không ghi rõ — cần liên hệ tác giả (Zhang, Paten) |
| mới | BUSCO lineage `aves_odb10` | https://busco.ezlab.org/ (chưa xác định URL file .tar.gz chính xác) | Bộ gene marker đơn bản (single-copy) cho Aves, ước ~8,338 gene | ✘ (chưa mở trực tiếp) | MIT-like (theo thông lệ BUSCO, chưa verify) |
| mới | OrthoDB | https://www.orthodb.org/?page=filelist | Danh sách orthologue theo clade, có thể chọn Aves | ✘ (chưa mở trực tiếp) | Free for academic use (theo thông lệ OrthoDB, chưa verify) |
| D04 | Ensembl Compara | https://academic.oup.com/database/article/doi/10.1093/database/bav096/2630091 (bài mô tả) + FTP tổng: ftp.ensembl.org/pub/release-*/mysql/ensembl_compara_*/ | GeneTree, orthologue/paralogue đa loài (bao gồm chim) | ✘ (chưa xác định URL bird-specific cụ thể) | Ensembl — dữ liệu mở |

## 4. Trả lời ngắn từng câu hỏi trong brief

1. **Assembly *P. jocosus*:** CÓ — GCA_013400435.1, scaffold-level, B10K 2020, N50 scaffold chỉ 218 kb (thấp, short-read SOAPdenovo). Loài khác trong họ: chỉ *P. cafer* có genome mới tốt hơn (2025, N50 3.04Mb, chưa có GCA/GCF chính thức — chỉ WGS master). *P. sinensis*, *P. aurigaster*, *Hypsipetes*, *Alophoixus* — ✘ không có genome nhân. [CONFIRMED cho P. jocosus/P. cafer; UNVERIFIED/✘ cho phần còn lại]
2. **Bài báo genome họ Chào mào:** Xác minh được 1 bài chính thức — Puthumana et al. 2025 *DNA Research* (P. cafer), có DOI thật, đọc trực tiếp qua PMC. Chưa tìm được bài "chromosome-level" cho bất kỳ loài Pycnonotidae nào (P. cafer chỉ ở mức scaffold). [CONFIRMED]
3. **Tham chiếu Passerida:** sẻ vằn GCA_003957565.2 (bTaeGut1.4.pri, VGP); sẻ ngô lớn GCF_001522545.1 (bản cũ hơn, có bản 1.1 mới hơn chưa chốt số GCF); sẻ nhà GCA_001700915.1 (1 nguồn). [STRONG_INFERENCE]
4. **Gene sắc tố Passeriformes (không gà/bồ câu):** MC1R+ASIP (Monarcha, GWAS, CONFIRMED-quality single study); OCA2/HERC2 (Sporophila, pangenome GWAS); MC1R (âm tính ở sẻ vằn — cảnh báo quan trọng về population structure); CYP2J19/BDH1L (house finch — có cả bằng chứng ủng hộ 2019 và phủ định 2025 cho chính loài này); MLPH + 9 gene melanin khác + 4 gene carotenoid (canary nuôi, WGS selection scan). [STRONG_INFERENCE cho từng claim riêng lẻ]
5. **Khả thi tính toán WSL2:** HAL 363-loài là 1 file "hàng trăm GB", không tải được riêng lẻ theo loài/track — đây là rào cản thật. Không có phyloP/phastCons xác nhận có sẵn trên hub UCSC (mâu thuẫn giả định D03 gốc). Ước lượng RAM (Perplexity, chưa kiểm chứng bằng benchmark thật): kịch bản (a) 12–24GB, (b) 8–16GB/họ locus, (c) 4–8GB — đều nằm trong tầm máy cá nhân 32GB RAM nếu KHÔNG tải toàn bộ HAL. [UNVERIFIED cho số liệu RAM cụ thể]
6. **Thay thế rẻ (Ensembl Compara/UCSC bảng orthologue tải sẵn):** Có tồn tại về nguyên tắc (Ensembl Compara FTP MySQL dump theo release; OrthoDB theo clade) nhưng CHƯA xác định được URL bird-specific cụ thể, sẵn sàng tải ngay, trong phiên 3-lượt Perplexity + WebSearch giới hạn này. [UNVERIFIED]
7. **1:1 orthologue chim có sẵn:** BUSCO `aves_odb10` ≈ 8,338 gene marker (chưa mở trực tiếp trang gốc để xác nhận số chính xác). [UNVERIFIED]

## 5. Câu hỏi còn mở / cần vòng 2

- Chưa xác nhận *P. cafer* có được gán số GCA_/GCF_ chính thức chưa (JBQLIZ có thể chỉ là WGS tạm) — cần tra lại NCBI Assembly bằng BioProject PRJNA1226769.
- Chưa đọc được nội dung đầy đủ 2 trang NCBI Assembly (bTaeGut1.4.pri, Parus_major1.0.3) — WebFetch chỉ trả về header/tiêu đề, cần công cụ khác (vd. NCBI `datasets` CLI trong WSL2) để lấy N50/BUSCO chính xác.
- Chưa xác nhận nội dung đầy đủ bài "Genome Assemblies for Seven Families of Birds From the Global South" (PMC13373495 / Vinay et al., *Mol Ecol Resources* 2026) — không rõ 7 họ đó có gồm Pycnonotidae hay chỉ nhắc P. jocosus để so sánh; 2 lần fetch đều thất bại (reCAPTCHA, rate limit 429).
- Chưa xác minh trực tiếp trang busco.ezlab.org, orthodb.org/?page=filelist, và FTP Ensembl Compara cho đường dẫn bird-specific chính xác — mới có qua tóm tắt WebSearch, cần R6 hoặc vòng 2 mở trực tiếp.
- Ước lượng RAM/đĩa ở mục 4.5 chỉ là suy luận tổng hợp (Perplexity), CHƯA có benchmark thực đo trên máy Windows 11 + WSL2 thật — nên coi là giả định làm việc, cần thực nghiệm nhỏ (1 locus, 1 gene) để hiệu chỉnh trước khi cam kết kịch bản (b)/(c).
- Chưa xác nhận trang UCSC có phyloP/phastCons hay không qua nguồn thứ hai (chỉ có 1 nguồn — trang tài liệu chính) — nếu R1 tìm được nguồn khác nói có, cần đối chiếu lại.

## 6. Search log

| tool | query | số kết quả | dùng được? |
|---|---|---|---|
| pubmed.search_articles | Pycnonotus jocosus genome | 0 | Không |
| pubmed.search_articles | bulbul chromosome-level genome assembly | 0 | Không |
| pubmed.search_articles | Pycnonotidae genome | 10 | Có (dẫn tới P. cafer PMID) |
| pubmed.search_articles | Passeriformes plumage pigmentation gene GWAS | 3 | Có |
| pubmed.search_articles | MC1R OR ASIP melanin plumage color passerine bird | 10 (2134 total) | Có (lấy 1 PMID liên quan) |
| pubmed.search_articles | CYP2J19 carotenoid plumage finch | 3 | Có |
| pubmed.search_articles | Darwin finch ALX1 HMGA2 beak plumage color | 0 | Không |
| pubmed.search_articles | white-throated sparrow supergene plumage color ZAL2 | 0 | Không |
| pubmed.search_articles | bulbul Pycnonotus genome invasive | 1 | Có |
| pubmed.get_article_metadata | 6 PMID (40985593, 27412275, 24489736, 40167337, 37194440, 31551059) | 6 | Có |
| WebSearch | Pycnonotus jocosus genome assembly site:ncbi.nlm.nih.gov | 8 link | Có |
| WebSearch | "Pycnonotus jocosus" GCA genome assembly NCBI | 9 link | Có |
| WebSearch | GCA_013400435.1 assembly | nhiều, nhiễu | Một phần (dẫn tới URL assembly page) |
| WebSearch | "Genome assemblies for seven families of birds from the Global South" Pycnonotidae Pycnonotus | 7 link | Một phần |
| WebSearch | Pycnonotus cafer genome DNA Research 2025 BUSCO N50 accession | 8 link | Có |
| WebSearch | Pycnonotus cafer JBQLIZ genome NCBI assembly GCA | 5 link | Có |
| WebSearch | Pycnonotus sinensis genome assembly NCBI accession | 9 link | Có (kết luận ✘ không có nuclear genome) |
| WebSearch | Pycnonotus aurigaster OR Hypsipetes OR Alophoixus genome assembly NCBI accession | 8 link | Có (kết luận ✘) |
| WebSearch | zebra finch bTaeGut1.4.pri VGP genome assembly accession GCF GCA | 7 link | Có |
| WebSearch | "Parus major" genome assembly GCF_001522545 OR GCF RefSeq accession | 3 link | Có |
| WebSearch | great tit Parus major genome assembly accession GCF house sparrow Passer domesticus assembly accession GCA | 6 link | Có |
| WebSearch | BUSCO aves_odb10 number of genes OrthoDB | 9 link | Có (gián tiếp) |
| WebSearch | Ensembl Compara birds orthologues download whole genome alignment UCSC 363 birds Cactus hub Genome Ark | 9 link | Một phần |
| WebSearch | Ensembl FTP compara gene_trees birds orthologs download tsv URL | 8 link | Một phần |
| WebSearch | OrthoDB aves download orthologous groups url orthodb.org | 10 link | Một phần |
| WebFetch | https://www.ncbi.nlm.nih.gov/assembly/GCA_013400435.1 | — | Một phần (chỉ tiêu đề) |
| WebFetch | https://pmc.ncbi.nlm.nih.gov/articles/PMC12666379/ | — | Có (nội dung đầy đủ) |
| WebFetch | https://ftp.ncbi.nlm.nih.gov/.../GCA_013400435.1_ASM1340043v1_assembly_report.txt | — | Có |
| WebFetch | https://ftp.ncbi.nlm.nih.gov/.../GCA_013400435.1_ASM1340043v1_assembly_stats.txt | — | Có |
| WebFetch | https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020-hub/documentation/b10kAlignment.html | — | Có |
| WebFetch | https://pmc.ncbi.nlm.nih.gov/articles/PMC13373495/ | — | Không (reCAPTCHA) |
| WebFetch | https://www.biorxiv.org/content/10.1101/2025.07.31.667860v1.full | — | Không (HTTP 429) |
| WebFetch | https://www.ncbi.nlm.nih.gov/assembly/10005361 | — | Một phần (chỉ tiêu đề) |
| WebFetch | https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_001522545.1/ | — | Một phần (chỉ tiêu đề) |
| pplx_usage | (kiểm tra quota, không tính vào 3 lượt) | — | Có |
| pplx_smart_query (intent=standard) | Ước lượng RAM/đĩa WSL2 cho halTools/PHAST/IQ-TREE2/codeml, 3 kịch bản | 1 phản hồi tổng hợp | Có (lượt 1/3 Perplexity đã dùng) |
