# Golden Trace Design Checklist

This checklist contains best practices to help you design a golden trace — a machine-readable, replayable assertion that encodes "this is what correct behavior looks like." Use it when building or reviewing your evalset.

---

## Evalset Coverage

- [ ] **Include at least one rejection case.** A set of only happy paths cannot catch an agent that approves everything.
- [ ] **Exercise every SOP branch.** If the SOP has *N* conditional paths, you need at least *N + 1* cases — one per branch, plus one full happy path.
- [ ] **Cover boundary values.** Budget exactly at the threshold, IDs at format limits, empty strings — boundaries are where regressions hide.
- [ ] **Include a "missing info" case.** What happens when the user omits a required field? The agent should ask — not hallucinate a value.

## Case Design

- [ ] **One behavioral concern per case.** A multi-concern case tells you *something* broke, not *what*. Split it.
- [ ] **Assert on arguments, not just tool names.** `check_approval_status` called with the wrong transaction ID is a broken agent — even though the trajectory "looks correct."
- [ ] **Assert on tool order.** If the SOP says "check *then* purchase," the golden trace must enforce that sequence.

## Evalset Hygiene

- [ ] **Commit the evalset to version control.** It is a behavioral specification, not disposable test data.
- [ ] **Add a case whenever you fix a bug.** The repro scenario becomes a permanent regression guard.
- [ ] **Never silently edit a golden trace to make a failing test pass.** Understand *why* the behavior changed first — then decide deliberately.
- [ ] **Audit for redundancy.** Two cases testing the same concern add cost without value. Remove duplicates.

## ADK Criteria Configuration

- [ ] **Set `tool_trajectory_avg_score: 1.0`** for CI/CD gating — exact trajectory match, fast and deterministic.
- [ ] **Set `response_match_score: 0.8`** for final response checks — allows minor wording variation.
- [ ] **Layer in `hallucinations_v1`** for groundedness checks when your agent surfaces data from tools.
- [ ] **Layer in `safety_v1`** for any agent that interacts with end users.
- [ ] **Configure criteria in `test_config.json`** — if missing, ADK defaults to `tool_trajectory: 1.0` and `response_match: 0.8`.

---

> The value of a golden trace is not what it proves today — it is what it catches tomorrow.
