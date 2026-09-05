# Databricks notebook source
import json
from pyspark.sql import functions as F

TABLE = "adb_nbo_nrt_mlops_dev.experiment_control.experiment_checkpoints"
CHECKPOINT_ID = "EXP3-B1-PAUSED-SAFE-001"
EXPECTED_COLUMNS = ["checkpoint_id", "experiment_id", "gate_id", "checkpoint_status", "contract_id", "recovery_recipe_id", "code_version_or_hash", "writer_source_commit", "manifest_json", "written_at"]

exists = spark.catalog.tableExists(TABLE)
if not exists:
    raise RuntimeError("Checkpoint table absent after failed run; stop for re-adjudication")

frame = spark.table(TABLE)
observed_columns = frame.columns
if observed_columns != EXPECTED_COLUMNS:
    raise RuntimeError(f"Checkpoint schema drift: {observed_columns}")

checkpoint_count = frame.filter(F.col("checkpoint_id") == CHECKPOINT_ID).count()
receipt = {"step": "EXP3_PHASE1_STEP3_PRE_RETRY_PREFLIGHT", "table_exists": exists, "observed_columns": observed_columns, "expected_columns": EXPECTED_COLUMNS, "checkpoint_id": CHECKPOINT_ID, "checkpoint_count": checkpoint_count, "expected_checkpoint_count": 0, "test_accessed": "NO", "result": "PASS" if checkpoint_count == 0 else "HALT"}
if checkpoint_count != 0:
    raise RuntimeError(json.dumps(receipt, sort_keys=True))
dbutils.notebook.exit(json.dumps(receipt, sort_keys=True))
