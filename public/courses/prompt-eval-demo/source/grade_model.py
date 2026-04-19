"""
Model-based grading — dùng Claude làm judge để chấm chất lượng output.
Phù hợp khi không có ground truth tuyệt đối (ví dụ: chấm reasoning, tone, độ hữu ích).

Usage:
    python grade_model.py
"""
import json
from pathlib import Path
import anthropic

client = anthropic.Anthropic()
JUDGE_MODEL = "claude-opus-4-7"

JUDGE_PROMPT = """You are grading a customer-support classifier's explanation quality.

Ticket: {ticket}
Category chosen: {category}
Reason given: {reason}

Score the REASON on a 1-5 scale:
  5 = clear, accurate, specific to this ticket
  3 = plausible but generic
  1 = wrong, vague, or irrelevant

Return JSON only: {{"score": <int 1-5>, "critique": "<one sentence>"}}"""


def judge_one(ticket: str, category: str, reason: str) -> dict:
    response = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": JUDGE_PROMPT.format(ticket=ticket, category=category, reason=reason),
        }],
    )
    text = next(b.text for b in response.content if b.type == "text")
    return json.loads(text)


def main():
    results = [json.loads(l) for l in Path("results.jsonl").read_text().splitlines() if l.strip()]

    scores = []
    for r in results:
        grade = judge_one(r["input"], r["output"]["category"], r["output"]["reason"])
        print(f"[{grade['score']}/5] id={r['id']}  {grade['critique']}")
        scores.append(grade["score"])

    avg = sum(scores) / len(scores)
    print(f"\nAverage reason-quality: {avg:.2f}/5  (n={len(scores)})")


if __name__ == "__main__":
    main()
