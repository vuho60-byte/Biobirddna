# R5 — Bộ gene chào mào / Pycnonotidae + khả thi pipeline (T06 của V4)

Đọc `research/briefs/_COMMON.md` trước. Output: `research/raw/R5-bulbul-genome-pipeline-feasibility.md`.

## Câu hỏi phải trả lời
1. NCBI Assembly / Datasets: có assembly *Pycnonotus jocosus* (chào mào má đỏ, red-whiskered bulbul) không? Accession (GCA_/GCF_), năm, mức (contig / scaffold / chromosome), N50, BUSCO nếu có, ai nộp. Các loài Pycnonotidae khác có assembly (*P. sinensis*, *P. cafer*, *P. aurigaster*, *Hypsipetes*, *Alophoixus*…). Dùng WebSearch với `site:ncbi.nlm.nih.gov` và PubMed.
2. Bài báo genome họ Chào mào ("Pycnonotus genome", "bulbul chromosome-level genome") — xác minh.
3. Tham chiếu gần nhất chất lượng cao trong Passerida: sẻ vằn (bTaeGut1.4 / VGP), sẻ ngô lớn, chim sẻ nhà — accession.
4. Gene sắc tố đã nghiên cứu ở Passeriformes (không phải gà/bồ câu): danh sách gene + loài + loại bằng chứng (GWAS / QTL / functional).
5. Khả thi tính toán trên máy cá nhân Windows 11 + WSL2: dung lượng HAL 363 loài (GB?), có tải riêng từng loài / từng track không; halTools, PHAST, IQ-TREE2, codeml chạy trong WSL2 được không; ước lượng RAM / đĩa cho ba kịch bản: (a) chỉ dùng track bảo tồn có sẵn, (b) ASR 50 locus × 50 loài, (c) dN/dS 500 gene × 50 loài.
6. Thay thế rẻ: Ensembl Compara / UCSC có bảng orthologue + alignment tải sẵn cho chim không (URL).
7. Danh sách 1:1 orthologue chim có sẵn (OrthoDB, BUSCO `aves_odb10`) — số gene.

## Giới hạn
Perplexity ≤3 lượt. Không đoán accession; không thấy thì ghi ✘. Mục 1 là exit gate T06 của V4: kết luận "khả thi / khả thi có điều kiện / chưa khả thi" kèm lý do kỹ thuật.
