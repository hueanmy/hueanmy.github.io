---
title: Prompt Eval 101
tagline: PROMPT EVAL · 101
description: Đánh giá một AI prompt trong 30 giây — phân loại support ticket bằng Claude, sau đó dùng LLM judge để chấm điểm lập luận.
description_en: Evaluate an AI prompt in 30 seconds — classify support tickets with Claude, then use an LLM judge to grade the reasoning.
video: /courses/prompt-eval-demo/demo.mp4
videoFull: /courses/prompt-eval-demo/full.mp4
thumbnail: /courses/prompt-eval-demo/thumbnail.png
duration: '0:45'
date: 2026-04-20
tags: [Python, Streamlit, Claude, Evaluation]
courseUrl: https://anthropic.skilljar.com/claude-with-the-anthropic-api
sourceDir: /courses/prompt-eval-demo/source
sourceFiles:
  - app.py
  - run_eval.py
  - grade_code.py
  - grade_model.py
  - dataset.jsonl
  - requirements.txt
featured: true
order: 3
---

<div class="lang-vi">

Demo end-to-end nhỏ gọn để hiểu cách evaluate một classifier prompt:

1. **Phân loại** ticket hỗ trợ khách hàng thành 1 trong 5 danh mục bằng Claude.
2. **Chấm điểm lập luận** bằng một Claude call thứ hai đóng vai judge (thang điểm 1–5).
3. **Phát hiện lỗi** — ticket #8 bị phân loại sai cố ý để bạn thấy một row xấu trông như thế nào.

Mock mode chạy offline với output đã tính sẵn, bạn có thể tương tác với UI trước khi cắm API key.

### Chạy local

```bash
pip install -r requirements.txt
streamlit run app.py                     # mock mode
ANTHROPIC_API_KEY=sk-ant-… streamlit run app.py   # live mode
```

</div>

<div class="lang-en">

A tiny end-to-end demo showing how to evaluate a classifier prompt:

1. **Classify** customer-support tickets into one of 5 categories using Claude.
2. **Grade the reasoning** with a second Claude call acting as judge (1–5 score).
3. **Spot a failure** — ticket #8 is intentionally misclassified so you can see what a bad row looks like.

Mock mode runs offline with pre-computed outputs, so you can play with the UI before plugging in an API key.

### Run locally

```bash
pip install -r requirements.txt
streamlit run app.py                     # mock mode
ANTHROPIC_API_KEY=sk-ant-… streamlit run app.py   # live mode
```

</div>
