# 04_01 — Capturing Golden Traces

Record a manually verified success trajectory and persist it as a reusable golden regression case in an evalset file.

**Learning goal:** Understand the golden trace capture workflow — from live agent run to saved evalset — and why these traces are the foundation of all downstream evaluation.

| File | Purpose |
|------|---------|
| `agent.py` | Procurement agent used for trace capture |
| `procurement_agent.evalset.json` | Pre-captured golden evalset |
| `checklist.md` | Manual verification checklist for golden trace review |
| `run_agent.py` | Demo runner to generate a fresh trace |

## Usage

```bash
# Run from repo root (programmatic)
python ch_04_01_capturing_golden_traces/run_agent.py

# Or capture via ADK Web UI (run from repo root)
adk web --allow_origins='*'
```

> **GitHub Codespaces note:** `--allow_origins='*'` is required to avoid `403 Forbidden` on session creation through the Codespaces port proxy.

In the Web UI: select `ch_04_01_capturing_golden_traces`, run a prompt, then go to the **Eval** tab and click **Add current session**.

**Expected output:** A `.evalset.json` file with the agent's verified tool trajectory saved as a golden case.
