"""
06_01 -- LLM-as-a-Judge: Custom Rubrics

Demonstrates ADK's rubric_based_final_response_quality_v1 criterion,
which uses a second LLM to judge the qualitative aspects of the agent's
responses against custom rubrics (tone, professionalism, refusal quality).

This is the bridge from "did the agent call the right tools?" (trajectory)
to "did the agent communicate well?" (qualitative judgment).
"""

import sys
from pathlib import Path

# Add parent dir so we can import shared helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import init_demo, run_adk_eval, parse_eval_results, clean_eval_history
init_demo()


def main():
    chapter_dir = Path(__file__).resolve().parent
    clean_eval_history(chapter_dir)

    print("LLM-AS-A-JUDGE: RUBRIC EVALUATION")
    print("=" * 60)
    print()
    print("  Rubrics under test:")
    print("    1. professional_tone")
    print("    2. actionable_detail")
    print("    3. refusal_justification")
    print("    4. no_hallucinated_data")
    print()
    print("  Running adk eval with LLM judge...")
    print()

    r = run_adk_eval(
        "ch_06_01_llm_as_a_judge",
        "ch_06_01_llm_as_a_judge/judge_rubrics.test.json",
        "ch_06_01_llm_as_a_judge/test_config.json",
    )

    # Parse per-rubric results from eval history
    case_results = parse_eval_results(chapter_dir)

    # Display per-case rubric scorecard
    print("-" * 60)
    print("PER-CASE RUBRIC SCORECARD")
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
