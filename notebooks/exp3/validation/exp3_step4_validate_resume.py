# Databricks notebook source
import json
from pyspark.sql import functions as F

SOURCE_COMMIT = "98e7c93f1c591c238be6fb8cccaf9d432fc53208"
SOURCE_TABLE = "adb_nbo_nrt_mlops_dev.simulation.bandit_logged_interactions_v0_2"
CHECKPOINT_TABLE = "adb_nbo_nrt_mlops_dev.experiment_control.experiment_checkpoints"
CHECKPOINT_ID = "EXP3-B1-PAUSED-SAFE-001"
CONTEXT_COLUMNS = ["segment_code", "event_type", "decision_channel", "contact_channel_history_count", "rank1_rank2_score_gap"]
EXPECTED = {"train_rows": 8002, "distinct_train_context_states": 7660, "distinct_actions": 5, "candidate_rows": 38300}

train = spark.table(SOURCE_TABLE).filter(F.col("data_split") == F.lit("TRAIN"))
train_rows = train.count()
context_states = train.select(*CONTEXT_COLUMNS).distinct().count()
actions = train.select("chosen_action").distinct().count()
observed = {"train_rows": train_rows, "distinct_train_context_states": context_states, "distinct_actions": actions, "candidate_rows": context_states * actions}

checkpoint_rows = spark.table(CHECKPOINT_TABLE).filter(F.col("checkpoint_id") == CHECKPOINT_ID).collect()
if len(checkpoint_rows) != 1:
    raise RuntimeError(f"Expected one checkpoint, observed {len(checkpoint_rows)}")
checkpoint = json.loads(checkpoint_rows[0]["manifest_json"])

def evaluate(expected):
    mismatches = {key: {"expected": expected.get(key), "observed": observed.get(key)} for key in sorted(set(expected) | set(observed)) if expected.get(key) != observed.get(key)}
    return {"resume_state": "DRIFT_DETECTED" if mismatches else "VALID", "expected": expected, "observed": observed, "mismatches": mismatches}

positive = evaluate(EXPECTED)
if positive["resume_state"] != "VALID":
    raise RuntimeError(json.dumps(positive, sort_keys=True))

negative_expected = dict(EXPECTED)
negative_expected["candidate_rows"] = 38301
negative = evaluate(negative_expected)
if negative["resume_state"] != "DRIFT_DETECTED":
    raise RuntimeError("Negative drift test did not fail closed")

trace = {
    "trace_schema": "EXP3_TRACE_ENVELOPE_SCHEMA:v1",
    "experiment_id": "EXP3",
    "current_gate": "B1",
    "checkpoint_id": CHECKPOINT_ID,
    "contract_id": checkpoint["contract_id"],
    "recovery_recipe_id": checkpoint["recovery_recipe_id"],
    "source_table": SOURCE_TABLE,
    "source_table_version": "NOT_CAPTURED",
    "model_run_id": checkpoint["model_run_id"],
    "artifact_uri": checkpoint["artifact_uri"],
    "code_version_or_hash": SOURCE_COMMIT,
    "execution_run_id": "CAPTURED_BY_DATABRICKS_RUN_RECEIPT",
    "observed": observed,
    "expected": EXPECTED,
    "resume_state": positive["resume_state"],
    "negative_test_resume_state": negative["resume_state"],
    "negative_test_mismatches": negative["mismatches"],
    "test_accessed": "NO",
    "model_training": "NO",
    "policy_training": "NO",
    "next_authorized_step": checkpoint["next_authorized_step"]
}
dbutils.notebook.exit(json.dumps(trace, sort_keys=True))
