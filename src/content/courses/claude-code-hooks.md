---
title: Claude Code Hooks
tagline: CLAUDE CODE · HOOKS
description: Tự động hóa workflow với hooks — chạy lệnh shell tại các điểm vòng đời xác định khi Claude sửa file, hoàn thành task, hoặc cần input từ bạn.
description_en: Automate your workflow with hooks — run shell commands at deterministic lifecycle points when Claude edits files, completes tasks, or needs your input.
video: /courses/claude-code-hooks/demo.mp4
thumbnail: /courses/claude-code-hooks/thumbnail.png
duration: '0:22'
date: 2026-05-02
tags: [Claude Code, Hooks, Automation, Shell]
demoUrl: /courses/claude-code-hooks/source/slides-vi.html
sourceDir: /courses/claude-code-hooks/source
sourceFiles:
  - slides-vi.html
  - slides-en.html
  - claude-code-hooks-vi.pptx
  - claude-code-hooks-en.pptx
featured: true
order: 1
---

<div class="lang-vi">

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

</div>

<div class="lang-en">

Hooks are shell commands you define that Claude Code runs at exact lifecycle points — independent of any LLM decision. This is the deterministic mechanism for automating formatting, auditing, file protection, and desktop notifications.

### 3 things to remember

1. **20+ lifecycle events.** `PreToolUse`, `PostToolUse`, `Notification`, `SessionStart`, `Stop`, `PreCompact`, `FileChanged`… each event is a deterministic injection point.
2. **5 hook types.** `command` (shell), `http` (webhook), `mcp_tool`, `prompt` (LLM judge), `agent` (multi-turn Claude). Pick the right execution model for each use case.
3. **Exit codes control flow.** `exit 0` → proceed; `exit 2` → block the action and send stderr to Claude as feedback; JSON stdout → structured decision (allow/deny + reason).

### Common patterns

- **Desktop notification** when Claude needs input via `Notification`.
- **Auto-format** run Prettier/ESLint after every `Edit|Write` via `PostToolUse`.
- **File protection** block edits to `.env`, `package-lock.json`, `.git` via `PreToolUse`.
- **Audit log** record every `ConfigChange` to a file for compliance tracking.
- **Auto-approve** skip permission dialogs for trusted tools (e.g. `ExitPlanMode`).

### Operational tips

- Use `matcher` to narrow scope — the tighter the better, avoid over-automating.
- Verify with `/hooks` (hooks browser) — if you don’t see the event, check regex and `chmod +x`.
- Don’t mix `exit 2` with JSON stdout — pick one.
- `Stop` hook fires per stream chunk → add an early-exit guard to avoid loops.

Slide deck (10 slides, English version) available for download below — full reference for events, hook types, matchers, and troubleshooting.

</div>
