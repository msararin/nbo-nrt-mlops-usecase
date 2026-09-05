# EXP3 Phase 1 Prime Gate adjudication packet

## Prime Gate role contract

Adjudicate only evidence sufficiency, classifications, defects, required mitigations, and claim ceilings for Phase 1. Do not edit artifacts, execute commands, claim direct observation, impersonate the Independent Checker, close scientific gate B1, authorize TEST access/training/policy construction, or make owner-reserved custody decisions.

## Producer evidence

The privacy-minimized producer packet was independently reviewed. Its SHA-256 is `a3fa4f5d4b72437d2764590f4e14e04ac7e1f46af4c84900ecdd10ab8bc49e20` and it identified:

- EXP3 / B1; V2 recovery CLOSED/PASS.
- 8002 TRAIN rows, 7660 context states, 5 actions, 38300 candidate rows.
- TEST/model training/policy training/greedy policy construction all `NO`.
- historical THIN_SUPPORT rule `NOT_DURABLY_PRESERVED`; B1 not closed.
- Step 2 Databricks recovery run PASS.
- Step 3 durable checkpoint preflight/write/read PASS after a recorded SQLSTATE 42601 failure and bounded corrected retry.
- Step 4 resume validation PASS at source commit `f21612ee7b9928cd06a9ed8dd349658f0985c453`; deliberate 38301 mismatch produced `DRIFT_DETECTED` against observed 38300.
- Local standard-library unittest suite 18/18 PASS.
- Explicit limitation: `source_table_version=NOT_CAPTURED`.
- Candidate claim: Phase 1 pause/resume control plane is durable and reproducible for the bounded EXP3 B1 checkpoint evidence; Phase 1 does not close B1 or establish production/policy claims.

## Independent Checker attributable work product

- Role: Independent Checker.
- Provider: OpenRouter.
- Exact requested and returned model: `anthropic/claude-sonnet-4.5`.
- Genuine generation ID: `gen-1788626492-z1hZPfVhHSVRLPOTalLI`.
- Confirmed delivery: `true`; HTTP 200.
- Request artifact SHA-256: `a3fa4f5d4b72437d2764590f4e14e04ac7e1f46af4c84900ecdd10ab8bc49e20`.
- Provider payload SHA-256: `8d6f99b223bce0344a749138e330bc69893df76cbe446e7061b1f7569acf06c1`.
- Raw response SHA-256: `f9bd2294b64cb37802b5671b1158a038f3ea797c9a5c79afe9044678ec194ef8`.
- Substantive response SHA-256: `cb3d55a52352ba2085adc3f218fbb4ce6299000a120d64b690d6f750bf0085dc`.
- Usage: 1584 input, 1763 output, 3347 total tokens; USD 0.031197; 34487 ms.
- Verdict: `CHECK_PASS_WITH_LIMITATIONS`.
- Checker found no blocking defect. It confirmed internal consistency, boundary compliance, evidence adequacy for the bounded claim, and the disclosed lineage gap.
- Checker recommended documenting the required unittest invocation in the repository.
- Checker explicitly did not observe live repository state, Databricks, tables, run logs, backup integrity, scan coverage, or test coverage adequacy.

Two prior invocations of the same Checker request were interrupted by the local host near 30 seconds before receipt creation. They are recorded as failed delivery / `ROLE_NOT_ENGAGED` and were not used. The successful call above used its own provider request and generation ID.

## Codex mitigation after Checker review

Codex—not the Checker or Prime Gate—added the exact standard-library unittest command and its claim boundary to README, reran 18/18 tests successfully, committed, and pushed.

- Mitigation commit and current remote-tracking SHA: `83cd2b8d95b08bc9cdc31a35f29eaaa1036c393b`.
- The Checker did not directly review or observe this new commit; the mitigation facts are producer-reported evidence for Prime Gate adjudication.

## Decision requested

Return exactly one disposition: `PHASE1_ACCEPT`, `PHASE1_ACCEPT_WITH_LIMITATIONS`, or `PHASE1_BLOCK`. Identify exact blocking/non-blocking defects, required mitigations, claim ceiling, whether the Checker evidence and role separation are sufficient, and whether the README mitigation resolves the test-command documentation issue. If blocked, prescribe bounded mitigation only; do not perform it.
