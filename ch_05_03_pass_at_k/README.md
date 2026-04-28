# 05_03 — Pass@k and Non-Determinism

Calculate Pass@k reliability scores across multiple eval runs to quantify LLM stochasticity and distinguish reliable agents from lucky ones.

**Learning goal:** Implement Pass@k, interpret the fragility gap between Pass@1 and Pass@k, and classify an agent as Reliable, Marginal, or Unreliable.

| File | Purpose |
|------|---------|
| `agent.py` | Procurement agent run k times per scenario |
| `pass_at_k.test.json` | Evalset for repeated-run statistical analysis |
| `test_config.json` | Evaluation criteria including trajectory matching |
| `run_agent.py` | Pass@k runner with reliability classification output |

## Usage

```bash
# Run from repo root
python ch_05_03_pass_at_k/run_agent.py
```

**Expected output:** Pass@1, Pass@3, Pass@5 scores with a Reliable / Marginal / Unreliable classification per scenario.
