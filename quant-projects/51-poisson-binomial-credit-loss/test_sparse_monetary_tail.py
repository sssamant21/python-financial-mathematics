"""Deterministic, synthetic cross-checks for bounded sparse Decimal DP."""
import unittest
from decimal import Decimal
from sparse_monetary_tail import sparse_tail
from stable_monetary_tail import stable_tail


class SparseTailTests(unittest.TestCase):
    def test_enumeration_cross_check(self):
        cases = [
            ([0.1, 0.2], [100, 200], [1, 1], 300),
            ([0.1, 0.2, 0.3], [100, 100, 100], [1, 1, 1], 200),
            ([1, 0, 0.4], [100, 200, 100], [1, 1, 0], 100),
            ([0.2, 0.3], [100, 200], [1, 1], 0),
            ([0.2, 0.3], [100, 200], [1, 1], 301),
        ]
        for p, e, g, h in cases:
            with self.subTest(p=p, h=h):
                self.assertEqual(sparse_tail(p, e, g, h),
                                 stable_tail(p, e, g, h))

    def test_underflow_preserved(self):
        self.assertEqual(sparse_tail(["1e-200", "1e-200"], [100, 100], [1, 1], 200),
                         Decimal("1e-400"))

    def test_more_than_sixteen_borrowers(self):
        self.assertEqual(sparse_tail(["0.5"] * 20, [100] * 20, [1] * 20, 2001),
                         Decimal(0))
        self.assertEqual(sparse_tail([1] * 20, [100] * 20, [1] * 20, 2000),
                         Decimal(1))

    def test_state_cap_is_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "state limit"):
            sparse_tail([0.5] * 8, [2**i for i in range(8)],
                        [1] * 8, 10, max_states=16)

    def test_guardrails(self):
        for kwargs in ({"precision": True}, {"precision": 31},
                       {"max_states": True}, {"max_states": 1}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                sparse_tail([0.2], [100], [1], 1, **kwargs)
        for p, e, g, h in [
            ([True], [100], [1], 1),
            (["NaN"], [100], [1], 1),
            ([0.2], [101], [0.5], 1),
            ([0.2], [100], [1], True),
            ([0.2], [100], [True], 1),
        ]:
            with self.subTest(p=p, e=e, g=g, h=h), self.assertRaises(ValueError):
                sparse_tail(p, e, g, h)

    def test_order_invariance(self):
        a = sparse_tail([0.1, 0.2, 0.3], [100, 200, 300], [1, 1, 1], 300)
        b = sparse_tail([0.3, 0.1, 0.2], [300, 100, 200], [1, 1, 1], 300)
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
