# EXP3 Phase 1 privacy-minimized closeout evidence packet

## Review boundary

This packet contains reported, hash-addressed evidence only. The reviewer has no direct access to the repository, Databricks workspace, tables, MLflow, local files, credentials, or live run logs. No customer rows, feature values, tokens, or secrets are included.

## Canonical source and custody

- Repository: `git@github.com:msararin/nbo-nrt-mlops-usecase.git`
- Branch: `codex/exp3-phase1-step2`
- Exact reviewed source commit: `f21612ee7b9928cd06a9ed8dd349658f0985c453`
- Local HEAD and remote tracking SHA were equal at packet creation.
- Repo status was clean immediately after the Step 4 commit and push.
- Repo Custodian route: `PROVENANCE_INTERFACE` plus read-only `SCAN_ONLY`.
- Backups predate Step 2 and Step 3 changes; no destructive cleanup is in this closeout scope.

## Scientific boundary

- Experiment: `EXP3`; current gate: `B1`.
- Reward Model V2 recovery: `CLOSED / PASS`.
- Model run ID: `59d42a1878b04dde967d816993e92fb0`.
- TRAIN rows: `8002`; context states: `7660`; actions: `5`; candidate rows: `38300`.
- TEST access: `NO`; model training: `NO`; policy training: `NO`; greedy policy construction: `NO`.
- Exact historical `THIN_SUPPORT` rule: `NOT_DURABLY_PRESERVED`.
- B1 overall support evidence is available; B1 localization is next; B1 final verdict is not closed.
- Next authorized step: B1 empirical support reconstruction and establishment of the exact versioned support classification contract.
- Production uplift, promotion, deployment-readiness, and policy-quality claims are prohibited.

## Durable artifacts

- Experiment contract SHA-256: `26ba3d3be4d5ddce0fe1a7aeed2e8e0429d10b264efc5d477e00ba743d841073`.
- TRAIN V2 recovery recipe SHA-256: `25dc88c30423c943b525f734a3bff078bc03625dc9184b1713f0600868849a5a`.
- PAUSED_SAFE checkpoint manifest SHA-256: `c8bb54810099b94f143ddd9cafcffc18d1a06f26ac8416f525429fd95055b21e`.
- Step 2 receipt SHA-256: `30a51803ed08d24fce847ba12f0d49c4a24dfaf9a406830833facc59a1417504`.
- Step 3 closeout SHA-256: `000760b59fc68f8bf91ee31c7b5e950129bc60ceeef1895ae33f9c5a691e7ab7`.
- Step 4 receipt SHA-256: `3481096374b5f6e233fb2a04bc5fff2bf947fd1280db398b5ccabdf660d9674e`.

## Runtime evidence

### Step 2 recovery validation

- Databricks parent run `289733114567399`, task run `177556032106721`, result `SUCCESS`.
- Recovered full TRAIN count `8002`; prohibited actions remained `NO`.

### Step 3 durable checkpoint

- Initial write parent run `297297513664857` failed with SQLSTATE `42601`; two task attempts were recorded.
- Prime Gate RCA and Independent Checker retry review used separate genuine OpenRouter requests and separate outputs.
- Preflight parent run `720509405272144`, task `684143539925273`, result `SUCCESS`; exact 10-column schema; zero target checkpoint rows.
- Corrected write parent run `55815994375489`, task `714131884460416`, attempt `0`, result `SUCCESS`.
- Separate read parent run `119633299689444`, task `478906069429943`, result `SUCCESS`; exactly one matching checkpoint with `PAUSED_SAFE`, B1 `ACTIVE`, and the scientific boundary above.

### Step 4 fail-closed resume validation

- Databricks parent run `125226956123826`, task run `1075465073264233`, attempt `0`, result `SUCCESS`.
- Positive assertion returned `resume_state=VALID` for 8002 / 7660 / 5 / 38300.
- Deliberate in-memory negative expected candidate count `38301` returned `DRIFT_DETECTED`, observed `38300`.
- `source_table_version=NOT_CAPTURED`; this is an explicit lineage limitation.

## Deterministic tests and operational failures

- Correctly scoped local suite: `python3 -m unittest discover -s tests/unit/exp3 -p test_*.py -v` => `18 tests`, `OK`.
- `git diff --check` passed before Step 4 commit.
- Bounded scan found no OpenRouter key or bearer-token marker in tracked/pending repo content.
- Two runner-discovery attempts were non-test infrastructure failures: bare `pytest` was absent; Homebrew Python had no pytest module. The repository tests use standard-library `unittest`; the explicit suite then passed 18/18.
- A first historical Step 3 model helper response lacked a generation/receipt ID and was classified `ROLE_NOT_ENGAGED`; it was not used or relabelled.

## Phase 1 acceptance candidate

Candidate conclusion: the pause/resume control plane is durable and reproducible for the bounded EXP3 B1 checkpoint evidence represented here. Phase 1 does not close scientific gate B1. The resume path fails closed on drift in asserted counts. Lineage remains incomplete because the source table version was not captured.

## Requested Independent Checker function

Check internal consistency, traceability, prohibited-action boundaries, separation-of-role evidence, and whether the candidate conclusion is supported by this packet. Return `CHECK_PASS`, `CHECK_PASS_WITH_LIMITATIONS`, or `CHECK_FAIL`, with exact defects and evidence references. Do not adjudicate release/promotion, edit artifacts, execute commands, or claim live observation.
