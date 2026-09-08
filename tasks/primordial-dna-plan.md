# PLAN — primordial-dna vòng 1 (2026-09-07)

GOAL:
  Có một điểm bắt đầu khoa học: sổ giả thuyết, khung project, registry dữ liệu/công cụ đã được xác minh sơ bộ bởi 6 nhánh tìm kiếm, và bản tổng hợp chỉ ra Pha 1 làm gì.

ACCEPTANCE_CRITERIA:
  - docs/00 ánh xạ đủ 6 câu hỏi → câu hỏi kiểm chứng + code tính được.
  - research/raw có 6 file R1–R6, mỗi claim mang nhãn bằng chứng, có search log; ≥1 nguồn cho mỗi dataset chính D01–D08.
  - research/synthesis/00-tong-hop-vong-1.md: trả lời ngắn từng Q1–Q6, bảng dataset ✔/✘, danh sách UNVERIFIED cần vòng 2, quyết định Pha 1.
  - Không claim nào vượt nhãn bằng chứng; Perplexity Pro dùng ≤20 lượt.

BLOCKING_QUESTIONS: (không có — chủ dự án đã chỉ định: plan + khung + subagent tìm trước)

ASSUMPTIONS: xem tasks/primordial-dna-think.md

TASKS:
  T1 Khung xương + docs (Main) — DONE trong phiên này.
  T2 R1 Bộ gene chim ổn định, tổ tiên, vùng bảo tồn (Q3, Q6) — Sonnet subagent.
  T3 R2 Tiến hóa quan sát được + catalog đột biến chim cảnh có gene (Q3, T22) — Sonnet subagent.
  T4 R3 Hành vi bẩm sinh & cá tính & canalization (Q1, Q2) — Sonnet subagent.
  T5 R4 Nguồn gốc, hóa thạch, aDNA, sổ giả thuyết H1/H2/H3, tuyệt chủng (Q4, Q5) — Sonnet subagent.
  T6 R5 Bộ gene chào mào/Pycnonotidae + khả thi pipeline trên WSL2 (T06) — Sonnet subagent.
  T7 R6 Khảo sát Google rộng (kể cả tiếng Việt, phổ thông) — ACPX antigravity-gemini-high, 0 token Claude.
  T8 Tổng hợp vòng 1 + FINAL ADJUSTMENT GATE (Main, Opus).
  T9 REVIEW độc lập bản tổng hợp (fresh-context subagent) + PROVE (kiểm file/nhãn/quota).

FILES_OR_ASSETS: README.md, CLAUDE.md, tasks/*, docs/00-02, research/briefs/*, research/raw/*, research/synthesis/00-*, data/registry.csv, pipeline/README.md, env/environment.yml

TOOLS_AND_MODELS: Sonnet ×5 (search+collate), ACPX Gemini ×1, Opus Main (synthesis/QC); PubMed, Consensus, bioRxiv, Perplexity smart_query (standard/quick), WebSearch.

SKILLS: tinbeta-protocol (khung), subagent-swarm + communication-board (giao việc), biobirddna-genetics (ranh giới bằng chứng, T06/T22), bio-research:scientific-problem-selection (sổ giả thuyết/risk — dùng phần Risk Assessment ở vòng 2).
  Rejected: superpowers:brainstorming (đây là nghiên cứu, không phải feature); research skill của harness (ghi 1 file Markdown — nhưng cần 6 nhánh song song với brief riêng).

TESTS_AND_VALIDATORS:
  - Script kiểm: mọi file research/raw/R*.md có 6 section bắt buộc + không có claim thiếu nhãn (grep).
  - Đối chiếu quota Perplexity trước/sau.
  - REVIEW fresh-context: tìm mâu thuẫn giữa R-file và bản tổng hợp.

REJECTED_ALTERNATIVES:
  - Deep Research của Perplexity (quota hiếm; chủ dự án chưa yêu cầu).
  - Tự align 363 bộ gene ngay (chưa có dữ liệu, chưa có máy).
  - Agent Team (không cần peer-debate ở vòng thu thập).

STATUS: READY_TO_EXECUTE (chủ dự án đã chỉ định làm plan + cho subagent tìm trước; không có hành động không hoàn tác)
