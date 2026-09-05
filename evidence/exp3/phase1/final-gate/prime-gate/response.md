# Prime Gate Adjudication — EXP3 Phase 1

## Disposition

**`PHASE1_ACCEPT_WITH_LIMITATIONS`**

## Scope statement and limitations of this adjudication

This adjudication is made solely on the supplied privacy-minimized evidence packet. Prime Gate did not directly observe:

- The producer artifact contents beyond the reported SHA-256 `a3fa4f5d…c49e20`.
- The Databricks environment, source table, backup, checkpoint files, run logs, or their integrity.
- The Independent Checker's provider transaction beyond the reported OpenRouter identifiers and hashes.
- The Codex mitigation commit `83cd2b8d…6c393b`, its diff, the README text, or the rerun test output.
- Test coverage adequacy, scan coverage, or repository state.

All findings below are conditional on the accuracy of the reported hashes, identifiers, and PASS/NO attestations.

## Checker evidence and role separation — sufficient

- Genuine provider delivery is corroborated by: model string, generation ID `gen-1788626492-z1hZPfVhHSVRLPOTalLI`, HTTP 200, four distinct SHA-256 hashes (request, provider payload, raw response, substantive response), token accounting, cost, and latency.
- Request artifact hash matches the producer packet hash, evidencing the Checker reviewed the same evidence Prime Gate is adjudicating.
- Two prior interrupted attempts are correctly recorded as `ROLE_NOT_ENGAGED` and excluded; the accepted call carries an independent generation ID. Role separation between Producer, Independent Checker, Codex mitigator, and Prime Gate is preserved as reported.
- The Checker's `CHECK_PASS_WITH_LIMITATIONS` verdict and its enumerated non-observations are consistent with a bounded, artifact-only review.

Prime Gate does not close scientific gate B1 and does not impersonate or re-perform the Checker's review.

## Producer evidence sufficiency for the bounded claim

Sufficient for the candidate claim as written: *"Phase 1 pause/resume control plane is durable and reproducible for the bounded EXP3 B1 checkpoint evidence; Phase 1 does not close B1 or establish production/policy claims."*

Supporting elements: V2 recovery CLOSED/PASS; row/state/action/candidate counts stated; Step 2 recovery PASS; Step 3 preflight/write/read PASS with a recorded SQLSTATE 42601 failure and bounded corrected retry (a positive negative-control datapoint); Step 4 resume PASS at pinned source commit with a deliberate 38301-vs-38300 `DRIFT_DETECTED` control; 18/18 unittest PASS; TEST/model/policy/greedy all `NO`.

## Defects

### Non-blocking defects (must remain disclosed in claim ceiling)

1. **Lineage gap — `source_table_version=NOT_CAPTURED`.** Disclosed by producer and Checker. Does not defeat the bounded control-plane claim but bars any lineage-dependent downstream use.
2. **Historical `THIN_SUPPORT` rule `NOT_DURABLY_PRESERVED`.** Consistent with B1 remaining open; must not be silently dropped from future phases.
3. **Codex mitigation not independently observed.** The README/test-command mitigation and its commit SHA `83cd2b8d…6c393b` are producer-reported only. The Checker did not review it.

### Blocking defects

None identified on the supplied evidence.

## README mitigation — provisionally resolves the documentation issue

The Checker's sole recommendation (document the required unittest invocation) is reported as addressed by Codex via README update, 18/18 rerun, commit, and push. Under Prime Gate's evidence-only posture this resolves the recommendation **provisionally**, because Prime Gate has not observed the commit or README text. This is a documentation issue, not a scientific-gate issue; provisional resolution is proportionate.

## Required mitigations (bounded, non-blocking)

Prime Gate prescribes only; it does not perform.

- **M1.** In the Phase 1 acceptance record, cite Codex mitigation commit `83cd2b8d95b08bc9cdc31a35f29eaaa1036c393b` and mark it as *producer-reported, not independently reviewed*.
- **M2.** Before any Phase 2 gating that depends on the documented command, obtain a bounded independent confirmation that the README at that commit contains the exact standard-library unittest invocation and the claim-boundary text, and that the command executes 18/18 PASS in a clean checkout. This is a Phase 2 precondition, not a Phase 1 blocker.
- **M3.** Preserve `source_table_version=NOT_CAPTURED` as an explicit limitation in every downstream artifact that cites Phase 1. Any future use requiring lineage must first capture and pin `source_table_version`.
- **M4.** Preserve the `THIN_SUPPORT` rule status (`NOT_DURABLY_PRESERVED`) as an open item carried into B1 closure work.
- **M5.** Retain the full Checker attribution block (model, generation ID, four hashes, usage, verdict) and the two `ROLE_NOT_ENGAGED` records with the Phase 1 acceptance record.

## Claim ceiling

Accepted claims for Phase 1 are ceilinged to the following, and no further:

1. The pause/resume control plane for the EXP3 B1 checkpoint path is **durable and reproducible** on the bounded evidence reviewed, with a demonstrated negative control (SQLSTATE 42601 recorded and corrected) and a demonstrated drift control (38301 vs 38300 → `DRIFT_DETECTED`).
2. V2 recovery is CLOSED/PASS on the bounded evidence.
3. Local standard-library unittest suite reported 18/18 PASS on the artifact under the producer hash, and again post-mitigation as producer-reported.

Explicitly **not** accepted, and must not be inferred from this disposition:

- B1 is **not** closed. Scientific gate B1 remains open.
- No TEST access, model training, policy training, or greedy policy construction is authorized or evidenced.
- No production, deployment, generalization, or performance claim is established.
- No lineage claim is established (`source_table_version=NOT_CAPTURED`).
- No owner-reserved custody decision is made.
- No live inspection of repository, Databricks, or Checker transport is claimed.

## Summary

Accept Phase 1 with limitations. Checker evidence and role separation are sufficient for the bounded claim. No blocking defect. The README mitigation provisionally resolves the sole Checker recommendation; independent confirmation of that commit is a Phase 2 precondition, not a Phase 1 blocker. Claim ceiling and disclosed limitations must travel with any downstream citation.
