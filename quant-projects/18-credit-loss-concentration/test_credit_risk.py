import unittest
from credit_risk import Exposure, summarize

class CreditRiskTests(unittest.TestCase):
    def setUp(self):
        self.book = [Exposure('A', 100, .1, .5), Exposure('B', 100, .2, .4)]

    def test_expected_loss(self):
        self.assertAlmostEqual(summarize(self.book)['expected_loss'], 13)

    def test_hhi(self):
        self.assertAlmostEqual(summarize(self.book)['ead_hhi'], .5)

    def test_stress(self):
        self.assertAlmostEqual(summarize(self.book, 2, .1)['expected_loss'], 32)

    def test_pd_cap(self):
        self.assertAlmostEqual(summarize([Exposure('A', 100, .9, 1)], 2)['expected_loss'], 100)

    def test_zero_total(self):
        with self.assertRaises(ValueError): summarize([Exposure('A', 0, .1, .5)])

    def test_duplicate_names(self):
        with self.assertRaises(ValueError): summarize(self.book + [self.book[0]])

    def test_invalid_probability(self):
        with self.assertRaises(ValueError): summarize([Exposure('A', 10, 1.1, .4)])

    def test_nonfinite(self):
        with self.assertRaises(ValueError): summarize([Exposure('A', float('nan'), .1, .5)])

    def test_invalid_stress(self):
        with self.assertRaises(ValueError): summarize(self.book, -1)

    def test_no_mutation(self):
        before = self.book[:]
        summarize(self.book, 2, .1)
        self.assertEqual(self.book, before)

if __name__ == '__main__': unittest.main()
