# X6 — Quét bất thường thành phần: tìm đoạn DNA "lạ" trong bộ gene chào mào

Chỉ tạo/sửa trong `pipeline/p04_anomaly/**`. **Không có lệnh xóa nào.** Python 3.11 **stdlib**. Không chạy docker.

## Câu hỏi khoa học
Chủ dự án đặt giả thuyết: bộ gene chim có thể chứa đoạn không thuộc dòng dõi Trái Đất. Đây là **phép thử thật** cho giả thuyết đó, và nó cũng chính là phương pháp chuẩn ngành để tìm **chuyển gene ngang** (horizontal gene transfer, HGT): một đoạn DNA đến từ nguồn khác thường mang **chữ ký thành phần** khác với phần còn lại của bộ gene chủ, vì mỗi dòng dõi có thiên lệch GC, thiên lệch dùng codon và phổ k-mer riêng.

Logic của phép thử:
- Nếu **không** tìm thấy đoạn nào lệch chuẩn → đó là bằng chứng chống lại giả thuyết "có đoạn ngoại lai", và là kết quả có giá trị.
- Nếu **có** đoạn lệch chuẩn → phải kiểm tiếp theo thứ tự khả năng: (1) lỗi lắp ráp hoặc nhiễm bẩn mẫu, (2) vùng lặp/transposon, (3) HGT từ vi khuẩn, virus, hoặc sinh vật cộng sinh — đây là hiện tượng **đã được ghi nhận** ở nhiều loài, (4) chỉ khi loại hết mới bàn tới khả năng khác. Viết rõ thứ tự này trong README.

## Dữ liệu có sẵn
- `data/ncbi/GCA_013400435.1/..._cds_from_genomic.fna.gz` — CDS chào mào (7,7 MB nén).
- `data/ncbi/GCA_013400435.1/..._genomic.fna.gz` — bộ gene (325 MB nén).
- `data/a2/bulbul_core.bed` — vùng lõi bảo tồn.

## Việc — `pipeline/p04_anomaly/composition_scan.py`, ba lệnh con

1. `profile --fasta <cds.fna.gz> --out profile.tsv [--min-len 300]`
   Với mỗi trình tự: chiều dài, GC%, GC ở vị trí codon thứ 3 (GC3), tần suất 64 codon, tần suất 4-mer chuẩn hóa. Bỏ trình tự ngắn hơn `--min-len`. Chạy theo luồng, không nạp cả tệp.

2. `outliers --profile profile.tsv --out outliers.tsv --stats outlier_stats.tsv [--z 4.0]`
   - Tính trung bình và độ lệch chuẩn toàn bộ gene cho GC, GC3.
   - Với mỗi trình tự tính **khoảng cách Mahalanobis xấp xỉ** trên vector tần suất codon (dùng phương sai từng chiều, không cần ma trận hiệp phương sai đầy đủ — nêu rõ đây là xấp xỉ), và **phân kỳ tần suất 4-mer** so với hồ sơ toàn bộ gene (dùng khoảng cách Jensen–Shannon, tự cài bằng `math.log`).
   - Đánh dấu bất thường khi vượt ngưỡng `--z` ở **ít nhất hai** trong ba thước đo (GC/GC3, codon, 4-mer). Yêu cầu hai thước đo để giảm dương tính giả.
   - Xuất TSV: `seq_id gene len gc gc3 z_gc z_gc3 codon_dist kmer_js n_flags`, sắp theo `n_flags` rồi `kmer_js` giảm dần.
   - `--stats`: trung bình/độ lệch chuẩn toàn cục, số trình tự xét, số bất thường theo từng mức cờ, và phân vị 50/90/99 của từng thước đo.

3. `report --outliers outliers.tsv --top 50 --out report.md`
   Bảng 50 trình tự lệch nhất, kèm cột `giai_thich_kha_di` để trống cho người điền, và **phần cảnh báo bắt buộc** in ra trong báo cáo: mọi kết quả ở đây là *tín hiệu cần kiểm tiếp*, không phải kết luận; thứ tự khả năng giải thích như mục trên; và bước kiểm bắt buộc tiếp theo là so trình tự đó với cơ sở dữ liệu protein toàn cầu (BLAST/DIAMOND, chưa làm trong dự án).

## Test (`pipeline/p04_anomaly/tests/test_composition_scan.py`, unittest, dữ liệu nhúng)
- `profile`: GC và GC3 tính đúng trên trình tự nhân tạo đã biết đáp án; bỏ đúng trình tự ngắn.
- `outliers`: trình tự có thành phần giống nền → không bị đánh dấu; trình tự nhân tạo lệch mạnh (ví dụ GC 80% giữa nền 45%, dùng bộ codon rất khác) → bị đánh dấu ≥2 cờ.
- Khoảng cách Jensen–Shannon: bằng 0 với hai phân phối giống nhau; dương và đối xứng với hai phân phối khác nhau; nằm trong [0, 1] khi dùng log cơ số 2.
- Ngưỡng `--z` thay đổi làm đổi số lượng bất thường theo đúng chiều.

## Tiêu chí xong
- `python -B -m unittest discover -s pipeline/p04_anomaly/tests -v` sạch; `--help` mỗi lệnh con thoát 0.
- `pipeline/p04_anomaly/README.md`: cách chạy, ý nghĩa cột, **thứ tự khả năng giải thích**, và ghi rõ giới hạn: phương pháp thành phần chỉ phát hiện được đoạn có nguồn gốc *khác xa* về thành phần và *chưa bị đồng hóa* theo thời gian; đoạn đã nằm lâu trong bộ gene sẽ mất chữ ký.
- Thêm đúng 1 dòng `tasks/primordial-dna-handoff.md`.

## Trả về ≤10 dòng
file tạo · dòng tổng kết unittest · xác nhận không lệnh xóa · giả định/giới hạn.
