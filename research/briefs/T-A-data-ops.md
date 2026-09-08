# T-A — data-ops: hoàn tất tải dữ liệu lõi, kiểm hash, ghi registry

Repo: `D:\BIRDBIODNA project`. Chỉ được ghi vào `data/` và thêm dòng vào `data/registry.csv`, `tasks/primordial-dna-handoff.md`. Không đụng file khác. Chủ dự án yêu cầu **canh RAM/đĩa**: không tải gì ngoài danh sách dưới; chạy `bash pipeline/p00_inventory/check_resources.sh` trước và sau.

## File phải hoàn tất (kích thước đích từ HTTP HEAD)
| File cục bộ | URL | Byte đích |
|---|---|---|
| `data/ucsc/ancRep_separate_models_rev.bw.conserved.bb` | `https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020-hub/Gallus_gallus/ancRep_separate_models_rev.bw.conserved.bb` | 345031105 |
| `data/ucsc/ancRep_separate_models_rev.bw.accelerated.bb` | `https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020-hub/Gallus_gallus/ancRep_separate_models_rev.bw.accelerated.bb` | 329399456 |
| `data/ncbi/GCA_013400435.1/GCA_013400435.1_ASM1340043v1_genomic.fna.gz` | `https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/013/400/435/GCA_013400435.1_ASM1340043v1/GCA_013400435.1_ASM1340043v1_genomic.fna.gz` | 324574462 |

## Quy trình (Git Bash)
1. **Một tiến trình curl khác của Main có thể đang tải tiếp các file này.** Trước khi làm gì: chạy `tasklist //FI "IMAGENAME eq curl.exe"`; nếu còn `curl.exe` → đợi bằng vòng lặp `until ! tasklist //FI "IMAGENAME eq curl.exe" | grep -q curl.exe; do sleep 30; done` (tối đa 15 phút). Tuyệt đối không chạy hai curl cùng ghi một file.
2. Với mỗi file chưa đủ byte: `curl -sS -L -C - --retry 5 --retry-delay 5 --max-time 590 -o <file> <url>`; lặp tối đa 6 lượt tới khi đủ byte. Ghi log từng lượt vào `data/download.log` (thời gian, file, byte trước/sau).
3. Khi đủ byte: `cd data/ncbi/GCA_013400435.1 && md5sum -c md5checksums.txt` — dòng `genomic.fna.gz` phải `OK`. Với 2 file `.bb`: kiểm đầu file là bigBed (4 byte đầu `87 89 f2 eb` hoặc `eb f2 89 87` qua `head -c 4 | od -An -tx1`).
4. Tính sha256 cho: 2 file `.bb`, `genomic.fna.gz`, `genomic.gff.gz`, `protein.faa.gz`, `cds_from_genomic.fna.gz`, `data/ucsc/Gallus_gallus.2bit` (đã đủ 265935614 byte). Ghi `data/SHA256SUMS.txt` (định dạng `sha256sum`).
5. Thêm vào `data/registry.csv` (cột: dataset_id,name,source_url,version_or_release,downloaded_on,local_path,size_bytes,sha256,license,notes) mỗi file một dòng, `downloaded_on=2026-09-07`; với dòng đã có cùng file (ví dụ D01-fna ghi "(chưa tải)") thì **thêm dòng mới** có hậu tố `-done`, không sửa dòng cũ.
6. Thêm 1 dòng vào bảng `tasks/primordial-dna-handoff.md`: `| root/data-ops | SESSION | primordial-dna-p1 | Done/Risks | … |`.

## Trả về Main ≤10 dòng
Mỗi file: byte cuối / byte đích / md5 hoặc magic / sha256 8 ký tự đầu · số lượt resume · kết quả check_resources (D: trống, data/ GB) · DONE/BLOCKED.
