"""
06_02 -- Groundedness and Faithfulness Checks

Demonstrates ADK's hallucinations_v1 criterion, which uses an LLM judge
to verify that every sentence in the agent's response is grounded in
actual tool outputs. A two-step process segments the response into
sentences, then labels each as supported, unsupported, or contradictory.
"""

import json
import sys
from pathlib import Path

# Add parent dir so we can import shared helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import init_demo, run_agent, run_adk_eval, parse_eval_results, clean_eval_history
init_demo()

from agent import root_agent


def _load_scenarios(evalset_path: Path) -> list:
    """Load eval cases from the evalset JSON — single source of truth."""
    data = json.loads(evalset_path.read_text())
    scenarios = []
    for case in data.get("eval_cases", []):
        eval_id = case.get("eval_id", "unknown")
        prompt = ""
        for turn in case.get("conversation", []):
            uc = turn.get("user_content", {})
            for part in uc.get("parts", []):
                if part.get("text"):
                    prompt = part["text"]
                    break
            if prompt:
                break
        scenarios.append({"eval_id": eval_id, "prompt": prompt})
    return scenarios


def main():
    chapter_dir = Path(__file__).resolve().parent
    clean_eval_history(chapter_dir)
    scenarios = _load_scenarios(chapter_dir / "groundedness.test.json")

    print("GROUNDEDNESS AND FAITHFULNESS CHECKS")
    print("=" * 60)
    print()
    print("  Criterion:  hallucinations_v1")
    print("  Threshold:  0.8  (80% of sentences must be grounded)")
    print("  Scope:      final + intermediate responses")
    print()

    # Run agent live against every eval case
    for s in scenarios:
        print(f"--- {s['eval_id']} ---")
        run_agent(root_agent, s["prompt"], session_id=s["eval_id"])
        print()

    # Formal groundedness evaluation
    print("  Running adk eval with hallucinations_v1 judge ...")
    print()

    r = run_adk_eval(
        "ch_06_02_groundedness_checks",
        "ch_06_02_groundedness_checks/groundedness.test.json",
        "ch_06_02_groundedness_checks/test_config.json",
    )

    # Parse per-case results from eval history
    case_results = parse_eval_results(chapter_dir)

    # Display scorecard
    print("-" * 60)
    print("GROUNDEDNESS SCORECARD")
    print("-" * 60)
    print(f"  {'Case':<40} {'Score':>6} {'Status':>8}")
    print(f"  {'-'*40} {'-'*6} {'-'*8}")

    for case in case_results:
        status = "PASS" if case["passed"] else "FAIL"
        score_str = f"{case['groundedness_score']:.2f}" if case["groundedness_score"] is not None else "N/A"
        print(f"  {case['eval_id']:<40} {score_str:>6} {status:>8}")

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Cases passed: {r['passed']}")
    print(f"  Cases failed: {r['failed']}")
    print(f"  Overall:      {'PASS' if r['failed'] == 0 else 'FAIL'}")
    print("=" * 60)

    sys.exit(0 if r["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
