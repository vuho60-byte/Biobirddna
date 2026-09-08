# pipeline/ — 6 module dự kiến (CHƯA viết code: chưa có dữ liệu, chưa có môi trường)

Nguyên tắc: code cho transform/validation deterministic; model chỉ dùng cho phán đoán. Mỗi module = một thư mục, một `run.py`, một `README.md`, input/output ghi rõ, kết quả có sha256.

| Module | Vào | Ra | Công cụ | Trả lời |
|---|---|---|---|---|
| p00_inventory | docs/02 registry | data/registry.csv đã điền, kiểm sha | NCBI datasets CLI, curl | Có gì để dùng |
| p01_fetch | registry | assembly + alignment/track cục bộ | datasets, halTools | — |
| p02_core_map | alignment/track + genome chào mào | BED vùng LÕI, thống kê % genome, giao UCE/ASHCE | pyranges, bedtools | Q3a, Q6(a)(b) |
| p03_asr | tập locus + cây | trình tự tổ tiên tại 3 nút + bảng khác biệt | MAFFT, IQ-TREE2 -asr | Q6(c), Q4 |
| p04_selection | orthologue CDS theo nhóm gene | ω (dN/dS) theo nhóm + kiểm định | codeml/HyPhy | Q1b, Q2b |
| p05_link_v4 | kết quả p02–p04 | JSON registry gene ứng viên (nguồn, loài, mức bằng chứng) cho tracker T22; báo cáo khả thi T06 | python | Nối V4 |

Chạy trong WSL2 với env/environment.yml. Windows chỉ giữ docs và điều phối.
