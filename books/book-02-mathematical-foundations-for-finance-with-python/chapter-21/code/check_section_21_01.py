"""Reference checks for requirements catalog; runtime validation pending."""
import unittest
from section_21_01 import REQUIREMENTS, pending_record, missing_fields

class RequirementsChecks(unittest.TestCase):
    def test_eight_requirements(self): self.assertEqual(len(REQUIREMENTS), 8)
    def test_ids(self): self.assertEqual(set(REQUIREMENTS), {f"F{i}" for i in range(1, 9)})
    def test_execution_pending(self): self.assertEqual(pending_record()["execution"], "not run")
    def test_review_pending(self): self.assertEqual(pending_record()["independent_review"], "pending")
    def test_approval_pending(self): self.assertEqual(pending_record()["approval"], "pending")
    def test_source_missing(self): self.assertIsNone(pending_record()["source_commit"])
    def test_missing_fields(self): self.assertEqual(missing_fields({}), ["source_commit", "environment", "command", "result"])
    def test_complete_fields(self):
        self.assertEqual(missing_fields({"source_commit":"abc", "environment":"Python", "command":"python test.py", "result":"record"}), [])
    def test_partial(self): self.assertNotIn("source_commit", missing_fields({"source_commit":"abc"}))
    def test_fresh_record(self):
        a, b = pending_record(), pending_record()
        a["requirements"]["F1"] = "changed"
        self.assertNotEqual(a["requirements"]["F1"], b["requirements"]["F1"])
    def test_no_result_claim(self): self.assertIn("result", missing_fields(pending_record()))
    def test_no_approval_claim(self): self.assertNotEqual(pending_record()["approval"], "approved")

if __name__ == "__main__": unittest.main()
