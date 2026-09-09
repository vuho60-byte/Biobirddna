# p04_anomaly — lối X6: quét bất thường thành phần trong bộ CDS chào mào

Bối cảnh đầy đủ: `research/briefs/X6-quet-bat-thuong-thanh-phan.md`. Tham khảo phong cách CLI và
cách xử lý theo luồng từ `pipeline/p02_core_map/conserved_to_bulbul.py` (không import module đó —
mỗi lối trong `pipeline/` tự chứa, đúng quy ước hiện có của dự án).

## Câu hỏi khoa học và logic phép thử

Chủ dự án đặt giả thuyết: bộ gene chim có thể chứa đoạn không thuộc dòng dõi Trái Đất. Đây là
**phép thử thật** cho giả thuyết đó, và nó cũng chính là phương pháp chuẩn ngành để tìm **chuyển
gene ngang** (horizontal gene transfer, HGT): một đoạn DNA đến từ nguồn khác thường mang **chữ ký
thành phần** khác với phần còn lại của bộ gene chủ (thiên lệch GC, thiên lệch dùng codon, phổ
k-mer riêng của mỗi dòng dõi).

- Nếu **không** tìm thấy đoạn nào lệch chuẩn → đó là bằng chứng chống lại giả thuyết "có đoạn
  ngoại lai", và **vẫn là kết quả có giá trị** (không phải thất bại của phép đo).
- Nếu **có** đoạn lệch chuẩn → xem mục "Thứ tự khả năng giải thích" dưới đây trước khi kết luận
  bất cứ điều gì.

## Ba lệnh con (`composition_scan.py`, Python 3.11, chỉ dùng stdlib)

```
python -B composition_scan.py profile  --fasta cds_from_genomic.fna.gz --out profile.tsv --min-len 300
python -B composition_scan.py outliers --profile profile.tsv --out outliers.tsv --stats outlier_stats.tsv --z 4.0
python -B composition_scan.py report   --outliers outliers.tsv --top 50 --out report.md
```

Dữ liệu vào thật của dự án: `data/ncbi/GCA_013400435.1/GCA_013400435.1_ASM1340043v1_cds_from_genomic.fna.gz`
(xem `data/registry.csv`). Chưa chạy script này trên dữ liệu thật trong phiên tạo code — brief X6 chỉ
giao viết code + test (dữ liệu nhúng), không giao chạy trên bộ dữ liệu 7,7 MB nén thật.

### 1. `profile` — đo thành phần từng trình tự CDS

Đọc CDS FASTA(.gz) **theo luồng**: chỉ giữ 1 record (danh sách dòng trình tự của record đó) trong
bộ nhớ tại 1 thời điểm, không nạp cả tệp. `seq_id` = token đầu tiên sau `>` (ví dụ
`lcl|VWYP01000003.1_cds_NXR70914.1_1`); `gene` lấy từ thuộc tính `[gene=...]` trong dòng header
kiểu NCBI (`[gene=Efcc1] [locus_tag=..] [protein=..]`) — để trống nếu header không có `[gene=]`.

Bỏ qua trình tự ngắn hơn `--min-len` (mặc định 300bp). Với mỗi trình tự còn lại, ghi 1 dòng
`profile.tsv` gồm:

| Cột | Ý nghĩa |
|---|---|
| `seq_id`, `gene` | định danh trình tự và tên gene (có thể rỗng) |
| `len` | độ dài thật (số ký tự trình tự, kể cả N nếu có) |
| `gc` | phần base G/C trên tổng base A/C/G/T hợp lệ (không tính N/ký tự mơ hồ khác vào tử số lẫn mẫu số) |
| `gc3` | phần codon có G/C ở vị trí thứ 3, trên tổng **codon đọc được từ khung dịch vị trí 0** (không bù lệch khung cho CDS `partial=5'` — xem Giới hạn) |
| `cod_AAA` … `cod_TTT` (64 cột) | tần số từng codon trong 64 codon, chuẩn hoá tổng = 1 trên tập codon hợp lệ (cả 3 ký tự đều A/C/G/T) của trình tự đó |
| `k4_AAAA` … `k4_TTTT` (256 cột) | tần số từng 4-mer (cửa sổ trượt chồng lấn, bước 1) trên toàn trình tự, chuẩn hoá tổng = 1 trên tập 4-mer hợp lệ |

Codon/4-mer chứa ký tự khác A/C/G/T (N, IUPAC mơ hồ…) bị loại **hoàn toàn** khỏi tử số lẫn mẫu số
của chính đơn vị đó (không làm sai lệch các đơn vị còn lại). Trình tự suy biến (mẫu số = 0, ví dụ
toàn N) trả tần số 0.0 cho toàn bộ chiều — trường hợp hiếm, không crash.

### 2. `outliers` — z-score GC/GC3 + Mahalanobis xấp xỉ (codon) + Jensen-Shannon (4-mer)

Đọc `profile.tsv` **2 lượt** (không giữ toàn bộ 320 cột đầu vào của mọi trình tự trong bộ nhớ cùng
lúc — chỉ lượt 1 tích luỹ tổng/tổng-bình-phương theo từng chiều, lượt 2 đọc lại để tính khoảng
cách/z-score và chỉ giữ kết quả rút gọn 9 cột/trình tự):

- Lượt 1: trung bình + độ lệch chuẩn **toàn cục** (population, chia cho N) cho `gc`, `gc3`, và
  từng chiều trong 64 chiều tần số codon; hồ sơ nền 4-mer = **trung bình không trọng số** của vector
  tần số 4-mer mọi trình tự (mỗi trình tự đóng góp như nhau, không theo độ dài).
- Lượt 2, với từng trình tự:
  - `z_gc = (gc - mean_gc) / std_gc`, `z_gc3` tương tự.
  - `codon_dist` = khoảng cách Mahalanobis **xấp xỉ**: `sqrt(Σ (x_i - mean_i)² / var_i)` trên 64
    chiều tần số codon, dùng **phương sai từng chiều** (đường chéo ma trận hiệp phương sai), **không
    dùng ma trận hiệp phương sai đầy đủ** (bỏ qua tương quan giữa các codon) — đây là **xấp xỉ**,
    không phải Mahalanobis chuẩn. Chiều có phương sai = 0 (không biến thiên trong nền) đóng góp 0.
  - `kmer_js` = phân kỳ Jensen-Shannon (log cơ số 2, đơn vị bit, tự cài bằng `math.log`, không dùng
    numpy/scipy) giữa vector tần số 4-mer của trình tự và hồ sơ nền — nằm trong [0, 1].

**Quy ước đánh dấu bất thường** (giả định rõ ràng của script — brief không nói rõ cách quy đổi
`codon_dist`/`kmer_js` về "đơn vị z"; so sánh thô 2 giá trị này với `--z` sẽ khiến `kmer_js` — bị
chặn trong [0,1] — không bao giờ vượt được ngưỡng mặc định 4.0):

- **GC/GC3** (1 thước đo): lệch **2 phía** đều đáng ngờ (quá cao lẫn quá thấp là thành phần lạ) →
  cờ bật khi `|z_gc| >= --z` HOẶC `|z_gc3| >= --z`.
- **codon** (1 thước đo): `codon_dist` là khoảng cách không âm, chỉ hướng "cao hơn = khác nền hơn"
  mới đáng chú ý → script tự tính z-score **của chính giá trị `codon_dist`** trên toàn bộ quần thể
  trình tự đang xét, rồi dùng **1 phía**: cờ bật khi z-score đó `>= --z`.
- **4-mer** (1 thước đo): tương tự, tự tính z-score của `kmer_js` trên toàn quần thể, cờ bật khi
  z-score đó `>= --z`.
- Đánh dấu bất thường (`n_flags` được tính) khi **>= 2 trong 3** thước đo trên có cờ bật.

Xuất `outliers.tsv`: `seq_id gene len gc gc3 z_gc z_gc3 codon_dist kmer_js n_flags`, sắp theo
`n_flags` giảm dần rồi `kmer_js` giảm dần. Xuất `--stats`: `mean_gc/std_gc/mean_gc3/std_gc3/
mean_codon_dist/std_codon_dist/mean_kmer_js/std_kmer_js`, `n_sequences`, số trình tự theo từng mức
`n_flags` (0–3), và phân vị 50/90/99 (nội suy tuyến tính, tự cài) của `z_gc`, `z_gc3`, `codon_dist`,
`kmer_js`.

`--profile` phải là **đường dẫn file thật** (không nhận `-`/stdin) vì lệnh đọc 2 lượt.

### 3. `report` — báo cáo Markdown top N + cảnh báo bắt buộc

Đọc `outliers.tsv`, **tự sắp xếp lại** theo đúng quy ước (`n_flags` giảm dần rồi `kmer_js` giảm dần
— không âm thầm tin tưởng thứ tự có sẵn trong file), xuất bảng Markdown top `--top` trình tự (mặc
định 50) kèm cột trống `giai_thich_kha_di` để người điền, và **luôn luôn** in phần cảnh báo bắt
buộc (xem ngay dưới) — không có cách nào tắt phần này.

## Thứ tự khả năng giải thích (BẮT BUỘC — in trong `report.md` và nhắc lại ở đây)

Mọi kết quả của 3 lệnh trên là **tín hiệu cần kiểm tiếp**, không phải kết luận. Một trình tự bị
đánh dấu CHƯA chứng minh nó đến từ ngoài Trái Đất hay không thuộc dòng dõi tổ tiên — chỉ có nghĩa
thành phần của nó khác hồ sơ nền hơn ngưỡng thống kê đã chọn. Phải kiểm theo **đúng thứ tự sau**,
chỉ chuyển sang mục tiếp theo sau khi đã loại được mục trước:

1. **Lỗi lắp ráp hoặc nhiễm bẩn mẫu** (assembly error / sample contamination) — khả năng **phổ biến
   nhất** cho 1 outlier đơn lẻ trong 1 bản lắp ráp mức độ scaffold (N50 thấp).
2. **Vùng lặp / transposon** (repeat region / transposable element) — các yếu tố lặp thường tự
   mang thành phần/phổ k-mer khác hẳn gene mã hoá bình thường.
3. **HGT (chuyển gene ngang) từ vi khuẩn, virus, hoặc sinh vật cộng sinh** — đây là hiện tượng **đã
   được ghi nhận** ở nhiều loài (không phải giả thuyết mới lạ), và là khả năng xếp cuối trong 3 khả
   năng "thông thường".
4. Chỉ khi đã loại hết (1)–(3) mới bàn tới khả năng khác. Không có bước nào trong công cụ này tự
   động loại được bất kỳ mục nào ở trên — người đọc phải tự kiểm.

**Bước kiểm bắt buộc tiếp theo (chưa làm trong dự án này):** so sánh từng trình tự bị đánh dấu với
cơ sở dữ liệu protein toàn cầu bằng BLAST hoặc DIAMOND (ví dụ so với nr/UniProt).

## Giới hạn phương pháp

- **Chỉ phát hiện được đoạn khác xa về thành phần VÀ chưa bị "đồng hoá" theo thời gian.** Một đoạn
  HGT/ngoại lai đã nằm trong bộ gene chủ đủ lâu sẽ dần trôi giạt thành phần (amelioration) về gần
  với nền của bộ gene chủ do áp lực đột biến/sửa chữa cục bộ — khi đó chữ ký thành phần mất đi và
  phương pháp này **không** phát hiện được, dù nguồn gốc ngoại lai vẫn đúng về mặt tiến hoá.
- **Mahalanobis là xấp xỉ đường chéo**: dùng phương sai từng chiều của 64 tần số codon, bỏ qua
  tương quan giữa các codon (ví dụ áp lực GC3 làm nhiều codon cùng lệch theo 1 hướng) — có thể đánh
  giá thấp hoặc thổi phồng khoảng cách thật tuỳ cấu trúc tương quan thật của bộ CDS.
- **Quần thể nền bao gồm cả ứng viên bất thường**: `outliers` không loại trình tự nghi ngờ ra khỏi
  tập tính trung bình/độ lệch chuẩn trước khi tính z-score (không dùng thống kê bền/robust như MAD
  hay cắt đuôi lặp) — nếu có **rất nhiều** outlier cùng hướng, độ lệch chuẩn sẽ bị thổi phồng và độ
  nhạy giảm.
- **Không bù lệch khung đọc cho CDS một phần**: header NCBI có thể ghi `[partial=5',3']` (CDS bị
  cắt ở đầu 5'/3' so với gene thật); `profile` luôn đọc codon từ vị trí 0 của chuỗi trong FASTA,
  không kiểm tra/bù lệch khung theo `[partial=...]` — có thể làm nhiễu nhẹ `gc3`/tần số codon của
  các bản ghi `partial=5'`. Không ảnh hưởng `gc` hay 4-mer (cả hai đo trên toàn trình tự, không
  phụ thuộc khung dịch).
- **`kmer_js` là phân kỳ Jensen-Shannon** (Jensen-Shannon **divergence**, không phải căn bậc 2 của
  nó — một số tài liệu gọi căn bậc 2 là "khoảng cách Jensen-Shannon"). Cả hai đại lượng đều thoả 3
  tính chất được kiểm trong test (bằng 0 khi giống hệt, đối xứng, nằm trong [0,1] với log cơ số 2);
  script báo cáo **phân kỳ** (không lấy căn), ghi rõ ở đây để tránh nhầm đơn vị khi so sánh với tài
  liệu khác.
- **`--stats` của `outliers` chưa từng chạy trên dữ liệu thật** (chỉ chạy trên dữ liệu nhúng trong
  `tests/test_composition_scan.py`) — số cột/số dòng theo cấu trúc đã tả ở trên, nhưng thời gian
  chạy trên toàn bộ CDS chào mào (hàng chục nghìn trình tự) chưa được đo.
- Công cụ này **không** tự nó đối chiếu với bất kỳ cơ sở dữ liệu protein/nucleotide bên ngoài nào —
  xem mục "Bước kiểm bắt buộc tiếp theo" ở trên.

## Test

`tests/test_composition_scan.py` — unittest thuần, dữ liệu nhúng ngay trong file (không đọc/ghi
ngoài thư mục tạm của test). Chạy:

```
python -B -m unittest discover -s pipeline/p04_anomaly/tests -v
```

Bao phủ: GC/GC3 tính đúng trên trình tự đã biết đáp án (kể cả có base N xen giữa); lọc đúng
`--min-len`; đọc được FASTA.gz; lấy đúng `[gene=...]`; nền không bị đánh dấu trong khi trình tự lệch
mạnh (GC~100% dùng bộ 4 codon giàu GC riêng biệt, xen giữa 12 trình tự nền GC~45–53% dùng nhiều
codon khác nhau) bị đánh dấu đủ 3/3 cờ ở `--z 2.0`; đổi `--z` đổi đúng chiều số lượng bất thường
(thực đo: z=2.0 bắt được 1, z=5.0 bắt được 0 trên cùng bộ dữ liệu); phân kỳ Jensen-Shannon bằng 0
khi giống hệt, đối xứng, đạt đúng giá trị max=1.0 ở trường hợp 2 phân phối rời rạc hoàn toàn, và
trong [0,1] ở trường hợp chồng lấn một phần; phân vị tuyến tính; Mahalanobis xấp xỉ bỏ qua đúng
chiều phương sai 0; báo cáo Markdown in đủ cảnh báo bắt buộc + đúng thứ tự khả năng giải thích +
nhắc BLAST/DIAMOND + cột `giai_thich_kha_di`; `--help` mọi lệnh (kể cả top-level) thoát mã 0.
