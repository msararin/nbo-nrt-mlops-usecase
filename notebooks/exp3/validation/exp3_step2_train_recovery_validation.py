# Databricks notebook source
import json
from pyspark.sql import functions as F

SOURCE_COMMIT = "82a0f46148594d990a325a206ce6026c98504a0c"
CONTRACT_ID = "EXP3_CONTRACT:v1"
RECIPE_ID = "EXP3_RECIPE_TRAIN_V2:v1"
SOURCE_TABLE = "adb_nbo_nrt_mlops_dev.simulation.bandit_logged_interactions_v0_2"
EXPECTED_TRAIN_ROWS = 8002

train_v2 = (
    spark.table(SOURCE_TABLE)
    .filter(F.col("data_split") == F.lit("TRAIN"))
    .withColumn("segment_action", F.concat_ws("::", F.col("segment_code"), F.col("chosen_action")))
    .withColumn("event_action", F.concat_ws("::", F.col("event_type"), F.col("chosen_action")))
    .withColumn("channel_action", F.concat_ws("::", F.col("decision_channel"), F.col("chosen_action")))
)

actual_train_rows = train_v2.count()
if actual_train_rows != EXPECTED_TRAIN_ROWS:
    raise RuntimeError(
        f"TRAIN_V2_RECOVERED drift: expected {EXPECTED_TRAIN_ROWS}, observed {actual_train_rows}"
    )

receipt = {
    "experiment_id": "EXP3",
    "current_gate": "B1",
    "contract_id": CONTRACT_ID,
    "recipe_id": RECIPE_ID,
    "source_commit": SOURCE_COMMIT,
    "source_table": SOURCE_TABLE,
    "authorized_split": "TRAIN",
    "train_v2_recovered": actual_train_rows,
    "interaction_columns": ["segment_action", "event_action", "channel_action"],
    "test_accessed": "NO",
    "model_training": "NO",
    "policy_training": "NO",
    "greedy_policy_construction": "NO",
    "step2_integration": "PASS",
}

print(json.dumps(receipt, sort_keys=True))
dbutils.notebook.exit(json.dumps(receipt, sort_keys=True))
