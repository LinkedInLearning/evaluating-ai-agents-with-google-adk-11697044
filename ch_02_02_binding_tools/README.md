# 02_02 — Binding Tools

Add real capabilities to the agent by binding Python functions as tools and observe the first populated Thought-Action-Observation trajectory.

**Learning goal:** See how ADK introspects function signatures and docstrings to generate tool schemas, and why tool binding is the inflection point that makes behavior formally evaluable.

| File | Purpose |
|------|---------|
| `agent.py` | Agent with `check_catalog`, `check_budget`, `place_order`, `refuse_request` bound |
| `run_agent.py` | Demo showing the populated trajectory vs. ch_02_01's empty one |

## Usage

```bash
# Run from repo root
python ch_02_02_binding_tools/run_agent.py
```

**Expected output:** `TRAJECTORY: ['check_catalog', 'check_budget', 'place_order']` — the first evaluable execution path.
