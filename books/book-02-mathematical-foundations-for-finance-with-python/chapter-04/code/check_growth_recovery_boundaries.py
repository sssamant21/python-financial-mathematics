"""Chapter 4 recovery-boundary checks; authored, not executed in this pass."""
import unittest
from section_4_09 import periodic_result, continuous_result

class GrowthRecoveryBoundaries(unittest.TestCase):
    def test_continuous_factor_underflow(self):
        with self.assertRaisesRegex(OverflowError, "growth factor underflow"):
            continuous_result(100, -1000, 1)

    def test_periodic_factor_underflow(self):
        with self.assertRaisesRegex(OverflowError, "growth factor underflow"):
            periodic_result(100, -.5, 1, 2000)

    def test_continuous_zero_horizon(self):
        result = continuous_result(100, -.05, 0)
        self.assertEqual(result["future_value"], 100)
        self.assertEqual(result["recovered_present_value"], 100)

    def test_periodic_known_value(self):
        result = periodic_result(100, .25, 1, 1)
        self.assertAlmostEqual(result["future_value"], 125)
        self.assertAlmostEqual(result["recovered_present_value"], 100)

    def test_zero_principal_ordinary_factor(self):
        result = continuous_result(0, -.05, 1)
        self.assertEqual(result["future_value"], 0)
        self.assertEqual(result["recovered_present_value"], 0)

if __name__ == "__main__":
    unittest.main()
