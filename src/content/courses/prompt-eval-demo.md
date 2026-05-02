---
title: Prompt Eval 101
tagline: PROMPT EVAL · 101
description: Evaluate an AI prompt in 30 seconds — classify support tickets with Claude, then use an LLM judge to grade the reasoning.
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
