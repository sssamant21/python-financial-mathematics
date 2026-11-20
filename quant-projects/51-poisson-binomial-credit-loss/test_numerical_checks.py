import math
import unittest
from decimal import Decimal
from numerical_checks import enumerate_decimal, all_default_log_probability, diagnostics
from poisson_binomial import distribution


class NumericalChecksTests(unittest.TestCase):
    def test_independent_enumeration(self):
        self.assertEqual(enumerate_decimal([0.2, 0.5]), [Decimal("0.40"), Decimal("0.50"), Decimal("0.10")])

    def test_mass_and_expectation(self):
        ps = [0.03, 0.12, 0.41, 0.75]
        exact = enumerate_decimal(ps)
        self.assertEqual(sum(exact), Decimal(1))
        self.assertEqual(sum(k * x for k, x in enumerate(exact)), sum((Decimal(str(p)) for p in ps), Decimal(0)))
        self.assertLess(float(diagnostics(ps)["max_absolute_pmf_error"]), 1e-14)

    def test_extreme_tail_log_domain(self):
        ps = [1e-6] * 100
        self.assertEqual(distribution(ps)[-1], 0.0)  # expected binary64 underflow
        self.assertAlmostEqual(all_default_log_probability(ps), 100 * math.log(1e-6), places=10)

    def test_zero_and_certain_defaults(self):
        self.assertEqual(all_default_log_probability([1, 1]), 0.0)
        self.assertEqual(all_default_log_probability([0, 0.5]), -math.inf)

    def test_order_invariance(self):
        self.assertEqual(enumerate_decimal([0.1, 0.2, 0.3]), enumerate_decimal([0.3, 0.1, 0.2]))

    def test_guardrails(self):
        for ps in ([], [float("nan")], [True], [0.1] * 17):
            with self.subTest(length=len(ps)):
                with self.assertRaises(ValueError):
                    enumerate_decimal(ps)
        for precision in (True, 10, 201, 40.5):
            with self.assertRaises(ValueError):
                enumerate_decimal([0.1], precision)
        with self.assertRaises(ValueError):
            all_default_log_probability([float("inf")])


if __name__ == "__main__":
    unittest.main()
