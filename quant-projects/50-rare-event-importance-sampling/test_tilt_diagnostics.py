import math
import unittest

from tilt_diagnostics import diagnose


class TiltDiagnosticsTests(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(diagnose(paths=200, seed=7), diagnose(paths=200, seed=7))

    def test_analytical_reference(self):
        self.assertAlmostEqual(diagnose(n=1, p=.2, threshold=1,
                                        tilts=(.2,), paths=200)[0]["exact"], .2)

    def test_ess_bounds(self):
        for row in diagnose(paths=300):
            self.assertGreater(row["ess"], 0)
            self.assertLessEqual(row["ess_fraction"], 1 + 1e-12)
            self.assertGreaterEqual(row["se"], 0)

    def test_identity_tilt_has_full_ess(self):
        row = diagnose(tilts=(.02,), paths=300)[0]
        self.assertAlmostEqual(row["ess_fraction"], 1, places=12)

    def test_reference_is_shared(self):
        rows = diagnose(tilts=(.08, .17), paths=300)
        self.assertEqual(rows[0]["exact"], rows[1]["exact"])

    def test_invalid_inputs(self):
        for kwargs in ({"tilts": ()}, {"tilts": (.1, .1)},
                       {"tilts": (0,)}, {"tilts": (math.nan,)},
                       {"tilts": (.1,)*13}, {"seed": -1},
                       {"paths": 50}, {"n": True}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                diagnose(**kwargs)


if __name__ == "__main__":
    unittest.main()
