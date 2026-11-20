import math
import unittest
from poisson_binomial import distribution, tail_probability, expected_defaults

class DistributionTests(unittest.TestCase):
    def test_single_obligor(self):
        self.assertEqual(distribution([0.2]), [0.8, 0.2])

    def test_heterogeneous_two_obligors(self):
        for a, b in zip(distribution([0.2, 0.5]), [0.4, 0.5, 0.1]):
            self.assertAlmostEqual(a, b)

    def test_mass_and_mean(self):
        ps = [0.01, 0.07, 0.2, 0.6]
        pmf = distribution(ps)
        self.assertAlmostEqual(math.fsum(pmf), 1)
        self.assertAlmostEqual(math.fsum(k*v for k, v in enumerate(pmf)), expected_defaults(ps))

    def test_deterministic_extremes(self):
        self.assertEqual(distribution([0, 1, 1]), [0, 0, 1, 0])

    def test_tail_boundaries(self):
        self.assertAlmostEqual(tail_probability([0.1, 0.2], 0), 1)
        self.assertEqual(tail_probability([0.1, 0.2], 3), 0)

    def test_order_invariance(self):
        a = distribution([0.01, 0.1, 0.5])
        b = distribution([0.5, 0.01, 0.1])
        for x, y in zip(a, b):
            self.assertAlmostEqual(x, y)

    def test_reject_invalid(self):
        for ps in ([], [float("nan")], [float("inf")], [-0.1], [1.1], [True], [0.1]*501):
            with self.subTest(ps=ps[:2]):
                with self.assertRaises(ValueError):
                    distribution(ps)
        with self.assertRaises(ValueError):
            tail_probability([0.1], True)

if __name__ == "__main__":
    unittest.main()
