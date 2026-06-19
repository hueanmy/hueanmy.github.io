---
title: aidlc-testagent
tagline: AIDLC · AI TEST AGENT
description: AI agent tự động sinh, chạy và tự heal bộ E2E test — chỉ cần trỏ vào target, duyệt plan, nhận lại test suite đã pass.
description_en: An AI agent that automatically generates, runs, and self-heals E2E test suites — point it at a target, approve the plan, get back a passing test suite.
date: 2026-06-17
tags: [AIDLC, AI Agent, Testing, Playwright, TypeScript]
repoUrl: https://github.com/aidlc-io/aidlc-testagent
featured: true
order: 10
---

<div class="lang-vi">

## Mục đích

`aidlc-testagent` giải quyết một vấn đề cụ thể: **viết và duy trì E2E test tốn thời gian**. Tool này đóng vai trò một agent tự động hóa toàn bộ vòng đời test — từ khám phá giao diện, lên kế hoạch, sinh code, chạy thử, đến tự sửa khi test fail. Mục tiêu cuối là có một test suite có thể commit vào repo, không phải chỉ là output tạm thời.

Phạm vi áp dụng: web app (Playwright), Electron desktop app, REST API, và mobile (roadmap).

## Kỹ thuật AI sử dụng

### 1. Structured Perception (Nhận thức có cấu trúc)
Thay vì đưa raw HTML hay pixel vào LLM, adapter tạo ra `PerceptionSnapshot` — snapshot chuẩn hóa gồm accessibility tree, danh sách element, và endpoint. Điều này giảm hallucination vì model nhìn thấy cấu trúc ý nghĩa, không phải markup thô.

### 2. Trust-Ordered Grounding (Ngữ cảnh theo thứ tự ưu tiên)
Planner nạp context theo thứ tự ưu tiên cứng: **requirements > manual tests > business rules > source code**. Ý định của con người luôn thắng implementation. LLM không được phép "sáng tạo" ra behavior không có trong tài liệu.

### 3. LLM Delegation qua CLI
Core agent không gọi trực tiếp model API. Thay vào đó, nó delegate qua một LLM provider interface gọi local CLI (ví dụ `claude`). Không có API key trong repo — xác thực do CLI quản lý.

### 4. Structured Output Validation
Mọi output từ LLM (test plan, generated code) đều được validate qua **Zod schema** trước khi dùng. Nếu không parse được, pipeline dừng lại — không có silent failure.

### 5. Self-Healing Loop
Khi test fail, agent không dừng lại. Nó re-observe target, gửi lại context + error cho LLM, và regenerate — tối đa `maxHealAttempts` lần. Đây là vòng lặp `execute → observe → heal → retry`.

### 6. Stability Gate (Cổng ổn định)
Mỗi test mới chạy N lần liên tiếp (configurable). Test chỉ được accept vào suite khi **tất cả** N lần pass. Test flaky bị quarantine, không commit vào repo.

### 7. Cost Metering
Mọi LLM call đều được đo chi phí (USD). Run bị abort nếu vượt budget được cấu hình trong `testagent.config.yaml`. Không có surprise bills.

## Nguyên lý hoạt động

Pipeline gồm 6 bước tuần tự:

```
explore → plan → [confirm] → generate → execute → heal
```

1. **Explore** — Adapter điều hướng đến target (URL, app), quan sát accessibility tree và DOM để tạo PerceptionSnapshot.
2. **Plan** — LLM nhận snapshot + grounding context, sinh ra test plan có cấu trúc với các stage: `setup → smoke → core → edge → teardown`.
3. **Confirm** — Human review plan. Nếu `autoApprove: false`, pipeline dừng để chờ duyệt. Đây là human-in-the-loop checkpoint duy nhất.
4. **Generate** — Generator biến plan đã duyệt thành Playwright specs + Page Object Models có thể commit.
5. **Execute** — Test chạy qua stability gate. Session auth được reuse để tránh login lặp lại.
6. **Heal** — Test fail → agent re-observe, gửi error context, regenerate, retry. Nếu vượt `maxHealAttempts` → mark failed và report.

Cuối pipeline, agent tính **verdict**: target pass nếu đạt đủ `minScenarios`, `mustPass`, stability threshold và không vượt budget.

## Manual Explore — Ghi lại hành vi thực tế

Khi app quá phức tạp để agent tự khám phá, dùng chế độ **manual explore**: bạn navigate trực tiếp trong browser thật, agent lặng lẽ ghi lại từng bước.

```bash
ata explore <target> --manual --headed
```

### Auto capture

- Mở browser thật (headed), bạn navigate tự do — agent tự động snap mỗi khi DOM idle
- **Tự đặt tên step từ DOM:** dialog title → heading → URL path → page title
- **Click capture:** mỗi lần click ghi lại tên element → step name = `click "Generate" — studio`
- **SPA-safe:** fingerprint gồm URL + title, nên route change luôn tạo step mới

### Toolbar (góc trên phải)

| Nút | Tác dụng |
|-----|----------|
| 📌 Checkpoint | Chọn step, đặt tên, đánh dấu common precondition (vd. `after-login`) → lưu `checkpoints/<name>.json` |
| 🎬 Use case | Chọn start step, navigate, bấm 🏁 End → LLM tự generate markdown test doc → `use-cases/<name>.md` |
| ✅ Done | Mở review panel |

### Review panel

- **Test case name:** điền tên → tự tạo use case bao toàn bộ session
- Danh sách tất cả steps với ô rename
- **👁 eye toggle** trên mỗi step: mờ → click → sáng xanh + preview ảnh full-screen → click lại hoặc ESC để đóng
- **Keep exploring** để quay lại, **✅ Save & Done** để lưu

### Output

```
generated/<target>/
  perception.json          ← toàn bộ steps, dùng với --reuse-perception
  use-cases/<name>.md      ← markdown test doc do LLM sinh
  checkpoints/<name>.json  ← named checkpoints
  .auth/<target>.json      ← browser session, specs load tự động
```

### Dùng lại session đã record

Record một lần, chạy nhiều lần — kể cả trong CI:

```bash
# Dùng lại perception.json + use-cases đã capture để plan
ata plan dreem --reuse-perception

# Full loop, bỏ qua bước explore
ata run dreem --reuse-perception --yes
```

## Behavior khi apply

### Chạy lần đầu
```bash
npx ata config          # Setup tương tác: chọn LLM provider, set budget
npx ata plan todomvc    # Chỉ propose plan, không sinh code — để review
npx ata run todomvc     # Full loop: explore → plan → confirm → generate → execute → heal
```

Khi `npx ata run` chạy:
- Agent mở browser (headless), navigate đến URL trong `targets/todomvc.target.yaml`
- Sinh PerceptionSnapshot từ DOM
- LLM tạo plan → terminal hiện plan để bạn approve (Y/n)
- Sau khi approve: sinh Playwright test files vào thư mục output
- Chạy tests, stability gate lọc flaky tests
- Nếu fail: healing loop tự động chạy
- Kết quả: thư mục `tests/` với spec files có thể commit

### CI Gate
```bash
npx ata validate        # Chạy tất cả targets, exit code 0 nếu pass
```
Dùng trong CI pipeline để block merge nếu test suite không pass verdict.

### Bảo vệ an toàn
- Production host bị từ chối mặc định (chỉ staging)
- Private targets để trong `.targets/private/` (gitignored)
- Credentials lấy từ env vars, không bao giờ trong YAML
- Action guardrail chặn các verb nguy hiểm: `delete`, `pay`, `remove`

## Cấu hình và triển khai

### Cấu trúc file
```
testagent.config.yaml        # Global: LLM provider, budget, stability runs
targets/
  todomvc.target.yaml        # Per-target: URL, auth, grounding sources, success criteria
  .targets/private/          # Gitignored private targets
```

### Ví dụ target config
```yaml
name: todomvc
adapter: playwright-web
url: https://todomvc.com/examples/react
auth:
  strategy: none
grounding:
  requirements: docs/requirements.md
  manualTests: docs/manual-tests.md
scope:
  include: ["todo list", "add item", "complete item"]
successCriteria:
  minScenarios: 5
  mustPass: ["add a todo item", "complete a todo item"]
```

### Roadmap
- **Phase 1 (hiện tại):** Web + Electron, reliability core
- **Phase 2:** REST API adapter + traceability report
- **Phase 3:** `--diff` mode (chỉ test code thay đổi) + MCP packaging
- **Phase 4+:** iOS, Android, vision fallback

</div>

<div class="lang-en">

## Purpose

`aidlc-testagent` solves a specific problem: **writing and maintaining E2E tests takes too long**. This tool acts as an agent that automates the entire test lifecycle — from exploring the UI, planning test cases, generating code, running tests, to self-healing when tests fail. The end goal is a committable test suite in your repo, not a temporary output.

Supported surfaces: web apps (Playwright), Electron desktop apps, REST APIs, and mobile (roadmap).

## AI Techniques

### 1. Structured Perception
Instead of feeding raw HTML or pixels to the LLM, the adapter produces `PerceptionSnapshot` — a normalized snapshot containing the accessibility tree, element lists, and endpoints. This reduces hallucination because the model sees meaningful structure, not raw markup.

### 2. Trust-Ordered Grounding
The planner loads context in strict priority order: **requirements > manual tests > business rules > source code**. Human intent always outranks implementation. The LLM cannot invent behavior that isn't documented.

### 3. LLM Delegation via CLI
The core agent never calls a model API directly. Instead, it delegates through an LLM provider interface that calls a local CLI (e.g. `claude`). No API keys in the repo — authentication is managed by the CLI.

### 4. Structured Output Validation
All LLM output (test plans, generated code) is validated against **Zod schemas** before use. If parsing fails, the pipeline stops — no silent failures.

### 5. Self-Healing Loop
When tests fail, the agent doesn't stop. It re-observes the target, sends error context back to the LLM, and regenerates — up to `maxHealAttempts` times. This is an `execute → observe → heal → retry` loop.

### 6. Stability Gate
Each new test runs N consecutive times (configurable). A test is only accepted into the suite when **all** N runs pass. Flaky tests are quarantined, never committed.

### 7. Cost Metering
Every LLM call is metered (USD). Runs abort if they exceed the budget configured in `testagent.config.yaml`. No surprise bills.

## How It Works

The pipeline has 6 sequential steps:

```
explore → plan → [confirm] → generate → execute → heal
```

1. **Explore** — The adapter navigates to the target (URL, app), observes the accessibility tree and DOM to produce a PerceptionSnapshot.
2. **Plan** — The LLM receives the snapshot + grounding context and generates a structured test plan with stages: `setup → smoke → core → edge → teardown`.
3. **Confirm** — Human reviews the plan. If `autoApprove: false`, the pipeline pauses for approval. This is the only human-in-the-loop checkpoint.
4. **Generate** — The generator converts the approved plan into Playwright specs + Page Object Models ready to commit.
5. **Execute** — Tests run through the stability gate. Auth sessions are reused to avoid repeated logins.
6. **Heal** — Test fails → agent re-observes, sends error context, regenerates, retries. If `maxHealAttempts` is exceeded → mark as failed and report.

At the end of the pipeline, the agent computes a **verdict**: the target passes if it meets `minScenarios`, `mustPass`, the stability threshold, and stays within budget.

## Manual Explore — Record real behavior

When the app is too complex for the agent to explore automatically, use **manual explore** mode: you navigate directly in a real headed browser while the agent silently records every step.

```bash
ata explore <target> --manual --headed
```

### Auto capture

- Opens a real headed browser — you navigate freely, agent auto-snaps on DOM idle
- **Auto-names steps from DOM:** dialog title → heading → URL path → page title
- **Click capture:** every click records the element name → step name = `click "Generate" — studio`
- **SPA-safe:** fingerprint uses URL + title, so route changes always create a new step

### Toolbar (top right)

| Button | Effect |
|--------|--------|
| 📌 Checkpoint | Select a step, name it, mark as a common precondition (e.g. `after-login`) → saves `checkpoints/<name>.json` |
| 🎬 Use case | Select start step, navigate, hit 🏁 End → LLM generates a markdown test doc → `use-cases/<name>.md` |
| ✅ Done | Opens the review panel |

### Review panel

- **Test case name:** fill in → auto-creates a use case covering the full session
- List of all steps with rename inputs
- **👁 eye toggle** on each step: dimmed → click → highlighted + full-screen screenshot preview → click again or ESC to close
- **Keep exploring** to go back, **✅ Save & Done** to save

### Output

```
generated/<target>/
  perception.json          ← all steps, used with --reuse-perception
  use-cases/<name>.md      ← LLM-generated markdown test doc
  checkpoints/<name>.json  ← named checkpoints
  .auth/<target>.json      ← browser session, auto-loaded by specs
```

### Reuse a recorded session

Record once, run many times — including in CI:

```bash
# Reuse perception.json + captured use-cases for planning
ata plan dreem --reuse-perception

# Full loop, skip the explore step
ata run dreem --reuse-perception --yes
```

## Behavior When Applied

### First run
```bash
npx ata config          # Interactive setup: choose LLM provider, set budget
npx ata plan todomvc    # Propose plan only, no code generated — for review
npx ata run todomvc     # Full loop: explore → plan → confirm → generate → execute → heal
```

When `npx ata run` executes:
- Agent opens a headless browser, navigates to the URL in `targets/todomvc.target.yaml`
- Generates a PerceptionSnapshot from the DOM
- LLM creates a plan → terminal displays the plan for you to approve (Y/n)
- After approval: generates Playwright test files to the output directory
- Runs tests through the stability gate, quarantining flaky tests
- If failures occur: the healing loop runs automatically
- Result: a `tests/` directory with committable spec files

### CI Gate
```bash
npx ata validate        # Run all targets, exit code 0 if all pass verdict
```
Use in CI pipelines to block merges if the test suite doesn't pass.

### Safety guardrails
- Production hosts are refused by default (staging only)
- Private targets live in `.targets/private/` (gitignored)
- Credentials come from env vars, never YAML
- Action guardrails block dangerous verbs: `delete`, `pay`, `remove`

## Configuration & Deployment

### File structure
```
testagent.config.yaml        # Global: LLM provider, budget, stability runs
targets/
  todomvc.target.yaml        # Per-target: URL, auth, grounding sources, success criteria
  .targets/private/          # Gitignored private targets
```

### Example target config
```yaml
name: todomvc
adapter: playwright-web
url: https://todomvc.com/examples/react
auth:
  strategy: none
grounding:
  requirements: docs/requirements.md
  manualTests: docs/manual-tests.md
scope:
  include: ["todo list", "add item", "complete item"]
successCriteria:
  minScenarios: 5
  mustPass: ["add a todo item", "complete a todo item"]
```

### Roadmap
- **Phase 1 (current):** Web + Electron, reliability core
- **Phase 2:** REST API adapter + traceability report
- **Phase 3:** `--diff` mode (test only changed code) + MCP packaging
- **Phase 4+:** iOS, Android, vision fallback

</div>
