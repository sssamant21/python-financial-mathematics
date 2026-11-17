import math
import unittest
from funding_basis import funding_interval, basis_sensitivity
from fx_forward import fair_forward


class FundingBasisTests(unittest.TestCase):
    def test_symmetric_zero_spread_matches_parity(self):
        lo, hi = funding_interval(1.1, 1.1, .04, .04, .02, .02, 1)
        self.assertAlmostEqual(lo, fair_forward(1.1, .04, .02, 1))
        self.assertAlmostEqual(hi, lo)

    def test_wider_funding_spreads_expand_interval(self):
        tight = funding_interval(1.09, 1.11, .04, .04, .02, .02, 1)
        wide = funding_interval(1.09, 1.11, .03, .05, .01, .03, 1)
        self.assertLess(wide[0], tight[0])
        self.assertGreater(wide[1], tight[1])

    def test_basis_scenarios_expand_interval(self):
        a = funding_interval(1.09, 1.11, .03, .05, .01, .03, 2)
        b = funding_interval(1.09, 1.11, .03, .05, .01, .03, 2, -.01, .01)
        self.assertLess(b[0], a[0])
        self.assertGreater(b[1], a[1])

    def test_basis_derivative_matches_small_bump(self):
        x = basis_sensitivity(1.1, .04, .02, 1.5, .003, .01)
        approx = x["bumped_change"] / (.01 * 1e-4)
        self.assertAlmostEqual(approx / x["d_forward_d_basis"], 1, places=5)

    def test_basis_sensitivity_exact_exponential_bump(self):
        # Synthetic analytic identity, independent of the implementation's bump subtraction.
        spot, rd, rf, years, basis, bump_bp = 1.15, .035, .02, 2.5, -.005, 2.0
        result = basis_sensitivity(spot, rd, rf, years, basis, bump_bp)
        expected_forward = spot * math.exp((rd - rf + basis) * years)
        expected_change = expected_forward * math.expm1(bump_bp * 1e-4 * years)
        self.assertAlmostEqual(result["forward"], expected_forward, places=12)
        self.assertAlmostEqual(result["d_forward_d_basis"], years * expected_forward, places=12)
        self.assertAlmostEqual(result["bumped_change"], expected_change, places=12)

    def test_tenor_and_notional_convention(self):
        x = basis_sensitivity(1.1, .04, .02, 2)
        self.assertAlmostEqual(x["d_forward_d_basis"], 2*x["forward"])

    def test_invalid_quotes_rates_and_basis(self):
        bad = [(0,1,.03,.05,.01,.03,1,0,0),
               (1.2,1.1,.03,.05,.01,.03,1,0,0),
               (1,1,.06,.05,.01,.03,1,0,0),
               (1,1,.03,.05,.04,.03,1,0,0),
               (1,1,.03,.05,.01,.03,0,0,0),
               (1,1,.03,.05,.01,.03,1,.02,-.02),
               (1,1,.03,.05,.01,.03,1,float("nan"),0)]
        for args in bad:
            with self.subTest(args=args), self.assertRaises(ValueError):
                funding_interval(*args)

    def test_overflow_guard(self):
        with self.assertRaises(ValueError):
            funding_interval(1,1,-1,1,-1,1,100,-1,1)

    def test_invalid_bumps(self):
        for bump in (0,-1,float("inf"),101):
            with self.subTest(bump=bump), self.assertRaises(ValueError):
                basis_sensitivity(1.1,.04,.02,1,bump_bp=bump)

    def test_no_mutation_and_determinism(self):
        args = (1.09,1.11,.03,.05,.01,.03,1)
        self.assertEqual(funding_interval(*args), funding_interval(*args))


if __name__ == "__main__":
    unittest.main()
