import math
import unittest
from geometric_control import geometric_call_exact, compare_estimators

class GeometricControlTests(unittest.TestCase):
    def test_reproducibility(self):
        self.assertEqual(compare_estimators(pairs=100,seed=4), compare_estimators(pairs=100,seed=4))
    def test_single_observation_identity(self):
        r=compare_estimators(observations=1,pairs=200)
        self.assertAlmostEqual(r['controlled_price'],r['geometric_exact'],places=10)
        self.assertLess(r['controlled_se'],1e-10)
    def test_geometric_bound(self):
        r=compare_estimators(pairs=300)
        self.assertGreaterEqual(r['geometric_exact'],0)
        self.assertTrue(all(math.isfinite(v) for v in r.values()))
    def test_precision_reduction_fixture(self):
        r=compare_estimators(pairs=500,seed=2026)
        self.assertLess(r['controlled_se'],r['arithmetic_se'])
    def test_invalid(self):
        for kwargs in ({'spot':0},{'volatility':float('nan')},{'observations':0},{'rate':100}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                geometric_call_exact(**kwargs)
        with self.assertRaises(ValueError): compare_estimators(pairs=1)

if __name__=='__main__': unittest.main()
