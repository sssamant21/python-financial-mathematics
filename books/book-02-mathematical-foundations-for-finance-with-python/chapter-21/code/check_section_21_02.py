"""Interface catalog reference checks; runtime validation pending."""
import unittest
from section_21_02 import interface_catalog, missing_contract_fields

class InterfaceChecks(unittest.TestCase):
    def test_module_count(self): self.assertEqual(len(interface_catalog()), 6)
    def test_cash_flow(self): self.assertIn("cash_flow", interface_catalog())
    def test_sensitivity(self): self.assertIn("sensitivity", interface_catalog())
    def test_linear_algebra(self): self.assertIn("linear_algebra", interface_catalog())
    def test_optimization(self): self.assertIn("optimization", interface_catalog())
    def test_continuous_time(self): self.assertIn("continuous_time", interface_catalog())
    def test_reporting(self): self.assertIn("reporting", interface_catalog())
    def test_complete_entries(self):
        for name, entry in interface_catalog().items():
            with self.subTest(name=name): self.assertEqual(missing_contract_fields(entry), [])
    def test_missing(self): self.assertEqual(missing_contract_fields({}), ["inputs", "output", "errors"])
    def test_blank(self): self.assertIn("inputs", missing_contract_fields({"inputs":"  ", "output":"x", "errors":"y"}))
    def test_type(self):
        with self.assertRaises(TypeError): missing_contract_fields([])
    def test_independent_copy(self):
        a, b = interface_catalog(), interface_catalog()
        a["cash_flow"]["output"] = "changed"
        self.assertNotEqual(a["cash_flow"]["output"], b["cash_flow"]["output"])

if __name__ == "__main__": unittest.main()
