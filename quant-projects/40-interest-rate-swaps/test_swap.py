import math
import unittest
from swap import value_swap


class SwapTests(unittest.TestCase):
    def setUp(self):
        self.a = [0.5] * 4
        self.d = [0.98, 0.96, 0.94, 0.92]

    def test_par_zero(self):
        par = value_swap(1e6, 0, self.a, self.d)['par_rate']
        self.assertAlmostEqual(value_swap(1e6, par, self.a, self.d)['net_pv'], 0, places=7)

    def test_payer_receiver_symmetry(self):
        payer = value_swap(1e6, .04, self.a, self.d)['net_pv']
        receiver = value_swap(1e6, .04, self.a, self.d, pay_fixed=False)['net_pv']
        self.assertAlmostEqual(payer, -receiver)

    def test_independent_coupon_sum(self):
        v = value_swap(2e6, .03, self.a, self.d)
        expected_fixed = sum(2e6*.03*.5*x for x in self.d)
        self.assertAlmostEqual(v['fixed_pv'], expected_fixed)
        self.assertAlmostEqual(v['floating_pv'], 2e6*(1-self.d[-1]))

    def test_fixed_rate_direction(self):
        low = value_swap(1e6, .03, self.a, self.d)['net_pv']
        high = value_swap(1e6, .05, self.a, self.d)['net_pv']
        self.assertGreater(low, high)

    def test_negative_forward_allowed(self):
        v = value_swap(1e6, -.02, [.5, .5], [1.01, 1.02])
        self.assertLess(v['par_rate'], 0)

    def test_input_guardrails(self):
        cases = [(0, .04, self.a, self.d), (1, math.nan, self.a, self.d),
                 (1, .04, [], []), (1, .04, [.5], self.d),
                 (1, .04, [0]*4, self.d), (1, .04, self.a, [math.inf]*4)]
        for args in cases:
            with self.subTest(args=args), self.assertRaises(ValueError):
                value_swap(*args)

    def test_single_period_telescoping(self):
        v = value_swap(100, .04, [.5], [.98])
        self.assertAlmostEqual(v['net_pv'], 100*(1-.98-.04*.5*.98))


if __name__ == '__main__':
    unittest.main()
