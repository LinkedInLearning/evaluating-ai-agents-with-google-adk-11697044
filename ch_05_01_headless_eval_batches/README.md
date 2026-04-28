# 05_01 — Running Headless Eval Batches

Execute bulk ADK evaluations via CLI across multiple chapters and generate a system-wide pass/fail dashboard.

**Learning goal:** Run evals programmatically without a human in the loop, and interpret aggregate score reports across an evalset suite.

| File | Purpose |
|------|---------|
| `agent.py` | Procurement agent under batch evaluation |
| `system_wide.test.json` | Multi-scenario evalset for batch runs |
| `test_config.json` | Batch evaluation criteria |
| `run_agent.py` | Headless batch runner with dashboard output |

## Usage

```bash
# Run from repo root
python ch_05_01_headless_eval_batches/run_agent.py
```

**Expected output:** A formatted dashboard showing pass/fail counts across all evalset cases with per-case scores.
