"""Chapter 5 recurrence cancellation and withdrawal regressions."""
import math
import unittest
from section_5_03 import balance_ledger
from section_5_09 import Period, run_engine, closed_form_reference

class RecurrenceBoundaries(unittest.TestCase):
    def test_near_minus_one_rate(self):
        rate=math.nextafter(-1,0)
        expected=1e16*(1+rate)
        balances,ledger=balance_ledger(1e16,[rate],[0])
        self.assertEqual(balances[-1],expected)
        result=run_engine(1e16,[Period(rate,0)])
        self.assertEqual(result.closing,expected)
        self.assertEqual(result.closing,closed_form_reference(1e16,[Period(rate,0)]))
        self.assertNotEqual(ledger[0]['rounding_adjustment'],0)
    def test_withdrawal_rejected_at_correct_available_balance(self):
        result=run_engine(1e16,[Period(math.nextafter(-1,0),-1.5)],allow_negative=False)
        self.assertEqual(result.first_rejected,1)
        self.assertEqual(result.ledger[0]['applied'],0)
    def test_beginning_payment(self):
        rate=math.nextafter(-1,0)
        result=run_engine(1e16,[Period(rate,1e16)],timing='begin')
        self.assertEqual(result.closing,2e16*(1+rate))

if __name__ == '__main__': unittest.main()
