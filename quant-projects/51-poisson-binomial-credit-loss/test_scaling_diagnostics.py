"""Synthetic-only checks for bounded state-growth diagnostics."""
import copy
import unittest
from scaling_diagnostics import summarize


def fixture():
    rows = []
    for pattern, ns in [('equal', (4, 8)), ('distinct', (4, 8))]:
        for n in ns:
            rows.append({'borrowers': n, 'pattern': pattern,
                         'expected_states': n + 1 if pattern == 'equal' else 2 ** n,
                         'analytical_tail': str(1 - __import__('decimal').Decimal('0.75') ** n),
                         'peak_traced_bytes_min': 100,
                         'peak_traced_bytes_median': 110,
                         'peak_traced_bytes_max': 120})
    return {'schema_version': 1, 'synthetic_only': True, 'repetitions': 3,
            'python_version': '3.11', 'platform': 'test',
            'batch_seconds_min': 0.1, 'batch_seconds_median': 0.2,
            'batch_seconds_max': 0.3, 'rows': rows}


class ScalingDiagnosticsTests(unittest.TestCase):
    def test_expected_growth_and_sorting(self):
        report = fixture()
        report['rows'].reverse()
        rows = summarize(report)
        self.assertEqual([(r['pattern'], r['borrowers']) for r in rows],
                         [('equal', 4), ('equal', 8), ('distinct', 4), ('distinct', 8)])
        self.assertEqual([r['state_growth_from_previous'] for r in rows],
                         [None, 9 / 5, None, 16.0])

    def test_rejects_corrupted_state_count(self):
        report = fixture()
        report['rows'][0]['expected_states'] = 6
        with self.assertRaises(ValueError):
            summarize(report)

    def test_rejects_non_synthetic_evidence(self):
        report = fixture()
        report['synthetic_only'] = False
        with self.assertRaises(ValueError):
            summarize(report)

    def test_no_mutation(self):
        report = fixture()
        before = copy.deepcopy(report)
        summarize(report)
        self.assertEqual(report, before)


if __name__ == '__main__':
    unittest.main()
