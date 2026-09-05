"""Fail-closed EXP3 resume assertions and trace-envelope construction."""

from __future__ import annotations

from typing import Any


EXPECTED = {
    "train_rows": 8002,
    "distinct_train_context_states": 7660,
    "distinct_actions": 5,
    "candidate_rows": 38300,
}
NEXT_AUTHORIZED_STEP = "B1 empirical support reconstruction and establishment of the exact versioned support classification contract."


def evaluate_resume(observed: dict[str, int], expected: dict[str, int] | None = None) -> dict[str, Any]:
    """Compare all resume invariants; any mismatch returns DRIFT_DETECTED."""
    expected_values = dict(EXPECTED if expected is None else expected)
    mismatches = {
        key: {"expected": expected_values.get(key), "observed": observed.get(key)}
        for key in sorted(set(expected_values) | set(observed))
        if expected_values.get(key) != observed.get(key)
    }
    return {
        "resume_state": "DRIFT_DETECTED" if mismatches else "VALID",
        "expected": expected_values,
        "observed": dict(observed),
        "mismatches": mismatches,
    }


def require_valid_resume(result: dict[str, Any]) -> None:
    """Block the next scientific step unless every invariant is exact."""
    if result.get("resume_state") != "VALID":
        raise RuntimeError(f"EXP3 resume blocked: {result.get('mismatches')}")


def build_trace_envelope(*, checkpoint: dict[str, Any], execution_run_id: str, code_version_or_hash: str, result: dict[str, Any]) -> dict[str, Any]:
    """Build the minimum durable trace envelope without inventing unavailable values."""
    return {
        "trace_schema": "EXP3_TRACE_ENVELOPE_SCHEMA:v1",
        "experiment_id": "EXP3",
        "current_gate": "B1",
        "checkpoint_id": checkpoint["checkpoint_id"],
        "contract_id": checkpoint["contract_id"],
        "recovery_recipe_id": checkpoint["recovery_recipe_id"],
        "source_table": checkpoint["source_table"],
        "source_table_version": checkpoint.get("source_table_version", "NOT_CAPTURED"),
        "model_run_id": checkpoint["model_run_id"],
        "artifact_uri": checkpoint["artifact_uri"],
        "code_version_or_hash": code_version_or_hash,
        "execution_run_id": execution_run_id,
        "observed": result["observed"],
        "expected": result["expected"],
        "resume_state": result["resume_state"],
        "test_accessed": "NO",
        "model_training": "NO",
        "policy_training": "NO",
        "next_authorized_step": NEXT_AUTHORIZED_STEP if result["resume_state"] == "VALID" else "BLOCKED_PENDING_DRIFT_RESOLUTION",
    }
