"""
Running the eval — chạy prompt qua dataset và lưu output để grade.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python run_eval.py
"""
import json
from pathlib import Path
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-opus-4-7"

PROMPT_TEMPLATE = """Classify this customer support ticket into exactly one category.
Categories: shipping, account, quality, billing, technical

Return JSON only: {{"category": "<one-category>", "reason": "<one sentence>"}}

Ticket: {ticket}"""


def run_one(ticket: str) -> dict:
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(ticket=ticket)}],
    )
    text = next(b.text for b in response.content if b.type == "text")
    return json.loads(text)


def main():
    dataset = [json.loads(l) for l in Path("dataset.jsonl").read_text().splitlines() if l.strip()]
    results = []
    for row in dataset:
        print(f"[{row['id']}] running...", flush=True)
        output = run_one(row["input"])
        results.append({**row, "output": output})
        print(f"       → {output['category']}")

    Path("results.jsonl").write_text("\n".join(json.dumps(r) for r in results))
    print(f"\nSaved {len(results)} results to results.jsonl")


if __name__ == "__main__":
    main()
