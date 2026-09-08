# TODO — BIRDBIODNA "DNA gốc của chim"

## Pha 0 — Điểm bắt đầu (phiên 2026-09-07)
- [x] Đọc V4 (skill v0.4.0), tracker 27 chủ đề, ranh giới bằng chứng
- [x] Tái định khung 6 câu hỏi → docs/00 (sổ giả thuyết H1/H2/H3)
- [x] Khung xương project (README, CLAUDE.md, docs 01–02, data/, pipeline/, env/)
- [x] Brief R1–R6 trong research/briefs
- [x] Chạy R1–R5 (Sonnet) + R6a/R6b (ACPX Gemini) → research/raw (xong 14:17, validator PASS 7/7)
- [x] R7 nguồn gốc chào mào + chiều đột biến màu (Sonnet) — xong 14:25, validator PASS 42 dòng
- [x] docs/03-suy-luan-nguon-goc-chao-mao.md — bản suy luận (Main viết 14:30, cần REVIEW): gốc từ đâu · có tiến hóa không · tiến hóa về gì · giả thuyết 'DNA được cải tiến bởi một nền văn minh' xử lý như H3
- [x] Tổng hợp vòng 1 → research/synthesis/00-tong-hop-vong-1.md (S1 Opus, 14:45; Main đã đọc hết — điều chỉnh: CORRECTION #10 én đá là bổ sung cơ chế, không phải sai)
- [x] REVIEW fresh-context V1 (Opus): NEEDS_FIX 0 BLOCKER/5 HIGH/11 MEDIUM/9 LOW → research/synthesis/01-review-vong-1.md
- [x] Vòng sửa duy nhất: S2 sửa tổng hợp 15/15 F · C1 áp 17 CORRECTIONS docs/00 + docs/02 · Main sửa docs/03 (F04,F05,F12–F16,F24,F25)
- [x] PROVE: validator 9/9 PASS · RECHECK 1,3 PASS · handoff 11 dòng · Perplexity Pro 78→66
- [x] VERDICT vòng 1: PASS_WITH_ACCEPTED_RISK (U1 HAL, U5 benchmark, D06 outgroup thiếu, mọi claim gene chào mào = U/S ngoại suy)

## Pha 1 — Môi trường & kiểm kê dữ liệu (chi tiết 7 việc P1.1–P1.7: research/synthesis/00-tong-hop-vong-1.md mục 9; P1.4 và P1.5 chạy song song, là GATE của Pha 2)
- [ ] WSL2 + conda env từ env/environment.yml; kiểm `python -c "import Bio"`
- [ ] Xác minh D01 (assembly Pycnonotus) — tải, BUSCO, ghi registry
- [ ] Xác minh D02/D03 (B10K alignment + track bảo tồn) — tải phần cần, ghi registry
- [ ] Quyết định: dùng track sẵn hay tự align (ghi ADR trong docs/)

## Pha 2 — Bản đồ LÕI bất biến
- [ ] Trích vùng bảo tồn ≥ ngưỡng trên ≥90% loài + ngoài nhóm → BED
- [ ] Giao với bộ gene chào mào; thống kê % genome, phân bố theo NST/vi NST
- [ ] Giao với ASHCE (D08) và UCE (D07)

## Pha 3 — Tái dựng tổ tiên (ASR) cho locus chọn
- [ ] Tập locus: gene màu lông V4 (T22) + gene hành vi Q2b
- [ ] MAFFT/PRANK → IQ-TREE2 -asr tại 3 nút (Neornithes, Passeriformes, Pycnonotidae)
- [ ] Báo cáo: vị trí khác biệt tổ tiên ↔ chào mào hiện đại

## Pha 4 — Quét chọn lọc (Q1b)
- [ ] dN/dS (codeml/HyPhy) nhóm toolkit vs nhóm hành vi vs nhóm sắc tố
- [ ] Kiểm định thống kê khác biệt giữa nhóm

## Pha 5 — Nối V4
- [ ] Đầu vào cho tracker T06 (khả thi nhánh gene) và T22 (registry gene ứng viên có nguồn/loài/mức bằng chứng)
- [ ] Không nâng ngôn ngữ bằng chứng; mọi claim gene ≤ G-level dữ liệu cho phép

## Pha 6 — Công bố & sổ giả thuyết
- [ ] Bảng H1/H2/H3 với kết quả đo thực tế cho từng dự đoán
- [ ] Bài tổng hợp tiếng Việt cho cộng đồng + bản kỹ thuật
