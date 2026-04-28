# 02_03 — Pydantic Enforcement

Lock down tool input contracts with Pydantic schemas so the agent cannot pass malformed, missing, or out-of-range arguments.

**Learning goal:** Understand how Pydantic schema validation eliminates a class of trajectory failures caused by formatting errors at tool boundaries.

| File | Purpose |
|------|---------|
| `agent.py` | Agent with Pydantic-validated tool schemas and regex constraints |
| `run_agent.py` | Contrastive demo: clean input vs. dirty input with schema enforcement |

## Usage

```bash
# Run from repo root
python ch_02_03_pydantic_enforcement/run_agent.py
```

**Expected output:** Schema validation intercepts malformed inputs before tool execution, producing a `ValidationError` instead of a silent bad call.
