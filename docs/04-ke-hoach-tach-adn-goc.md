# 04 — Kế hoạch thao tác: tách "ADN gốc" (core-invariant) của chào mào bằng code

Ngày 2026-09-07. Mọi URL, kích thước dưới đây đã kiểm trực tiếp bằng HTTP HEAD/GET (không tải file lớn). Trả lời câu hỏi "ta cần làm gì để coding tách ADN tiền sử ra trước".

---

## 1. "ADN gốc" phải là thứ code tính được — ba sản phẩm

| Sản phẩm | Định nghĩa vận hành | Đầu vào | Đầu ra |
|---|---|---|---|
| **A. LÕI-363** | Tập vùng mà phyloP trên alignment 363 loài chim gọi là *bảo tồn có ý nghĩa* (FDR < 5%), tức vùng gần như không đổi suốt lịch sử lớp chim (~100+ triệu năm) | `ancRep_separate_models_rev.bw.conserved.bb` (tọa độ gà) | BED vùng bảo tồn trên tọa độ gà |
| **B. LÕI-chào-mào** | Ánh xạ A sang bộ gene chào mào và giao với annotation gene | A + bigMaf 363 loài (có hàng *Pycnonotus_jocosus*) + GFF chào mào | BED trên tọa độ chào mào; % genome; vùng nào là exon, intron, điều hòa; danh sách gene chứa LÕI |
| **C. Tổ tiên tái dựng theo locus** | Trình tự suy tại nút tổ tiên Neornithes, Passeriformes, Pycnonotidae cho từng gene đã chọn (gene màu T22 của V4 + gene hành vi Q2b) | Alignment 363 loài rút theo vùng từ bigMaf + cây loài | Trình tự tổ tiên + bảng vị trí khác biệt tổ tiên ↔ chào mào hiện đại |

Ghi chú ngôn ngữ: A và B là "vùng chịu chọn lọc lọc từ tổ tiên chung" — dấu vết theo nghĩa `docs/03` mục 6, **không** phải "DNA khủng long còn nguyên". Không đổi cách gọi này khi công bố.

---

## 2. Dữ liệu đã xác minh hôm nay

| File | URL | Kích thước | Range | Dùng cho |
|---|---|---|---|---|
| Vùng bảo tồn 363 loài | `https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020-hub/Gallus_gallus/ancRep_separate_models_rev.bw.conserved.bb` | 345 MB | ✔ | A |
| Vùng tăng tốc 363 loài (đối chứng) | `…/Gallus_gallus/ancRep_separate_models_rev.bw.accelerated.bb` | 329 MB | ✔ | A |
| phyloP điểm từng base 363 loài | `…/Gallus_gallus/ancRep_separate_models_rev.bw` | 3,86 GB | ✔ | A (tùy chọn) |
| Alignment 363 loài dạng bigMaf, neo gà (galGal4) | `…/Gallus_gallus/chicken.bigMaf.bb` | 195,9 GB | ✔ — **đọc theo vùng, không tải** | B, C |
| HAL Cactus 363 loài | `https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020.hal` | 417,3 GB | ✔ | Lối B (dự phòng) |
| Chào mào trong hub | `…/363-avian-2020-hub/Pycnonotus_jocosus/` (2bit 268 MB, genes.bb 2,3 MB, chrom.sizes) | — | ✔ | B; xác nhận chào mào là 1/363 genome |
| Bộ gene chào mào NCBI | `https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/013/400/435/GCA_013400435.1_ASM1340043v1/` (fna.gz 325 MB, gff, protein, cds; md5 có) | ~0,5 GB | ✔ | B, C |
| Mô hình trung tính phyloP | `b10k_model_363_{macros,micros,sex}.mod` | 19 KB × 3 | ✔ | tự chạy phyloP nếu cần |
| Gà 2bit + chrom.sizes | `…/Gallus_gallus/Gallus_gallus.2bit` (266 MB); chrom.sizes cho thấy galGal4 | — | ✔ | tham chiếu tọa độ |

Đã đóng: U1 (HAL có range, chào mào có trong alignment). Link S3 `birds-final.hal` trong R1 là link chết (404).

---

## 3. Hai lối đi

**Lối A — rẻ, làm ngay (khuyến nghị):** kent tools (`bigBedToBed`, `bigWigToBedGraph`) đọc bigBed/bigWig/bigMaf **từ xa theo vùng** qua HTTP range. Không tải HAL, không tải bigMaf. Quy trình:
1. Lấy BED vùng bảo tồn (A) từ `conserved.bb` (tải 345 MB hoặc đọc từ xa).
2. Với từng vùng, đọc block MAF từ `chicken.bigMaf.bb` theo tọa độ gà → block chứa hàng `Pycnonotus_jocosus` kèm tọa độ chào mào → ghi BED chào mào (B). Đây là phép "liftover" trực tiếp, không cần HAL.
3. Giao BED chào mào với GFF NCBI → gene/exon/intron/điều hòa; thống kê.
4. Với gene đã chọn: rút MAF 363 loài của vùng gene → MAFFT/IQ-TREE2 `-asr` → C.

**Lối B — đầy đủ, dự phòng:** tải HAL 417 GB về ổ D (còn 483 GB, sẽ chật) → `halStats`, `hal2maf`, `halLiftover` cục bộ. Chỉ mở khi lối A quá chậm hoặc cần vùng không neo được trên gà. **Không tải khi chưa duyệt.**

Rào cản đã biết của lối A: bigMaf neo trên gà, nên vùng chào mào không align được với gà sẽ không có mặt (ước lượng thiếu ~vài %; ghi rõ khi báo cáo). Bổ khuyết sau bằng `halLiftover` từ xa nếu hal tools đọc được URL (gate P1.3).

---

## 4. Môi trường: Docker (đã có, đang mở), không cài Ubuntu

Mọi tool chạy trong container, mount `D:\BIRDBIODNA project\data` vào `/data`. Image dự kiến (tag kiểm trên quay.io trước khi pull, không đoán):
- kent tools: `quay.io/biocontainers/ucsc-bigbedtobed`, `ucsc-bigwigtobedgraph`, `ucsc-bedtobigbed`
- hal + cactus: `quay.io/comparative-genomics-toolkit/cactus` (chứa `halStats`, `hal2maf`, `halLiftover`)
- PHAST: `quay.io/biocontainers/phast` · MAFFT: `quay.io/biocontainers/mafft` · IQ-TREE 2: `quay.io/biocontainers/iqtree` · PAML: `quay.io/biocontainers/paml` · BUSCO: `ezlabgva/busco`
- Python: `python:3.11` + `biopython pandas pyranges pyBigWig`

`env/environment.yml` giữ làm phương án nếu sau này có WSL Ubuntu; hiện không dùng.

---

## 5. Trình tự việc (thay cho P1.1–P1.7 trong tổng hợp vòng 1)

| # | Việc | Cần duyệt | Tiêu chí xong |
|---|---|---|---|
| P1.0 | Thăm dò URL/kích thước/range — **xong hôm nay** | — | bảng mục 2 |
| P1.1 | Pull image kent tools; chạy `bigBedToBed` đọc **từ xa một vùng nhỏ** của `conserved.bb` (vài KB) | pull image (~50–150 MB) | in ra được ≥1 dòng BED; ghi thời gian |
| P1.2 | Tải về máy: `conserved.bb` 345 MB, `accelerated.bb` 329 MB, 3 file `.mod`, genome chào mào fna+gff+protein+cds (~0,5 GB) → sha256/md5 vào `data/registry.csv` | tải ~1,2 GB | md5 fna khớp `b856b3cb…`; registry đủ dòng |
| P1.3 | Script `pipeline/p02_core_map/conserved_to_bulbul.py`: đọc block MAF từ bigMaf từ xa cho từng vùng bảo tồn, rút hàng *Pycnonotus_jocosus* → BED chào mào. **Benchmark trên NST 1 của gà trước**, ngoại suy thời gian toàn genome | — (đọc từ xa vài trăm MB) | BED chr1; log thời gian; ước lượng toàn genome |
| P1.4 | Chạy toàn genome nếu P1.3 chấp nhận được; thống kê % genome, giao GFF → báo cáo "LÕI chào mào v0" | — | `research/synthesis/03-loi-chao-mao-v0.md` + BED + sha256 |
| P1.5 | (song song) BUSCO `aves_odb10` trên genome chào mào để chốt chất lượng tham chiếu | pull image BUSCO (~vài GB) + lineage (~?) | báo cáo BUSCO |
| P1.6 | Chọn 20 locus đầu (10 gene màu từ registry T22 + 10 gene hành vi Q2b) → rút MAF → cây → ASR (sản phẩm C, phiên bản 0) | — | trình tự tổ tiên tại 3 nút cho 20 locus, nhãn U/S |
| Gate | P1.3 quá chậm (> ~24 h ước lượng cho toàn genome) hoặc thiếu vùng | duyệt tải HAL 417 GB | quyết định lối B |

---

## 6. Cần chủ dự án duyệt trước khi tôi chạy

1. Pull image Docker kent tools (nguồn quay.io/biocontainers; ~50–150 MB).
2. Tải 4 nhóm file ở P1.2, tổng ~1,2 GB, vào `D:\BIRDBIODNA project\data\`.
3. (Sau) Pull image BUSCO + lineage `aves_odb10` (vài GB) cho P1.5.
Không có mục nào ghi ra ngoài máy, không đăng, không gửi dữ liệu đi đâu.

---

## 7. Không làm
- Không tải HAL 417 GB hay bigMaf 196 GB khi chưa duyệt và chưa chứng minh lối A thiếu.
- Không suy gene chào mào từ gà/bồ câu/yến hót (T22 giữ U).
- Không gọi vùng bảo tồn là "DNA khủng long còn nguyên"; không nâng nhãn khi chưa có kết quả chạy thật.

---

## 8. Kết quả P1.1 (2026-09-07, chạy thật qua Docker) và điều chỉnh lối A

| Kiểm | Kết quả |
|---|---|
| `bigBedInfo` conserved.bb (từ xa) | 70.370.065 mục, phủ **134.568.082 base** trên gà galGal4 (≈12,9% genome) → đây là kích thước "LÕI-363" trên tọa độ gà. Phần lớn mục là 1 base (điểm phyloP có ý nghĩa), cần gộp thành phần tử |
| `bigBedToBed` conserved.bb chr1:1,00–1,10 Mb (từ xa) | trả BED trong ~6 s (chủ yếu khởi động container + đọc index) |
| `bigBedInfo` chicken.bigMaf.bb (từ xa) | 155.265.270 block, 673 Mb gà được phủ, 12.267 NST/scaffold; schema `bedMaf` (chrom, start, end, mafBlock) |
| Block MAF chr1:5.902.608–5.904.174 (113 block) | Có hàng `Pycnonotus_jocosus` với **trình tự thật** nhưng **tọa độ giả** (`.1 1 1 + 6000`, giống 39.476 hàng khác); chỉ một số loài giữ tọa độ thật (ví dụ *Geospiza_fortis.scaffold428 62194*) |
| `bigBedToBed` conserved.bb cục bộ, chr1 gà (stream, 28 s) | 12.592.395 khoảng, 22.345.958 bp phủ (≈11,4% chr1); 9.317.873 cặp kề nhau ≤10 bp → sau gộp còn cỡ vài triệu phần tử, lọc ≥20 bp sẽ giảm mạnh; toàn genome ước ~3 phút đọc |

**Hệ quả:** bigMaf cho **trình tự** chào mào theo vùng gà (đủ cho sản phẩm C: cây + ASR theo locus) nhưng **không cho vị trí** trên bộ gene chào mào. Bước 2 của lối A (liftover qua bigMaf) bị loại. Thay bằng:

- **Lối A2 (khuyến nghị, rẻ):** gộp các base bảo tồn thành phần tử (ví dụ gộp khoảng cách ≤10 bp, giữ phần tử ≥20 bp) → rút trình tự gà bằng `twoBitToFa` (kent, đọc 2bit từ xa hoặc tải 266 MB) → căn lên bộ gene chào mào bằng `minimap2` (chế độ asm20 / hoặc LAST nếu phân kỳ cao) → BED chào mào + % phần tử ánh xạ được. Ưu: không cần HAL; nhược: phần tử ngắn hoặc phân kỳ >20% có thể không căn được → báo tỉ lệ thiếu.
- **Lối B2 (chính xác nhất, cần thử):** `halLiftover` của hal tools trong image cactus (516 MB) đọc HAL 417 GB **từ xa** nếu bản build hỗ trợ URL; nếu được, liftover gà→chào mào là chính xác theo alignment gốc, không cần tải HAL.

Cần duyệt thêm: pull `minimap2` (~71 MB) + tải `Gallus_gallus.2bit` (266 MB) cho A2; pull image cactus (516 MB) để thử B2.
