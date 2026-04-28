"""
05_03 -- Pass@k and Non-Determinism

Runs the same evalset k times against the agent and calculates Pass@k --
the probability that at least one of k independent runs produces a
correct trajectory. This quantifies whether failures are genuine bugs
or stochastic noise from LLM sampling.

Pass@k formula (unbiased estimator):
  Pass@k = 1 - C(n-c, k) / C(n, k)

Where:
  n = total runs, c = number of passing runs, k = sample size
"""

import sys
from pathlib import Path

# Add parent dir so we can import shared helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import init_demo, run_adk_eval
init_demo()


# ---------------------------------------------------------------------------
# PASS@K FORMULA
# ---------------------------------------------------------------------------
def pass_at_k(n: int, c: int, k: int) -> float:
    """Calculate Pass@k using the numerically stable product form.

    Args:
        n: Total number of independent runs.
        c: Number of runs that passed.
        k: Sample size (how many attempts does the user get).

    Returns:
        Probability that at least 1 of k attempts passes.
    """
    if n - c < k:
        return 1.0
    # Product form avoids large binomial coefficient overflow:
    #   Pass@k = 1 - prod_{i=0}^{k-1} (n - c - i) / (n - i)
    result = 1.0
    for i in range(k):
        result *= (n - c - i) / (n - i)
    return 1.0 - result


def main():
    # Number of independent runs
    K = 5

    print(f"PASS@K RELIABILITY ANALYSIS  (k={K})")
    print("=" * 60)

    # Run the evalset k times
    run_results = []
    for i in range(1, K + 1):
        print(f"\n  Run {i}/{K}...", end=" ", flush=True)
        r = run_adk_eval(
            "ch_05_03_pass_at_k",
            "ch_05_03_pass_at_k/pass_at_k.test.json",
            "ch_05_03_pass_at_k/test_config.json",
        )
        run_results.append(r)
        print(f"{r['passed']} passed, {r['failed']} failed")

    # Aggregate: count how many runs had zero failures
    total_runs = len(run_results)
    perfect_runs = sum(1 for r in run_results if r["failed"] == 0)

    # Calculate Pass@k for k=1, k=3, k=5
    print("\n" + "=" * 60)
    print("PASS@K RESULTS")
    print("=" * 60)
    print(f"  Total runs (n):     {total_runs}")
    print(f"  Perfect runs (c):   {perfect_runs}")
    print(f"  {'k':<8} {'Pass@k':>10}  Interpretation")
    print(f"  {'-'*8} {'-'*10}  {'-'*30}")

    for k_val in [1, 3, 5]:
        if k_val > total_runs:
            continue
        score = pass_at_k(total_runs, perfect_runs, k_val)
        if score >= 0.95:
            tag = "RELIABLE"
        elif score >= 0.70:
            tag = "MARGINAL"
        else:
            tag = "UNRELIABLE"
        print(f"  {k_val:<8} {score:>9.1%}  {tag}")

    # Per-run breakdown
    print(f"\n{'  Run':<8} {'Passed':>8} {'Failed':>8} {'Status':>8}")
    print(f"  {'-'*4} {'-'*8} {'-'*8} {'-'*8}")
    for i, r in enumerate(run_results, 1):
        status = "PASS" if r["failed"] == 0 else "FAIL"
        print(f"  {i:<4} {r['passed']:>8} {r['failed']:>8} {status:>8}")

    print()
    sys.exit(0 if perfect_runs == total_runs else 1)


if __name__ == "__main__":
    main()
