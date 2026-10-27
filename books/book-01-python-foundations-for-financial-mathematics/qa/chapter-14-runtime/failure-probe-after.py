from math import fsum, isfinite
import unittest

def validate(weights):
    if not weights:
        raise ValueError("empty distribution")
    for p in weights.values():
        if isinstance(p, bool) or not isinstance(p, (int,float)) or not isfinite(p) or not 0 <= p <= 1:
            raise ValueError("probabilities must be finite and between 0 and 1")
    if abs(fsum(weights.values())-1) > 1e-12:
        raise ValueError("probabilities must sum to 1")
    return dict(weights)

def probability(weights, event):
    weights=validate(weights)
    event=set(event)
    if not event.issubset(weights):
        raise ValueError("event outside sample space")
    return fsum(weights[outcome] for outcome in event)

def complement(weights, event):
    weights=validate(weights)
    return probability(weights, set(weights)-set(event))

def union_probability(weights, a, b):
    return probability(weights, set(a)|set(b))

def intersection_probability(weights, a, b):
    return probability(weights, set(a)&set(b))

def conditional_probability(weights, a, given):
    denominator=probability(weights,given)
    if denominator == 0:
        raise ValueError("conditioning event has zero probability")
    return intersection_probability(weights,a,given)/denominator

def independent(weights,a,b,tolerance=1e-12):
    pa=probability(weights,a)
    pb=probability(weights,b)
    pab=intersection_probability(weights,a,b)
    return abs(pab-pa*pb)<=tolerance

class ProbabilityRulesTests(unittest.TestCase):
    def setUp(self):
        self.weights={"normal_ok":.72,"normal_default":.08,
                      "stress_ok":.15,"stress_default":.05}
        self.stress={"stress_ok","stress_default"}
        self.default={"normal_default","stress_default"}
    def test_01_total(self): self.assertAlmostEqual(probability(self.weights,self.weights),1)
    def test_02_empty(self): self.assertEqual(probability(self.weights,[]),0)
    def test_03_complement(self): self.assertAlmostEqual(complement(self.weights,self.stress),.8)
    def test_04_stress(self): self.assertAlmostEqual(probability(self.weights,self.stress),.2)
    def test_05_default(self): self.assertAlmostEqual(probability(self.weights,self.default),.13)
    def test_06_intersection(self): self.assertAlmostEqual(intersection_probability(self.weights,self.stress,self.default),.05)
    def test_07_union(self): self.assertAlmostEqual(union_probability(self.weights,self.stress,self.default),.28)
    def test_08_conditional(self): self.assertAlmostEqual(conditional_probability(self.weights,self.default,self.stress),.25)
    def test_09_dependent(self): self.assertFalse(independent(self.weights,self.stress,self.default))
    def test_10_disjoint_addition(self):
        a={"normal_ok"}
        b={"stress_ok"}
        self.assertAlmostEqual(union_probability(self.weights,a,b),.87)
    def test_11_invalid_weights(self):
        with self.assertRaises(ValueError): probability({"a":.7,"b":.4},{"a"})
    def test_12_invalid_events(self):
        for fn in (lambda:probability(self.weights,{"missing"}),
                   lambda:conditional_probability(self.weights,self.default,set()),
                   lambda:probability({"a":float("nan")},{"a"})):
            with self.assertRaises(ValueError): fn()

if __name__ == "__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ProbabilityRulesTests)
    suite.addTest(unittest.FunctionTestCase(lambda: (_ for _ in ()).throw(AssertionError("intentional failure probe"))))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
