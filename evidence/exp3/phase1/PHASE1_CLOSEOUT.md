# EXP3 Phase 1 closeout

## Disposition

`PHASE1_ACCEPT_WITH_LIMITATIONS`

Phase 1 establishes a durable, fail-closed pause/resume control plane for the bounded EXP3 B1 checkpoint evidence. It does not close B1.

## Accepted source

- Canonical repository: `git@github.com:msararin/nbo-nrt-mlops-usecase.git`
- Branch: `codex/exp3-phase1-step2`
- Producer source/README mitigation commit reviewed by Prime Gate as reported evidence: `83cd2b8d95b08bc9cdc31a35f29eaaa1036c393b`.
- The README mitigation is producer-reported and was not independently observed by the Checker or Prime Gate.

## Validated boundary

- Experiment `EXP3`, gate `B1`.
- Reward Model V2 recovery `CLOSED / PASS`; run `59d42a1878b04dde967d816993e92fb0`.
- TRAIN `8002`; contexts `7660`; actions `5`; candidate rows `38300`.
- Step 4 resume state `VALID`; deliberate expected `38301` produced `DRIFT_DETECTED` against observed `38300`.
- TEST access, model training, policy training, and greedy policy construction: `NO`.
- Full local deterministic suite: 18/18 PASS.

## External role decisions

- Independent Checker: OpenRouter `anthropic/claude-sonnet-4.5`, generation `gen-1788626492-z1hZPfVhHSVRLPOTalLI`, `CHECK_PASS_WITH_LIMITATIONS`.
- Prime Gate: OpenRouter `anthropic/claude-opus-4.7`, generation `gen-1788626597-FDhdt7ENC8R06JfOC3Vs`, `PHASE1_ACCEPT_WITH_LIMITATIONS`.
- Calls, prompts, generation IDs, and outputs are separate. Neither reviewer claims live repository or Databricks observation.

## Mandatory carried limitations

1. `source_table_version=NOT_CAPTURED`; no lineage-dependent claim is accepted.
2. Historical `THIN_SUPPORT` rule remains `NOT_DURABLY_PRESERVED`.
3. B1 remains open; B1 localization/support-contract work is next.
4. Before a later gate relies on the README command, independently confirm the command and 18/18 result in a clean checkout.
5. No production, deployment, model/policy quality, promotion, or uplift claim is established.

## Next authorized scientific step

B1 empirical support reconstruction and establishment of the exact versioned support classification contract, using TRAIN only.

## Role/authenticity record

The detailed provider receipts, two unsuccessful Checker invocations classified `ROLE_NOT_ENGAGED`, historical incomplete Prime helper classification, runtime IDs, test failures, costs, tokens, latency, and claim ceiling are preserved in `telemetry-receipt.json`.
