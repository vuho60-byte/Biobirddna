# BIRDBIODNA — Dự án "DNA gốc của chim" (Primordial Avian Genome)

Nhánh nghiên cứu mở rộng từ skill **BioBirdDNA Genetics v0.4.0** (V4: hỗ trợ quyết định di truyền màu lông chim cảnh).
V4 trả lời "màu lông truyền thế nào". Dự án này hỏi câu lớn hơn: **phần nào của bộ gene chim KHÔNG đổi qua hàng chục triệu năm, phần nào đổi, và tái dựng "bộ gene tổ tiên" bằng tính toán được tới đâu.**

## Ba lớp của mô hình làm việc

| Lớp | Nội dung | Ai xử lý |
|---|---|---|
| LÕI (core-invariant) | Vùng bảo tồn cực cao qua mọi loài chim + ngoài nhóm (UCE/CNE), yếu tố điều hòa riêng lớp chim (ASHCE), gene phát triển cơ thể | Dự án này |
| VỎ (variable shell) | Màu lông, cỡ mỏ, kích thước… đột biến + chọn lọc trong vài thế hệ | V4 (`biobirddna-genetics`) |
| CÁ TÍNH (behaviour) | Hành vi bẩm sinh (di cư, hót, làm tổ) + cá tính đa gene + môi trường | Dự án này (nhánh hành vi) |

## Bản đồ thư mục

```
README.md                      ← bạn đang đọc
CLAUDE.md                      ← luật project (nhỏ, cố định)
tasks/todo.md                  ← kế hoạch theo pha, tick được
tasks/lessons.md               ← #LESSONS
tasks/primordial-dna-think.md  ← THINK (mục tiêu thật, giả định, rủi ro)
tasks/primordial-dna-plan.md   ← PLAN (tiêu chí chấp nhận, task, skill)
tasks/primordial-dna-handoff.md← bảng bàn giao subagent (append-only)
docs/00-tai-dinh-khung-cau-hoi.md  ← 6 câu hỏi gốc → câu hỏi khoa học kiểm chứng được + sổ giả thuyết H1/H2/H3
docs/01-thuat-ngu.md               ← từ điển thuật ngữ Việt–Anh
docs/02-nguon-du-lieu-va-cong-cu.md← registry dataset/tool (trạng thái: cần xác minh)
research/briefs/               ← brief giao cho subagent (R1–R6)
research/raw/                  ← kết quả thô từ subagent (không sửa tay)
research/synthesis/            ← tổng hợp của Main sau mỗi vòng
data/registry.csv              ← mọi file dữ liệu tải về: nguồn, phiên bản, sha256
pipeline/README.md             ← 6 module code dự kiến (chưa viết code khi chưa có dữ liệu)
env/environment.yml            ← môi trường conda (WSL2) cho phần tính toán
```

## Luật bằng chứng (kế thừa V4)

Mọi khẳng định trong `research/` và `docs/` mang nhãn: `CONFIRMED` (≥2 nguồn độc lập) · `STRONG_INFERENCE` (1 nguồn) · `UNVERIFIED` (chưa tìm được nguồn, nói rõ). Không bịa DOI/URL. Không nâng ngôn ngữ bằng chứng.
