"""Deterministic synthetic tests; no market data or trading access."""
import unittest
from option_payoff import leg, payoff_at_expiry, stress_table

class OptionPayoffTests(unittest.TestCase):
    def test_long_call(self):
        x = (leg("call", 100, 6),)
        self.assertEqual(payoff_at_expiry(x, 80), -6)
        self.assertEqual(payoff_at_expiry(x, 120), 14)
        self.assertEqual(payoff_at_expiry(x, 106), 0)
    def test_long_put(self):
        x = (leg("put", 100, 4),)
        self.assertEqual(payoff_at_expiry(x, 80), 16)
        self.assertEqual(payoff_at_expiry(x, 120), -4)
    def test_short_leg_sign(self):
        long = (leg("call", 100, 5),)
        short = (leg("call", 100, 5, -1),)
        self.assertEqual(payoff_at_expiry(long, 115), -payoff_at_expiry(short, 115))
    def test_vertical_spread_cap(self):
        spread = (leg("call", 100, 7), leg("call", 110, 3, -1))
        self.assertEqual(payoff_at_expiry(spread, 90), -4)
        self.assertEqual(payoff_at_expiry(spread, 120), 6)
        self.assertEqual(payoff_at_expiry(spread, 100), -4)
    def test_additivity(self):
        a, b = leg("call", 100, 5), leg("put", 100, 4)
        self.assertEqual(payoff_at_expiry((a,b), 120), payoff_at_expiry((a,), 120)+payoff_at_expiry((b,), 120))
    def test_scenarios(self):
        rows = stress_table((leg("put", 100, 3),), (90, 100, 110))
        self.assertEqual(rows, ((90.0, 7.0), (100.0, -3.0), (110.0, -3.0)))
    def test_bad_inputs(self):
        for args in (("call",0,1), ("call",100,-1), ("other",100,1), ("put",100,1,0), ("call",100,1,float("nan"))):
            with self.subTest(args=args), self.assertRaises(ValueError):
                leg(*args)
        for spot in (-1, float("inf"), float("nan"), True):
            with self.subTest(spot=spot), self.assertRaises(ValueError):
                payoff_at_expiry((leg("call",100,5),), spot)
        with self.assertRaises(ValueError):
            payoff_at_expiry((),100)
        with self.assertRaises(ValueError):
            stress_table((leg("call",100,5),), ())
    def test_inputs_unchanged(self):
        x = (leg("call",100,5), leg("put",90,2,-1))
        before = repr(x)
        payoff_at_expiry(x, 105)
        self.assertEqual(repr(x),before)

if __name__ == "__main__":
    unittest.main()
