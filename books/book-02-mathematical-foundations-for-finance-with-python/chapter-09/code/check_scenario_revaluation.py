"""Regression cases for direct shocked cash-flow valuation."""
import math
import unittest
from section_9_09 import scenario

class ScenarioRevaluation(unittest.TestCase):
    def test_small_positive_value_after_large_shock(self):
        report=scenario([(100,1)],0,400000)
        expected=100*math.exp(-40)
        self.assertGreater(report['exact_value'],0)
        self.assertTrue(math.isclose(report['exact_value'],expected,rel_tol=1e-14,abs_tol=0))
    def test_zero_shock_known_value(self):
        report=scenario([(100,1)],math.log(2),0)
        self.assertAlmostEqual(report['exact_value'],50)
        self.assertEqual(report['exact_change'],0)
    def test_multi_flow_direct_reference(self):
        report=scenario([(100,1),(200,2)],0,10000*math.log(2))
        self.assertAlmostEqual(report['exact_value'],100)
    def test_ordinary_value_change_reconciles(self):
        report=scenario([(100,1)],0,100)
        self.assertTrue(math.isclose(report['exact_value']-100,report['exact_change'],rel_tol=1e-12,abs_tol=1e-12))

if __name__ == '__main__': unittest.main()
