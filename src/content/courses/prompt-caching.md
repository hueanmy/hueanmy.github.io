---
title: Prompt Caching
tagline: CLAUDE CODE · CACHING
description: Tại sao Claude Code không cần đọc lại toàn bộ codebase mỗi message — và prompt caching tiết kiệm cho bạn 90% input token, 85% latency như thế nào.
description_en: Why Claude Code doesn’t re-read your entire codebase every message — and how prompt caching saves 90% of input tokens and 85% latency.
video: /courses/prompt-caching/demo.mp4
thumbnail: /courses/prompt-caching/thumbnail.png
duration: '0:55'
date: 2026-05-01
tags: [Claude Code, Prompt Caching, Tokens, Latency]
sourceDir: /courses/prompt-caching/source
sourceFiles:
  - slides.html
featured: true
order: 2
---

<div class="lang-vi">

Prompt caching là tính năng tự động trong Claude Code: phần “tĩnh” của context (CLAUDE.md, project structure, source files) được lưu lại như một checkpoint. Từ message thứ 2 trở đi, bạn chỉ trả token cho phần mới.

### 3 điều cần nhớ

1. **Write một lần, đọc nhiều lần.** Lần đầu tốn thêm 25% để ghi cache — nhưng chỉ 1 lần. Sau đó giảm 90% input token và 85% latency.
2. **Cache TTL là 5 phút.** Idle quá 5 phút → cache expire → write lại từ đầu tự động. Không cần config gì.
3. **Session dài vẫn tốn token.** Static context được cache, nhưng conversation history thì không. Dùng `/compact` để nén khi cần.

### Ai cần biết điều này?

- Đang chạy Claude Code trên codebase lớn (>20k tokens context).
- Thấy session dài đột ngột tốn nhiều token hơn — đó là history tích lũy, không phải static context.
- Muốn hiểu tại sao message đầu tiên trong session “chậm” hơn các message sau.

</div>

<div class="lang-en">

Prompt caching is an automatic feature in Claude Code: the “static” part of your context (CLAUDE.md, project structure, source files) is saved as a checkpoint. From the second message onward, you only pay tokens for the new content.

### 3 things to remember

1. **Write once, read many times.** The first message pays an extra 25% to write the cache — but only once. After that, you get 90% fewer input tokens and 85% lower latency.
2. **Cache TTL is 5 minutes.** Idle for more than 5 minutes → cache expires → automatically re-written on the next message. No config needed.
3. **Long sessions still cost tokens.** Static context is cached, but conversation history is not. Use `/compact` to compress when needed.

### Who needs to know this?

- Running Claude Code on a large codebase (>20k tokens of context).
- Noticing that long sessions suddenly cost more tokens — that’s accumulated history, not static context.
- Wondering why the first message in a session is “slower” than subsequent ones.

</div>
