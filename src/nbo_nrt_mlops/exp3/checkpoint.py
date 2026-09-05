"""Validation and durable Delta persistence for EXP3 checkpoint manifests."""

from __future__ import annotations

import json
import re
from typing import Any


CHECKPOINT_TABLE = "adb_nbo_nrt_mlops_dev.experiment_control.experiment_checkpoints"
NEXT_AUTHORIZED_STEP = (
    "B1 empirical support reconstruction and establishment of the exact versioned "
    "support classification contract."
)


class CheckpointContractError(RuntimeError):
    """Raised when a checkpoint would violate the EXP3 pause/resume boundary."""


def validate_checkpoint(manifest: dict[str, Any]) -> None:
    """Validate the current EXP3 checkpoint and fail closed on boundary drift."""
    exact = {
        "checkpoint_status": "PAUSED_SAFE",
        "experiment_id": "EXP3",
        "current_gate": "B1",
        "current_gate_status": "ACTIVE",
        "recovery_recipe_id": "EXP3_RECIPE_TRAIN_V2:v1",
        "next_authorized_step": NEXT_AUTHORIZED_STEP,
    }
    for field, expected in exact.items():
        if manifest.get(field) != expected:
            raise CheckpointContractError(f"Checkpoint field drift: {field}")

    expected_results = {
        "train_rows": 8002,
        "distinct_train_context_states": 7660,
        "distinct_actions": 5,
        "candidate_rows": 38300,
        "test_accessed": "NO",
    }
    if manifest.get("verified_results") != expected_results:
        raise CheckpointContractError("Verified B1 results drifted")
    if manifest.get("reconciliation") != {"expression": "7660 * 5 = 38300", "status": "PASS"}:
        raise CheckpointContractError("Candidate-row reconciliation drifted")
    if manifest.get("known_open_issues", {}).get("B1_SUPPORT_RULE.thin_support_rule") != "NOT_DURABLY_PRESERVED":
        raise CheckpointContractError("THIN_SUPPORT rule must remain explicitly unresolved")
    required_prohibitions = {"TEST_ACCESS", "MODEL_TRAINING", "POLICY_TRAINING", "GREEDY_CANDIDATE_POLICY_CONSTRUCTION"}
    if not required_prohibitions.issubset(set(manifest.get("prohibitions", []))):
        raise CheckpointContractError("Checkpoint lost a scientific prohibition")


def checkpoint_row(manifest: dict[str, Any]) -> dict[str, Any]:
    """Return the minimal row written to the append-safe Delta checkpoint table."""
    validate_checkpoint(manifest)
    return {
        "checkpoint_id": manifest["checkpoint_id"],
        "experiment_id": manifest["experiment_id"],
        "gate_id": manifest["current_gate"],
        "checkpoint_status": manifest["checkpoint_status"],
        "contract_id": manifest["contract_id"],
        "recovery_recipe_id": manifest["recovery_recipe_id"],
        "code_version_or_hash": manifest["code_version_or_hash"],
        "manifest_json": json.dumps(manifest, sort_keys=True, separators=(",", ":")),
    }


def validate_table_name(table_name: str) -> str:
    """Restrict persistence to a three-part Unity Catalog identifier."""
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*", table_name):
        raise CheckpointContractError("Invalid Unity Catalog table name")
    return table_name
