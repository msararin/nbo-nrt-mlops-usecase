import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src/nbo_nrt_mlops/exp3/resume.py"
CHECKPOINT_PATH = ROOT / "conf/experiments/exp3/checkpoints/exp3-b1-paused-safe-001.json"
spec = importlib.util.spec_from_file_location("exp3_resume", MODULE_PATH)
resume = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = resume
spec.loader.exec_module(resume)


class ResumeTest(unittest.TestCase):
    def test_exact_values_are_valid(self):
        result = resume.evaluate_resume(dict(resume.EXPECTED))
        self.assertEqual(result["resume_state"], "VALID")
        resume.require_valid_resume(result)

    def test_single_drift_is_detected_and_blocks(self):
        altered_expected = dict(resume.EXPECTED)
        altered_expected["candidate_rows"] = 38301
        result = resume.evaluate_resume(dict(resume.EXPECTED), altered_expected)
        self.assertEqual(result["resume_state"], "DRIFT_DETECTED")
        self.assertEqual(result["mismatches"]["candidate_rows"], {"expected": 38301, "observed": 38300})
        with self.assertRaises(RuntimeError):
            resume.require_valid_resume(result)

    def test_missing_value_is_drift(self):
        observed = dict(resume.EXPECTED)
        del observed["distinct_actions"]
        self.assertEqual(resume.evaluate_resume(observed)["resume_state"], "DRIFT_DETECTED")

    def test_trace_envelope_preserves_claim_boundary(self):
        checkpoint = json.loads(CHECKPOINT_PATH.read_text())
        result = resume.evaluate_resume(dict(resume.EXPECTED))
        trace = resume.build_trace_envelope(checkpoint=checkpoint, execution_run_id="LOCAL_UNIT_TEST", code_version_or_hash="TEST_SHA", result=result)
        self.assertEqual(trace["resume_state"], "VALID")
        self.assertEqual(trace["test_accessed"], "NO")
        self.assertEqual(trace["source_table_version"], "NOT_CAPTURED")
        self.assertEqual(trace["next_authorized_step"], resume.NEXT_AUTHORIZED_STEP)

    def test_drift_trace_blocks_next_step(self):
        checkpoint = json.loads(CHECKPOINT_PATH.read_text())
        result = resume.evaluate_resume(dict(resume.EXPECTED), {**resume.EXPECTED, "train_rows": 1})
        trace = resume.build_trace_envelope(checkpoint=checkpoint, execution_run_id="LOCAL_NEGATIVE_TEST", code_version_or_hash="TEST_SHA", result=result)
        self.assertEqual(trace["next_authorized_step"], "BLOCKED_PENDING_DRIFT_RESOLUTION")


if __name__ == "__main__":
    unittest.main()
