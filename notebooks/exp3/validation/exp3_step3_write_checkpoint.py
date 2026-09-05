# Databricks notebook source
import json

CHECKPOINT_PATH = "/Workspace/Users/msararin@gmail.com/exp3_phase1_validation/exp3-b1-paused-safe-001.json"
TABLE = "adb_nbo_nrt_mlops_dev.experiment_control.experiment_checkpoints"
WRITER_SOURCE_COMMIT = "40e51370401ee8990c935adb07029698e12b21a9"

with open(CHECKPOINT_PATH, "r", encoding="utf-8") as stream:
    manifest = json.load(stream)

assert manifest["checkpoint_status"] == "PAUSED_SAFE"
assert manifest["current_gate"] == "B1"
assert manifest["current_gate_status"] == "ACTIVE"
assert manifest["recovery_recipe_id"] == "EXP3_RECIPE_TRAIN_V2:v1"
assert manifest["verified_results"]["test_accessed"] == "NO"
assert manifest["known_open_issues"]["B1_SUPPORT_RULE.thin_support_rule"] == "NOT_DURABLY_PRESERVED"

payload = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
row = [(manifest["checkpoint_id"], manifest["experiment_id"], manifest["current_gate"], manifest["checkpoint_status"], manifest["contract_id"], manifest["recovery_recipe_id"], manifest["code_version_or_hash"], WRITER_SOURCE_COMMIT, payload)]
columns = "checkpoint_id string, experiment_id string, gate_id string, checkpoint_status string, contract_id string, recovery_recipe_id string, code_version_or_hash string, writer_source_commit string, manifest_json string"
spark.createDataFrame(row, columns).createOrReplaceTempView("exp3_checkpoint_candidate")

spark.sql(f"""
MERGE INTO {TABLE} AS target
USING exp3_checkpoint_candidate AS source
ON target.checkpoint_id = source.checkpoint_id
WHEN MATCHED AND target.manifest_json <> source.manifest_json THEN
  UPDATE SET
    target.experiment_id = source.experiment_id,
    target.gate_id = source.gate_id,
    target.checkpoint_status = source.checkpoint_status,
    target.contract_id = source.contract_id,
    target.recovery_recipe_id = source.recovery_recipe_id,
    target.code_version_or_hash = source.code_version_or_hash,
    target.writer_source_commit = source.writer_source_commit,
    target.manifest_json = source.manifest_json,
    target.written_at = current_timestamp()
WHEN NOT MATCHED THEN
  INSERT (checkpoint_id, experiment_id, gate_id, checkpoint_status, contract_id,
          recovery_recipe_id, code_version_or_hash, writer_source_commit, manifest_json, written_at)
  VALUES (source.checkpoint_id, source.experiment_id, source.gate_id, source.checkpoint_status,
          source.contract_id, source.recovery_recipe_id, source.code_version_or_hash,
          source.writer_source_commit, source.manifest_json, current_timestamp())
""")

receipt = {"step": "EXP3_PHASE1_STEP3_WRITE", "checkpoint_id": manifest["checkpoint_id"], "table": TABLE, "writer_source_commit": WRITER_SOURCE_COMMIT, "checkpoint_status": "PAUSED_SAFE", "test_accessed": "NO", "result": "PASS"}
dbutils.notebook.exit(json.dumps(receipt, sort_keys=True))
