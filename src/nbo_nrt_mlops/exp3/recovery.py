"""Durable TRAIN-only reconstruction for Experiment 3 Reward Model V2 inputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


CONTRACT_ID = "EXP3_CONTRACT:v1"
RECIPE_ID = "EXP3_RECIPE_TRAIN_V2:v1"


class RecoveryContractError(RuntimeError):
    """Raised when a recovery contract or invariant is invalid."""


def load_json_compatible_yaml(path: str | Path) -> dict[str, Any]:
    """Load the versioned contract files, which use JSON-compatible YAML."""
    with Path(path).open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise RecoveryContractError(f"Expected an object in {path}")
    return value


def validate_contract_pair(contract: dict[str, Any], recipe: dict[str, Any]) -> None:
    """Fail closed when stable identities or TRAIN-only boundaries drift."""
    if contract.get("contract_id") != CONTRACT_ID:
        raise RecoveryContractError("Unexpected Experiment 3 contract identity")
    if recipe.get("recipe_id") != RECIPE_ID:
        raise RecoveryContractError("Unexpected TRAIN V2 recovery recipe identity")
    if recipe.get("experiment_contract_id") != CONTRACT_ID:
        raise RecoveryContractError("Recipe is not bound to the Experiment 3 contract")
    split_filter = recipe.get("filter", {})
    if split_filter != {"column": "data_split", "operator": "EQUALS", "value": "TRAIN"}:
        raise RecoveryContractError("Recovery recipe must remain TRAIN-only")
    if contract.get("data_boundary", {}).get("test_access") != "PROHIBITED":
        raise RecoveryContractError("TEST access boundary drifted")
    if recipe.get("expected_invariants", {}).get("train_rows") != 8002:
        raise RecoveryContractError("Expected TRAIN row invariant drifted")


def reconstruct_train_v2(spark: Any, recipe: dict[str, Any]) -> Any:
    """Reconstruct the ephemeral train_v2 DataFrame from its durable recipe."""
    from pyspark.sql import functions as F

    if recipe.get("filter", {}).get("value") != "TRAIN":
        raise RecoveryContractError("Refusing non-TRAIN reconstruction")

    frame = spark.table(recipe["source_table"]).filter(F.col("data_split") == F.lit("TRAIN"))
    for output_column, derivation in recipe["derived_columns"].items():
        if derivation.get("operation") != "concat_ws" or derivation.get("separator") != "::":
            raise RecoveryContractError(f"Unsupported derivation for {output_column}")
        frame = frame.withColumn(
            output_column,
            F.concat_ws("::", *(F.col(column) for column in derivation["inputs"])),
        )
    return frame


def assert_recovered_train_rows(train_v2: Any, expected_rows: int = 8002) -> int:
    """Count the reconstructed TRAIN frame and fail closed on row drift."""
    actual_rows = train_v2.count()
    if actual_rows != expected_rows:
        raise RecoveryContractError(
            f"TRAIN_V2_RECOVERED drift: expected {expected_rows}, observed {actual_rows}"
        )
    return actual_rows
