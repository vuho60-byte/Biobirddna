# 02 — Cập nhật thăm dò dữ liệu trực tiếp (Main, 2026-09-07, sau vòng 1)

Ghi đè các điểm sau của `00-tong-hop-vong-1.md` (không sửa file đó để giữ audit):

| Điểm trong tổng hợp | Kết quả thăm dò HEAD/GET | Hệ quả |
|---|---|---|
| Mục 4 D03: HAL tại `alignment-output.s3.amazonaws.com/birds-final.hal`, "hàng trăm GB, không tải riêng loài" | Link S3 → 404. HAL thật: `https://cgl.gi.ucsc.edu/data/cactus/363-avian-2020.hal`, 417.276.452.293 byte, `Accept-Ranges: bytes` | U1 đóng: đọc từ xa theo vùng được; không cần tải cả file |
| Mục 7 #2 / U (mới): chào mào có trong 363 genome không | Hub có thư mục `Pycnonotus_jocosus/` (2bit, genes.bb, chrom.sizes 142.341 scaffold / 1,035 Gb) | Đóng theo hướng CÓ (quan sát trực tiếp) |
| Mục 4 D03: phyloP ✔ nhưng chưa rõ file | `Gallus_gallus/ancRep_separate_models_rev.bw` (3,86 GB) + `.conserved.bb` (345 MB) + `.accelerated.bb` (329 MB); còn 53-way, 77-way | Sản phẩm A (LÕI-363) lấy trực tiếp từ `.conserved.bb` |
| Mục 9 P1.4/P1.5 (cắt HAL hoặc đường vòng orthologue) | `Gallus_gallus/chicken.bigMaf.bb` 195,9 GB, range OK: alignment 363 loài dạng MAF neo galGal4, có hàng *Pycnonotus_jocosus* | Lối A trong `docs/04`: liftover gà→chào mào bằng bigMaf từ xa, không cần HAL |
| Mục 10 điều kiện 1 (dữ liệu cứng) | Thỏa bằng lối A; lối B (tải HAL) là dự phòng | T06 vẫn "khả thi có điều kiện", điều kiện 1 đã hạ mức |
| Máy tính (U5) | WSL2 chỉ docker-desktop; Docker 29.7.2, 16 CPU, VM cấp ~2 GB RAM; RAM máy 15 GB; D: trống 483 GB | Chạy tool qua Docker; BUSCO cần nâng RAM Docker ≥8 GB |

Bằng chứng: `data/probe-2026-09-07.tsv` (script `pipeline/p00_inventory/probe_remote.sh`), `docs/02` mục D, `data/registry.csv`.
Chưa tải file dữ liệu nào; chờ duyệt theo `docs/04` mục 6.
