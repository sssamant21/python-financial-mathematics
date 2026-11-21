"""Synthetic validation of log-domain all-default probability."""
import math
import unittest
from log_default_diagnostic import log_all_default_probability


class LogDefaultDiagnosticTests(unittest.TestCase):
    def test_regular_case(self):
        self.assertAlmostEqual(log_all_default_probability([0.1, 0.2]), math.log(0.02))

    def test_extreme_underflow(self):
        value = log_all_default_probability([1e-200, 1e-200])
        self.assertTrue(math.isfinite(value))
        self.assertAlmostEqual(value, 2 * math.log(1e-200))
        self.assertEqual(math.exp(value), 0.0)

    def test_deterministic_endpoints(self):
        self.assertEqual(log_all_default_probability([1, 1]), 0.0)
        self.assertEqual(log_all_default_probability([0, 1]), float("-inf"))

    def test_reject_invalid_even_after_zero(self):
        for values in ([0, float("nan")], [0, -0.1], [True], [], [1.1]):
            with self.subTest(values=values), self.assertRaises(ValueError):
                log_all_default_probability(values)


if __name__ == "__main__":
    unittest.main()
