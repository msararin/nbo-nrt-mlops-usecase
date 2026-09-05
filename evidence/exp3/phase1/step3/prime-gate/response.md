# Prime Gate Adjudication — EXP3 Phase 1 Step 3

**Scope acknowledgment:** Review restricted to the supplied evidence packet. No live repository, artifact, or Databricks inspection performed. No role beyond Prime Gate assumed.

---

## 1. RCA_CLASSIFICATION

**Category:** Deterministic SQL syntax defect in checkpoint-write DML — control-plane authoring error.

**Accepted candidate cause:** Databricks Spark SQL MERGE grammar does not permit combining the `UPDATE SET *` wildcard with additional explicit column assignments in the same `WHEN MATCHED THEN UPDATE` clause. The parser fault at the comma following `*` (`[PARSE_SYNTAX_ERROR]`, SQLSTATE `42601`) is consistent with this grammar constraint.

**Classification confidence:** High, conditional on the reported error class, SQLSTATE, and parser location being faithful. The failure mode is reproducible in principle from the reported fragment alone; no runtime, data, permission, or concurrency factor is implicated.

**Not classified as:** data corruption, schema drift, permission fault, transient infrastructure failure, or scientific-artifact contamination.

---

## 2. EVIDENCE_SUFFICIENCY

**Sufficient for:**
- Adjudicating this as a syntax-class defect confined to the checkpoint MERGE statement.
- Confirming the two task attempts terminated before MERGE completion.
- Confirming no Codex-initiated retry or repair after terminal failure.

**Insufficient / not directly observed:**
- The full text of the offending MERGE statement (only a fragment is quoted).
- The state of `experiment_checkpoints` (existence, row count for the checkpoint ID, prior residue).
- Whether pre-MERGE DDL committed schema/table creation, partially or fully.
- Independent confirmation of commit SHA ↔ executed code correspondence.
- Whether any other MERGE/UPDATE sites in the same change set share the wildcard+assignment pattern.

**Verdict:** Sufficient to authorize a *bounded* diagnostic and repair adjudication. **Insufficient** to authorize any scientific, policy, or gate-progression claim.

---

## 3. DEFECT_SEVERITY

**Severity:** Low-to-moderate — **control-plane only**.

Justification:
- No scientific artifact (Reward Model V2, TEST data, policy artifacts) was touched.
- Failure occurred pre-MERGE-completion; idempotent checkpoint semantics are preserved by non-writing failure.
- Blast radius bounded to checkpoint-row authorship for `EXP3-B1-PAUSED-SAFE-001`.

Elevating factors (keeping this from "trivial"):
- The defect landed in code attributed to a candidate commit intended to advance experiment control.
- Automatic retry (attempt 1) reproduced the failure, confirming the defect is deterministic and was not caught by any pre-merge validation.

---

## 4. CLAIM_CEILING

Permitted claims after successful bounded repair and independent verification:

- ✅ Checkpoint row `EXP3-B1-PAUSED-SAFE-001` was written exactly once with the declared manifest fields.
- ✅ The MERGE syntax defect is resolved for this statement.
- ✅ EXP3 remains in **B1 PAUSED-SAFE** control state.

**Explicitly denied ceiling (do not claim):**
- ❌ EXP3 B1 gate approval or progression.
- ❌ Any policy training, greedy policy construction, or TEST access authorization.
- ❌ Reward Model V2 re-validation beyond its already-CLOSED/PASS status.
- ❌ Production readiness, uplift, generalizable code-quality, or process-maturity claims.
- ❌ Any inference that other MERGE sites are defect-free absent inspection.

---

## 5. REQUIRED_MITIGATIONS

Bounded, mandatory before retry authorization is exercised:

1. **Statement rewrite:** Replace `UPDATE SET *, written_at = current_timestamp()` with an explicit column assignment list covering all target columns plus `written_at`. No wildcard.
2. **Pre-retry read-only probe:** `SELECT COUNT(*)` (or equivalent) filtered on `checkpoint_id = 'EXP3-B1-PAUSED-SAFE-001'` against the intended table. Expected result: 0. If ≠ 0, halt and re-adjudicate.
3. **Idempotency preservation:** Retry must use the identical `checkpoint_id` and semantically identical payload. No renaming, no payload drift.
4. **Post-retry verification job:** Executed as a **separate** serverless read-only job (distinct run, distinct task), asserting:
   - Exactly one row for the checkpoint ID.
   - All manifest fields match declared values byte-for-byte where applicable.
   - `written_at` is populated and monotonic vs. attempt window.
5. **Scope lock:** Repair diff limited to the offending MERGE statement and, if present, structurally identical sibling statements in the same file. No opportunistic edits.
6. **Sibling-pattern scan (read-only):** Grep-equivalent search in the candidate commit for `UPDATE SET *` co-occurring with `,` in MERGE contexts; report findings before retry. Do not silently repair others without re-adjudication.
7. **No scientific surface touched:** Retry path must not read, write, or reference TEST data, reward model artifacts, or policy artifacts.

---

## 6. RETRY_AUTHORIZATION_RECOMMENDATION

**Recommendation:** **Conditional retry permitted**, scoped strictly to the checkpoint-write control row, contingent on **all** items in §5 being satisfied and independently verified by an Independent Checker (not by me, and not by Codex self-attestation alone).

Retry must:
- Be a new task run under the same parent or a successor control run — clearly attributable.
- Fail closed on any deviation from §5.
- Not be auto-retried by Codex on failure; a second failure requires re-adjudication.

**Retry does not confer** any gate advance. On success, EXP3 remains B1 PAUSED-SAFE with a durable checkpoint; further progression requires separate adjudication.

---

## 7. Explicit Limitations & Evidence Not Directly Observed

I have **not**:
- Inspected the repository, branch, or commit `40e51370401ee8990c935adb07029698e12b21a9`.
- Read the full MERGE statement, surrounding DDL, or the checkpoint payload schema.
- Verified the Databricks run IDs (`297297513664857`, `994342206050083`, `1071823427695582`) or their logs.
- Confirmed the current state of `adb_nbo_nrt_mlops_dev.experiment_control.experiment_checkpoints` (existence, contents, permissions).
- Validated that pre-MERGE DDL is idempotent or that no partial schema state exists.
- Confirmed the exact parser location or that the quoted fragment is verbatim.
- Assessed whether other statements in the change set share the defective pattern.
- Executed, edited, or caused any command, artifact, or configuration change.

All findings above are conditional on the packet's faithfulness. Any material divergence between the packet and reality invalidates this adjudication and requires resubmission.

**Adjudication does not extend to:** EXP3 B1 approval, TEST access, model or policy training, greedy policy construction, production readiness, or uplift. All remain prohibited under the stated scientific boundary.

---

**Prime Gate — adjudication complete. Bounded retry authorization is conditional; scientific surface remains locked.**
