import importlib.util
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = ROOT / "conf/experiments/exp3/checkpoints/exp3-b1-paused-safe-001.json"
MODULE_PATH = ROOT / "src/nbo_nrt_mlops/exp3/checkpoint.py"

spec = importlib.util.spec_from_file_location("exp3_checkpoint", MODULE_PATH)
checkpoint = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = checkpoint
spec.loader.exec_module(checkpoint)


class CheckpointTest(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(MANIFEST_PATH.read_text())

    def test_checkpoint_loads_without_notebook_state(self):
        checkpoint.validate_checkpoint(self.manifest)

    def test_checkpoint_identifies_resume_path_and_gate(self):
        self.assertEqual(self.manifest["recovery_recipe_id"], "EXP3_RECIPE_TRAIN_V2:v1")
        self.assertEqual(self.manifest["current_gate"], "B1")
        self.assertEqual(self.manifest["current_gate_status"], "ACTIVE")
        self.assertEqual(self.manifest["next_authorized_step"], checkpoint.NEXT_AUTHORIZED_STEP)

    def test_checkpoint_preserves_durable_and_ephemeral_state(self):
        self.assertIn("Unity Catalog source", self.manifest["durable_state"])
        self.assertIn("Spark DataFrames", self.manifest["ephemeral_state"])
        self.assertEqual(self.manifest["ephemeral_loss_interpretation"], "NOT_A_MODEL_FAILURE_RECONSTRUCT_FROM_DURABLE_RECIPE")

    def test_thin_support_rule_cannot_be_invented(self):
        altered = deepcopy(self.manifest)
        altered["known_open_issues"]["B1_SUPPORT_RULE.thin_support_rule"] = "COUNT_LT_5"
        with self.assertRaises(checkpoint.CheckpointContractError):
            checkpoint.validate_checkpoint(altered)

    def test_test_access_drift_fails_closed(self):
        altered = deepcopy(self.manifest)
        altered["verified_results"]["test_accessed"] = "YES"
        with self.assertRaises(checkpoint.CheckpointContractError):
            checkpoint.validate_checkpoint(altered)

    def test_checkpoint_row_is_deterministic(self):
        first = checkpoint.checkpoint_row(self.manifest)
        second = checkpoint.checkpoint_row(self.manifest)
        self.assertEqual(first, second)
        self.assertEqual(json.loads(first["manifest_json"]), self.manifest)

    def test_table_name_is_fail_closed(self):
        self.assertEqual(checkpoint.validate_table_name(checkpoint.CHECKPOINT_TABLE), checkpoint.CHECKPOINT_TABLE)
        with self.assertRaises(checkpoint.CheckpointContractError):
            checkpoint.validate_table_name("catalog.schema.table; DROP TABLE x")


if __name__ == "__main__":
    unittest.main()
