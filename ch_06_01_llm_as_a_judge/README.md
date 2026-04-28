# 06_01 — LLM-as-a-Judge: Custom Rubrics

Design qualitative scoring rubrics to evaluate tone, professionalism, and refusal quality using ADK's `rubric_based_final_response_quality_v1` criterion.

**Learning goal:** Write binary, observable rubrics and interpret LLM-as-a-Judge scores — understanding why rubric precision determines score reliability.

| File | Purpose |
|------|---------|
| `agent.py` | Procurement agent under qualitative evaluation |
| `judge_rubrics.test.json` | Evalset with custom rubric definitions |
| `test_config.json` | Rubric-based evaluation config |
| `run_agent.py` | Eval runner with per-rubric score breakdown |

## Usage

```bash
# Run from repo root
python ch_06_01_llm_as_a_judge/run_agent.py
```

**Expected output:** Per-rubric scores (0.0 or 1.0) for each evalset case with an overall quality verdict.
