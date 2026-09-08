# BIRDBIODNA project — luật cố định

- Đọc `README.md` và `tasks/todo.md` trước khi làm bất cứ gì.
- Skill nền: `biobirddna-genetics` (V4, v0.4.0). Không sửa skill từ project này; project chỉ TẠO đầu vào cho tracker T06 (bộ gene chào mào) và T22 (gene ứng viên) của V4.
- Nhãn bằng chứng bắt buộc cho mọi claim: CONFIRMED / STRONG_INFERENCE / UNVERIFIED. Không bịa trích dẫn.
- `research/raw/` là output subagent, không sửa tay; sửa thì ghi ở `research/synthesis/`.
- Dữ liệu tải về ghi vào `data/registry.csv` (nguồn, phiên bản, ngày, sha256). Không commit file dữ liệu lớn.
- Giả thuyết cạnh tranh (H1 tiến hóa chuẩn · H2 tiến hóa + ràng buộc mạnh · H3 bộ gene gốc được thiết kế/gieo) được đối xử bằng CÙNG một câu hỏi: "dữ liệu nào phân biệt được?" — không kết luận bằng ý kiến.
- Không dùng project để hướng dẫn lấy mẫu xâm lấn; mẫu phân tử thuộc SOP thú y riêng (kế thừa V4).

## Luật giao việc (chủ dự án chốt 2026-09-08)

- **CẤM dùng Codex** (MCP hoặc CLI) cho mọi việc trong project này. Muốn dùng lại phải hỏi và được chủ dự án phê duyệt từng lần.
- Đội làm việc: **Claude team** (Main Opus + teammate Sonnet/Haiku) phối hợp **Antigravity** qua `acpx antigravity-gemini-high`, trao đổi qua Communication Board (participant `acpx-antigravity/birdbiodna`).
- **CẤM đưa thao tác xóa (rm/rmdir/del/Remove-Item) vào brief giao cho bất kỳ agent nào.** Main tự dọn bằng Bash sau khi `ls` đích. Lý do: sự cố 2026-09-08 (xem `tasks/RESTORE_LOG-2026-09-08.txt`).
- Commit git sau mỗi bước có kết quả; không để project không có git.
