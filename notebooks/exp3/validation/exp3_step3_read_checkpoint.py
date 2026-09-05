# Databricks notebook source
import json
from pyspark.sql import functions as F

TABLE = "adb_nbo_nrt_mlops_dev.experiment_control.experiment_checkpoints"
CHECKPOINT_ID = "EXP3-B1-PAUSED-SAFE-001"

# This job starts in a fresh serverless session and does not use writer variables.
rows = spark.table(TABLE).filter(F.col("checkpoint_id") == CHECKPOINT_ID).collect()
if len(rows) != 1:
    raise RuntimeError(f"Expected exactly one checkpoint row, observed {len(rows)}")

manifest = json.loads(rows[0]["manifest_json"])
assert manifest["checkpoint_status"] == "PAUSED_SAFE"
assert manifest["current_gate"] == "B1"
assert manifest["current_gate_status"] == "ACTIVE"
assert manifest["recovery_recipe_id"] == "EXP3_RECIPE_TRAIN_V2:v1"
assert manifest["next_authorized_step"] == "B1 empirical support reconstruction and establishment of the exact versioned support classification contract."
assert manifest["known_open_issues"]["B1_SUPPORT_RULE.thin_support_rule"] == "NOT_DURABLY_PRESERVED"
assert manifest["verified_results"] == {"train_rows": 8002, "distinct_train_context_states": 7660, "distinct_actions": 5, "candidate_rows": 38300, "test_accessed": "NO"}

receipt = {"step": "EXP3_PHASE1_STEP3_INDEPENDENT_READ", "checkpoint_id": CHECKPOINT_ID, "table": TABLE, "checkpoint_status": manifest["checkpoint_status"], "current_gate": manifest["current_gate"], "current_gate_status": manifest["current_gate_status"], "recovery_recipe_id": manifest["recovery_recipe_id"], "next_authorized_step": manifest["next_authorized_step"], "thin_support_rule": manifest["known_open_issues"]["B1_SUPPORT_RULE.thin_support_rule"], "test_accessed": manifest["verified_results"]["test_accessed"], "result": "PASS"}
dbutils.notebook.exit(json.dumps(receipt, sort_keys=True))
