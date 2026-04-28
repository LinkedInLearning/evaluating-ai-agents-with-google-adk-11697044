# 06_02 — Groundedness and Faithfulness Checks

Verify that every claim in the agent's response is grounded in actual tool outputs using ADK's `hallucinations_v1` criterion.

**Learning goal:** Understand the two-stage groundedness evaluation pipeline (segmenter + validator) and detect unsupported or contradictory claims.

| File | Purpose |
|------|---------|
| `agent.py` | Agent evaluated for response grounding |
| `groundedness.test.json` | Evalset with grounded and hallucinated response scenarios |
| `test_config.json` | Groundedness evaluation config using `hallucinations_v1` |
| `run_agent.py` | Eval runner: shows evidence chain, agent response, and aggregate score per case |

## Usage

```bash
# Run from repo root
python ch_06_02_groundedness_checks/run_agent.py
```

**Expected output:** For each eval case: the user prompt, the evidence chain (tool calls + results), the agent's full response, and the `hallucinations_v1` aggregate score with PASS/FAIL status. A summary scorecard follows.


> **Note:** The `hallucinations_v1` judge performs sentence-level segmentation and validation internally, but only the aggregate score (0.0–1.0) is written to the eval history. This is standard for CLI-based evaluation frameworks.
