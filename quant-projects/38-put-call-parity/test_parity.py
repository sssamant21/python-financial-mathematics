import math
import unittest
from parity import parity_bounds

class ParityTests(unittest.TestCase):
    def test_exact_parity(self):
        target = 100 * math.exp(-0.01) - 100 * math.exp(-0.03)
        result = parity_bounds(100, 100, 1, .03, .01, target + 7, target + 7, 7, 7)
        self.assertTrue(result['compatible'])
        self.assertAlmostEqual(result['gap'], 0)

    def test_spread_absorbs_midpoint_disagreement(self):
        result = parity_bounds(100, 100, 1, 0, 0, 8, 12, 8, 12)
        self.assertTrue(result['compatible'])

    def test_disjoint_intervals(self):
        result = parity_bounds(100, 100, 1, 0, 0, 12, 13, 5, 6)
        self.assertFalse(result['compatible'])
        self.assertEqual(result['gap'], 6)

    def test_negative_rates_allowed(self):
        result = parity_bounds(100, 100, 1, -.01, 0, 5, 6, 5, 6)
        self.assertLess(result['theoretical_call_minus_put'], 0)

    def test_bad_inputs(self):
        base = [100, 100, 1, 0, 0, 5, 6, 5, 6]
        for idx, val in [(0, 0), (2, 0), (5, -1), (6, 4), (0, float('nan')), (0, True)]:
            with self.subTest(idx=idx, val=val):
                bad = base.copy(); bad[idx] = val
                with self.assertRaises(ValueError): parity_bounds(*bad)

if __name__ == '__main__': unittest.main()
