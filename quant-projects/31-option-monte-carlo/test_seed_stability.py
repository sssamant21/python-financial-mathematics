import unittest
from seed_stability import study


class SeedStabilityTests(unittest.TestCase):
    def test_deterministic_nested_seed_prefixes(self):
        args = dict(pairs=30, seeds=(3, 5, 7, 11), counts=(2, 4))
        first = study(**args)
        self.assertEqual(first, study(**args))
        self.assertEqual([r["seed_count"] for r in first["rows"]], [2, 4])
        self.assertEqual(first["paths_per_estimator_per_seed"], 60)

    def test_metrics_are_finite_or_explicitly_undefined(self):
        for row in study(pairs=30, seeds=(3, 5, 7, 11), counts=(2, 4))["rows"]:
            for key in ("naive_coverage", "antithetic_coverage"):
                self.assertGreaterEqual(row[key], 0)
                self.assertLessEqual(row[key], 1)
            for key in ("naive_variance", "antithetic_variance"):
                self.assertGreaterEqual(row[key], 0)
            ratio = row["variance_ratio"]
            self.assertTrue(ratio is None or ratio >= 0)

    def test_guardrails(self):
        invalid = ({"pairs": True}, {"pairs": 1}, {"seeds": (1, 1)},
                   {"seeds": (1, True)}, {"counts": (1,)},
                   {"counts": (4, 2)}, {"counts": (2, 2)},
                   {"seeds": (1, 2), "counts": (4,)})
        for kwargs in invalid:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                study(**kwargs)


if __name__ == "__main__":
    unittest.main()
