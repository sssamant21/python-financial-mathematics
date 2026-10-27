"""Reference checks for continuous-time scenario; runtime validation pending."""
import math
import unittest
from section_21_07 import transition, scenario_report

class ScenarioChecks(unittest.TestCase):
    def test_zero_rate(self): self.assertEqual(transition(1000, 0, 200, 3), 1600)
    def test_subnormal_rate_limit(self): self.assertEqual(transition(0, 5e-324, 100, .5), 50)
    def test_zero_time(self): self.assertEqual(transition(100, .1, 10, 0), 100)
    def test_double(self): self.assertAlmostEqual(transition(1000, math.log(2), 0, 1), 2000)
    def test_withdrawal(self): self.assertEqual(transition(100, 0, -60, 2), -20)
    def test_zero_crossing(self): self.assertAlmostEqual(transition(120, 0, -40, 3), 0)
    def test_zero_flow_zero_rate(self): self.assertEqual(transition(100, 0, 0, 5), 100)
    def test_composition(self):
        first = transition(1000, .04, 200, 2)
        self.assertTrue(math.isclose(transition(first, .04, 200, 3), transition(1000, .04, 200, 5), rel_tol=1e-12))
    def test_negative_time(self):
        with self.assertRaises(ValueError): transition(1, 0, 0, -1)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): transition(math.nan, 0, 0, 1)
    def test_boolean(self):
        with self.assertRaises(TypeError): transition(True, 0, 0, 1)
    def test_overflow(self):
        with self.assertRaises(OverflowError): transition(1, 1000, 0, 1)
    def test_pending(self):
        report = scenario_report(100, 0, 0, 1)
        self.assertEqual(report["validation_execution"], "not run")
        self.assertEqual(report["approval"], "pending")

if __name__ == "__main__": unittest.main()
