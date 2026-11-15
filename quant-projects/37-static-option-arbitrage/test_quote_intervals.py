import unittest
from quote_intervals import screen, calendar_screen

class QuoteIntervalTests(unittest.TestCase):
    def test_feasible(self):
        self.assertTrue(screen([90,100,110],[14,9,5],[15,10,6])["valid_necessary_conditions"])
    def test_monotonicity(self):
        self.assertIn("monotonicity:0",screen([90,100,110],[10,12,4],[11,13,5])["issues"])
    def test_vertical(self):
        self.assertIn("vertical_spread_bound:0",screen([90,100,110],[25,8,5],[26,9,6])["issues"])
    def test_irregular_convexity(self):
        self.assertIn("convexity:1",screen([90,100,130],[18,16,2],[19,17,3])["issues"])
    def test_wide_spread(self):
        self.assertTrue(screen([90,100,110],[7,6,2],[20,18,16])["valid_necessary_conditions"])
    def test_calendar(self):
        self.assertIn("calendar:1",calendar_screen([8,9,2],[10,7,4],earlier_discount=1,later_discount=1)["issues"])
    def test_discount(self):
        self.assertTrue(calendar_screen([9],[8.5],earlier_discount=1,later_discount=.9)["valid_necessary_conditions"])
        self.assertIn("calendar:0",calendar_screen([10],[8],earlier_discount=1,later_discount=.9)["issues"])
    def test_guards(self):
        for k,b,a in [([90,100,110],[1,2,3],[2,1,4]),([90,90,110],[1,2,3],[2,3,4]),([90,100,110],[1,float("nan"),3],[2,3,4])]:
            with self.assertRaises(ValueError): screen(k,b,a)
        with self.assertRaises(ValueError): screen([90,100,110],[1,2,3],[2,3,4],discount=True)
        with self.assertRaises(ValueError): calendar_screen([1],[2],earlier_discount=0,later_discount=1)

if __name__ == "__main__":
    unittest.main()
