"""Synthetic Monte Carlo diagnostics: fixed-seed checks, not market calibration."""
import math
import unittest

from correlated_defaults import simulate


class MonteCarloDiagnostics(unittest.TestCase):
    def test_standard_error_shrinks_with_more_paths(self):
        # Compare a stable positive-variance setting; not a coverage guarantee.
        small = simulate(n=20, pd=.1, lgd=.7, attachment=0, detachment=1,
                         rho=.3, paths=2000, seed=47)
        large = simulate(n=20, pd=.1, lgd=.7, attachment=0, detachment=1,
                         rho=.3, paths=16000, seed=47)
        self.assertGreater(small["se"], 0)
        self.assertLess(large["se"], small["se"] * .65)

    def test_portfolio_loss_reconciles_to_expected_pd_lgd(self):
        # Correlation changes the loss distribution, not its theoretical mean.
        for rho in (0, .25, .6):
            with self.subTest(rho=rho):
                result = simulate(n=20, pd=.1, lgd=.7, attachment=0,
                                  detachment=1, rho=rho, paths=20000, seed=17)
                self.assertLess(abs(result["mean"] - .07), 5 * result["se"] + .002)

    def test_tranche_partition_reconciles_using_mc_uncertainty(self):
        # Separate seeded simulations: errors are not independent, so use a
        # conservative sum of standard errors rather than a joint CI.
        layers = ((0, .05), (.05, .2), (.2, 1))
        results = [simulate(n=20, pd=.1, lgd=.7, attachment=a,
                            detachment=d, rho=.45, paths=18000, seed=9)
                   for a, d in layers]
        discrepancy = abs(sum(x["mean"] for x in results) - .07)
        self.assertLess(discrepancy, 5 * sum(x["se"] for x in results) + .002)

    def test_seeded_pathwise_tranche_partition_identity(self):
        # Identical seeds and simulation parameters produce identical default
        # paths across tranche calls. Their losses must add up path by path,
        # hence the sample means must reconcile to floating-point precision.
        common = dict(n=20, pd=.1, lgd=.7, rho=.45, paths=2000, seed=91)
        portfolio = simulate(attachment=0, detachment=1, **common)
        layers = [(0, .05), (.05, .2), (.2, 1)]
        layer_means = [
            simulate(attachment=a, detachment=d, **common)["mean"]
            for a, d in layers
        ]
        self.assertAlmostEqual(sum(layer_means), portfolio["mean"], places=11)

    def test_stress_results_are_bounded_and_finite(self):
        for rho in (0, .25, .6):
            with self.subTest(rho=rho):
                x = simulate(n=20, pd=.06, lgd=.8, attachment=.3,
                             detachment=1, rho=rho, paths=5000, seed=23)
                self.assertTrue(all(math.isfinite(v) for v in
                                    (x["mean"], x["se"], *x["ci95"])))
                self.assertLessEqual(0, x["ci95"][0])
                self.assertLessEqual(x["ci95"][0], x["mean"])
                self.assertLessEqual(x["mean"], x["ci95"][1])
                self.assertLessEqual(x["ci95"][1], .7 + 1e-12)


if __name__ == "__main__":
    unittest.main()
