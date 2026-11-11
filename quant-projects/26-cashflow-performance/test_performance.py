import math
import unittest
from performance import evaluate


class PerformanceTests(unittest.TestCase):
    def test_no_flows(self):
        result = evaluate(100, [110, 121], [0, 0])
        self.assertAlmostEqual(result['twr'], .21)
        self.assertAlmostEqual(result['mwr'], .1)

    def test_flow_neutral_twr(self):
        self.assertAlmostEqual(evaluate(100, [120, 198], [0, 100])['twr'], .08)

    def test_mwr_differs_after_contribution(self):
        result = evaluate(100, [120, 198], [0, 100])
        self.assertLess(result['mwr'], result['twr'])

    def test_single_period(self):
        result = evaluate(100, [120], [20])
        self.assertAlmostEqual(result['twr'], 0)
        self.assertAlmostEqual(result['mwr'], 0)

    def test_withdrawal_has_ambiguous_irr(self):
        self.assertIsNone(evaluate(100, [100, 100], [0, -20])['mwr'])

    def test_invalid_history(self):
        for navs, flows in [([], []), ([110], []), ([0], [0]), ([10], [-100])]:
            with self.subTest(navs=navs, flows=flows):
                with self.assertRaises(ValueError):
                    evaluate(100, navs, flows)

    def test_reject_bool_and_nonfinite(self):
        for initial in [True, math.inf, math.nan, 0]:
            with self.assertRaises(ValueError):
                evaluate(initial, [110], [0])
        with self.assertRaises(ValueError):
            evaluate(100, [110], [float('nan')])

    def test_deterministic(self):
        self.assertEqual(evaluate(100, [120, 198], [0, 100]), evaluate(100, [120, 198], [0, 100]))

    def test_cashflow_convention(self):
        self.assertEqual(evaluate(100, [120, 198], [0, 100])['cashflows'], (-100.0, -100.0, 198.0))

    def test_mismatched_types(self):
        with self.assertRaises(ValueError):
            evaluate(100, '110', [0])


if __name__ == '__main__':
    unittest.main()
