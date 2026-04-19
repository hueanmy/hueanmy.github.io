"""
Code-based grading — so sánh trực tiếp bằng code (exact match).
Nhanh, rẻ, deterministic. Phù hợp khi output có ground truth rõ ràng.

Usage:
    python grade_code.py
"""
import json
from pathlib import Path


def grade_one(expected: str, actual: str) -> bool:
    return expected.strip().lower() == actual.strip().lower()


def main():
    results = [json.loads(l) for l in Path("results.jsonl").read_text().splitlines() if l.strip()]

    passed = 0
    for r in results:
        actual = r["output"]["category"]
        expected = r["expected_category"]
        ok = grade_one(expected, actual)
        marker = "PASS" if ok else "FAIL"
        print(f"[{marker}] id={r['id']}  expected={expected:<10} got={actual}")
        if ok:
            passed += 1

    accuracy = passed / len(results)
    print(f"\nAccuracy: {passed}/{len(results)} = {accuracy:.1%}")


if __name__ == "__main__":
    main()
