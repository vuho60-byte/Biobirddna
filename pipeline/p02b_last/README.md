# p02b_last — lối X4: LAST cho phần tử bảo tồn ngắn (<100 bp)

Bối cảnh đầy đủ: `research/briefs/X4-last-short-elements.md`. Đọc `pipeline/p02_core_map/README.md`
(lối A2) trước — module này **nối tiếp** A2, không thay thế: A2 (minimap2) map được phần lớn
phần tử ≥100bp; module này bắt lại phần <100bp mà minimap2 gần như bỏ sót (0,3% ở bin 20–49bp,
7,8% ở bin 50–99bp — số đo thật trên dữ liệu dự án, xem `docs/04` mục 10b), rồi gộp 2 kết quả.

Ba file:
- `short_elements.py` — Python 3.11, **chỉ dùng stdlib**, 3 lệnh con `filter` / `maf2bed` / `merge-beds`.
- `run_last.sh` — wrapper Git Bash gọi docker (LAST), resume theo output + tham số (giống `run_a2.sh`).
- `tests/test_short_elements.py` — unittest thuần, dữ liệu nhúng trong file.

**Trạng thái**: `run_last.sh` và `short_elements.py` **chưa được chạy trên dữ liệu thật** (brief
cấm chạy docker/LAST thật ở bước tạo script này). Đã kiểm: `bash -n run_last.sh` sạch, unittest
sạch, `--help` mọi lệnh con (kể cả `run_last.sh --help`) thoát mã 0 không đụng Docker. Trước khi
dùng cho kết quả thật, chạy thử `--help` từng lệnh rồi chạy `run_last.sh` trên 1 mảnh nhỏ để xác
nhận cú pháp `lastdb`/`lastal`/`last-split` đúng với image `last:1654--h5814d7d_1`.

## Luồng dữ liệu

```
data/a2/elements.fa + data/a2/elements.bed   (dau ra buoc twoBitToFa cua A2)
  │  filter --in-fa elements.fa --in-bed elements.bed --out short.fa
  │          --max-len 99 [--min-len 20] --stats filter_stats.tsv
  ▼
short.fa   (chi con phan tu 20-99bp)
  │  split_fasta.py --in bulbul.fna.gz --out-dir genome_chunks_last_<N> --max-bases <N>
  │  (tai dung tu p02_core_map; N mac dinh 90.000.000 - xem "Bo nho" duoi)
  ▼
[moi manh] docker: lastdb -P <T> -uNEAR  chunk_NN.fa
           docker: lastal -P <T> -D1e6  short.fa  |  docker: last-split   >> aln.maf
  │  (noi MAF cua moi manh; -uNEAR/-D1e6 co dinh, them tham so qua --lastdb-extra/--lastal-extra)
  ▼
maf2bed --maf aln.maf --out bulbul_short.bed --unmapped unmapped_short.txt
        --stats map_stats_short.tsv --min-identity 0.70 --min-coverage 0.80
        --query-list elements.bed
  │  (1 hit tot nhat/query TINH QUA CA CAC MANH; BED 6+ cung dinh dang cot voi paf2bed cua A2)
  ▼
bulbul_short.bed
  │  merge-beds --in data/a2/bulbul_core.bed --in bulbul_short.bed
  │             --out bulbul_core_all.bed --stats merge_beds_stats.tsv
  ▼
bulbul_core_all.bed  =  toan bo vung bao ton (ca da can bang minimap2 lan LAST) tren toa do chao mao
```

## Lệnh con

### 1. `filter` — lọc phần tử ngắn ra FASTA riêng

```
python -B short_elements.py filter \
  --in-fa elements.fa --in-bed elements.bed --out short.fa \
  --max-len 99 [--min-len 20] --stats filter_stats.tsv
```

- Độ dài lấy từ `--in-bed` (cột 3 − cột 2), **không** đếm ký tự trong FASTA — tránh sai lệch nếu
  FASTA có định dạng xuống dòng khác thường. Mỗi `id` trong `--in-fa` (token đầu dòng header, sau
  `>`) phải có mặt trong `--in-bed`, nếu không script dừng với lỗi rõ ràng.
- Giữ phần tử có độ dài trong `[--min-len, --max-len]` (2 đầu đều được tính), ghi lại **nguyên
  văn** các dòng trình tự gốc (kể cả khi 1 record trải nhiều dòng) — không đổi cách xuống dòng.
- `--stats`: `total_in_bed`, `total_in_fasta`, `kept`, `excluded_too_long`, `excluded_too_short`,
  `bp_kept`, rồi bảng `length_bin\tcount` (5 bin như `conserved_to_bulbul.py`, tính trên **mọi**
  phần tử đọc được từ FASTA, không chỉ phần được giữ).

### 2. `maf2bed` — chọn hit tốt nhất mỗi query, đổi MAF (LAST) → BED

```
python -B short_elements.py maf2bed \
  --maf aln.maf --out bulbul_short.bed --unmapped unmapped_short.txt \
  --stats map_stats_short.tsv --min-identity 0.70 --min-coverage 0.80 \
  [--query-list elements.bed]
```

- Đọc MAF theo khối (`a score=...` rồi đúng 2 dòng `s`: dòng 1 = **target** — sinh ra từ `lastdb`
  trên mảnh bộ gene chào mào; dòng 2 = **query** — sinh ra từ `short.fa`, phần tử gốc trên tọa độ
  gà). Đây là quy ước cố định của LAST khi chạy `lastal <db-từ-lastdb> <query.fa>` (db luôn đứng
  dòng đầu).
- Khối lỗi (thiếu `score=`, không đúng 2 dòng `s` hợp lệ, hoặc 2 chuỗi align khác độ dài) bị **bỏ
  qua và đếm riêng** (`bad_block_reason` trong `--stats`), không làm dừng chương trình — MAF là
  đầu ra công cụ ngoài, một file hàng chục GB có thể có khối lẻ tẻ ở cuối.
- Với mỗi `qname` (tên query), giữ **1 hit tốt nhất**: ưu tiên `score` LAST thô → số base khớp →
  độ dài align (số cột của khối, tính cả gap).
- `identity = base khớp / độ dài align`; `coverage = độ dài query được gán trong khối (không tính
  gap phía query) / độ dài gốc query`.
- Tọa độ target đổi về mạch `+` của chrom/scaffold đích (BED luôn ở mạch `+`); mạch tương đối ghi
  ở cột `strand` = `+` nếu target và query cùng mạch MAF, `-` nếu khác.
- Cột đầu ra **CÙNG ĐỊNH DẠNG** với `conserved_to_bulbul.py paf2bed` để `merge-beds` ghép được:

  | # | Cột | Ý nghĩa |
  |---|---|---|
  | 1 | tname | scaffold chào mào |
  | 2 | tstart | start 0-based (đã đổi về mạch `+`) |
  | 3 | tend | end (nửa mở) |
  | 4 | qname | ID phần tử gốc (`chrom:start-end` trên gà) |
  | 5 | identity×1000 | 0–1000, làm tròn |
  | 6 | strand | `+`/`-` (mạch tương đối target/query) |
  | 7 | qlen | độ dài gốc query |
  | 8 | coverage | 0–1, 4 chữ số thập phân |
  | 9 | **điểm LAST thô** (làm tròn) | **KHÔNG phải mapq** — LAST không có khái niệm mapq; giữ vị trí cột 9 chỉ để `merge-beds` ghép 2 nguồn, không so sánh trực tiếp được với cột 9 của `bulbul_core.bed` (thang điểm khác nhau) |

- `--query-list elements.bed` (dùng **toàn bộ** elements.bed, không chỉ phần ngắn — `run_last.sh`
  luôn truyền vậy): phát hiện `no_hit`, và cấp `total` cho bảng `mapped_pct` theo `qlen_bin`. Hệ
  quả: các bin ≥100bp sẽ luôn hiện `mapped=0` (những phần tử đó chưa từng được đưa vào LAST ở lối
  này — đã/đang được xử lý bởi A2) — **đây là điều đã lường trước, không phải lỗi**; đọc kèm
  `filter_stats.tsv` để biết bao nhiêu phần tử thật sự nằm trong phạm vi bin 20–99bp.
- `--stats`: `blocks_total`/`blocks_bad` + bảng `bad_block_reason`, rồi các bảng giống hệt
  `map_stats.tsv` của A2 (`qlen_bin\tcount`, `identity_bin`, `qlen_bin\tmapped\ttotal\tmapped_pct`).

### 3. `merge-beds` — gộp BED 6+, loại trùng theo id query

```
python -B short_elements.py merge-beds \
  --in bulbul_core.bed --in bulbul_short.bed \
  --out bulbul_core_all.bed --stats merge_beds_stats.tsv
```

- `--in` lặp lại được (≥1 file), mỗi file BED ≥6 cột cùng định dạng paf2bed/maf2bed (cột 4 = id
  query, cột 5 = identity×1000). Id trùng (cùng file hoặc khác file) → giữ dòng **score cao hơn**
  (bằng điểm thì giữ dòng gặp trước, để kết quả ổn định giữa các lần chạy).
- `--stats`: `inputs`, `total_rows_in`, `unique_ids_out`, `duplicate_ids`, bảng `source\trows`.

## `run_last.sh`

```
bash pipeline/p02b_last/run_last.sh [--force] [--threads N] \
  [--chunk-bases 90000000] [--max-len 99] \
  [--lastdb-extra "..."] [--lastal-extra "..."] [--data-dir D:\...\data]
```

- Thứ tự: `filter` → chia mảnh bộ gene chào mào riêng cho LAST (`split_fasta.py`, tái dùng từ
  `p02_core_map`) → mỗi mảnh `lastdb -uNEAR` rồi `lastal -D1e6 | last-split` (nối MAF) → `maf2bed`
  → `merge-beds` với `data/a2/bulbul_core.bed` (yêu cầu A2 đã chạy xong `paf2bed`). Output ghi vào
  `data/a2_last/`.
- **Bộ nhớ**: `lastdb -uNEAR` cho 1 mảnh 90 Mbp (mặc định) có thể vượt 2 GB RAM và bị container
  giết (`exit 137`) trên VM Docker ~2 GB. Gặp lỗi này: chạy lại với `--chunk-bases 45000000`.
- **Khác `run_a2.sh` ở 1 điểm có chủ đích**: bước chia mảnh **không xóa** thư mục mảnh cũ trước
  khi chia lại (`run_a2.sh` dùng `rm -rf` cho việc này). Dự án cấm tuyệt đối lệnh xóa trong script
  (xem `CLAUDE.md` + `tasks/RESTORE_LOG-2026-09-08.txt` — sự cố xóa nhầm 2026-09-08). Thay vào đó,
  thư mục mảnh được đặt tên kèm `--chunk-bases` (`genome_chunks_last_<N>`), nên đổi `--chunk-bases`
  tự chuyển sang thư mục mới (rỗng) thay vì để lẫn mảnh cũ khác số lượng — không còn nguy cơ mảnh
  "mồ côi". Đánh đổi: đổi `--chunk-bases` nhiều lần sẽ giữ lại nhiều thư mục mảnh trên đĩa (không
  tự dọn); dọn tay nếu cần tiết kiệm chỗ.
  `--force` chỉ điều khiển việc CHẠY LẠI bước (bỏ qua kiểm tra output+tham số), không xóa gì.
- Áp dụng đúng cơ chế `.params` có danh tính input (`input_id`) như `run_a2.sh`: 5 bước
  (`filter`, `split_genome_last`, `last_chunks`, `maf2bed`, `merge_beds`) đều SKIP khi output đã có
  **và** tham số lần này khớp file `.params` cạnh nó; đổi tham số (quên `--force`) sẽ tự chạy lại
  đúng bước đó.
- `MSYS_NO_PATHCONV=1` đặt ngay trước mỗi `docker run` (như `run_a2.sh`); `lastal | last-split`
  chạy trên **2 container riêng nối qua pipe ở host** (`last-split` đọc MAF từ stdin, không nhận
  đường dẫn file) — container nhận stdin cần `-i`.
- `--lastdb-extra`/`--lastal-extra`: chuỗi tham số chèn thêm sau `-uNEAR`/`-D1e6` cố định, áp dụng
  cho mọi mảnh (giống `--mm-extra` của `run_a2.sh`).
- `-h`/`--help` in hướng dẫn rồi thoát ngay, **không** chạm Docker.

## Giới hạn (đọc trước khi diễn giải kết quả)

- **LAST chậm hơn minimap2 nhiều lần** trên cùng khối lượng dữ liệu — đây là lý do chỉ áp dụng
  cho tập đã lọc riêng (<100bp, thường chỉ vài phần trăm tổng bp so với toàn bộ `elements.fa`),
  không dùng LAST cho toàn bộ `elements.fa` như A2 dùng minimap2.
- **Phần tử 20–49bp vẫn có thể mơ hồ dù dùng LAST**: với trình tự cực ngắn, khả năng khớp ngẫu
  nhiên tăng lên; ngưỡng `--min-identity`/`--min-coverage` mặc định (0.70/0.80, giống A2) giảm
  nhưng không loại bỏ hoàn toàn rủi ro này — luôn đọc bảng `qlen_bin\tmapped\ttotal\tmapped_pct`
  trong `map_stats_short.tsv` trước khi dùng `bulbul_short.bed`/`bulbul_core_all.bed` làm kết luận.
- **`--query-list` dùng `elements.bed` đầy đủ** (không lọc riêng phần ngắn) theo đúng brief X4 —
  xem hệ quả (`mapped=0` cho bin ≥100bp) ở mục `maf2bed` phía trên.
- **Cột 9 của `bulbul_short.bed` không cùng thang đo với cột 9 của `bulbul_core.bed`** (điểm LAST
  thô so với mapq minimap2) — chỉ dùng để `merge-beds` hoạt động (giữ đúng số cột), không dùng để
  so sánh "độ tin cậy" giữa 2 nguồn map. Muốn so sánh chất lượng, dùng cột 5 (identity×1000, cùng
  công thức cho cả 2 nguồn) hoặc cột 8 (coverage).
- **Chưa chạy trên dữ liệu thật** (xem "Trạng thái" ở đầu file) — cú pháp `lastdb -P -uNEAR`,
  `lastal -P -D1e6`, `last-split` lấy nguyên văn từ `research/briefs/X4-last-short-elements.md`,
  chưa được xác minh bằng cách chạy thật trên image `last:1654--h5814d7d_1`.
- Script không tự kiểm tra `docker`/`last*` cài đúng phiên bản; nếu tag sai/thiếu, `docker run` sẽ
  báo lỗi ở đúng bước đó trong `run.log`.

## Test

```
python -B -m unittest discover -s pipeline/p02b_last/tests -v
```

14 test (unittest thuần, dữ liệu nhúng trong `tests/test_short_elements.py`): `filter` (lọc đúng
khoảng độ dài + giữ nguyên FASTA nhiều dòng, báo lỗi khi id FASTA thiếu trong BED), `maf2bed`
(chọn hit tốt nhất qua score→matches→alnlen kèm 2 test tie-break riêng tầng `matches`/`alnlen`, 2
lý do loại + `no_hit` qua `--query-list`, đổi tọa độ mạch `-` của target + tính mạch tương đối, 3
kiểu khối MAF hỏng (thiếu dòng `s`, thiếu `score=`, 2 chuỗi align khác độ dài) bị bỏ qua không
crash và được đếm đúng lý do trong `bad_block_reason`, trường số không hợp lệ trong dòng `s` cũng
bị bỏ qua tương tự chứ không dừng chương trình), `merge-beds` (loại trùng giữ score cao hơn, báo
lỗi khi thiếu cột), và `--help` (top-level + cả 3 lệnh con thoát mã 0).
