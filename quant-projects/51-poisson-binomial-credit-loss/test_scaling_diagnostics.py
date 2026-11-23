"""Synthetic-only checks for bounded state-growth diagnostics."""
import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
from scaling_diagnostics import main, summarize


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

    def test_memory_passthrough_and_reproducibility(self):
        report = fixture()
        first = summarize(report)
        self.assertEqual(first, summarize(report))
        self.assertEqual([r['peak_traced_bytes_median'] for r in first],
                         [110, 110, 110, 110])
        self.assertEqual([r['states'] for r in first], [5, 9, 16, 256])

    def test_rejects_corrupted_analytical_tail(self):
        report = fixture()
        report['rows'][0]['analytical_tail'] = '0.5'
        with self.assertRaises(ValueError):
            summarize(report)

    def test_no_mutation(self):
        report = fixture()
        before = copy.deepcopy(report)
        summarize(report)
        self.assertEqual(report, before)


    def test_cli_json_contract(self):
        report = fixture()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'synthetic.json'
            path.write_text(json.dumps(report), encoding='utf-8')
            output = io.StringIO()
            with patch('sys.argv', ['scaling_diagnostics.py', str(path)]):
                with redirect_stdout(output):
                    main()
        payload = json.loads(output.getvalue())
        self.assertIs(payload['synthetic_only'], True)
        self.assertEqual(len(payload['state_growth']), 4)
        self.assertEqual(set(payload), {'synthetic_only', 'state_growth', 'caveat'})
        self.assertTrue(payload['caveat'])
        for row in payload['state_growth']:
            self.assertEqual(set(row), {
                'pattern', 'borrowers', 'states',
                'state_growth_from_previous', 'peak_traced_bytes_median'})
            self.assertIsInstance(row['states'], int)
            self.assertGreater(row['peak_traced_bytes_median'], 0)

    def test_cli_rejects_invalid_report_without_json_success(self):
        report = fixture()
        report['rows'][0]['expected_states'] = 999
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'invalid.json'
            path.write_text(json.dumps(report), encoding='utf-8')
            output = io.StringIO()
            with patch('sys.argv', ['scaling_diagnostics.py', str(path)]):
                with redirect_stdout(output):
                    with self.assertRaises(ValueError):
                        main()
        self.assertEqual(output.getvalue(), '')


    def test_three_point_growth_matches_exact_support_sizes(self):
        report = fixture()
        report['rows'] = []
        from decimal import Decimal
        for pattern in ('equal', 'distinct'):
            for n in (4, 8, 12):
                report['rows'].append({
                    'borrowers': n, 'pattern': pattern,
                    'expected_states': n + 1 if pattern == 'equal' else 2 ** n,
                    'analytical_tail': str(Decimal(1) - Decimal('0.75') ** n),
                    'peak_traced_bytes_min': 100,
                    'peak_traced_bytes_median': 110,
                    'peak_traced_bytes_max': 120,
                })
        rows = summarize(report)
        self.assertEqual([r['states'] for r in rows], [5, 9, 13, 16, 256, 4096])
        self.assertEqual([r['state_growth_from_previous'] for r in rows],
                         [None, 9 / 5, 13 / 9, None, 16.0, 16.0])


    def test_rejects_invalid_memory_ordering_and_nonfinite_values(self):
        for field, value in (
            ('peak_traced_bytes_min', 121),
            ('peak_traced_bytes_median', -1),
            ('peak_traced_bytes_max', float('nan')),
            ('peak_traced_bytes_max', float('inf')),
            ('peak_traced_bytes_min', True),
        ):
            with self.subTest(field=field, value=str(value)):
                report = fixture()
                report['rows'][0][field] = value
                with self.assertRaises(ValueError):
                    summarize(report)

    def test_rejects_duplicate_scenarios_and_invalid_batch_timing(self):
        report = fixture()
        report['rows'].append(copy.deepcopy(report['rows'][0]))
        with self.assertRaises(ValueError):
            summarize(report)
        for value in (-1, float('inf'), True):
            with self.subTest(batch_seconds_median=str(value)):
                report = fixture()
                report['batch_seconds_median'] = value
                with self.assertRaises(ValueError):
                    summarize(report)


if __name__ == '__main__':
    unittest.main()
