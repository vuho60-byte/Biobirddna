# T-C — locus-c: sản phẩm C phiên bản 0 — 20 locus, tọa độ galGal4, alignment 363 loài theo exon

Repo: `D:\BIRDBIODNA project`. Được ghi: `data/c_loci/**`, `pipeline/p03_asr/**`, `research/synthesis/04-locus-c-v0.md`, 1 dòng `tasks/primordial-dna-handoff.md`. Không đụng file khác. **Không pull image mới, không tải file > 50 MB, không dùng Perplexity.** Canh đĩa: tổng `data/c_loci/` < 400 MB; RAM: xử lý dòng theo luồng.

## Bối cảnh (đọc trước)
- `docs/04-ke-hoach-tach-adn-goc.md` mục 1 (sản phẩm C), mục 8 (bigMaf: trình tự thật, tọa độ giả cho nhiều loài — chỉ tọa độ gà là thật).
- `research/synthesis/00-tong-hop-vong-1.md` mục 5 (registry gene: 5A màu, 5B toolkit, 5C hành vi).
- Docker image đã có: `quay.io/biocontainers/ucsc-bigbedtobed:482--h0b57e2e_0`. Chạy trên Git Bash: **`MSYS_NO_PATHCONV=1 docker run --rm quay.io/biocontainers/ucsc-bigbedtobed:482--h0b57e2e_0 bigBedToBed <url|file> -chrom=<chr> -start=<s> -end=<e> stdout`**. bigMaf: `https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020-hub/Gallus_gallus/chicken.bigMaf.bb` (196 GB, **chỉ đọc theo vùng**, tuyệt đối không tải). Mỗi dòng ra = `chrom start end mafBlock` với mafBlock là các dòng MAF nối bằng `;` (ví dụ `a;s Gallus_gallus.chr1 1000002 1 + 195276750 A;s Alca_torda.1 1 1 + 6000 T;…`).

## Việc
1. **Chọn 20 gene**: 10 từ 5A/5B (ưu tiên có ở gà và có trong registry: MC1R, TYR, SLC45A2, MLPH, PMEL, TYRP1, SOX10, OCA2, ASIP, BMP4) và 10 từ 5C/5B (FOXP2, CRY4, CLOCK, NPAS2, ADCYAP1, DRD4, SLC6A4, CREB1, CALM1, SHH). Nếu gene nào không có trên galGal4 thì thay bằng gene khác trong registry, ghi lý do.
2. **Tọa độ galGal4** (alignment neo trên galGal4, không dùng GRCg6a/7b): dùng UCSC REST `https://api.genome.ucsc.edu/getData/track?genome=galGal4;track=refGene;chrom=<chr>;start=<s>;end=<e>` hoặc tra theo tên qua `https://api.genome.ucsc.edu/search?genome=galGal4;search=<GENE>` rồi lấy exon/CDS (`exonStarts/exonEnds/cdsStart/cdsEnd`). Lưu `data/c_loci/loci_galGal4.tsv` (gene, chrom, txStart, txEnd, cdsStart, cdsEnd, exonStarts, exonEnds, nguồn). Nếu refGene không có, thử track `ncbiRefSeq` hoặc `ensGene`; vẫn không có → ghi UNVERIFIED và thay gene.
3. **Rút alignment theo CDS exon** (không rút cả gene — quá lớn): viết `pipeline/p03_asr/extract_locus.py` (Python 3.11 stdlib): với mỗi exon CDS, gọi bigBedToBed theo vùng, parse mafBlock, ghép các block theo thứ tự → cho mỗi loài chuỗi CDS (giữ gap `-`; loài thiếu ở block → `-`), nối exon theo chiều gene (đảo bổ sung nếu gene trên strand `-`). Ghi `data/c_loci/<GENE>/<GENE>.cds363.fa` (363 hàng, tên loài) + `<GENE>.blocks.tsv` (số block, base gà, % loài có dữ liệu). Hàng `Pycnonotus_jocosus` phải có mặt.
4. **Kiểm nhanh**: với 3 gene, dịch chuỗi gà (không gap) sang protein và so với protein gà trong NCBI/UCSC (đọc từ refGene hoặc bỏ qua nếu không có) — ít nhất kiểm không có codon dừng sớm bất thường ở gà. Ghi kết quả.
5. Báo cáo `research/synthesis/04-locus-c-v0.md`: bảng 20 gene (tọa độ, số exon, tổng bp CDS, số loài có ≥50% vị trí, % gap ở chào mào), thời gian chạy, dung lượng, giới hạn (galGal4 anchor; block nhỏ; tọa độ loài khác giả), bước tiếp (IQ-TREE2 `-asr` — cần duyệt pull image). Nhãn: đây là dữ liệu trung gian, không kết luận sinh học.
6. Thêm 1 dòng handoff.

## Trả về Main ≤10 dòng
số gene có tọa độ / 20 · số gene rút xong · tổng bp CDS · % loài có dữ liệu trung bình · % gap chào mào trung bình · dung lượng `data/c_loci` · thời gian · DONE/BLOCKED · đường dẫn.
