# 02 — Registry nguồn dữ liệu & công cụ (cập nhật vòng 1 (2026-09-07): 8 ✔ / 6 ✘)

Mọi dòng dưới đây là **giả định làm việc** cho tới khi subagent R1/R5 xác minh URL, phiên bản và license. Sau vòng 1, cột "Xác minh" phải là ✔/✘ kèm ngày.

## A. Dữ liệu bộ gene & alignment

| ID | Nguồn | Dùng cho | Xác minh |
|---|---|---|---|
| D01 | NCBI Datasets / GenBank — assembly *Pycnonotus jocosus* CÓ: `GCA_013400435.1` (B10K nộp 2020), scaffold, N50 218 kb, ~1,02 Gb và họ Pycnonotidae | Bộ gene tham chiếu chào mào (T06 của V4) | ✔ R5 |
| D02 | B10K (Bird 10,000 Genomes) — 363 bộ gene (Feng 2020), cây 2024 (Stiller) | Alignment đa loài, cây loài | ✔ R1 (b10k.genomics.cn; CNGB) — license chưa rõ |
| D03 | UCSC / Genome Ark hub "363 birds" — Cactus HAL + phastCons/phyloP | Điểm bảo tồn tính sẵn (tránh tự align) | ✔ R1 — HAL `birds-final.hal` trên S3 là MỘT file hàng trăm GB, không tải riêng loài; phyloP ✔ (3 `.mod`), phastCons ✘ |
| D04 | Ensembl Rapid Release / Ensembl Compara | Annotation, orthologue | ✘ — Compara chỉ có MySQL dump, chưa có đường dẫn bird-specific |
| D05 | VGP (Vertebrate Genomes Project) — sẻ vằn bTaeGut, gà GRCg7b… | Tham chiếu chất lượng cao Passeriformes + ngoài nhóm | ✔ một phần — sẻ vằn `GCA_003957565.2`, sẻ ngô lớn `GCF_001522545.1`, sẻ nhà `GCA_001700915.1` |
| D06 | Bộ gene ngoài nhóm: cá sấu Mỹ, rùa, thằn lằn | Định gốc, so bảo tồn | ✘ — chưa R-file nào cho accession ngoài nhóm (ưu tiên 1 vòng 2) |
| D07 | Bộ probe UCE Tetrapods-5Kv1 (phyluce) | Tập UCE chuẩn | ✔ — Figshare + github faircloth-lab/uce-probe-sets; 5.472 bait / 5.060 locus |
| D08 | Dữ liệu ASHCE (Seki 2017) — bảng bổ sung | Tập "DNA riêng chim" | ✘ — supplementary Seki 2017 bị chặn |
| D09 | aDNA chim tuyệt chủng: moa, chim voi, dodo, bồ câu viễn khách (GenBank/ENA) | Nhánh khảo cổ | ✘ — accession nằm trong bài, chưa mở |
| D10 | TimeTree / Open Tree of Life | Tuổi phân tách | ✔ — TimeTree, chỉ dùng nghiên cứu cá nhân, không redistribute |
| D11 | Paleobiology Database (PBDB) | Mốc hóa thạch chim | ✔ trang chủ, license chưa xác định |
| D12 | IUCN Red List API | Thống kê tuyệt chủng Q5 | ✘ (403) → thay bằng BirdLife DataZone ✔ |
| D13 | Catalog đột biến màu chim cảnh có gene (gà, bồ câu, yến hót, vẹt đuôi dài, sẻ vằn) | Nối V4 T22 | ✔ — dựng từ registry 49 dòng trong `00-tong-hop` mục 5 |
| D14 | Genome nhân Pycnonotidae ngoài *P. jocosus* (*P. sinensis*, *P. aurigaster*, *Hypsipetes*, *Alophoixus*; *P. cafer* chưa có GCA/GCF) | chặn ASR trong chi | ✘ R5 |

## B. Công cụ tính toán (chạy trong WSL2 + conda, xem env/environment.yml)

| Công cụ | Việc | Ghi chú |
|---|---|---|
| Biopython, pandas, pyranges | thao tác trình tự/khoảng | |
| halTools / hal2maf | đọc alignment Cactus | cần WSL2 |
| PHAST (phastCons, phyloP) | điểm bảo tồn nếu phải tự tính | ưu tiên dùng track có sẵn |
| MAFFT / PRANK | align locus nhỏ | |
| IQ-TREE 2 | cây + ASR (`-asr`) | |
| PAML (codeml) / HyPhy | dN/dS | |
| phyluce | trích UCE | |
| BUSCO | đánh giá assembly | |
| minimap2 / samtools | map, index | |
| NCBI `datasets` CLI | tải assembly có kiểm sha | |

## C. Công cụ tìm tài liệu (đã có trong phiên Claude)

PubMed MCP · Consensus MCP · bioRxiv MCP · Perplexity MCP (Pro Search — ngân sách 78/tuần, mỗi subagent ≤3) · WebSearch · ACPX Gemini (Google grounding, 0 token Claude).

## E. Cập nhật vòng 2 (R8, 2026-09-07)

- **D06 ngoài nhóm — accession thấy trực tiếp trên NCBI Datasets:** GCF_001723895.1, GCF_011386835.1, GCF_015237465.2, GCF_030867095.1, GCF_035594765.1 (cá sấu Mỹ, cá sấu nước mặn, rùa xanh, rùa sơn Mỹ, thằn lằn Anolis — C). Chưa tải.
- **D08 ASHCE:** Seki 2017 Supplementary Data 1 mở được (HTTP 200, ~33 MB xlsx): `https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fncomms14229/MediaObjects/41467_2017_BFncomms14229_MOESM1288_ESM.xlsx` — hệ tọa độ galGal4 là STRONG_INFERENCE, phải kiểm bằng cách giao với `Gallus_gallus.chrom.sizes`. Chưa tải.
- **U17 mốc tuổi (TimeTree, neo quanh, chưa có số crown Pycnonotidae):**
  - **1) U17 — mốc tuổi phân tách Pycnonotidae/Pycnonotus:** Không có con số "crown Pycnonotidae" xác nhận trực tiếp từ Oliveros 2019/Kuhl 2021/Stiller 2024 trong vòng này (UNVERIFIED — bảng phụ lục không mở được). Có 4 mốc 
- **Gene răng ở gà:** ENAM/AMELX/AMBN/DSPP/AMTN không có bản ghi trên NCBI Gene (C); MEPE có gene thật và không thuộc bộ gene Meredith 2014 dùng → phép thử H1 trên chào mào phải làm bằng tblastn protein cá sấu/rùa lên genome (cần image BLAST, chưa duyệt).
