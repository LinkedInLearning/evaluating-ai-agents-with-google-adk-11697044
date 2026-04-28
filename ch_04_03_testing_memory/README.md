# 04_03 — Testing Memory: Context Persistence

Measure whether the agent retains constraints across a multi-turn conversation by evaluating context decay over sequential turns.

**Learning goal:** Design multi-turn evalset cases and detect memory decay — when the agent ignores earlier constraints in later turns.

| File | Purpose |
|------|---------|
| `agent.py` | Procurement agent with session-based memory |
| `memory_decay.test.json` | Multi-turn evalset probing constraint retention |
| `test_config.json` | Evaluation criteria for multi-turn correctness |
| `run_agent.py` | Multi-turn eval runner |

## Usage

```bash
# Run from repo root
python ch_04_03_testing_memory/run_agent.py
```

**Expected output:** Pass/fail results per turn showing where (if anywhere) the agent drops its earlier constraints.
