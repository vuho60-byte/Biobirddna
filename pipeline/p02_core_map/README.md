# p02_core_map — lối A2: vùng bảo tồn 363 loài (tọa độ gà) → tọa độ chào mào

Xem bối cảnh đầy đủ tại `docs/04-ke-hoach-tach-adn-goc.md` mục 1, 3, 8 (không sửa file đó).
Brief thực thi: `research/briefs/X1-codex-conserved-to-bulbul.md`.

Hai file:
- `conserved_to_bulbul.py` — Python 3.11, **chỉ dùng stdlib**, 3 lệnh con `merge` / `paf2bed` / `annotate`. Xử lý theo luồng (streaming), không nạp toàn bộ 70 triệu dòng vào bộ nhớ.
- `run_a2.sh` — wrapper Git Bash gọi docker (kent tools + minimap2) theo đúng thứ tự, ghi log thời gian, hỗ trợ resume (theo cả output lẫn tham số — xem mục `step_needed`) và benchmark theo 1 NST.
- `split_fasta.py` — chia FASTA(.gz) thành các mảnh ≤ N base (không cắt giữa scaffold), stdlib-only, streaming. Dùng trong bước 3 của `run_a2.sh`.

## Luồng dữ liệu

```
ancRep_separate_models_rev.bw.conserved.bb (bigBed, tọa độ gà galGal4, 70.370.065 mục ~1bp)
  │  docker: bigBedToBed ... stdout   (KHÔNG ghi file all.bed 1,4 GB trung gian)
  ▼
merge --in - --out elements.bed --gap 10 --min-len 20 --stats merge_stats.tsv
  │  (gộp khoảng cách ≤ gap, giữ phần tử ≥ min-len; BED 4 cột, cột 4 = chrom:start-end)
  ▼
docker: twoBitToFa Gallus_gallus.2bit elements.fa -bed=elements.bed
  │  (tên mỗi sequence trong FASTA = cột 4 của elements.bed)
  ▼
split_fasta.py --in bulbul.fna.gz --out-dir genome_chunks --max-bases 180000000
  │  (chia bộ gene chào mao thành mảnh ≤ chunk-bases; bỏ qua nếu đã có mảnh)
  ▼
[mỗi mảnh] docker: minimap2 -x asm20 -k 13 -w 5 -s 30 -m 20 -n 2 -t <N> --secondary=no -c \
             genome_chunks/chunk_NN.fa elements.fa >> elements.paf
  │  (nối PAF của mọi mảnh; -k/-w/-s/-m/-n cấu hình qua --mm-extra)
  ▼
paf2bed --paf elements.paf --out bulbul_core.bed --unmapped unmapped.txt --stats map_stats.tsv \
        --min-identity 0.70 --min-coverage 0.80 [--query-list elements.bed]
  │  (1 hit tốt nhất / query TÍNH QUA CẢ CÁC MẢNH; BED 6+ tọa độ chào mào)
  ▼
annotate --bed bulbul_core.bed --gff genomic.gff.gz --out core_annot.tsv --stats annot_stats.tsv
  │  (feature_class + gene cho từng vùng)
  ▼
core_annot.tsv  =  BED vùng bảo tồn trên tọa độ chào mào + phân loại CDS/exon/intron/intergenic
```

## Lệnh con

### 1. `merge` — gộp khoảng bảo tồn thành phần tử

```
python -B conserved_to_bulbul.py merge \
  --in all.bed --out elements.bed --gap 10 --min-len 20 --stats merge_stats.tsv
```

- `--in`: BED 3 cột đã sắp theo chrom rồi start (đúng thứ tự `bigBedToBed` xuất ra). **`--in -` đọc từ stdin** — dùng để pipe thẳng từ `bigBedToBed ... stdout`, tránh ghi BED ~1,4 GB trung gian.
- `--out`: BED 4 cột (`chrom`, `start`, `end`, `id=chrom:start-end`); `--out -` ghi ra stdout.
- `--gap N`: gộp hai khoảng cùng chrom nếu `start_kế_tiếp - end_hiện_tại ≤ N` (mặc định 10).
- `--min-len N`: chỉ giữ phần tử sau gộp dài ≥ N (mặc định 20).
- `--stats FILE`: TSV gồm `metric\tvalue` (intervals_in, elements_out, bp_in, bp_out, histogram độ dài 5 bin: `20_49`/`50_99`/`100_199`/`200_499`/`500_plus`) rồi một bảng `chrom\telements` top 40 NST theo số phần tử.
- **Kiểm tra thứ tự đầu vào**: nếu `start` giảm trong cùng 1 chrom, hoặc 1 chrom quay lại sau khi đã chuyển sang chrom khác (không nhóm liên tục), script dừng với lỗi rõ ràng (`SystemExit`, exit code 1) thay vì âm thầm cho kết quả sai.
- Xử lý từng dòng một (generator + biến trạng thái đơn), không nạp cả file vào bộ nhớ dù đầu vào 70 triệu dòng.

### 2. `paf2bed` — chọn hit tốt nhất mỗi query, đổi PAF → BED

```
python -B conserved_to_bulbul.py paf2bed \
  --paf elements.paf --out bulbul_core.bed --unmapped unmapped.txt --stats map_stats.tsv \
  --min-identity 0.70 --min-coverage 0.80 [--query-list elements.bed]
```

- Đọc PAF chuẩn 12 cột (`minimap2 -c`). Với mỗi `qname`, giữ **1 hit tốt nhất**, xếp hạng theo thứ tự ưu tiên: `mapq` → số match (cột 10) → độ dài align (cột 11).
- `identity = matches / alignment_block_length` (cột 10 / cột 11); `coverage = (qend - qstart) / qlen`.
- Loại nếu `identity < --min-identity` (lý do `low_identity`, kiểm trước) hoặc `coverage < --min-coverage` (lý do `low_coverage`, kiểm sau).
- `--query-list FILE` (tuỳ chọn, không có trong lệnh gốc của brief nhưng cần để phát hiện `no_hit`): danh sách toàn bộ tên query đã đưa vào minimap2 (ví dụ chính `elements.bed`, script tự lấy cột 4). Query có trong danh sách này nhưng **không xuất hiện một dòng PAF nào** → `unmapped` với lý do `no_hit`. **Nếu không truyền `--query-list`, không thể phân biệt được query "chưa từng thử map" — vì PAF không có dòng nào cho các query hoàn toàn không align, nên chỉ `low_identity`/`low_coverage` được phát hiện.** `run_a2.sh` luôn truyền `--query-list elements.bed`.
- `--out` (BED 6+, cột 4 = trace về conserved-element gốc):

  | # | Cột | Ý nghĩa |
  |---|---|---|
  | 1 | tname | scaffold chào mào |
  | 2 | tstart | start 0-based |
  | 3 | tend | end (nửa mở) |
  | 4 | qname | ID phần tử gốc (`chrom:start-end` trên gà, từ cột 4 `elements.bed`) |
  | 5 | identity×1000 | 0–1000 (quy ước điểm BED), làm tròn |
  | 6 | strand | `+`/`-` |
  | 7 | qlen | độ dài query (gà) |
  | 8 | coverage | 0–1, 4 chữ số thập phân |
  | 9 | mapq | mapping quality từ minimap2 |

- `--unmapped` (TSV có header `qname\treason\tdetail`): `reason` ∈ {`no_hit`, `low_identity`, `low_coverage`}; `detail` ghi giá trị đo được (vd `identity=0.6000`) hoặc rỗng cho `no_hit`.
- `--stats`: tổng query, mapped/mapped_pct, unmapped, `second_hit_queries` (số query có ≥2 dòng PAF — chỉ dấu có hit phụ dù `--secondary=no`), bảng `qlen_bin\tcount` (histogram độ dài query, cùng 5 bin như merge) tính trên **mọi query có ≥1 hit** (kể cả bị loại), phân bố identity (6 bin: `lt_0.70`, `0.70_0.80`, `0.80_0.90`, `0.90_0.95`, `0.95_1.00`, `eq_1.00`) cũng trên tập đó, và bảng `qlen_bin\tmapped\ttotal\tmapped_pct` — % **mapped/total mỗi bin độ dài**, trong đó `total` là **toàn bộ query trong bin** kể cả `no_hit` (độ dài suy từ `--query-list`, vd cột 2/3 của `elements.bed`; nếu không truyền `--query-list` thì query không có hit không xác định được bin nên không tính vào `total`). Bảng này trả lời trực tiếp câu hỏi "phần tử ngắn bao nhiêu % map được" — khác bảng `qlen_bin\tcount` ở trên chỉ đếm số query có PAF hit, không phải tỉ lệ map thành công.

### 3. `annotate` — gán feature_class + gene cho từng vùng

```
python -B conserved_to_bulbul.py annotate \
  --bed bulbul_core.bed --gff genomic.gff.gz --out core_annot.tsv --stats annot_stats.tsv
```

- Đọc GFF3 `.gz` một lần, lấy feature `gene`, **`pseudogene`** (xử lý giống `gene` — xem dưới), `mRNA`, `exon`, `CDS`. `mRNA` chỉ dùng để nối `Parent` → gene: với mỗi bản ghi `exon`/`CDS`, gene được suy ra từ chính `Parent`/`ID` của bản ghi đó (`CDS.Parent → mRNA.ID`, `mRNA.Parent → gene.ID`) — **không** suy theo vị trí không gian, để tránh gán nhầm sang gene hàng xóm khi 2 gene chồng tọa độ (thường gặp ở gene 2 mạch đối nhau).
- **`pseudogene`** được nạp vào cùng chỉ mục với `gene` (GFF chào mào có 1.653 bản ghi `pseudogene`, mỗi bản ghi có `mRNA` con dạng `pseudo=true` rồi `exon`/`CDS` con — xác nhận trực tiếp trên dữ liệu dự án, xem `research/synthesis/05-review-code-x1.md` Finding #1). Vùng BED rơi trong thân `pseudogene` nhưng ngoài mọi exon của nó → `intron` (trước bản vá này bị báo sai thành `intergenic`). `gene_name` lấy attribute `Name`, nếu không có thì `gene`, nếu vẫn không có thì fallback về chính `ID` — áp dụng như nhau cho `gene` lẫn `pseudogene`.
- Với mỗi vùng BED, thứ tự ưu tiên: giao **CDS** → `CDS`; else giao **exon** (không giao CDS) → `exon_noncoding`; else giao **gene/pseudogene** (không giao exon nào, kể cả gene không có exon nào trong GFF) → `intron`; else → `intergenic`. Gene name/ID lấy từ CDS/exon cụ thể bị giao (nếu class là CDS/exon_noncoding) hoặc từ gene/pseudogene giao nhiều nhất theo bp (nếu class là intron — khi 2 gene chồng tọa độ trên cùng scaffold, xem test `test_annotate_overlapping_genes_same_scaffold_picks_larger_overlap`).
- Index theo scaffold (142.341 scaffold trong assembly chào mào): mỗi scaffold có 1 `IntervalIndex` riêng (mảng start đã sắp + mảng end + mảng "max-end lũy tích"), tra bằng `bisect` + dừng sớm khi max-end lũy tích ≤ điểm bắt đầu vùng cần tra — **không** có vòng lặp O(n×m) toàn cục.
- `--out`: giữ nguyên toàn bộ cột đầu vào (thường là 9 cột từ `paf2bed`), nối thêm 3 cột `feature_class`, `gene_id`, `gene_name` (rỗng nếu `intergenic`).
- `--stats`: bảng `feature_class\tregions\tbp` cho 4 lớp; bảng `gene_id\tgene_name\tbp` top 50 gene theo tổng bp các vùng được gán cho gene đó (tính **toàn bộ chiều dài vùng BED**, không cắt theo phần giao thực tế — xem Giới hạn).

## `run_a2.sh`

```
bash pipeline/p02_core_map/run_a2.sh [--chrom chr1] [--force] [--threads N] \
  [--chunk-bases 180000000] [--mm-extra "-k 13 -w 5 -s 30 -m 20 -n 2"] [--clean-chunks] \
  [--min-identity 0.70] [--min-coverage 0.80] \
  [--gap 10] [--min-len 20] [--data-dir D:\...\data]
```

- Chạy theo thứ tự: `bigBedToBed | merge` (một pipe — xem dưới) → `twoBitToFa -bed=elements.bed` → `split_fasta.py` (chia bộ gene chào mào thành mảnh) → `minimap2` theo từng mảnh (nối PAF) → `paf2bed` → `annotate`. Output ghi vào `data/a2/`.
- **Không còn dùng `minimap2 -I <size>` làm mặc định.** Bản đầu chạy `minimap2` 1 lần trên toàn bộ genome chào mào với `-I` để chia lô index (VM Docker ~2 GB RAM) nhưng vẫn **OOM (exit 137)** ngay cả với `-I 200M`/4 thread khi xây lô index thứ 2 (xem docs/04 mục 9). Mặc định mới: `split_fasta.py` chia trước file FASTA genome chào mào thành mảnh ≤ `--chunk-bases` (mặc định 180.000.000 bp), mỗi mảnh index nguyên khối rồi map riêng, nối PAF lại — 6 mảnh chạy hết 38 giây, RAM đỉnh ~74% của 1,86 GiB, không OOM (docs/04 mục 10). `paf2bed` không đổi: vẫn chọn 1 hit tốt nhất/query dựa trên `best[qname]`, tự động đúng dù PAF nối từ nhiều mảnh.
- `--chunk-bases N`: kích thước mảnh tối đa cho `split_fasta.py`. Bỏ qua bước chia mảnh nếu thư mục `data/a2/genome_chunks` đã có mảnh **với cùng `--chunk-bases`** (so khớp qua file `.params` — xem dưới); đổi `--chunk-bases` (hoặc `--force`) thì chia lại.
- `--mm-extra "CHUỖI"`: tham số seed minimap2 (`-k`/`-w`/`-s`/-`m`/`-n`) chèn sau `-x asm20`, áp dụng cho mọi mảnh. Mặc định `"-k 13 -w 5 -s 30 -m 20 -n 2"` — kết quả tốt nhất trong thí nghiệm 15.000 phần tử của docs/04 mục 10 (84,3% mapped ở bin 200–499bp, so với 6,5% của `asm20` mặc định `-k19 -w10 -s200`). `-t`/`--secondary=no`/`-c`/`-x asm20` giữ cố định, không cấu hình qua `--mm-extra`.
- `--clean-chunks`: xoá `data/a2/genome_chunks` ngay sau khi map xong toàn bộ mảnh (tiết kiệm đĩa — mỗi mảnh FASTA có thể vài trăm MB); lần chạy sau sẽ phải chia mảnh lại từ đầu.
- **`MSYS_NO_PATHCONV=1` đặt ngay trước mỗi lệnh `docker run`** (biến môi trường chỉ áp cho đúng lệnh đó), tránh Git Bash tự "sửa" đường dẫn kiểu `/data` bên trong container. Vế trái của `-v` được đổi sang đường dẫn Windows thật (`cygpath -w`) vì `MSYS_NO_PATHCONV=1` tắt luôn việc tự quy đổi đường dẫn. `split_fasta.py` chạy bằng Python thuần trên host (đọc trực tiếp file `.fna.gz` qua đường dẫn Windows), **không** qua Docker.
- **`bigBedToBed` và `merge` chạy trong 1 pipe duy nhất** (`docker run ... bigBedToBed ... stdout | python ... merge --in - ...`) đúng yêu cầu "không ghi BED 1,4 GB trung gian". Vì hai lệnh chạy đồng thời trong 1 pipe, log ghi chung 1 cặp START/END tên `bigbedtobed_merge` thay vì tách riêng — quyết định có chủ đích, ghi rõ ở đây để không hiểu nhầm là thiếu bước.
- Mỗi bước ghi `START`/`END`/`SKIP` kèm mốc giờ vào `data/a2/run.log`; mỗi mảnh minimap2 log riêng dòng `CHUNK <tên> START/END` kèm thời gian chạy (giây) và tổng số dòng PAF gộp tới lúc đó.
- **`step_needed` giờ so khớp cả tham số, không chỉ sự tồn tại của output** (REQUIRED_FIX #5 trong `research/synthesis/05-review-code-x1.md`): mỗi output chính có 1 file `<output>.params` cạnh nó ghi lại chuỗi tham số đã dùng (vd `gap=10 min_len=20 chrom=ALL` cho `elements.bed`, `min_identity=0.70 min_coverage=0.80` cho `bulbul_core.bed`, `chunk_bases=... mm_extra=... threads=...` cho `elements.paf`). Bước chỉ SKIP khi **output đã có VÀ tham số lần này khớp file `.params`**; đổi bất kỳ tham số nào (mà quên `--force`) sẽ tự động chạy lại đúng bước đó — không còn âm thầm dùng lại output cũ theo ngưỡng cũ như trước.
- `--chrom chr1`: chèn `awk -F'\t' '$1=="chr1"'` ngay trên pipe, giữa `bigBedToBed` và `merge` — lọc trước khi gộp, không tạo `all.bed`. Dùng để benchmark thời gian trên 1 NST trước khi chạy toàn genome (P1.3 trong docs/04).
- `-t` mặc định = số CPU − 2 (fallback 12 nếu không đọc được `nproc`); ghi đè bằng `--threads`.
- `--force` chạy lại toàn bộ (bỏ qua cả kiểm tra output lẫn tham số, kể cả bước chia mảnh).
- `-h`/`--help` in hướng dẫn rồi thoát ngay, **không** chạm Docker.

## Giới hạn (đọc trước khi diễn giải kết quả)

- **Neo trên gà (galGal4)**: toàn bộ vùng bảo tồn xuất phát từ `conserved.bb` neo trên hệ tọa độ gà. Phần bộ gene chào mào không có đối chiếu trên gà (hoặc phân kỳ quá cao so với gà) sẽ không bao giờ xuất hiện trong `bulbul_core.bed` — đây là giới hạn cấu trúc của lối A2 (xem docs/04 mục 3, 8), không phải lỗi script.
- **Phần tử rất ngắn (<100bp) vẫn khó căn dù đã đổi tham số seed**: thí nghiệm 15.000 phần tử (docs/04 mục 10) với mặc định mới `-k 13 -w 5 -s 30 -m 20 -n 2` đạt 8,7% (bin 50–99bp) và 46,6% (bin 100–199bp) mapped — hơn hẳn `asm20` mặc định (0%/0%) nhưng vẫn thấp; ≈80% số phần tử sau `merge` (≈41% tổng bp) ngắn hơn 100bp và cần công cụ khác (vd LAST theo mảnh) hoặc chấp nhận `unmapped`. Luôn đọc bảng `qlen_bin\tmapped\ttotal\tmapped_pct` trong `map_stats.tsv` để biết tỉ lệ mapped thật theo từng khoảng độ dài trước khi dùng `bulbul_core.bed` làm kết luận.
- **`no_hit` cần `--query-list`**: nếu chạy `paf2bed` không kèm `--query-list`, thống kê `unmapped` chỉ phản ánh `low_identity`/`low_coverage`, KHÔNG có `no_hit` (vì PAF không ghi dòng nào cho query không align được nên script không có cách nào biết những query đó từng tồn tại); bảng `mapped_pct theo qlen_bin` khi đó cũng chỉ tính `total` trên các query có ≥1 hit (không suy được độ dài của query hoàn toàn không có hit).
- **Gán gene cho intron xấp xỉ theo bp giao lớn nhất**: khi 2 gene (hoặc pseudogene) chồng tọa độ (khác mạch) và vùng bảo tồn rơi vào phần chồng lấn nhưng không nằm trong exon nào, `annotate` gán gene có phần giao (bp) lớn hơn — có thể không phải gene "đúng" về mặt sinh học nếu annotation không rõ ràng. Đã có test khoá hành vi này (`test_annotate_overlapping_genes_same_scaffold_picks_larger_overlap`).
- **bp gán cho gene tính theo toàn bộ chiều dài vùng BED**, không cắt theo phần thực sự nằm trong ranh giới gene (trường hợp vùng bảo tồn vắt qua biên gene). Ảnh hưởng nhỏ vì phần tử sau `merge` thường ngắn (~vài chục–vài trăm bp).
- `Parent` nhiều giá trị (phân tách bởi dấu phẩy, hiếm gặp — vd exon dùng chung giữa nhiều isoform) chỉ lấy giá trị đầu tiên làm đại diện.
- Script không tự kiểm tra `docker`/`minimap2` có cài đúng phiên bản hay không — `run_a2.sh` chỉ gọi đúng tag image đã pull sẵn (ghi trong `research/briefs/X1-codex-conserved-to-bulbul.md`); nếu tag sai/thiếu, `docker run` sẽ báo lỗi ở đúng bước đó trong `run.log`.

## Test

```
python -B -m unittest discover -s pipeline/p02_core_map/tests -v
```

18 test (unittest thuần, dữ liệu nhúng ngay trong `tests/test_conserved_to_bulbul.py`, không đọc/ghi ngoài thư mục tạm của test): `merge` (gộp theo gap/min-len đúng số liệu tay tính, đọc từ stdin, báo lỗi khi thứ tự sai/chrom lặp lại/thiếu cột, input rỗng), `paf2bed` (chọn hit tốt nhất qua mapq→matches→alnlen kèm test tie-break riêng cho tầng `nmatch` và tầng `alnlen`, 2 lý do loại + `no_hit` qua `--query-list`, fallback khi không có `--query-list`, báo lỗi cột PAF thiếu), `annotate` (CDS/exon_noncoding/intron/intergenic trên nhiều scaffold, gene không có exon nào vẫn ra `intron` đúng, 2 gene chồng tọa độ cùng scaffold chọn đúng gene giao lớn hơn, thân `pseudogene` ngoài exon ra `intron` + `gene_name` lấy `Name`/fallback ID, thống kê bp/gene), và `--help` (top-level + cả 3 lệnh con thoát mã 0).
