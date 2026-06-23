---
title: aidlc-testagent
tagline: AIDLC · AI TEST AGENT
description: AI agent tự động sinh, chạy và tự heal bộ E2E test — chỉ cần trỏ vào target, duyệt plan, nhận lại test suite đã pass.
description_en: An AI agent that automatically generates, runs, and self-heals E2E test suites — point it at a target, approve the plan, get back a passing test suite.
date: 2026-06-23
tags: [AIDLC, AI Agent, Testing, Playwright, TypeScript, v0.6.0]
repoUrl: https://github.com/aidlc-io/aidlc-testagent
featured: true
order: 1
---

<h2>
  <span class="lang-en">Purpose</span>
  <span class="lang-vi">Mục đích</span>
</h2>
<p class="lang-en"><code>aidlc-testagent</code> solves a specific problem: <strong>writing and maintaining E2E tests takes too long</strong>. This tool acts as an agent that automates the entire test lifecycle — from exploring the UI, planning test cases, generating code, running tests, to self-healing when tests fail. The end goal is a committable test suite in your repo, not a temporary output.</p>
<p class="lang-vi"><code>aidlc-testagent</code> giải quyết một vấn đề cụ thể: <strong>viết và duy trì E2E test tốn thời gian</strong>. Tool này đóng vai trò một agent tự động hóa toàn bộ vòng đời test — từ khám phá giao diện, lên kế hoạch, sinh code, chạy thử, đến tự sửa khi test fail. Mục tiêu cuối là có một test suite có thể commit vào repo, không phải chỉ là output tạm thời.</p>
<p class="lang-en">Supported surfaces: web apps (Playwright), Electron desktop apps, REST APIs, and mobile (roadmap).</p>
<p class="lang-vi">Phạm vi áp dụng: web app (Playwright), Electron desktop app, REST API, và mobile (roadmap).</p>

<p class="lang-en"><strong>What's new in v0.6.0</strong> — a <strong>manual explore mode</strong> with an in-browser toolbar (checkpoints with screenshot previews, use-case recording → auto-generated markdown docs, live XHR/fetch monitoring, and HAR capture per use case), plus <a href="https://www.npmjs.com/package/@playwright/mcp" target="_blank" rel="noopener"><code>@playwright/mcp</code></a> integration so the agent drives the browser through the Playwright MCP server. Requires Node ≥ 20.</p>
<p class="lang-vi"><strong>Mới ở v0.6.0</strong> — <strong>manual explore mode</strong> với toolbar ngay trong trình duyệt (checkpoint kèm screenshot preview, ghi use case → tự sinh markdown docs, theo dõi XHR/fetch trực tiếp, và bắt HAR theo từng use case), cùng tích hợp <a href="https://www.npmjs.com/package/@playwright/mcp" target="_blank" rel="noopener"><code>@playwright/mcp</code></a> để agent điều khiển trình duyệt qua Playwright MCP server. Yêu cầu Node ≥ 20.</p>

<h2>
  <span class="lang-en">Architecture</span>
  <span class="lang-vi">Kiến trúc</span>
</h2>
<p class="lang-en">The system is organized into three layers: a CLI entry point, a core reasoning engine with pluggable modules, and surface adapters. The core never imports Playwright or Appium directly — it only talks to the <code>TestAdapter</code> interface.</p>
<p class="lang-vi">Hệ thống chia thành ba lớp: CLI entry point, core reasoning engine với các module có thể thay thế, và surface adapter. Core không bao giờ import Playwright hay Appium trực tiếp — chỉ giao tiếp qua interface <code>TestAdapter</code>.</p>

<div class="arch-diagram">
  <div class="arch-layer">
    <div class="arch-layer-label">
      <span class="lang-en">Entry point</span>
      <span class="lang-vi">Điểm vào</span>
    </div>
    <div class="arch-row">
      <div class="arch-box accent-border">
        <div class="arch-box-title">CLI — npx ata</div>
        <div class="arch-box-desc lang-en">config · plan · run · validate</div>
        <div class="arch-box-desc lang-vi">config · plan · run · validate</div>
      </div>
    </div>
  </div>

  <div class="arch-connector"><div class="arch-connector-line"></div></div>

  <div class="arch-layer">
    <div class="arch-layer-label">
      <span class="lang-en">Core — Orchestrator</span>
      <span class="lang-vi">Core — Orchestrator</span>
    </div>
    <div class="arch-row">
      <div class="arch-box wide">
        <div class="arch-box-title">Orchestrator</div>
        <div class="arch-box-desc lang-en">Drives the 6-step pipeline · manages state · computes final verdict</div>
        <div class="arch-box-desc lang-vi">Điều phối 6 bước pipeline · quản lý state · tính verdict cuối</div>
      </div>
      <div class="arch-box">
        <div class="arch-box-title">Cost Meter</div>
        <div class="arch-box-desc lang-en">USD budget guard per run</div>
        <div class="arch-box-desc lang-vi">Giới hạn chi phí USD mỗi run</div>
      </div>
    </div>
  </div>

  <div class="arch-connector"><div class="arch-connector-line"></div></div>

  <div class="arch-layer">
    <div class="arch-layer-label">
      <span class="lang-en">Core modules</span>
      <span class="lang-vi">Các module core</span>
    </div>
    <div class="arch-row">
      <div class="arch-box">
        <div class="arch-box-title">Planner</div>
        <div class="arch-box-desc lang-en">Grounding + trust-ordered context → test plan</div>
        <div class="arch-box-desc lang-vi">Grounding + context ưu tiên → test plan</div>
      </div>
      <div class="arch-box">
        <div class="arch-box-title">Generator</div>
        <div class="arch-box-desc lang-en">Plan → Playwright specs + Page Objects</div>
        <div class="arch-box-desc lang-vi">Plan → Playwright specs + Page Objects</div>
      </div>
      <div class="arch-box">
        <div class="arch-box-title">Executor</div>
        <div class="arch-box-desc lang-en">Stability gate · session reuse</div>
        <div class="arch-box-desc lang-vi">Stability gate · tái sử dụng session</div>
      </div>
      <div class="arch-box">
        <div class="arch-box-title">Healer</div>
        <div class="arch-box-desc lang-en">Re-observe → re-generate → retry loop</div>
        <div class="arch-box-desc lang-vi">Re-observe → re-generate → vòng lặp retry</div>
      </div>
    </div>
  </div>

  <div class="arch-connector"><div class="arch-connector-line"></div></div>

  <div class="arch-layer">
    <div class="arch-layer-label">
      <span class="lang-en">Shared services</span>
      <span class="lang-vi">Dịch vụ dùng chung</span>
    </div>
    <div class="arch-row">
      <div class="arch-box">
        <div class="arch-box-title">LLM Provider</div>
        <div class="arch-box-desc lang-en">Delegates to local CLI (e.g. claude). No API keys in repo.</div>
        <div class="arch-box-desc lang-vi">Gọi qua local CLI (vd. claude). Không có API key trong repo.</div>
      </div>
      <div class="arch-box">
        <div class="arch-box-title">Perception · Playwright MCP</div>
        <div class="arch-box-desc lang-en">PerceptionSnapshot via @playwright/mcp — accessibility tree, element list, endpoints; auto + manual explore</div>
        <div class="arch-box-desc lang-vi">PerceptionSnapshot qua @playwright/mcp — accessibility tree, element list, endpoint; explore tự động + thủ công</div>
      </div>
      <div class="arch-box">
        <div class="arch-box-title">Config Loader</div>
        <div class="arch-box-desc lang-en">testagent.config.yaml + targets/*.target.yaml → Zod-validated</div>
        <div class="arch-box-desc lang-vi">testagent.config.yaml + targets/*.target.yaml → Zod validate</div>
      </div>
    </div>
  </div>

  <div class="arch-connector"><div class="arch-connector-line"></div></div>

  <div class="arch-layer">
    <div class="arch-layer-label">
      <span class="lang-en">Surface adapters (TestAdapter interface)</span>
      <span class="lang-vi">Surface adapter (interface TestAdapter)</span>
    </div>
    <div class="arch-row">
      <div class="arch-box accent-border">
        <div class="arch-box-title">playwright-web</div>
        <div class="arch-box-desc lang-en">Phase 1 · Web apps</div>
        <div class="arch-box-desc lang-vi">Phase 1 · Web app</div>
      </div>
      <div class="arch-box accent-border">
        <div class="arch-box-title">playwright-electron</div>
        <div class="arch-box-desc lang-en">Phase 1 · Desktop apps</div>
        <div class="arch-box-desc lang-vi">Phase 1 · Desktop app</div>
      </div>
      <div class="arch-box muted">
        <div class="arch-box-title">REST API</div>
        <div class="arch-box-desc lang-en">Phase 2 · roadmap</div>
        <div class="arch-box-desc lang-vi">Phase 2 · roadmap</div>
      </div>
      <div class="arch-box muted">
        <div class="arch-box-title">iOS / Android</div>
        <div class="arch-box-desc lang-en">Phase 4+ · roadmap</div>
        <div class="arch-box-desc lang-vi">Phase 4+ · roadmap</div>
      </div>
    </div>
  </div>
</div>

<h2>
  <span class="lang-en">Pipeline</span>
  <span class="lang-vi">Pipeline</span>
</h2>
<p class="lang-en">Six sequential steps. The <strong>Confirm</strong> step is the only human-in-the-loop checkpoint — the pipeline pauses here when <code>autoApprove: false</code>.</p>
<p class="lang-vi">Sáu bước tuần tự. Bước <strong>Confirm</strong> là human-in-the-loop checkpoint duy nhất — pipeline dừng ở đây khi <code>autoApprove: false</code>.</p>

<div class="pipeline-diagram">
  <div class="pipeline-steps">
    <div class="pipe-step">
      <div class="pipe-box">
        <span class="lang-en">Explore</span>
        <span class="lang-vi">Explore</span>
      </div>
      <div class="pipe-label lang-en">observe target</div>
      <div class="pipe-label lang-vi">quan sát target</div>
    </div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-step">
      <div class="pipe-box">
        <span class="lang-en">Plan</span>
        <span class="lang-vi">Plan</span>
      </div>
      <div class="pipe-label lang-en">LLM → test plan</div>
      <div class="pipe-label lang-vi">LLM → test plan</div>
    </div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-step">
      <div class="pipe-box accent">
        <span class="lang-en">Confirm ✓</span>
        <span class="lang-vi">Confirm ✓</span>
      </div>
      <div class="pipe-label accent lang-en">human gate</div>
      <div class="pipe-label accent lang-vi">duyệt bởi người</div>
    </div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-step">
      <div class="pipe-box">
        <span class="lang-en">Generate</span>
        <span class="lang-vi">Generate</span>
      </div>
      <div class="pipe-label lang-en">specs + POMs</div>
      <div class="pipe-label lang-vi">specs + POMs</div>
    </div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-step">
      <div class="pipe-box">
        <span class="lang-en">Execute</span>
        <span class="lang-vi">Execute</span>
      </div>
      <div class="pipe-label lang-en">stability gate</div>
      <div class="pipe-label lang-vi">stability gate</div>
    </div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-step">
      <div class="pipe-box">
        <span class="lang-en">Heal</span>
        <span class="lang-vi">Heal</span>
      </div>
      <div class="pipe-label lang-en">re-observe · retry</div>
      <div class="pipe-label lang-vi">re-observe · retry</div>
    </div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-step">
      <div class="pipe-box accent">
        <span class="lang-en">Verdict</span>
        <span class="lang-vi">Verdict</span>
      </div>
      <div class="pipe-label accent lang-en">pass / fail</div>
      <div class="pipe-label accent lang-vi">pass / fail</div>
    </div>
  </div>
</div>

<ol>
  <li class="lang-en"><strong>Explore</strong> — Adapter navigates to the target (autonomously, or driven by you in <strong>manual mode</strong>), observes accessibility tree + DOM → <code>PerceptionSnapshot</code>. The snapshot persists to <code>perception.json</code> and is reused across runs without reopening the browser.</li>
  <li class="lang-en"><strong>Plan</strong> — LLM receives snapshot + trust-ordered grounding context → structured test plan with stages: <code>setup → smoke → core → edge → teardown</code>.</li>
  <li class="lang-en"><strong>Confirm</strong> — Terminal shows the plan for human approval (Y/n). Only proceeds after explicit sign-off.</li>
  <li class="lang-en"><strong>Generate</strong> — Approved plan → Playwright specs + Page Object Models, Zod-validated before write.</li>
  <li class="lang-en"><strong>Execute</strong> — Tests run N times through the stability gate. Flaky tests are quarantined, never committed.</li>
  <li class="lang-en"><strong>Heal</strong> — Failures trigger re-observation + LLM regeneration. Retries up to <code>maxHealAttempts</code>.</li>

  <li class="lang-vi"><strong>Explore</strong> — Adapter điều hướng đến target (tự động, hoặc do bạn điều khiển ở <strong>manual mode</strong>), quan sát accessibility tree + DOM → <code>PerceptionSnapshot</code>. Snapshot được lưu vào <code>perception.json</code> và tái sử dụng giữa các run mà không cần mở lại browser.</li>
  <li class="lang-vi"><strong>Plan</strong> — LLM nhận snapshot + grounding context theo thứ tự ưu tiên → test plan có cấu trúc: <code>setup → smoke → core → edge → teardown</code>.</li>
  <li class="lang-vi"><strong>Confirm</strong> — Terminal hiện plan để duyệt (Y/n). Chỉ tiếp tục sau khi được approve.</li>
  <li class="lang-vi"><strong>Generate</strong> — Plan đã duyệt → Playwright specs + Page Object Models, Zod-validated trước khi ghi.</li>
  <li class="lang-vi"><strong>Execute</strong> — Test chạy N lần qua stability gate. Test flaky bị quarantine, không commit.</li>
  <li class="lang-vi"><strong>Heal</strong> — Fail → re-observe + LLM regenerate. Retry tối đa <code>maxHealAttempts</code> lần.</li>
</ol>

<h2>
  <span class="lang-en">Manual Explore Mode <span style="font-weight:400">· new in v0.6.0</span></span>
  <span class="lang-vi">Manual Explore Mode <span style="font-weight:400">· mới ở v0.6.0</span></span>
</h2>
<p class="lang-en">Autonomous exploration doesn't always reach the screen you care about — behind a login, a multi-step wizard, a feature flag. Manual mode hands you the keyboard: you drive a real headed browser to the exact state you want, and an in-browser toolbar records it as grounded context the planner can trust.</p>
<p class="lang-vi">Explore tự động không phải lúc nào cũng tới được màn hình bạn cần — sau login, qua wizard nhiều bước, hay sau feature flag. Manual mode trao quyền điều khiển cho bạn: bạn tự lái một headed browser tới đúng trạng thái mong muốn, và toolbar ngay trong trình duyệt ghi lại nó thành grounding context mà planner tin cậy.</p>

<pre><code>npx ata explore myapp --manual --headed</code></pre>

<table class="technique-table">
  <thead>
    <tr>
      <th><span class="lang-en">Toolbar action</span><span class="lang-vi">Hành động trên toolbar</span></th>
      <th><span class="lang-en">What it captures</span><span class="lang-vi">Ghi lại gì</span></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Checkpoint</td>
      <td>
        <span class="lang-en">Snapshots the current DOM + accessibility tree with a screenshot preview, so the planner sees the exact state you reached.</span>
        <span class="lang-vi">Chụp DOM + accessibility tree hiện tại kèm screenshot preview, để planner thấy đúng trạng thái bạn đã tới.</span>
      </td>
    </tr>
    <tr>
      <td>Record use case</td>
      <td>
        <span class="lang-en">Records a named flow of your actions and auto-generates a markdown doc describing the steps — committable grounding for the plan.</span>
        <span class="lang-vi">Ghi lại một flow có tên từ thao tác của bạn và tự sinh markdown doc mô tả các bước — grounding có thể commit cho plan.</span>
      </td>
    </tr>
    <tr>
      <td>Network monitor</td>
      <td>
        <span class="lang-en">Live XHR/fetch call log surfaces the endpoints each screen depends on, feeding the API surface map.</span>
        <span class="lang-vi">Log XHR/fetch trực tiếp cho thấy endpoint mỗi màn hình phụ thuộc, bổ sung cho API surface map.</span>
      </td>
    </tr>
    <tr>
      <td>HAR capture</td>
      <td>
        <span class="lang-en">Writes a HAR file per recorded use case — a complete network trace for debugging and replay.</span>
        <span class="lang-vi">Ghi một file HAR cho mỗi use case — network trace đầy đủ để debug và replay.</span>
      </td>
    </tr>
  </tbody>
</table>

<h2>
  <span class="lang-en">AI Techniques</span>
  <span class="lang-vi">Kỹ thuật AI</span>
</h2>

<table class="technique-table">
  <thead>
    <tr>
      <th><span class="lang-en">Technique</span><span class="lang-vi">Kỹ thuật</span></th>
      <th><span class="lang-en">What it does</span><span class="lang-vi">Vai trò</span></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Structured Perception</td>
      <td>
        <span class="lang-en">Adapter normalizes DOM into an accessibility tree + element list (<code>PerceptionSnapshot</code>) rather than feeding raw HTML to the LLM. Reduces hallucination.</span>
        <span class="lang-vi">Adapter chuẩn hóa DOM thành accessibility tree + element list (<code>PerceptionSnapshot</code>) thay vì đưa raw HTML vào LLM. Giảm hallucination.</span>
      </td>
    </tr>
    <tr>
      <td>Browser Control via MCP</td>
      <td>
        <span class="lang-en">Perception and exploration run through <code>@playwright/mcp</code> — the agent observes and drives the browser over the Playwright MCP server instead of hand-rolled scripting.</span>
        <span class="lang-vi">Perception và exploration chạy qua <code>@playwright/mcp</code> — agent quan sát và điều khiển browser qua Playwright MCP server thay vì script thủ công.</span>
      </td>
    </tr>
    <tr>
      <td>Trust-Ordered Grounding</td>
      <td>
        <span class="lang-en">Planner loads context in strict priority: requirements → manual tests → business rules → source code. Human intent always outranks implementation.</span>
        <span class="lang-vi">Planner nạp context theo thứ tự cứng: requirements → manual tests → business rules → source code. Ý định con người luôn thắng implementation.</span>
      </td>
    </tr>
    <tr>
      <td>LLM Delegation via CLI</td>
      <td>
        <span class="lang-en">Core never calls a model API directly — delegates through a local CLI (e.g. <code>claude</code>). No API keys in the repo.</span>
        <span class="lang-vi">Core không gọi model API trực tiếp — delegate qua local CLI (vd. <code>claude</code>). Không có API key trong repo.</span>
      </td>
    </tr>
    <tr>
      <td>Structured Output (Zod)</td>
      <td>
        <span class="lang-en">All LLM output (plans, generated code) is validated against Zod schemas before use. If parsing fails, the pipeline stops — no silent failures.</span>
        <span class="lang-vi">Mọi output từ LLM (plan, code) được validate qua Zod schema trước khi dùng. Nếu không parse được, pipeline dừng — không có silent failure.</span>
      </td>
    </tr>
    <tr>
      <td>Self-Healing Loop</td>
      <td>
        <span class="lang-en">On test failure: re-observe target → send error context to LLM → regenerate test → retry. Up to <code>maxHealAttempts</code>.</span>
        <span class="lang-vi">Khi test fail: re-observe target → gửi error context cho LLM → regenerate → retry. Tối đa <code>maxHealAttempts</code> lần.</span>
      </td>
    </tr>
    <tr>
      <td>Stability Gate</td>
      <td>
        <span class="lang-en">Each new test runs N consecutive times before acceptance. All N must pass. Flaky tests are quarantined and never committed to the suite.</span>
        <span class="lang-vi">Mỗi test mới chạy N lần liên tiếp trước khi accept. Tất cả N lần phải pass. Test flaky bị quarantine, không commit vào suite.</span>
      </td>
    </tr>
    <tr>
      <td>Cost Metering</td>
      <td>
        <span class="lang-en">Every LLM call is metered in USD. Runs abort automatically when the configured budget is exceeded.</span>
        <span class="lang-vi">Mọi LLM call được đo chi phí bằng USD. Run tự động abort khi vượt budget đã cấu hình.</span>
      </td>
    </tr>
  </tbody>
</table>

<h2>
  <span class="lang-en">Behavior when applied</span>
  <span class="lang-vi">Behavior khi apply</span>
</h2>

<h3>
  <span class="lang-en">First run</span>
  <span class="lang-vi">Chạy lần đầu</span>
</h3>

<pre><code>npx playwright install chromium     # One-time browser setup
npx ata config                      # Interactive setup: LLM provider, budget
npx ata explore myapp --manual --headed   # Optional: drive the browser yourself, record use cases
npx ata plan todomvc                # Propose plan only, no code generated
npx ata run todomvc                 # Full loop: explore → plan → [confirm] → generate → execute (+stability) → heal</code></pre>

<p class="lang-en">When <code>npx ata run</code> executes, the agent opens a browser, navigates to the configured URL (or reuses a saved <code>perception.json</code>), generates a PerceptionSnapshot, asks the LLM to plan, pauses for your approval, then generates Playwright spec files and runs them through the stability gate. If any fail, the healing loop kicks in automatically. Each run leaves behind a committable <code>tests/</code> directory plus <code>perception.json</code> (session reuse), a human-readable <code>plan.md</code> and machine <code>plan.json</code>, and per-use-case HAR network logs.</p>
<p class="lang-vi">Khi <code>npx ata run</code> chạy, agent mở browser, navigate đến URL trong config (hoặc tái dùng <code>perception.json</code> đã lưu), sinh PerceptionSnapshot, hỏi LLM để lên plan, dừng chờ bạn duyệt, sau đó sinh Playwright spec files và chạy qua stability gate. Nếu có fail, healing loop tự động chạy. Mỗi run để lại thư mục <code>tests/</code> có thể commit cùng <code>perception.json</code> (tái dùng session), <code>plan.md</code> cho người đọc và <code>plan.json</code> cho máy, và HAR network log theo từng use case.</p>

<h3>CI Gate</h3>

<pre><code>npx ata validate        # Run all targets, exit 0 if all pass verdict</code></pre>

<p class="lang-en">Plug into your CI pipeline to block merges when the test suite doesn't pass verdict thresholds (<code>minScenarios</code>, <code>mustPass</code>, stability).</p>
<p class="lang-vi">Cắm vào CI pipeline để block merge khi test suite không đạt verdict threshold (<code>minScenarios</code>, <code>mustPass</code>, stability).</p>

<h3>
  <span class="lang-en">Safety guardrails</span>
  <span class="lang-vi">Bảo vệ an toàn</span>
</h3>
<ul>
  <li class="lang-en">Production hosts refused by default — staging only unless explicitly allowlisted</li>
  <li class="lang-en">Private targets in <code>.targets/private/</code> (gitignored)</li>
  <li class="lang-en">Credentials from env vars, never YAML</li>
  <li class="lang-en">Action guardrails block dangerous verbs: <code>delete</code>, <code>pay</code>, <code>remove</code></li>

  <li class="lang-vi">Production host bị từ chối mặc định — chỉ staging trừ khi allowlist rõ ràng</li>
  <li class="lang-vi">Private targets trong <code>.targets/private/</code> (gitignored)</li>
  <li class="lang-vi">Credentials từ env vars, không bao giờ trong YAML</li>
  <li class="lang-vi">Action guardrail chặn verb nguy hiểm: <code>delete</code>, <code>pay</code>, <code>remove</code></li>
</ul>

<h2>
  <span class="lang-en">Configuration</span>
  <span class="lang-vi">Cấu hình</span>
</h2>

<h3>
  <span class="lang-en">File structure</span>
  <span class="lang-vi">Cấu trúc file</span>
</h3>

<pre><code>testagent.config.yaml        # Global: LLM provider, budget, stability runs
targets/
  todomvc.target.yaml        # Per-target: URL, auth, grounding, success criteria
  .targets/private/          # Gitignored private targets</code></pre>

<h3>
  <span class="lang-en">Example target</span>
  <span class="lang-vi">Ví dụ target config</span>
</h3>

<pre><code>name: todomvc
adapter: playwright-web
url: https://todomvc.com/examples/react
auth:
  strategy: none
grounding:
  requirements: docs/requirements.md
  manualTests:  docs/manual-tests.md
scope:
  include: ["todo list", "add item", "complete item"]
successCriteria:
  minScenarios: 5
  mustPass: ["add a todo item", "complete a todo item"]</code></pre>

<h2>Roadmap</h2>
<ul>
  <li class="lang-en"><strong>Phase 1 (current)</strong> — Web + Electron, reliability core (auth, stability gate, cost guard, healing, scope, CLI)</li>
  <li class="lang-en"><strong>Phase 2</strong> — REST API adapter + traceability report</li>
  <li class="lang-en"><strong>Phase 3</strong> — <code>--diff</code> mode (test only changed code) + Claude Code skill / MCP packaging</li>
  <li class="lang-en"><strong>Phase 4+</strong> — iOS, Android, vision fallback, policy engine</li>

  <li class="lang-vi"><strong>Phase 1 (hiện tại)</strong> — Web + Electron, reliability core (auth, stability gate, cost guard, healing, scope, CLI)</li>
  <li class="lang-vi"><strong>Phase 2</strong> — REST API adapter + traceability report</li>
  <li class="lang-vi"><strong>Phase 3</strong> — <code>--diff</code> mode (chỉ test code thay đổi) + Claude Code skill / MCP packaging</li>
  <li class="lang-vi"><strong>Phase 4+</strong> — iOS, Android, vision fallback, policy engine</li>
</ul>
