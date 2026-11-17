import math
import unittest
from curve import bootstrap, forwards, reprice


class CurveTests(unittest.TestCase):
    def test_flat_curve(self):
        ds = bootstrap([0.04] * 5)
        for n, d in enumerate(ds, 1):
            self.assertAlmostEqual(d, (1.04) ** -n, places=12)

    def test_repricing(self):
        quotes = (0.03, 0.035, 0.04, 0.038)
        for actual, expected in zip(reprice(bootstrap(quotes)), quotes):
            self.assertAlmostEqual(actual, expected, places=12)

    def test_forward_discount_identity(self):
        ds = bootstrap((0.02, 0.03, 0.05))
        prev = 1.0
        for d, f in zip(ds, forwards(ds)):
            self.assertAlmostEqual(prev, d * (1 + f), places=12)
            prev = d

    def test_negative_rates_supported(self):
        ds = bootstrap((-0.01, -0.005))
        self.assertGreater(ds[0], 1.0)
        self.assertAlmostEqual(reprice(ds)[1], -0.005)

    def test_bad_quotes(self):
        for rates in ([], [float("nan")], [float("inf")], [-1.0], [True], [0.01, 2.0]):
            with self.subTest(rates=rates), self.assertRaises(ValueError):
                bootstrap(rates)

    def test_repricing_bad_discounts(self):
        for d in ([0], [-1], [math.nan], [math.inf]):
            with self.subTest(d=d), self.assertRaises(ValueError):
                reprice(d)

    def test_forwards_bad_discounts(self):
        with self.assertRaises(ValueError):
            forwards([0.5, 0.0])


if __name__ == "__main__":
    unittest.main()
