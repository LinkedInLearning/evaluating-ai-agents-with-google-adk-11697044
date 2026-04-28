# 01_03 — The Policy Violation

Demonstrate how an unguarded agent silently approves a purchase that violates corporate policy. This is the motivating failure the rest of the course teaches you to detect and prevent.

**Learning goal:** Understand why a correct-sounding final answer can hide a policy-violating execution path.

| File | Purpose |
|------|---------|
| `agent.py` | Agent without policy guardrails |
| `run_agent.py` | Scenario that produces the silent policy violation |

## Usage

```bash
# Run from repo root
python ch_01_03_policy_violation/run_agent.py
```

**Expected output:** Agent approves a restricted purchase — the final answer sounds correct, but the trajectory reveals a policy violation.
