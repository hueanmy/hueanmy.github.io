"""
Streamlit UI cho prompt eval demo.

Usage:
    pip install streamlit anthropic
    streamlit run app.py                           # mock mode — no API key needed
    ANTHROPIC_API_KEY=sk-ant-... streamlit run app.py   # live mode
"""
import json
import os
import re
import time
from pathlib import Path

import anthropic
import streamlit as st


def _extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise

MODEL = "claude-opus-4-7"
JUDGE_MODEL = "claude-opus-4-7"

# Pre-computed outputs for mock mode — realistic, includes intentional failures.
MOCK_CLASSIFY = {
    "1": {"category": "shipping", "reason": "The customer reports a 2-week delay on order #1234, which is a delivery issue."},
    "2": {"category": "account", "reason": "Password reset is a standard account-management request."},
    "3": {"category": "quality", "reason": "The product physically broke after short use, indicating a product quality problem."},
    "4": {"category": "billing", "reason": "A refund request relates directly to billing and payments."},
    "5": {"category": "technical", "reason": "App crashes on a specific OS version is a technical/software issue."},
    "6": {"category": "shipping", "reason": "Package marked delivered but not received — a delivery/shipping issue."},
    "7": {"category": "billing", "reason": "Duplicate charge on the same order is clearly a billing problem."},
    # Intentional FAIL for demo purposes — misclassified as 'account' instead of 'technical'.
    "8": {"category": "account", "reason": "Login button not working suggests the customer cannot access their account."},
}

MOCK_JUDGE = {
    "1": {"score": 5, "critique": "Specific — references the 2-week delay and order number."},
    "2": {"score": 3, "critique": "Correct but generic; could mention 'reset password' explicitly."},
    "3": {"score": 5, "critique": "Tight reasoning tying 'broke' to product quality."},
    "4": {"score": 4, "critique": "Accurate; slightly thin explanation."},
    "5": {"score": 5, "critique": "Notes both the crash and the OS version context."},
    "6": {"score": 5, "critique": "Identifies the delivery discrepancy precisely."},
    "7": {"score": 5, "critique": "Clear — 'duplicate charge' maps directly to billing."},
    "8": {"score": 2, "critique": "Reason sounds plausible but the category is wrong — this is a technical bug."},
}


def is_mock_mode() -> bool:
    return not os.environ.get("ANTHROPIC_API_KEY")

CLASSIFY_PROMPT = """Classify this customer support ticket into exactly one category.
Categories: shipping, account, quality, billing, technical

Return JSON only: {{"category": "<one-category>", "reason": "<one sentence>"}}

Ticket: {ticket}"""

JUDGE_PROMPT = """You are grading a customer-support classifier's explanation quality.

Ticket: {ticket}
Category chosen: {category}
Reason given: {reason}

Score the REASON on a 1-5 scale:
  5 = clear, accurate, specific to this ticket
  3 = plausible but generic
  1 = wrong, vague, or irrelevant

Return JSON only: {{"score": <int 1-5>, "critique": "<one sentence>"}}"""


@st.cache_resource
def get_client():
    return anthropic.Anthropic()


def load_dataset():
    path = Path(__file__).parent / "dataset.jsonl"
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def run_classifier(row: dict) -> dict:
    if is_mock_mode():
        time.sleep(0.6)  # simulate network latency for demo pacing
        return MOCK_CLASSIFY[row["id"]]
    resp = get_client().messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": CLASSIFY_PROMPT.format(ticket=row["input"])}],
    )
    text = next(b.text for b in resp.content if b.type == "text")
    return _extract_json(text)


def run_judge(row: dict, category: str, reason: str) -> dict:
    if is_mock_mode():
        time.sleep(0.5)
        return MOCK_JUDGE[row["id"]]
    resp = get_client().messages.create(
        model=JUDGE_MODEL,
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": JUDGE_PROMPT.format(ticket=row["input"], category=category, reason=reason),
        }],
    )
    text = next(b.text for b in resp.content if b.type == "text")
    return _extract_json(text)


st.set_page_config(page_title="Prompt Eval Demo", layout="wide")

st.markdown("""
<style>
  /* Hide Streamlit chrome for video recording */
  #MainMenu, header, footer, .stDeployButton, [data-testid="stToolbar"] { visibility: hidden !important; height: 0 !important; }

  /* Tighter layout for 9:16 */
  section.main > div.block-container {
    padding: 1.2rem 1.4rem !important;
    max-width: 100% !important;
  }

  .stApp { background: #0a0a12 !important; }

  /* Title with purple glow — match daily-video style */
  h1 {
    font-weight: 900 !important;
    font-size: 3.2rem !important;
    letter-spacing: -0.03em !important;
    line-height: 1.05 !important;
    background: linear-gradient(135deg, #E0D9FF 0%, #9F91E6 70%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    text-shadow: 0 0 60px rgba(159, 145, 230, 0.35);
    padding: 0.5rem 0 !important;
  }

  h2, h3 { color: #E0D9FF !important; font-weight: 700 !important; }

  [data-testid="stCaptionContainer"] { color: #8B8B9C !important; }

  /* Purple buttons */
  .stButton > button {
    background: linear-gradient(135deg, #9F91E6 0%, #7B6FD1 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    padding: 0.7rem 1.6rem !important;
    box-shadow: 0 6px 24px rgba(159, 145, 230, 0.35) !important;
    transition: transform 0.15s !important;
  }
  .stButton > button:hover { transform: translateY(-1px); }

  /* Tabs — purple active */
  button[role="tab"] { color: #8B8B9C !important; font-weight: 600 !important; font-size: 1.05rem !important; }
  button[role="tab"][aria-selected="true"] { color: #C4B5FD !important; }
  button[role="tab"][aria-selected="true"]::after { background: #9F91E6 !important; }

  /* Cards */
  [data-testid="stCodeBlock"], [data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden !important;
  }
  [data-testid="stCodeBlock"] pre { background: #16161f !important; }

  /* Metrics */
  [data-testid="stMetricValue"] { color: #C4B5FD !important; font-weight: 900 !important; }
  [data-testid="stMetricLabel"] { color: #8B8B9C !important; }

  /* Banners */
  [data-testid="stInfo"] {
    background: rgba(159, 145, 230, 0.08) !important;
    border-left: 3px solid #9F91E6 !important;
    border-radius: 12px !important;
  }
  [data-testid="stSuccess"] {
    background: rgba(34, 197, 94, 0.08) !important;
    border-left: 3px solid #22c55e !important;
    border-radius: 12px !important;
  }

  /* Progress */
  [data-testid="stProgressBar"] > div > div { background: linear-gradient(90deg, #9F91E6, #C4B5FD) !important; }
</style>
""", unsafe_allow_html=True)

st.title("Prompt Eval 🎯")
st.caption("Anthropic course · Chapter: Prompt evaluation")

if is_mock_mode():
    st.info("🎭 Demo mode — mock outputs")
else:
    st.success("🔑 Live — real Claude API")

if "results" not in st.session_state:
    st.session_state.results = None
if "code_graded" not in st.session_state:
    st.session_state.code_graded = None
if "model_graded" not in st.session_state:
    st.session_state.model_graded = None

dataset = load_dataset()

tab_data, tab_run, tab_code, tab_model = st.tabs([
    "1. Dataset",
    "2. Running the eval",
    "3. Code-based grading",
    "4. Model-based grading",
])

with tab_data:
    st.subheader("Test dataset")
    st.write(f"**{len(dataset)}** customer support tickets. Each has a ground-truth category.")
    st.dataframe(
        [{"id": r["id"], "input": r["input"], "expected_category": r["expected_category"]}
         for r in dataset],
        use_container_width=True,
        hide_index=True,
    )

with tab_run:
    st.subheader("Run prompt across dataset")
    st.code(CLASSIFY_PROMPT, language="text")

    if st.button("▶ Run eval", type="primary", key="run"):
        progress = st.progress(0, text="Starting…")
        rows = []
        container = st.empty()

        for i, row in enumerate(dataset, 1):
            progress.progress(i / len(dataset), text=f"[{i}/{len(dataset)}] {row['input'][:60]}…")
            out = run_classifier(row)
            rows.append({**row, "output": out})
            container.dataframe(
                [{"id": r["id"], "input": r["input"][:50] + "…",
                  "predicted": r["output"]["category"],
                  "reason": r["output"]["reason"]} for r in rows],
                use_container_width=True, hide_index=True,
            )

        st.session_state.results = rows
        st.session_state.code_graded = None
        st.session_state.model_graded = None
        progress.empty()
        st.success(f"Done. {len(rows)} results ready for grading.")

with tab_code:
    st.subheader("Code-based grading — exact match on category")
    st.caption("Fast, free, deterministic. Works when ground truth is crisp.")

    if st.session_state.results is None:
        st.info("Run the eval in tab 2 first.")
    else:
        if st.button("✓ Grade by code", key="grade_code"):
            graded = []
            for r in st.session_state.results:
                expected = r["expected_category"].strip().lower()
                actual = r["output"]["category"].strip().lower()
                graded.append({**r, "passed": expected == actual})
            st.session_state.code_graded = graded

        if st.session_state.code_graded:
            graded = st.session_state.code_graded
            passed = sum(1 for r in graded if r["passed"])
            col1, col2 = st.columns(2)
            col1.metric("Accuracy", f"{passed / len(graded):.1%}")
            col2.metric("Passed", f"{passed}/{len(graded)}")

            st.dataframe(
                [{"id": r["id"],
                  "expected": r["expected_category"],
                  "predicted": r["output"]["category"],
                  "result": "✅ PASS" if r["passed"] else "❌ FAIL"}
                 for r in graded],
                use_container_width=True, hide_index=True,
            )

with tab_model:
    st.subheader("Model-based grading — Claude judges the reasoning")
    st.caption("Use when there's no crisp ground truth (tone, explanation quality, helpfulness).")
    st.code(JUDGE_PROMPT, language="text")

    if st.session_state.results is None:
        st.info("Run the eval in tab 2 first.")
    else:
        if st.button("⭐ Grade by model", key="grade_model"):
            progress = st.progress(0, text="Judging…")
            graded = []
            container = st.empty()

            for i, r in enumerate(st.session_state.results, 1):
                progress.progress(i / len(st.session_state.results),
                                  text=f"[{i}/{len(st.session_state.results)}] judging…")
                judgment = run_judge(r, r["output"]["category"], r["output"]["reason"])
                graded.append({**r, "judgment": judgment})
                container.dataframe(
                    [{"id": x["id"],
                      "score": f"{x['judgment']['score']}/5",
                      "predicted": x["output"]["category"],
                      "reason": x["output"]["reason"],
                      "critique": x["judgment"]["critique"]} for x in graded],
                    use_container_width=True, hide_index=True,
                )

            progress.empty()
            st.session_state.model_graded = graded

        if st.session_state.model_graded:
            graded = st.session_state.model_graded
            avg = sum(r["judgment"]["score"] for r in graded) / len(graded)
            st.metric("Average reasoning quality", f"{avg:.2f} / 5")
