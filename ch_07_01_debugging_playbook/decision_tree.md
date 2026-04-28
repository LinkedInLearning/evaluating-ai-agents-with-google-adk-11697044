# Debugging Decision Tree

When an eval fails, follow this tree to isolate the root-cause layer before attempting any fix.

---

## Step 0: Rule Out the Evaluation

- [ ] Is the golden trace still correct?
- [ ] Are the thresholds appropriate?
- [ ] Is the infrastructure healthy? (API keys, model availability)

If the eval itself is wrong, you are debugging a false positive.

---

## Step 1: Reproduce — Run 5 Times

```
Same failure every run?
├── YES → Deterministic (Step 2)
└── NO  → Stochastic (Step 3)
```

---

## Step 2: Deterministic — Tool or Prompt?

```
Correct tool, wrong arguments?
├── YES → TOOL LAYER
│         Fix: tighten Pydantic schema, improve tool docstring
│
└── NO → Correct arguments, wrong sequence?
         ├── YES → PROMPT LAYER
         │         Fix: add explicit ordering ("NEVER call X before Y")
         │
         └── NO → Right tool being called at all?
                  ├── NO → PROMPT LAYER
                  │         Fix: differentiate tool descriptions
                  │
                  └── YES (trace looks correct, output still wrong)
                           → CASCADING ERROR
                           Fix: trace backward to first divergent step
```

---

## Step 3: Stochastic — Variance or Capability?

```
Does temperature = 0.0 fix it?
├── YES → SAMPLING VARIANCE
│         Fix: lower temperature or add structural constraints
│
└── NO → Does adding "do NOT skip steps" fix it?
         ├── YES → INSTRUCTION UNDERSPECIFICATION
         │         Fix: make SOP explicit, add few-shot examples
         │
         └── NO → CAPABILITY LIMIT
                  Fix (in order): pipeline constraints → sub-agents → upgrade model
```

---

## Step 4: Close the Loop

- [ ] Add a regression case to the evalset
- [ ] Re-run Pass@k (5 runs) to confirm the fix holds
- [ ] Run full evalset to check for side effects
- [ ] Document the root cause

---

## Quick Reference

| Symptom | Layer | First Fix |
|---------|-------|-----------|
| Wrong argument format | Tool | Tighten Pydantic schema |
| Wrong tool sequence | Prompt | Add SOP ordering constraint |
| Wrong tool selected | Prompt | Differentiate tool descriptions |
| Correct trace, wrong answer | Cascading | Trace backward to first divergence |
| Inconsistent across runs | Model | Lower temperature, add constraints |
| Agent retries endlessly | Tool | Improve error response messaging |
| Agent skips steps sometimes | Model/Prompt | Add "MUST" language + lower temp |
| Agent fabricates data | Model | Add groundedness check |

---

> The most expensive debugging mistake is not a failed fix — it is a correct fix applied to the wrong layer.
