import unittest
from crystallization import simulate_schedule

class CrystallizationTests(unittest.TestCase):
    def test_no_fees_compounding(self):
        rows = simulate_schedule([0.1, -0.2], performance_rate=0)
        self.assertAlmostEqual(rows[-1].ending_nav, 88)

    def test_monthly_vs_annual_fee_timing(self):
        r = [0.10, -0.05] + [0.0] * 10
        monthly = simulate_schedule(r, crystallize_every=1)
        annual = simulate_schedule(r, crystallize_every=12)
        self.assertLess(monthly[-1].ending_nav, annual[-1].ending_nav)
        self.assertEqual(sum(x.performance_fee for x in annual[:-1]), 0)

    def test_hard_hurdle_reduces_fee(self):
        r = [0.02] * 12
        no_hurdle = simulate_schedule(r, crystallize_every=12)
        with_hurdle = simulate_schedule(r, crystallize_every=12, annual_hurdle_rate=0.05)
        self.assertLess(sum(x.performance_fee for x in with_hurdle), sum(x.performance_fee for x in no_hurdle))
        self.assertGreater(with_hurdle[-1].ending_nav, no_hurdle[-1].ending_nav)

    def test_zero_return_below_hurdle(self):
        rows = simulate_schedule([0.0]*12, crystallize_every=12, annual_hurdle_rate=0.05)
        self.assertEqual(rows[-1].performance_fee, 0)
        self.assertAlmostEqual(rows[-1].ending_nav, 100)

    def test_first_month_known_value(self):
        row = simulate_schedule([0.1])[0]
        self.assertAlmostEqual(row.performance_fee, 2)
        self.assertAlmostEqual(row.ending_nav, 108)

    def test_management_fee_charged_each_month(self):
        row = simulate_schedule([0], annual_management_rate=0.12, performance_rate=0)[0]
        self.assertAlmostEqual(row.management_fee, 1)
        self.assertAlmostEqual(row.ending_nav, 99)

    def test_no_crystallization_before_year_end(self):
        rows = simulate_schedule([0.1]*11, crystallize_every=12)
        self.assertTrue(all(x.performance_fee == 0 for x in rows))

    def test_full_loss_and_no_negative_nav(self):
        rows = simulate_schedule([-1.0, 0.1], annual_management_rate=0.12)
        self.assertEqual(rows[-1].ending_nav, 0)
        self.assertTrue(all(x.performance_fee == 0 for x in rows))

    def test_bad_inputs(self):
        for kwargs in ({"initial_nav": 0}, {"annual_management_rate": True},
                       {"annual_hurdle_rate": -0.1}, {"performance_rate": 1.1},
                       {"crystallize_every": True}, {"crystallize_every": 2}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                simulate_schedule([0.1], **kwargs)
        for values in ([], [float('nan')], [-1.01], [True], [float('inf')]):
            with self.subTest(values=values), self.assertRaises(ValueError):
                simulate_schedule(values)

    def test_future_mutation_isolation(self):
        r = [0.03]*12
        a = simulate_schedule(r, crystallize_every=3)
        r[-1] = -0.4
        b = simulate_schedule(r, crystallize_every=3)
        self.assertEqual(a[:9], b[:9])

    def test_determinism(self):
        self.assertEqual(simulate_schedule([0.01]*12), simulate_schedule([0.01]*12))

if __name__ == '__main__':
    unittest.main()
