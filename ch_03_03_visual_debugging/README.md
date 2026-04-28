# 03_03 — Visual Debugging with ADK Trace View

Use the ADK Web UI to step through a stalling agent's Thought-Action-Observation loop and diagnose the infinite cycle visually.

**Learning goal:** Read a cyclic trace in the ADK trace viewer and identify the tool observation that triggers the loop.

| File | Purpose |
|------|---------|
| `agent.py` | Agent with a deliberate stalling condition |
| `run_agent.py` | Runner that produces the failed trace for inspection |

## Usage

```bash
# Step 1 — generate the failed trace in the terminal
python ch_03_03_visual_debugging/run_agent.py

# Step 2 — open the visual trace viewer
# Run from the repo root:
adk web --allow_origins='*'
```

> **GitHub Codespaces note:** The `--allow_origins='*'` flag is required because
> Codespaces forwards port 8000 through a proxy that changes the request origin.
> Without it, `POST /sessions` returns `403 Forbidden` when creating a new chat session.
> This flag is safe for local/Codespaces development — do not use it in production.

Select `ch_03_03_visual_debugging` in the agent dropdown, send the same prompt, and explore the cyclic trace in the right-hand panel.

**Expected output:** Five repeating `check_approval_status` rows visible in the trace viewer — four pending, one `SYSTEM_TIMEOUT`.
