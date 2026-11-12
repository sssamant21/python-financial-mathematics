import unittest
from schedule_sensitivity import MarketBar, evaluate_schedule

class ScheduleTests(unittest.TestCase):
    def setUp(self):
        self.bars = [MarketBar(100, 100), MarketBar(102, 100)]
    def run_case(self, weights=(.5,.5), **kw):
        return evaluate_schedule(self.bars, 10, weights, arrival_price=100, **kw)
    def test_equal_full_fill(self):
        r = self.run_case()
        self.assertEqual(r['filled'], 10)
        self.assertAlmostEqual(r['shortfall'], 10)
    def test_sell_sign(self):
        self.assertAlmostEqual(self.run_case(side='sell')['shortfall'], -10)
    def test_cap_partial_and_terminal_mark(self):
        r = self.run_case(participation=.02)
        self.assertEqual(r['filled'], 4)
        self.assertEqual(r['unfilled'], 6)
        self.assertAlmostEqual(r['opportunity_cost'], 12)
    def test_fee(self):
        self.assertAlmostEqual(self.run_case(fee_bps=10)['fees'], 1.01)
    def test_impact(self):
        self.assertGreater(self.run_case(impact_bps=10)['shortfall'], self.run_case()['shortfall'])
    def test_schedule_matters(self):
        self.assertLess(self.run_case((1,0))['shortfall'], self.run_case((0,1))['shortfall'])
    def test_zero_volume(self):
        r = evaluate_schedule([MarketBar(100,0)], 10, [1], arrival_price=100)
        self.assertEqual(r['filled'], 0)
    def test_invalid_fraction(self):
        with self.assertRaises(ValueError): self.run_case((.2,.2))
    def test_negative_fraction(self):
        with self.assertRaises(ValueError): self.run_case((-1,2))
    def test_bad_cap(self):
        with self.assertRaises(ValueError): self.run_case(participation=1.1)
    def test_bad_side(self):
        with self.assertRaises(ValueError): self.run_case(side='hold')
    def test_nan(self):
        with self.assertRaises(ValueError): self.run_case(fee_bps=float('nan'))
    def test_bad_bar(self):
        with self.assertRaises(ValueError): evaluate_schedule([MarketBar(-1,100)], 10, [1], arrival_price=100)
    def test_no_lookahead_in_schedule(self):
        a = self.run_case((1,0))
        b = evaluate_schedule([self.bars[0], MarketBar(150,100)], 10, (1,0), arrival_price=100)
        self.assertEqual(a['filled'], b['filled'])
        self.assertEqual(a['price_cost'], b['price_cost'])

if __name__ == '__main__': unittest.main()
