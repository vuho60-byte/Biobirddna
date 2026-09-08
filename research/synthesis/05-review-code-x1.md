# 05 — Review độc lập: X1 (conserved_to_bulbul.py + run_a2.sh)

Reviewer: root/review-x1 (độc lập, không thấy quá trình viết code của root/code-x1).
Phạm vi: `research/briefs/X1-codex-conserved-to-bulbul.md` (spec) đối chiếu
`pipeline/p02_core_map/{conserved_to_bulbul.py,run_a2.sh,README.md,tests/test_conserved_to_bulbul.py}`.
Không sửa code, không chạy docker/minimap2 thật, không sửa file nào ngoài file review này +
1 dòng `tasks/primordial-dna-handoff.md`.

## STATUS: NEEDS_FIX

Không có BLOCKER/HIGH. Có 1 lỗi phân loại MEDIUM đã xác nhận bằng dữ liệu GFF thật
(annotate bỏ sót feature `pseudogene`) + 2 chỗ test yếu (không khóa được đúng phần logic
tinh vi nhất của spec) + 2 ghi chú LOW về vận hành `run_a2.sh`. Cấu trúc streaming, các cột
output, và thuật toán bisect/prefix-max-end đều ĐÚNG (đã tự viết property-test đối chiếu
brute-force, xem mục Bằng chứng bên dưới) — không có gì phải viết lại từ đầu, chỉ cần vá 1
nhánh + bổ sung test.

## Tóm tắt kiểm theo 6 tiêu chí (a)-(f)

| # | Tiêu chí | Kết quả |
|---|---|---|
| a | Đúng lệnh con + cột output theo spec | PASS. `merge`/`paf2bed`/`annotate` đúng tên cờ, đúng số cột, đúng công thức identity/coverage. `paf2bed` thêm `--query-list` (không có trong lệnh gốc của brief) — đã surface rõ trong `--help` + README, cần thiết để phát hiện `no_hit`; không tính là vi phạm. |
| b | `merge` streaming + biên (gap/min-len/chrom đổi/thứ tự) | PASS. 1 dòng = O(1) trạng thái, không tích luỹ mảng lớn. Test tay đã đối chiếu số học (bp_in/bp_out/elements_out) khớp 100%. Báo lỗi đúng cho: start giảm, chrom quay lại, thiếu cột. |
| c | `paf2bed` chọn hit tốt nhất, identity/coverage, unmapped reason, nhiều lô `-I` | PASS. Cột PAF map đúng theo vị trí 0-based (`fields[9]`=nmatch cột10, `fields[10]`=alnlen cột11, `fields[11]`=mapq cột12). `docs/04-ke-hoach-tach-adn-goc.md` mục 9 xác nhận: chạy `minimap2 -I 400M` do RAM Docker ~2GB, và **"chọn hit tốt nhất qua các lô do paf2bed đảm nhiệm"** — đúng bằng cơ chế `best[qname]` hiện có (không giả định ≤1 dòng PAF/query). |
| d | `annotate`: GFF gz, Parent-chain, intron/intergenic, bisect theo scaffold, không O(n·m) | PASS_WITH_1_MEDIUM. Parent-chain CDS/exon→mRNA→gene đúng. Bisect + prefix-max-end đúng thuật toán (xem Bằng chứng). Nhưng bỏ sót feature type `pseudogene` — xem Finding #1. |
| e | `run_a2.sh`: MSYS_NO_PATHCONV, tag image, `-I` cấu hình được, `--chrom` benchmark, skip, không xoá gì thừa, mount Windows | PASS_WITH_2_LOW. `MSYS_NO_PATHCONV=1` đặt đúng trước cả 3 lệnh `docker run`; tag image khớp nguyên văn brief; `-I` qua `--minimap-index-size`; `--chrom` lọc đúng trên pipe trước `merge`, không tạo `all.bed`; script không xoá file nào. 2 ghi chú LOW: đường dẫn có khoảng trắng chưa kiểm chứng thực tế (cấm chạy docker), và skip theo tồn tại file chứ không theo tham số. |
| f | Test yếu? | NEEDS_FIX. 15/15 test unittest PASS (xem bằng chứng chạy lại), nhưng bộ test không phủ 2 nhánh logic tinh vi nhất: (1) tie-break 3 tầng mapq→nmatch→alnlen của `paf2bed` chỉ test tầng đầu; (2) `IntervalIndex.best_overlap` (bisect/prefix-max-end) chưa từng được test với 2 khoảng chồng lấn trên cùng scaffold — đúng kịch bản mà chính README liệt vào "Giới hạn". Xem Finding #2, #3. |

## Bằng chứng đã tự chạy (không đụng docker/minimap2)

1. **Unit test gốc** — `python -B -m unittest discover -s pipeline/p02_core_map/tests -v`
   → **15/15 PASS, 0 lỗi** (Python 3.14.3 tại máy review; brief yêu cầu 3.11 nhưng code chỉ
   dùng stdlib ổn định — argparse/bisect/gzip/collections/urllib.parse/contextlib — nên rủi ro
   khác biệt 3.11↔3.14 là thấp, chưa kiểm trực tiếp trên 3.11).
2. `--help` cấp cao nhất + `merge --help` + `paf2bed --help` + `annotate --help` + `run_a2.sh --help`
   → cả 5 đều thoát mã 0, `run_a2.sh --help` xác nhận không đụng Docker.
3. Đọc trực tiếp `data/ncbi/GCA_013400435.1/GCA_013400435.1_ASM1340043v1_genomic.gff.gz` (đã có
   sẵn trên máy, không tải mạng) để đếm feature type thật: `exon 119299, CDS 119299, region 60582,
   mRNA 15553, gene 13900, pseudogene 1653`. Xác nhận 1653 bản ghi `pseudogene` đều có `mRNA` con
   (`pseudo=true`) và `mRNA` đó có `exon`/`CDS` con — dùng để xác nhận Finding #1 là thật trên
   chính bộ dữ liệu của dự án, không phải suy đoán lý thuyết.
4. Viết script ad-hoc (không sửa file dự án) import `IntervalIndex` từ `conserved_to_bulbul.py`,
   chạy 2000 truy vấn ngẫu nhiên trên 2000 khoảng chồng lấn, đối chiếu `best_overlap()` với hàm
   brute-force O(n). Kết quả: **độ dài giao lớn nhất luôn khớp 100% (0 lỗi thật)**; các lần
   "khác nhau" ban đầu chỉ là hòa điểm (nhiều khoảng cùng đạt độ dài giao lớn nhất) — thuật toán
   bisect/prefix-max-end xác nhận ĐÚNG, nhưng chính vì việc này cần viết test riêng để xác minh
   mới thấy an tâm, nên bộ test hiện có (chỉ test gene rời rạc, khác scaffold) là thiếu — Finding #2.

## Bảng finding

| # | Mức | file:dòng | Vấn đề | Sửa thế nào |
|---|---|---|---|---|
| 1 | MEDIUM | `pipeline/p02_core_map/conserved_to_bulbul.py:559-565,578-581` | `_load_gff` chỉ nạp `gene_raw`/`gene_name_by_id` khi `ftype == "gene"`. GFF chào mào thật có 1653 bản ghi `ftype=pseudogene` (đều có `mRNA` con dạng `pseudo=true` rồi `exon`/`CDS` con — đã xác nhận trực tiếp, xem Bằng chứng #3). Hệ quả: (a) vùng bảo tồn rơi trong thân pseudogene nhưng ngoài mọi exon của nó bị phân loại `intergenic` thay vì `intron` vì pseudogene không có trong `gene_index`; (b) `gene_name` cho các hit CDS/exon thuộc pseudogene hiển thị ID thô `gene-PYCJOC_Rxxxxx` thay vì tên sạch, vì `gene_name_by_id` không có key này. Brief chỉ ghi literal "feature gene" nên đây là điểm mù của spec chứ không hẳn code sai lệnh, nhưng README "Giới hạn" hiện không nhắc gì tới pseudogene — nên bị bỏ sót âm thầm. | Thêm `ftype in ("gene", "pseudogene")` vào nhánh nạp `gene_raw`/`gene_name_by_id` (dòng 559), hoặc lọc theo `gene_biotype=pseudogene` trong attrs; nếu cố ý bỏ qua thì phải ghi rõ trong README mục Giới hạn kèm số liệu (1653 bản ghi) để người đọc `annot_stats.tsv` không hiểu nhầm `intergenic`. |
| 2 | MEDIUM | `pipeline/p02_core_map/tests/test_conserved_to_bulbul.py:267-332` | `TestAnnotate` chỉ có gene rời rạc, mỗi gene 1 scaffold riêng (scafA/scafB) — không có ca 2 gene chồng tọa độ trên CÙNG 1 scaffold. Đây chính xác là kịch bản mà `IntervalIndex.best_overlap` (bisect + "prefix-max-end" dừng sớm, `conserved_to_bulbul.py:442-482`) được thiết kế để xử lý, và README tự liệt vào "Giới hạn" ("khi 2 gene chồng tọa độ (khác mạch)..."). Tôi đã tự kiểm bằng property-test ngẫu nhiên và xác nhận thuật toán hiện tại ĐÚNG (xem Bằng chứng #4), nhưng bộ test của X1 không tự chứng minh được điều đó — nếu sau này có người sửa nhầm điều kiện dừng sớm `prefix_max_end[i] <= q_start` thành lỗi, 15/15 test hiện tại vẫn PASS. | Thêm 1 test: 2 gene chồng tọa độ trên cùng scaffold (khác mạch), 1 vùng BED rơi đúng phần chồng lấn nhưng ngoài mọi exon — assert `feature_class == "intron"` và `gene_id` đúng là gene có bp giao lớn hơn. |
| 3 | LOW-MEDIUM | `pipeline/p02_core_map/tests/test_conserved_to_bulbul.py:152-227` | `test_best_hit_threshold_and_no_hit` chỉ test tầng ưu tiên đầu tiên của rank (`mapq` 60 vs 10, hit còn lại dù `nmatch`/`alnlen` cao hơn vẫn thua) — không có ca `mapq` bằng nhau nhưng `nmatch` khác nhau, cũng không có ca `mapq`+`nmatch` bằng nhau nhưng `alnlen` khác nhau. Brief yêu cầu đúng thứ tự 3 tầng "mapq → matches (cột 10) → alnlen (cột 11)" (`conserved_to_bulbul.py:343`: `rank_key = (mapq, nmatch, alnlen)`) nhưng chỉ 1/3 tầng được khóa bằng test. | Thêm PAF: 2 dòng cùng `qname`, `mapq` bằng nhau, `nmatch` khác nhau → assert chọn `nmatch` lớn hơn; thêm 2 dòng `mapq`+`nmatch` bằng nhau, `alnlen` khác nhau → assert chọn `alnlen` lớn hơn. |
| 4 | LOW | `pipeline/p02_core_map/run_a2.sh:103-114` | `win_path()`/`cygpath -w` + `-v "${WIN_DATA_DIR}:/data"` là kỹ thuật đúng chuẩn cho Git Bash + Docker, nhưng đường dẫn thật của dự án có khoảng trắng (`D:\BIRDBIODNA project`) và việc mount này CHƯA được xác minh chạy thật (nhiệm vụ cấm chạy docker). Thiết kế trông đúng (1 đối số duy nhất, có trích dẫn kép) nhưng là suy luận, chưa phải bằng chứng trực tiếp. | Trước khi chạy toàn genome, chủ dự án tự chạy thử `run_a2.sh --chrom <NST rất nhỏ>` 1 lần để xác nhận mount hoạt động đúng với khoảng trắng trong đường dẫn; không cần sửa code nếu chạy thử ổn. |
| 5 | LOW | `pipeline/p02_core_map/run_a2.sh:92-101` | `step_needed()` chỉ kiểm sự tồn tại của file output, không ghi lại tham số (`--min-identity`, `--min-coverage`, `--gap`, `--min-len`) đã dùng ở lần chạy trước. Đổi ngưỡng mà quên `--force` sẽ âm thầm tái sử dụng output cũ theo ngưỡng cũ. Đã ghi trong README nhưng là hành vi dễ gây nhầm khi vận hành thật, không phải lỗi logic. | Khuyến nghị (không bắt buộc): ghi 1 file marker nhỏ mỗi bước (vd JSON tham số) để `step_needed` so khớp cả tham số, hoặc tối thiểu log rõ tham số dùng trong `run.log` mỗi khi SKIP để người vận hành tự phát hiện lệch. |

## REQUIRED_FIX

1. **[MEDIUM, bắt buộc]** Thêm `pseudogene` (hoặc lọc theo `gene_biotype`) vào nạp gene trong
   `_load_gff` (Finding #1) — hoặc nếu giữ nguyên hành vi, ghi rõ số liệu 1653 bản ghi vào README
   mục Giới hạn để không ai hiểu nhầm `intergenic` là tuyệt đối chính xác.
2. **[MEDIUM, bắt buộc]** Thêm test 2 gene chồng tọa độ cùng scaffold cho `annotate` (Finding #2).
3. **[LOW-MEDIUM, khuyến nghị mạnh]** Thêm test tie-break `nmatch`/`alnlen` cho `paf2bed`
   (Finding #3).
4. **[LOW, khuyến nghị]** Chạy thử `run_a2.sh --chrom <NST nhỏ>` 1 lần trước khi chạy toàn genome
   để xác nhận mount Windows có khoảng trắng hoạt động đúng (Finding #4) — việc này KHÔNG do
   reviewer thực hiện (nhiệm vụ cấm chạy docker thật).
5. **[LOW, tuỳ chọn]** Cân nhắc ghi tham số vào marker file cho `step_needed` (Finding #5).

Không cần viết lại kiến trúc: luồng streaming, format cột PAF/BED, và thuật toán bisect đều đúng.
