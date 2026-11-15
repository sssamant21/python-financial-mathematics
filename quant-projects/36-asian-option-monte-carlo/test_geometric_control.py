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


    def test_deep_in_the_money_geometric_limit(self):
        # With a very low strike, the call approaches discounted E[G] - discounted K.
        spot, strike, rate, vol, maturity, n = 100., 1e-6, .03, .2, 1., 12
        mu = math.log(spot) + (rate-vol**2/2)*maturity*(n+1)/(2*n)
        variance = vol**2*maturity*(n+1)*(2*n+1)/(6*n*n)
        expected = math.exp(-rate*maturity)*(math.exp(mu+variance/2)-strike)
        self.assertAlmostEqual(geometric_call_exact(spot,strike,rate,vol,maturity,n), expected, places=8)

    def test_single_fixing_black_scholes_reference(self):
        # An independently written vanilla call expression for n=1.
        spot, strike, rate, vol, maturity = 100., 105., .02, .3, 1.5
        sd = vol*math.sqrt(maturity)
        d1 = (math.log(spot/strike)+(rate+vol**2/2)*maturity)/sd
        d2 = d1-sd
        cdf = lambda x: math.erfc(-x/math.sqrt(2))/2
        reference = spot*cdf(d1)-strike*math.exp(-rate*maturity)*cdf(d2)
        self.assertAlmostEqual(geometric_call_exact(spot,strike,rate,vol,maturity,1), reference, places=10)

    def test_high_volatility_stress_finite_and_reproducible(self):
        # Stress within the implementation's declared volatility-times-sqrt(T) bound.
        params = dict(spot=100.,strike=100.,rate=-.01,volatility=1.5,
                      maturity=1.,observations=12,pairs=120,seed=123)
        a = compare_estimators(**params)
        b = compare_estimators(**params)
        self.assertEqual(a,b)
        for key in ('arithmetic_price','arithmetic_se','controlled_price',
                    'controlled_se','geometric_exact'):
            self.assertTrue(math.isfinite(a[key]), key)
        self.assertGreaterEqual(a['arithmetic_se'],0)
        self.assertGreaterEqual(a['controlled_se'],0)

    def test_exponent_guard_and_bool_inputs(self):
        for kwargs in ({'volatility':3.1},{'rate':60.},{'observations':True}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                geometric_call_exact(**kwargs)
        with self.assertRaises(ValueError):
            compare_estimators(pairs=True)

if __name__=='__main__': unittest.main()
