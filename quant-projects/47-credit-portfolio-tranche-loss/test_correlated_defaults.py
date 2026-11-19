"""Seeded synthetic regression tests for correlated default stress."""
import unittest
from correlated_defaults import simulate

class CorrelatedDefaultTests(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(simulate(paths=200, seed=7), simulate(paths=200, seed=7))
    def test_zero_correlation_matches_exact_with_uncertainty(self):
        x = simulate(n=12, pd=.15, lgd=.6, attachment=0, detachment=.2, rho=0, paths=12000, seed=17)
        self.assertLess(abs(x['mean']-x['independent_exact']), 4*x['se']+.0005)
    def test_full_capital_expected_loss(self):
        x = simulate(n=10, pd=.12, lgd=.7, attachment=0, detachment=1, rho=.5, paths=16000, seed=11)
        self.assertLess(abs(x['mean']-.084), 4*x['se']+.001)
    def test_correlation_changes_senior_tail(self):
        a = simulate(n=20, pd=.06, lgd=.8, attachment=.3, detachment=1, rho=0, paths=14000, seed=5)
        b = simulate(n=20, pd=.06, lgd=.8, attachment=.3, detachment=1, rho=.7, paths=14000, seed=5)
        self.assertGreater(b['mean'], a['mean']+4*(a['se']+b['se']))
    def test_deterministic_extremes(self):
        self.assertEqual(simulate(pd=0)['mean'], 0)
        self.assertAlmostEqual(simulate(pd=1, lgd=.6, attachment=.1, detachment=.3)['mean'], .2)
        self.assertEqual(simulate(lgd=0)['se'], 0)
    def test_confidence_interval_and_bounds(self):
        x = simulate(paths=400, seed=2)
        self.assertLessEqual(x['ci95'][0], x['mean'])
        self.assertLessEqual(x['mean'], x['ci95'][1])
        self.assertGreaterEqual(x['se'], 0)
    def test_invalid(self):
        for kwargs in ({'rho':-.1}, {'rho':1}, {'rho':float('nan')}, {'rho':True},
                       {'paths':1}, {'paths':True}, {'seed':-1}, {'seed':True},
                       {'n':200, 'paths':30000}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                simulate(**kwargs)

if __name__ == "__main__":
    unittest.main()
