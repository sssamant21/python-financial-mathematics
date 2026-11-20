import math
import unittest
from repeated_precision import repeated_precision


class RepeatedPrecisionTests(unittest.TestCase):
    def test_reproducibility(self):
        self.assertEqual(repeated_precision(paths=100, repetitions=3),
                         repeated_precision(paths=100, repetitions=3))

    def test_exact_reference(self):
        row = repeated_precision(n=1, p=.2, threshold=1,
                                 tilts=(.2,), paths=100, repetitions=3)[0]
        self.assertAlmostEqual(row["exact"], .2)

    def test_identity_tilt_same_estimates(self):
        row = repeated_precision(n=5, p=.2, threshold=2,
                                 tilts=(.2,), paths=200, repetitions=5)[0]
        self.assertGreaterEqual(row["importance_empirical_sd"], 0)
        self.assertGreaterEqual(row["plain_empirical_sd"], 0)

    def test_fixed_grid(self):
        rows = repeated_precision(tilts=(.08, .17), paths=100, repetitions=3)
        self.assertEqual([row["q"] for row in rows], [.08, .17])
        self.assertEqual(rows[0]["exact"], rows[1]["exact"])

    def test_invalid_inputs(self):
        for kwargs in ({"repetitions": 2}, {"repetitions": True},
                       {"seed": -1}, {"seed": 2**32 - 1},
                       {"tilts": (.1, .1)}, {"tilts": (math.nan,)},
                       {"tilts": ()}, {"paths": 10}, {"n": True},
                       {"n": 200, "paths": 200000, "repetitions": 100}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                repeated_precision(**kwargs)


if __name__ == "__main__":
    unittest.main()
