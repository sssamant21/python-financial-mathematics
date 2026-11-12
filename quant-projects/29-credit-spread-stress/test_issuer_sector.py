import math
import unittest
from spread_stress import Position, scenario
from issuer_sector import CreditHolding, evaluate, example

class IssuerSectorTests(unittest.TestCase):
    def setUp(self):
        self.h = [CreditHolding(Position("a", 1000, 4, 10), "A", "Tech"),
                  CreditHolding(Position("b", 1000, 2), "B", "Energy")]

    def run_case(self, sectors=None, issuers=None, holdings=None):
        return evaluate(self.h if holdings is None else holdings,
                        {"Tech": 100, "Energy": 50} if sectors is None else sectors,
                        {} if issuers is None else issuers)

    def test_zero(self):
        self.assertEqual(self.run_case({"Tech": 0, "Energy": 0})["pnl"], 0)

    def test_parallel_matches_baseline(self):
        self.assertAlmostEqual(self.run_case({"Tech": 100, "Energy": 100})["pnl"],
                               scenario([h.position for h in self.h], 100)["pnl"])

    def test_issuer_additive(self):
        self.assertAlmostEqual(self.run_case(issuers={"A": 50})["position_pnl"]["a"],
                               scenario([self.h[0].position], 150)["pnl"])

    def test_attribution(self):
        r = example()
        self.assertAlmostEqual(sum(r["position_pnl"].values()), r["pnl"])
        self.assertAlmostEqual(sum(r["issuer_pnl"].values()), r["pnl"])
        self.assertAlmostEqual(sum(r["sector_pnl"].values()), r["pnl"])
        self.assertAlmostEqual(r["loss"], -r["pnl"])

    def test_hhi(self):
        r = self.run_case()
        self.assertAlmostEqual(r["issuer_hhi"], 0.5)
        self.assertAlmostEqual(r["sector_hhi"], 0.5)
        self.assertAlmostEqual(example()["issuer_hhi"], 0.625)

    def test_determinism(self):
        self.assertEqual(example(), example())

    def test_empty(self):
        with self.assertRaises(ValueError):
            self.run_case(holdings=[])

    def test_missing_or_extra_sector(self):
        for m in ({"Tech": 100}, {"Tech": 100, "Energy": 50, "Other": 1}):
            with self.subTest(m=m), self.assertRaises(ValueError):
                self.run_case(sectors=m)

    def test_unknown_issuer(self):
        with self.assertRaises(ValueError):
            self.run_case(issuers={"Z": 20})

    def test_bad_shocks(self):
        for x in (math.nan, math.inf, True, 2001):
            with self.subTest(x=x), self.assertRaises(ValueError):
                self.run_case(sectors={"Tech": x, "Energy": 50})

    def test_combined_cap(self):
        with self.assertRaises(ValueError):
            self.run_case(sectors={"Tech": 1900, "Energy": 0}, issuers={"A": 200})

    def test_bad_holding(self):
        for h in (CreditHolding(Position("a", 100, 2), "", "Tech"),
                  CreditHolding(Position("a", 100, 2), "A", "")):
            with self.subTest(h=h), self.assertRaises(ValueError):
                self.run_case(holdings=[h])

    def test_duplicate_positions(self):
        with self.assertRaises(ValueError):
            self.run_case(holdings=[self.h[0], self.h[0]])

if __name__ == "__main__":
    unittest.main()
