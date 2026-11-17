"""Independent checks for off-grid interpolation and analytical node risk."""
import math
import unittest
from offgrid import weights, value_and_gradient, finite_difference_pv01, parallel_pv01

N = (1.0, 3.0, 5.0)
R = (0.02, 0.03, 0.04)
P = ((1.5, 3.0), (2.5, 3.0), (4.0, 103.0))

class OffGridTests(unittest.TestCase):
    def test_midpoint_weights(self):
        self.assertEqual(weights(2.0, N), {0: 0.5, 1: 0.5})

    def test_exact_node(self):
        self.assertEqual(weights(3.0, N), {1: 1.0})

    def test_hand_calculated_single_payment(self):
        pv, grad = value_and_gradient((1., 3.), (0.02, 0.04), ((2., 100.),))
        expected = 100 * math.exp(-0.06)
        self.assertAlmostEqual(pv, expected)
        self.assertAlmostEqual(grad[0], -expected)
        self.assertAlmostEqual(grad[1], -expected)

    def test_analytic_against_finite_difference(self):
        _, grad = value_and_gradient(N, R, P)
        numerical = finite_difference_pv01(N, R, P, bump=0.00001)
        for d, fd in zip(grad, numerical):
            self.assertAlmostEqual(fd, -d*0.00001, delta=2e-7)

    def test_parallel_reconciles(self):
        self.assertAlmostEqual(sum(finite_difference_pv01(N, R, P)),
                               parallel_pv01(N, R, P), delta=2e-8)

    def test_gradient_parallel_direction(self):
        pv, grad = value_and_gradient(N, R, P)
        self.assertAlmostEqual(sum(grad),
            -sum(t*a*math.exp(-t*sum(R[j]*w for j,w in weights(t,N).items())) for t,a in P))

    def test_no_extrapolation(self):
        with self.assertRaises(ValueError):
            value_and_gradient(N, R, ((6., 10.),))

    def test_bad_curve(self):
        with self.assertRaises(ValueError):
            value_and_gradient((1., 1.), (0.02, 0.03), ((1., 10.),))

    def test_bad_bump(self):
        with self.assertRaises(ValueError):
            finite_difference_pv01(N, R, P, bump=float("nan"))

    def test_nonfinite_cashflow(self):
        with self.assertRaises(ValueError):
            value_and_gradient(N, R, ((2., float("inf")),))

    def test_input_immutability(self):
        rates = list(R)
        payments = list(P)
        value_and_gradient(N, rates, payments)
        self.assertEqual(rates, list(R))
        self.assertEqual(payments, list(P))

if __name__ == "__main__":
    unittest.main()
