"""Focused Chapter 1 representation, schedule and batch boundaries."""
import unittest
from copy import deepcopy
from fractions import Fraction as F
from section_1_02 import split_minor_units
from section_1_05 import present_value, dated_payments
from section_1_11 import minimum_transfer, evaluate_transfer
from section_1_14 import run_batch, unique_object, reject_constant


class FoundationBoundaries(unittest.TestCase):
    def test_minor_unit_conservation(self):
        for total in (0, 1, 7, 10**100 + 3):
            for count in (1, 2, 7):
                result = split_minor_units(total, count)
                self.assertEqual(sum(result), total)
                self.assertLessEqual(max(result)-min(result), 1)
                self.assertEqual(result, sorted(result, reverse=True))

    def test_one_shot_signed_repeated_date_schedule(self):
        self.assertEqual(present_value(periods=iter((1, 1, 0)),
                                      amounts=iter((125, -62.5, -50)), period_rate=.25), 0)
        self.assertEqual(present_value(periods=iter(()), amounts=iter(()), period_rate=0), 0)
        with self.assertRaises(ValueError):
            dated_payments(periods=iter((0, 1)), amounts=iter((10,)))

    def test_zero_transfer_fee_discontinuity(self):
        params = dict(source=10, destination=5, reserve=10, target=5,
                      fixed_fee=2, fee_rate=0)
        zero = minimum_transfer(**params)
        self.assertEqual(zero["transfer"], 0)
        self.assertEqual(zero["candidate_report"]["fee"], 0)
        positive = evaluate_transfer(transfer=F(1, 10**100), **params)
        self.assertEqual(positive["fee"], 2)
        self.assertFalse(positive["feasible"])
        self.assertIsNone(minimum_transfer(**(params | {"target": 6}))["transfer"])

    def test_batch_status_isolation_and_input_preservation(self):
        good = dict(id="good", formula="growth", currency="USD",
                    inputs=dict(principal=100, rate=10, representation="percent", periods=2),
                    observed=121)
        wrong = deepcopy(good)
        wrong.update(id="wrong", observed=110)
        invalid = deepcopy(good)
        invalid["id"] = "invalid"
        del invalid["inputs"]["representation"]
        document = dict(schema_version=1, cases=[good, wrong, invalid])
        before = deepcopy(document)
        result = run_batch(document)
        self.assertEqual(result["counts"], dict(PASS=1, FAIL=1, INVALID=1))
        self.assertEqual(document, before)
        self.assertFalse(result["success"])

    def test_ambiguous_json_and_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):
            unique_object([("rate", 1), ("rate", 2)])
        for token in ("NaN", "Infinity", "-Infinity"):
            with self.assertRaises(ValueError):
                reject_constant(token)
        with self.assertRaises(ValueError):
            run_batch(dict(schema_version=1, cases=[dict(id="same"), dict(id="same")]))


if __name__ == "__main__":
    unittest.main()
