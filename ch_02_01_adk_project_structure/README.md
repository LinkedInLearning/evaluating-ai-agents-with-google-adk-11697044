# 02_01 — ADK Project Structure

Set up the standard ADK project layout required for the CLI toolchain to discover, load, and evaluate your agent.

**Learning goal:** Understand the three-file convention (`__init__.py`, `agent.py`, `run_agent.py`) and validate graceful degradation with a tool-free baseline agent.

| File | Purpose |
|------|---------|
| `__init__.py` | Package registration — the ADK discovery contract |
| `agent.py` | Tool-free baseline agent that verifies graceful degradation |
| `run_agent.py` | Baseline demo producing an empty trajectory |

## Usage

```bash
# Run from repo root
python ch_02_01_adk_project_structure/run_agent.py
```

**Expected output:** `TRAJECTORY: []` — zero tool calls, confirming the instruction layer handles capability absence correctly.
