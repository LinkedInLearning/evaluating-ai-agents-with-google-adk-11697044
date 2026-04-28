"""
06_03 -- Safe Refusal via Negative Logic

Demonstrates ADK's rubric_based_tool_use_quality_v1 criterion with
negative-logic rubrics: assertions about what the agent must NOT do.
Previous chapters tested positive behavior (call X, respond with Y).
This chapter tests guardrails (do NOT call place_order on restricted items).
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
    scenarios = _load_scenarios(chapter_dir / "safe_refusal.test.json")

    print("SAFE REFUSAL: NEGATIVE LOGIC EVALUATION")
    print("=" * 60)
    print()
    print("  Criteria:")
    print("    Tool-use rubrics  (threshold: 1.0)")
    print("      1. no_order_on_restricted")
    print("      2. no_order_on_frozen_budget")
    print("      3. no_budget_check_on_restricted")
    print("    Response rubrics  (threshold: 0.8)")
    print("      4. refuses_with_reason")
    print()

    # Run agent live against every eval case
    for s in scenarios:
        print(f"--- {s['eval_id']} ---")
        run_agent(root_agent, s["prompt"], session_id=s["eval_id"])
        print()

    # Formal negative-logic evaluation
    print("  Running adk eval with negative-logic judge...")
    print()

    r = run_adk_eval(
        "ch_06_03_safe_refusal",
        "ch_06_03_safe_refusal/safe_refusal.test.json",
        "ch_06_03_safe_refusal/test_config.json",
    )

    # Parse per-rubric results from eval history
    case_results = parse_eval_results(chapter_dir)

    # Display per-case rubric scorecard
    print("-" * 60)
    print("SAFE REFUSAL SCORECARD")
    print("-" * 60)

    for case in case_results:
        status = "PASS" if case["passed"] else "FAIL"
        print(f"\n  [{status}] {case['eval_id']}")
        for rs in case["rubric_scores"]:
            verdict = "YES" if rs["score"] >= 0.5 else "NO"
            print(f"         {rs['rubric_id']:<30} {verdict}")

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
