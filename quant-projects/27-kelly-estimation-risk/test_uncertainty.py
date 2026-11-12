"""Deterministic Wilson-score and Kelly uncertainty tests."""
import math
import unittest
from uncertainty import wilson_interval, conservative_diagnostic


class UncertaintyTests(unittest.TestCase):
    def test_symmetric_half(self):
        lo, hi = wilson_interval(50, 100)
        self.assertAlmostEqual(lo + hi, 1.)
        self.assertLess(lo, .5)
    def test_known_wilson(self):
        lo, hi = wilson_interval(55, 100)
        self.assertAlmostEqual(lo, .452445, places=5)
        self.assertAlmostEqual(hi, .643855, places=5)
    def test_sample_size_narrows(self):
        a, b = wilson_interval(11, 20)
        c, d = wilson_interval(550, 1000)
        self.assertLess(d-c, b-a)
    def test_zero_successes(self):
        lo, hi = wilson_interval(0, 10)
        self.assertEqual(lo, 0.)
        self.assertGreater(hi, 0.)
    def test_all_successes(self):
        lo, hi = wilson_interval(10, 10)
        self.assertEqual(hi, 1.)
        self.assertLess(lo, 1.)
    def test_reject_invalid_counts(self):
        for w, n in ((-1, 10), (11, 10), (0, 0), (True, 10), (1., 10), (1, False)):
            with self.subTest(w=w, n=n), self.assertRaises(ValueError): wilson_interval(w, n)
    def test_reject_invalid_z(self):
        for z in (0., -1., float('nan'), float('inf'), True):
            with self.subTest(z=z), self.assertRaises(ValueError): wilson_interval(5, 10, z)
    def test_conservative_no_more_than_point(self):
        _, _, point, robust, _ = conservative_diagnostic(60, 100)
        self.assertLessEqual(robust, point)
    def test_low_evidence_zero_fraction(self):
        _, _, point, robust, _ = conservative_diagnostic(55, 100)
        self.assertAlmostEqual(point, .1)
        self.assertEqual(robust, 0.)
    def test_scenarios_fixed(self):
        *_, rows = conservative_diagnostic(65, 100)
        self.assertEqual([r[0] for r in rows], [.45, .5, .55])
        self.assertTrue(all(math.isfinite(g) for _, a, b in rows for g in (a, b)))
    def test_invalid_payoff(self):
        with self.assertRaises(ValueError): conservative_diagnostic(55, 100, win_return=-1)
    def test_boundary_point(self):
        _, _, point, robust, _ = conservative_diagnostic(0, 10)
        self.assertEqual(point, 0.)
        self.assertEqual(robust, 0.)


if __name__ == '__main__':
    unittest.main()
