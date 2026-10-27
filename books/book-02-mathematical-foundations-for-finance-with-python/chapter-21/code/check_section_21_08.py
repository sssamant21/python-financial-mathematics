"""Validation-plan reference checks; runtime validation pending."""
import unittest
from section_21_08 import make_plan, missing_case_fields

class PlanChecks(unittest.TestCase):
    def test_case_count(self): self.assertEqual(len(make_plan()["cases"]), 6)
    def test_unique_ids(self):
        ids = [case["id"] for case in make_plan()["cases"]]
        self.assertEqual(len(ids), len(set(ids)))
    def test_known_value(self): self.assertIn("known_value", [c["layer"] for c in make_plan()["cases"]])
    def test_boundary(self): self.assertIn("boundary", [c["layer"] for c in make_plan()["cases"]])
    def test_invalid(self): self.assertIn("invalid", [c["layer"] for c in make_plan()["cases"]])
    def test_property(self): self.assertIn("property", [c["layer"] for c in make_plan()["cases"]])
    def test_integration(self): self.assertIn("integration", [c["layer"] for c in make_plan()["cases"]])
    def test_complete_cases(self):
        for case in make_plan()["cases"]: self.assertEqual(missing_case_fields(case), [])
    def test_missing(self): self.assertEqual(missing_case_fields({}), ["id", "layer", "description"])
    def test_invalid_type(self):
        with self.assertRaises(TypeError): missing_case_fields([])
    def test_pending(self):
        plan = make_plan()
        self.assertEqual(plan["execution"], "not run")
        self.assertEqual(plan["independent_review"], "pending")
        self.assertEqual(plan["approval"], "pending")
    def test_fresh_copy(self):
        a, b = make_plan(), make_plan()
        a["cases"][0]["id"] = "changed"
        self.assertNotEqual(a["cases"][0]["id"], b["cases"][0]["id"])

if __name__ == "__main__": unittest.main()
