"""
05_01 -- Headless Eval Batches

Demonstrates how to execute bulk ADK evaluations via CLI and collect
system-wide pass/fail metrics. This is the bridge from manual
spot-checking to automated quality gates.
"""

import sys
from pathlib import Path

# Add parent dir so we can import shared helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import init_demo, run_adk_eval
init_demo()


# ---------------------------------------------------------------------------
# EVAL SUITE REGISTRY
# ---------------------------------------------------------------------------
EVAL_SUITES = [
    {
        "name": "Tool Recall (ch_02_04)",
        "agent": "ch_02_04_first_eval",
        "evalset": "ch_02_04_first_eval/tool_recall.test.json",
        "config": "ch_02_04_first_eval/test_config.json",
    },
    {
        "name": "Trajectory Rules (ch_04_02)",
        "agent": "ch_04_02_trajectory_matching",
        "evalset": "ch_04_02_trajectory_matching/trajectory_rules.test.json",
        "config": "ch_04_02_trajectory_matching/test_config.json",
    },
    {
        "name": "Memory Decay (ch_04_03)",
        "agent": "ch_04_03_testing_memory",
        "evalset": "ch_04_03_testing_memory/memory_decay.test.json",
        "config": "ch_04_03_testing_memory/test_config.json",
    },
    {
        "name": "System-Wide Batch (ch_05_01)",
        "agent": "ch_05_01_headless_eval_batches",
        "evalset": "ch_05_01_headless_eval_batches/system_wide.test.json",
        "config": "ch_05_01_headless_eval_batches/test_config.json",
    },
]


def main():
    print("HEADLESS EVAL BATCH")
    print("=" * 60)

    results = []
    for suite in EVAL_SUITES:
        print(f"\n  Running: {suite['name']}...")
        r = run_adk_eval(suite["agent"], suite["evalset"], suite["config"])
        results.append({"name": suite["name"], **r})
        status = "PASS" if r["failed"] == 0 and r["passed"] > 0 else "FAIL"
        print(f"  Result:  {r['passed']} passed, {r['failed']} failed  [{status}]")

    # Dashboard
    print("\n" + "=" * 60)
    print("SYSTEM-WIDE DASHBOARD")
    print("=" * 60)
    print(f"  {'Suite':<35} {'Passed':>8} {'Failed':>8} {'Status':>8}")
    print(f"  {'-'*35} {'-'*8} {'-'*8} {'-'*8}")

    total_passed = 0
    total_failed = 0
    for r in results:
        total_passed += r["passed"]
        total_failed += r["failed"]
        status = "PASS" if r["failed"] == 0 and r["passed"] > 0 else "FAIL"
        print(f"  {r['name']:<35} {r['passed']:>8} {r['failed']:>8} {status:>8}")

    print(f"  {'-'*35} {'-'*8} {'-'*8} {'-'*8}")
    overall = "PASS" if total_failed == 0 else "FAIL"
    print(f"  {'TOTAL':<35} {total_passed:>8} {total_failed:>8} {overall:>8}")
    print()

    sys.exit(0 if total_failed == 0 else 1)


if __name__ == "__main__":
    main()
