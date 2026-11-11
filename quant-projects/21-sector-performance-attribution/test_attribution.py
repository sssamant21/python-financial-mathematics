"""Deterministic regression tests for arithmetic attribution."""
import math
import unittest
from attribution import attribute


class AttributionTests(unittest.TestCase):
    def calc(self, wp=(0.6, 0.4), wb=(0.5, 0.5), rp=(0.1, 0.02), rb=(0.08, 0.03)):
        return attribute(('A', 'B'), wp, wb, rp, rb)

    def test_reconciles_active_return(self):
        result = self.calc()
        self.assertAlmostEqual(result['effects']['active'], result['active_return'])

    def test_equal_portfolios_zero(self):
        result = self.calc(wp=(0.5, 0.5), rp=(0.08, 0.03))
        self.assertAlmostEqual(result['active_return'], 0)
        self.assertTrue(all(abs(x['active']) < 1e-12 for x in result['sectors']))

    def test_allocation_only(self):
        result = self.calc(rp=(0.08, 0.03))
        self.assertAlmostEqual(result['effects']['selection'], 0)
        self.assertAlmostEqual(result['effects']['interaction'], 0)

    def test_selection_only(self):
        result = self.calc(wp=(0.5, 0.5))
        self.assertAlmostEqual(result['effects']['allocation'], 0)
        self.assertAlmostEqual(result['effects']['interaction'], 0)

    def test_one_sector(self):
        result = attribute(('Only',), (1,), (1,), (0.1,), (0.03,))
        self.assertAlmostEqual(result['effects']['selection'], 0.07)

    def test_reject_weights(self):
        for wp in ((0.6, 0.5), (-0.1, 1.1), (math.nan, 0.5)):
            with self.subTest(wp=wp), self.assertRaises(ValueError):
                self.calc(wp=wp)

    def test_reject_bad_returns(self):
        for rp in ((-1.01, 0), (math.inf, 0)):
            with self.subTest(rp=rp), self.assertRaises(ValueError):
                self.calc(rp=rp)

    def test_reject_duplicate_names(self):
        with self.assertRaises(ValueError):
            attribute(('A', 'A'), (0.5, 0.5), (0.5, 0.5), (0, 0), (0, 0))

    def test_reject_length_mismatch(self):
        with self.assertRaises(ValueError):
            self.calc(rp=(0.1,))

    def test_repeatability(self):
        self.assertEqual(self.calc(), self.calc())


if __name__ == '__main__':
    unittest.main()
