import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CONTRACT_PATH = ROOT / "conf/experiments/exp3/experiment_contract.v1.yaml"
RECIPE_PATH = ROOT / "conf/experiments/exp3/recovery_recipe_train_v2.v1.yaml"
MODULE_PATH = ROOT / "src/nbo_nrt_mlops/exp3/recovery.py"

spec = importlib.util.spec_from_file_location("exp3_recovery", MODULE_PATH)
recovery = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = recovery
spec.loader.exec_module(recovery)


class CountOnlyFrame:
    def __init__(self, rows):
        self.rows = rows

    def count(self):
        return self.rows


class ContractAndRecoveryTest(unittest.TestCase):
    def setUp(self):
        self.contract = recovery.load_json_compatible_yaml(CONTRACT_PATH)
        self.recipe = recovery.load_json_compatible_yaml(RECIPE_PATH)

    def test_contracts_reload_without_notebook_state(self):
        recovery.validate_contract_pair(self.contract, self.recipe)
        self.assertEqual(self.contract["experiment_id"], "EXP3")
        self.assertEqual(self.contract["current_gate"], "B1")

    def test_recipe_is_exactly_train_only(self):
        self.assertEqual(
            self.recipe["filter"],
            {"column": "data_split", "operator": "EQUALS", "value": "TRAIN"},
        )
        serialized = json.dumps(self.recipe)
        self.assertNotIn('"value": "TEST"', serialized)

    def test_recipe_preserves_interaction_contract(self):
        expected = {
            "segment_action": ["segment_code", "chosen_action"],
            "event_action": ["event_type", "chosen_action"],
            "channel_action": ["decision_channel", "chosen_action"],
        }
        observed = {
            name: rule["inputs"] for name, rule in self.recipe["derived_columns"].items()
        }
        self.assertEqual(observed, expected)
        self.assertTrue(all(rule["separator"] == "::" for rule in self.recipe["derived_columns"].values()))

    def test_expected_train_count_passes(self):
        self.assertEqual(recovery.assert_recovered_train_rows(CountOnlyFrame(8002)), 8002)

    def test_train_count_drift_fails_closed(self):
        with self.assertRaises(recovery.RecoveryContractError):
            recovery.assert_recovered_train_rows(CountOnlyFrame(8001))

    def test_thin_support_rule_remains_unresolved(self):
        self.assertEqual(
            self.contract["unresolved_contract_fields"]["B1_SUPPORT_RULE.thin_support_rule"],
            "NOT_DURABLY_PRESERVED",
        )


if __name__ == "__main__":
    unittest.main()
