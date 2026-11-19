"""Deterministic synthetic tests; standard library only."""
import unittest
from tranche_loss import expected_tranche_loss, expected_portfolio_loss, tranche_loss


class TrancheTests(unittest.TestCase):
    def test_zero_default(self):
        self.assertEqual(expected_tranche_loss(pd=0), 0)
    def test_certain_default(self):
        self.assertAlmostEqual(expected_tranche_loss(n=5, pd=1, lgd=.6, attachment=.1, detachment=.3), .2)
    def test_single_name(self):
        self.assertAlmostEqual(expected_tranche_loss(n=1, pd=.2, lgd=.6, attachment=0, detachment=.5), .1)
    def test_total_portfolio_identity(self):
        for p in (.001, .1, .5, .999):
            self.assertAlmostEqual(expected_tranche_loss(n=30, pd=p, lgd=.7, attachment=0, detachment=1), expected_portfolio_loss(30,p,.7), places=12)
    def test_partition_reconciles(self):
        edges=(0, .03, .1, .3, 1)
        total=sum(expected_tranche_loss(n=40,pd=.06,lgd=.65,attachment=a,detachment=b) for a,b in zip(edges,edges[1:]))
        self.assertAlmostEqual(total,.06*.65,places=12)
    def test_monotone_pd(self):
        a=expected_tranche_loss(pd=.02)
        b=expected_tranche_loss(pd=.04)
        self.assertLessEqual(a,b)
    def test_bounds(self):
        x=expected_tranche_loss(attachment=.1,detachment=.2)
        self.assertGreaterEqual(x,0)
        self.assertLessEqual(x,.1)
    def test_invalid(self):
        cases=({"n":True},{"n":0},{"pd":float("nan")},{"pd":1.1},{"lgd":-1},{"attachment":.5,"detachment":.5},{"detachment":2},{"pd":True})
        for kwargs in cases:
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):
                expected_tranche_loss(**kwargs)
    def test_tranche_payoff(self):
        self.assertEqual(tranche_loss(.2,.05,.15),.1)


if __name__=="__main__":
    unittest.main()
