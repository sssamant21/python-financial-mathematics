import unittest
from fee_lab import simulate


class FeeLabTests(unittest.TestCase):
    def test_no_fees_compound(self):
        rows = simulate([0.1, -0.2], management_rate=0, performance_rate=0)
        self.assertAlmostEqual(rows[-1].ending_nav, 88)

    def test_first_gain_fee(self):
        row = simulate([0.1], management_rate=0)[0]
        self.assertAlmostEqual(row.performance_fee, 2)
        self.assertAlmostEqual(row.ending_nav, 108)
        self.assertAlmostEqual(row.high_water_mark, 108)

    def test_loss_then_partial_recovery_no_performance_fee(self):
        rows = simulate([-0.2, 0.1], management_rate=0)
        self.assertEqual(rows[-1].performance_fee, 0)
        self.assertEqual(rows[-1].high_water_mark, 100)

    def test_recovery_above_hwm(self):
        rows = simulate([-0.2, 0.5], management_rate=0)
        self.assertAlmostEqual(rows[-1].performance_fee, 4)
        self.assertAlmostEqual(rows[-1].ending_nav, 116)

    def test_management_fee_periodic(self):
        row = simulate([0], management_rate=0.12, performance_rate=0, periods_per_year=12)[0]
        self.assertAlmostEqual(row.management_fee, 1)
        self.assertAlmostEqual(row.ending_nav, 99)

    def test_management_before_performance(self):
        row = simulate([0.1], management_rate=0.12, periods_per_year=12)[0]
        self.assertAlmostEqual(row.management_fee, 1)
        self.assertAlmostEqual(row.performance_fee, 1.8)
        self.assertAlmostEqual(row.ending_nav, 107.2)

    def test_zero_return_hwm_no_new_performance_fee(self):
        rows = simulate([0.1, 0], management_rate=0)
        self.assertEqual(rows[-1].performance_fee, 0)

    def test_full_loss_no_negative_fee(self):
        row = simulate([-1], management_rate=0.2)[0]
        self.assertEqual(row.ending_nav, 0)
        self.assertEqual(row.management_fee, 0)

    def test_reject_bad_inputs(self):
        for kwargs in ({"initial_nav": 0}, {"management_rate": True},
                       {"performance_rate": 1.1}, {"periods_per_year": True}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                simulate([0.1], **kwargs)
        for values in ([], [float('nan')], [-1.01], [True], [float('inf')]):
            with self.subTest(values=values), self.assertRaises(ValueError):
                simulate(values)

    def test_no_mutation_and_determinism(self):
        data = [0.03, -0.02, 0.04]
        self.assertEqual(simulate(data), simulate(data))
        self.assertEqual(data, [0.03, -0.02, 0.04])


if __name__ == '__main__':
    unittest.main()
