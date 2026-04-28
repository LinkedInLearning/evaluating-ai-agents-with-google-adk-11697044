# 03_01 — Trap Mocks

Stress-test agent reasoning using adversarial tool observations that return valid but semantically conflicting data.

**Learning goal:** Learn how to engineer trap mocks that expose brittle decision logic the agent would pass on clean data.

| File | Purpose |
|------|---------|
| `agent.py` | Agent wired to trap mock tools with hidden semantic conflicts |
| `run_agent.py` | Adversarial scenarios: budget trap, compliance flag trap, vendor trap |

## Usage

```bash
# Run from repo root
python ch_03_01_trap_mocks/run_agent.py
```

**Expected output:** Trajectories showing whether the agent correctly handles conflicting signals — or falls for the trap.
