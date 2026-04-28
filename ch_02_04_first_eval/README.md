# 02_04 — Your First Eval

Run your first `adk eval` against a golden evalset and interpret pass/fail scores.

**Learning goal:** Understand the anatomy of an evalset file, what `tool_trajectory_avg_score` measures, and how to read the evaluation report.

| File | Purpose |
|------|---------|
| `agent.py` | Procurement agent under evaluation |
| `tool_recall.test.json` | Golden evalset with expected tool trajectories |
| `test_config.json` | Evaluation criteria and thresholds |
| `run_agent.py` | Programmatic eval runner with pass/fail summary |

## Usage

```bash
# Run from repo root
python ch_02_04_first_eval/run_agent.py

# Or run via ADK CLI directly
adk eval ch_02_04_first_eval/ ch_02_04_first_eval/tool_recall.test.json --config_file_path=ch_02_04_first_eval/test_config.json
```

**Expected output:** Eval report showing `tool_trajectory_avg_score` per test case with a final pass/fail count.
