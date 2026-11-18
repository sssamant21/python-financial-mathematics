import math
import unittest
from bootstrap import bootstrap, par_spread, survival


class BootstrapTests(unittest.TestCase):
    def test_recover_curve(self):
        t = [1, 2, 3]
        h = [0.01, 0.025, 0.04]
        s = [par_spread(x, h[:i+1], t[:i+1]) for i, x in enumerate(t)]
        for actual, expected in zip(bootstrap(t, s), h):
            self.assertAlmostEqual(actual, expected, places=10)

    def test_zero_spreads(self):
        self.assertTrue(all(abs(h) < 1e-10 for h in bootstrap([1, 2], [0, 0])))

    def test_survival_piecewise(self):
        self.assertAlmostEqual(survival(1.5, [0.1, 0.2], [1, 2]), math.exp(-0.2))

    def test_infeasible_decreasing_quote(self):
        with self.assertRaises(ValueError):
            bootstrap([1, 2], [0.1, 0.0001])

    def test_invalid_inputs(self):
        for maturities, spreads in [([2, 1], [0.01, 0.02]), ([1], [-0.1]),
                                    ([1], [float("nan")]), ([], [])]:
            with self.subTest(maturities=maturities, spreads=spreads):
                with self.assertRaises(ValueError):
                    bootstrap(maturities, spreads)

    def test_recovery_effect(self):
        self.assertGreater(par_spread(1, [0.03], [1], recovery=0.2),
                           par_spread(1, [0.03], [1], recovery=0.6))

    def test_maturity_grid(self):
        with self.assertRaises(ValueError):
            par_spread(1.1, [0.02], [1.1])


if __name__ == "__main__":
    unittest.main()
