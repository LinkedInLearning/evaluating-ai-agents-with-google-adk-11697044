# 01_02 — The Procurement Agent

Meet the procurement agent — the AI system we evaluate throughout this course. It processes purchase requests against a catalog, budget, and policy database using four tools.

**Learning goal:** Observe the first Thought-Action-Observation loop and understand why trajectory evaluation is necessary.

| File | Purpose |
|------|---------|
| `agent.py` | Procurement agent definition with four tools and SOP instruction |
| `run_agent.py` | Two contrastive scenarios: budget-frozen refusal vs. approved order |

## Usage

```bash
# Run from repo root
python ch_01_02_procurement_agent/run_agent.py
```

**Expected output:** Two trajectories — `[check_catalog, check_budget, refuse_request]` for the refused scenario (ineligible department + frozen budget) and `[check_catalog, check_budget, place_order]` for the approved order. Both follow the same 3-step SOP, diverging only at step 3.

