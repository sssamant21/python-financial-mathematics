import unittest
from monetary_loss import loss_distribution, expected_loss, tail_probability


class MonetaryLossTests(unittest.TestCase):
    def test_two_borrowers(self):
        pmf = loss_distribution([0.1, 0.2], [100, 200], ["0.5", "0.5"])
        self.assertEqual(set(pmf), {0, 50, 100, 150})
        for k, expected in {0: 0.72, 50: 0.08, 100: 0.18, 150: 0.02}.items():
            self.assertAlmostEqual(pmf[k], expected)
        self.assertAlmostEqual(expected_loss(pmf), 25)
        self.assertAlmostEqual(tail_probability(pmf, 100), 0.2)

    def test_zero_lgd_coalesces(self):
        self.assertEqual(loss_distribution([0.5], [100], ["0"]), {0: 1.0})

    def test_deterministic(self):
        self.assertEqual(loss_distribution([1, 0], [100, 200], ["0.5", "1"]), {50: 1.0})

    def test_nonintegral_cent_rejected(self):
        with self.assertRaises(ValueError):
            loss_distribution([0.5], [1], ["0.5"])

    def test_bad_inputs(self):
        for probs, exposures, lgds in [([float("nan")], [100], ["1"]),
                                       ([True], [100], ["1"]),
                                       ([0.2], [-1], ["1"]),
                                       ([0.2], [100], ["1.1"]),
                                       ([0.2], [100], ["NaN"])]:
            with self.assertRaises(ValueError):
                loss_distribution(probs, exposures, lgds)

    def test_threshold_guardrail(self):
        with self.assertRaises(ValueError):
            tail_probability({0: 1}, -1)


if __name__ == "__main__":
    unittest.main()
