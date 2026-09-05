# EXP3 Phase 1 route ledger

## Route

- Task: close EXP3 Phase 1 durable traceability and pause/resume architecture.
- Canonical source: `/Users/apple/Documents/MLOPS/nbo-nrt-mlops-usecase`.
- Repo Custodian route: `PROVENANCE_INTERFACE` with `SCAN_ONLY` state verification.
- MLOps lifecycle scope: reproducibility and lineage evidence only.
- Why narrower routes were insufficient: scan-only cannot bind source SHA to Databricks receipts; provenance binding was required.
- Why broader routes were rejected: no destructive remediation, recovery, deployment, promotion, training, policy construction, or platform reconfiguration was required.

## Role and decision-right separation

| Role | Execution mechanism | Decision rights | Forbidden |
|---|---|---|---|
| Codex | local shell, Git, Databricks CLI | produce evidence; implement authorized bounded corrections | self-approve as Checker/Prime; destructive owner decisions |
| AIOS Enforcement v0.2 | deterministic local control | apply declared rules | act as external worker/reviewer |
| Independent Checker | separate OpenRouter request, `anthropic/claude-sonnet-4.5` | evidence-packet consistency and sufficiency check | live inspection claims; release/promotion adjudication; edits |
| Prime Gate | separate OpenRouter request, `anthropic/claude-opus-4.7` | disposition, defects, mitigations, claim ceiling | edits; local execution; Checker impersonation; owner custody |
| Owner | explicit user authorization | destructive and material custody authority | delegated approval is not inferred beyond stated scope |

## Allowed actions

- Add bounded EXP3 contracts, recovery/resume code, tests, Databricks validation projections, receipts, and closeout records.
- Execute TRAIN-only validations and checkpoint read/write.
- Commit and push the approved branch.
- Make separate external review requests with privacy-minimized evidence.

## Forbidden actions

- Access TEST; train models or policies; construct greedy policy; invent THIN_SUPPORT classification; close B1; claim production uplift/readiness.
- Relabel one provider response as two roles.
- Store API keys or raw customer data in Git.

## Expected evidence and claim boundary

- Exact Git SHA, artifact hashes, Databricks run/task IDs, deterministic test results, separate external generation IDs, costs/tokens/latencies, failures/retries, limitations, and final claim ceiling.
- Acceptance applies only to Phase 1 pause/resume control-plane durability and reproducibility for the recorded B1 checkpoint evidence.

## Timing note

The route decisions and boundaries were declared before the corresponding closeout actions in the interactive session. This durable ledger was materialized during closeout; it does not claim to be a pre-existing file.
