---
title: Claude Code Hooks
tagline: CLAUDE CODE · HOOKS
description: Tự động hóa workflow với hooks — chạy lệnh shell tại các điểm vòng đời xác định khi Claude sửa file, hoàn thành task, hoặc cần input từ bạn.
video: /courses/claude-code-hooks/demo.mp4
thumbnail: /courses/claude-code-hooks/thumbnail.png
duration: '0:22'
date: 2026-05-02
tags: [Claude Code, Hooks, Automation, Shell]
demoUrl: /courses/claude-code-hooks/source/slides.html
sourceDir: /courses/claude-code-hooks/source
sourceFiles:
  - slides.html
  - claude-code-hooks-vi.pptx
featured: true
order: 1
---

Hooks là lệnh shell do bạn định nghĩa, được Claude Code chạy đúng tại các điểm vòng đời xác định — không phụ thuộc vào quyết định của LLM. Đây là cơ chế deterministic để tự động hóa format, audit, bảo vệ file, và thông báo desktop.

### 3 điều cần nhớ

1. **Hơn 20 sự kiện vòng đời.** `PreToolUse`, `PostToolUse`, `Notification`, `SessionStart`, `Stop`, `PreCompact`, `FileChanged`… mỗi event là một điểm chèn deterministic.
2. **5 loại hook.** `command` (shell), `http` (webhook), `mcp_tool`, `prompt` (LLM judge), `agent` (Claude đa lượt). Chọn đúng mô hình thực thi cho từng use case.
3. **Exit code điều khiển flow.** `exit 0` → tiến hành; `exit 2` → chặn hành động và gửi stderr cho Claude làm phản hồi; JSON stdout → quyết định có cấu trúc (allow/deny + reason).

### Pattern phổ biến

- **Thông báo** desktop khi Claude cần input qua `Notification`.
- **Auto-format** chạy Prettier/ESLint sau mỗi `Edit|Write` qua `PostToolUse`.
- **Bảo vệ file** chặn sửa `.env`, `package-lock.json`, `.git` qua `PreToolUse`.
- **Audit log** ghi lại mọi `ConfigChange` ra file để theo dõi tuân thủ.
- **Auto-approve** bỏ qua hộp thoại xin quyền cho tool đáng tin (vd. `ExitPlanMode`).

### Mẹo vận hành

- Dùng `matcher` để giới hạn phạm vi — càng hẹp càng tốt, tránh tự động hóa quá rộng.
- Xác minh bằng `/hooks` (hooks browser) — nếu không thấy event, kiểm tra regex và `chmod +x`.
- Không trộn `exit 2` với JSON stdout — chọn một.
- `Stop` hook chạy cho mỗi chunk stream → cần logic thoát sớm để khỏi loop.

Slide deck (10 trang, tiếng Việt) có sẵn để tải về bên dưới — tham chiếu đầy đủ events, hook types, matchers, troubleshooting.
