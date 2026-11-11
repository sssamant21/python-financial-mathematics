import unittest
from withdrawal_sensitivity import funding_diagnostics, sensitivity_grid
from sequence_risk import simulate


class WithdrawalSensitivityTests(unittest.TestCase):
    def test_no_shortfall(self):
        r = funding_diagnostics(100, 10, [0, 0])
        self.assertEqual(r['total_shortfall'], 0)
        self.assertEqual(r['total_funded'], 20)
        self.assertEqual(r['terminal'], 80)

    def test_partial_funding_and_future_shortfall(self):
        r = funding_diagnostics(10, 8, [0, 0, 0])
        self.assertEqual([x['funded'] for x in r['rows']], [8, 2, 0])
        self.assertEqual([x['shortfall'] for x in r['rows']], [0, 6, 8])
        self.assertEqual(r['ruin_year'], 2)
        self.assertEqual(r['total_shortfall'], 14)

    def test_exact_exhaustion_not_ruin(self):
        self.assertIsNone(funding_diagnostics(10, 10, [0])['ruin_year'])

    def test_matches_baseline_terminal_and_ruin(self):
        for rs in ([0.1, -0.2, 0.3], [-1, 0, 0], [0, 0]):
            with self.subTest(rs=rs):
                a = funding_diagnostics(100, 35, rs, 0.02)
                b = simulate(100, 35, rs, 0.02)
                self.assertAlmostEqual(a['terminal'], b['terminal'])
                self.assertEqual(a['ruin_year'], b['ruin_year'])

    def test_accounting_identity(self):
        r = funding_diagnostics(100, 50, [-0.5, 0, 0], 0.1)
        self.assertAlmostEqual(r['total_due'], r['total_funded'] + r['total_shortfall'])

    def test_higher_inflation_not_less_shortfall_for_zero_returns(self):
        a = funding_diagnostics(100, 40, [0, 0, 0], 0)
        b = funding_diagnostics(100, 40, [0, 0, 0], 0.1)
        self.assertGreaterEqual(b['total_shortfall'], a['total_shortfall'])

    def test_grid_size_and_reproducibility(self):
        self.assertEqual(sensitivity_grid(), sensitivity_grid())
        self.assertEqual(len(sensitivity_grid()), 12)

    def test_zero_withdrawal(self):
        r = sensitivity_grid(returns=[0, 0], rates=[0], inflations=[0])[0]
        self.assertEqual(r['funded_fraction'], 1)
        self.assertEqual(r['total_shortfall'], 0)

    def test_invalid_rates_and_grid(self):
        for kwargs in ({'rates': [-0.01]}, {'rates': [1.01]}, {'rates': [float('nan')]},
                       {'inflations': [-1]}, {'inflations': [float('inf')]},
                       {'rates': []}, {'inflations': []}, {'initial': 0}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                sensitivity_grid(**kwargs)

    def test_invalid_returns(self):
        with self.assertRaises(ValueError):
            funding_diagnostics(100, 10, [float('nan')])

    def test_no_mutation(self):
        rs = [-0.2, 0.3]
        funding_diagnostics(100, 10, rs)
        self.assertEqual(rs, [-0.2, 0.3])


if __name__ == '__main__':
    unittest.main()
