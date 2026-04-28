# 04_02 — Trajectory Matching Rules

Define mandatory and forbidden tool sequences to formally score agent correctness using `tool_trajectory_avg_score`.

**Learning goal:** Write trajectory matching rules in `test_config.json` and interpret the score output for pass and fail scenarios.

| File | Purpose |
|------|---------|
| `agent.py` | Procurement agent under evaluation |
| `trajectory_rules.test.json` | Evalset with golden tool-call sequences |
| `test_config.json` | Trajectory matching criteria and thresholds |
| `run_agent.py` | Eval runner with pass/fail summary |

## Usage

```bash
# Step 1 — run manually and verify trajectories
python ch_04_02_trajectory_matching/run_agent.py

# Step 2 — run formal evaluation
adk eval ch_04_02_trajectory_matching/ \
    ch_04_02_trajectory_matching/trajectory_rules.test.json \
    --config_file_path=ch_04_02_trajectory_matching/test_config.json
```

**Expected output:** Three scenarios — mandatory pipeline approved, catalog-reject halted, budget-reject halted — all scoring `tool_trajectory_avg_score: 1.0`. `Tests passed: 3 / Tests failed: 0`.
