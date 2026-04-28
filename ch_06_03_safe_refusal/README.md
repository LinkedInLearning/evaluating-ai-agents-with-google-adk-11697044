# 06_03 — Safe Refusal via Negative Logic

Enforce guardrails that verify the agent does NOT call forbidden tools on policy-violating requests, using ADK's `rubric_based_tool_use_quality_v1` criterion.

**Learning goal:** Write negative logic rubrics ("must NOT call X") and understand why safe refusal evaluation requires separate evalset cases from positive-path tests.

| File | Purpose |
|------|---------|
| `agent.py` | Agent with safe refusal instruction |
| `safe_refusal.test.json` | Evalset with forbidden-tool scenarios |
| `test_config.json` | Negative logic rubric config |
| `run_agent.py` | Eval runner validating guardrail enforcement |

## Usage

```bash
# Run from repo root
python ch_06_03_safe_refusal/run_agent.py
```

**Expected output:** Pass/fail per forbidden-tool scenario — confirming `place_order` is never called on restricted items.
