"""Checklist behavior reference checks; runtime validation pending."""
import unittest
from section_20_08 import evaluate_checklist, REQUIRED

def complete():
    return {key: {"status": "complete", "reference": "record-1"} for key in REQUIRED}

class GateChecks(unittest.TestCase):
    def test_empty(self): self.assertFalse(evaluate_checklist({})["checklist_complete"])
    def test_complete(self): self.assertTrue(evaluate_checklist(complete())["checklist_complete"])
    def test_never_approves(self): self.assertFalse(evaluate_checklist(complete())["release_approved"])
    def test_missing_field(self):
        data = complete(); del data["tests"]
        self.assertIn("tests: missing", evaluate_checklist(data)["reasons"])
    def test_pending(self):
        data = complete(); data["tests"]["status"] = "pending"
        self.assertIn("tests: not complete", evaluate_checklist(data)["reasons"])
    def test_failed(self):
        data = complete(); data["tests"]["status"] = "failed"
        self.assertFalse(evaluate_checklist(data)["checklist_complete"])
    def test_no_reference(self):
        data = complete(); data["tests"]["reference"] = ""
        self.assertFalse(evaluate_checklist(data)["checklist_complete"])
    def test_blank_reference(self):
        data = complete(); data["tests"]["reference"] = "  "
        self.assertFalse(evaluate_checklist(data)["checklist_complete"])
    def test_invalid_entry(self):
        data = complete(); data["tests"] = None
        self.assertFalse(evaluate_checklist(data)["checklist_complete"])
    def test_wrong_input(self):
        with self.assertRaises(TypeError): evaluate_checklist([])
    def test_multiple_reasons(self):
        self.assertEqual(len(evaluate_checklist({})["reasons"]), len(REQUIRED))
    def test_reference_type(self):
        data = complete(); data["tests"]["reference"] = 1
        self.assertFalse(evaluate_checklist(data)["checklist_complete"])

if __name__ == "__main__": unittest.main()
