# NBO–NRT MLOps Use-Case Evidence

This repository holds bounded, public-safe evidence for the NBO–NRT MLOps use case.

- [Phase 5C — ADLS Landing and Read-Back Evidence](evidence/phase5c-adls-landing/README.md)

## EXP3 local validation

EXP3 tests use Python's standard-library `unittest` runner and require no `pytest` installation:

```bash
python3 -m unittest discover -s tests/unit/exp3 -p 'test_*.py' -v
```

The local suite validates durable contracts and fail-closed recovery/resume behavior. It does not verify live Databricks state, data provenance, deployment, model quality, policy quality, or production readiness.

Evidence in this repository does not establish production readiness, Databricks ingestion, model execution, or real customer behavior.
