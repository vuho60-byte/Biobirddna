# X1 — Viết script lối A2: vùng bảo tồn 363 loài (tọa độ gà) → tọa độ chào mào

Repo: `D:\BIRDBIODNA project`. Chỉ được tạo/sửa trong `pipeline/p02_core_map/` và `pipeline/p02_core_map/tests/`. Không đụng file khác. Không cần mạng. Đọc `docs/04-ke-hoach-tach-adn-goc.md` mục 1, 3, 8 để hiểu bối cảnh (không sửa).

## Mục tiêu
Một script Python 3.11 **chỉ dùng stdlib** `pipeline/p02_core_map/conserved_to_bulbul.py` với 3 lệnh con, và một wrapper `pipeline/p02_core_map/run_a2.sh` gọi docker theo thứ tự. Đầu ra cuối: BED vùng bảo tồn trên tọa độ chào mào + thống kê.

## Dữ liệu (đã có trên máy sau khi tải xong)
- `data/ucsc/ancRep_separate_models_rev.bw.conserved.bb` — bigBed 3 cột, 70.370.065 mục, phần lớn là khoảng 1 base, tọa độ gà galGal4; 134.568.082 base được phủ.
- `data/ucsc/Gallus_gallus.2bit` — bộ gene gà (2bit).
- `data/ncbi/GCA_013400435.1/GCA_013400435.1_ASM1340043v1_genomic.fna.gz` — bộ gene chào mào (142.341 scaffold, 1,02 Gb), gz.
- `data/ncbi/GCA_013400435.1/GCA_013400435.1_ASM1340043v1_genomic.gff.gz` — annotation NCBI (gz).

## Docker image đã pull (tag chính xác, dùng nguyên văn)
- `quay.io/biocontainers/ucsc-bigbedtobed:482--h0b57e2e_0` — `bigBedToBed in.bb out.bed`
- `quay.io/biocontainers/ucsc-twobittofa:482--hdc0a859_0` — `twoBitToFa in.2bit out.fa -bed=elements.bed` (tên FASTA = cột 4 của BED)
- `quay.io/biocontainers/minimap2:2.30--h577a1d6_0` — `minimap2 -x asm20 -t <N> --secondary=no -c target.fna.gz query.fa > out.paf`
Wrapper chạy trên Git Bash Windows: **bắt buộc** `MSYS_NO_PATHCONV=1` trước mỗi `docker run`, mount `-v "<đường dẫn Windows của data>:/data"`, đường dẫn trong container dùng `/data/...`.

## Lệnh con
1. `merge --in all.bed --out elements.bed --gap 10 --min-len 20 --stats merge_stats.tsv`
   - Đọc BED 3 cột đã sắp theo chrom rồi start (bigBedToBed xuất đúng thứ tự; vẫn kiểm và báo lỗi nếu không tăng dần). Gộp các khoảng cùng chrom có khoảng cách ≤ gap; giữ phần tử dài ≥ min-len. Cột 4 = ID `chrom:start-end`. Stream từng dòng, không nạp 70 triệu dòng vào bộ nhớ.
   - Stats: số khoảng vào, số phần tử ra, tổng bp vào/ra, histogram độ dài (bin 20–49, 50–99, 100–199, 200–499, ≥500), số phần tử theo chrom (top 40).
2. `paf2bed --paf elements.paf --out bulbul_core.bed --unmapped unmapped.txt --stats map_stats.tsv --min-identity 0.70 --min-coverage 0.80`
   - PAF chuẩn 12 cột + tag. Với mỗi query giữ **một** hit tốt nhất: ưu tiên mapq, rồi số match (cột 10), rồi độ dài align (cột 11). identity = matches/alignment-block-length; coverage = (qend−qstart)/qlen. Loại hit dưới ngưỡng → vào unmapped kèm lý do (`no_hit`, `low_identity`, `low_coverage`).
   - Ra BED 6+: `tname tstart tend qname identity(0–1000) strand qlen coverage mapq`. Stats: tổng query, mapped %, theo bin độ dài query, số query có hit thứ hai (nếu có dòng thứ hai trong PAF), phân bố identity.
3. `annotate --bed bulbul_core.bed --gff genomic.gff.gz --out core_annot.tsv --stats annot_stats.tsv`
   - Đọc GFF gz, lấy feature `gene`, `exon`, `CDS` (và `mRNA` để nối gene name qua `Parent`/`ID`). Với mỗi vùng BED: giao với exon/CDS/gene/intergenic (intron = trong gene nhưng không exon). Vì có 142 nghìn scaffold, index theo scaffold, sort theo start, dùng bisect; không O(n·m) toàn cục.
   - Ra: mỗi vùng một dòng với `feature_class` (CDS/exon_noncoding/intron/intergenic) + gene name/ID nếu có. Stats: số vùng và bp theo feature_class; top 50 gene theo bp lõi.

## Wrapper `run_a2.sh`
Thứ tự: bigBedToBed → `merge` → twoBitToFa (-bed elements.bed) → minimap2 (`-t` = số CPU−2, mặc định 12) → `paf2bed` → `annotate`. Mỗi bước ghi thời gian bắt đầu/kết thúc vào `data/a2/run.log`; bỏ qua bước đã có output (`--force` để chạy lại). Có chế độ `--chrom chr1` để benchmark: lọc `all.bed` theo chrom trước khi merge.

## Test
`pipeline/p02_core_map/tests/test_conserved_to_bulbul.py` (unittest, không pytest): merge (gap/min-len, kiểm thứ tự), paf2bed (chọn hit tốt nhất, ngưỡng, unmapped reason), annotate (CDS/exon/intron/intergenic, nhiều scaffold). Dữ liệu test nhúng trong file test. Chạy: `python -B -m unittest discover -s pipeline/p02_core_map/tests -v`.

## Tiêu chí xong
- `python -B pipeline/p02_core_map/conserved_to_bulbul.py --help` và mỗi lệnh con `--help` chạy.
- Test sạch. Không dependency ngoài stdlib. Không đọc/ghi ngoài đường dẫn tham số.
- README ngắn `pipeline/p02_core_map/README.md`: cách chạy, tham số, ý nghĩa cột output, giới hạn (galGal4 anchor; phần tử ngắn/phân kỳ cao có thể không căn được).
- Báo cáo ≤10 dòng: file đã tạo, kết quả test, giả định.
