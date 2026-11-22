"""Contract regression tests with synthetic fixtures only."""
import copy
import unittest
from validate_benchmark import validate


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.report = {'schema_version': 1, 'synthetic_only': True, 'repetitions': 3,
                       'python_version': '3.11.18', 'platform': 'linux',
                       'batch_seconds_min': 0.1, 'batch_seconds_median': 0.2,
                       'batch_seconds_max': 0.3,
                       'rows': [{'borrowers': 4, 'pattern': 'equal', 'expected_states': 5,
                                 'analytical_tail': '0.68359375',
                                 'peak_traced_bytes_min': 100, 'peak_traced_bytes_median': 110,
                                 'peak_traced_bytes_max': 120}]}

    def test_valid(self):
        self.assertEqual(validate(self.report), 1)

    def test_rejects_bad_contract(self):
        for key, value in [('schema_version', 2), ('synthetic_only', False), ('repetitions', True)]:
            with self.subTest(key=key):
                r = copy.deepcopy(self.report); r[key] = value
                with self.assertRaises(ValueError): validate(r)

    def test_rejects_state_or_tail(self):
        for key, value in [('expected_states', 6), ('analytical_tail', 'NaN'), ('analytical_tail', '1.1')]:
            with self.subTest(key=key):
                r = copy.deepcopy(self.report); r['rows'][0][key] = value
                with self.assertRaises(ValueError): validate(r)

    def test_rejects_bad_measurements(self):
        for key, value in [('batch_seconds_median', -1), ('batch_seconds_max', float('nan')),
                           ('peak_traced_bytes_median', 999)]:
            with self.subTest(key=key):
                r = copy.deepcopy(self.report)
                target = r['rows'][0] if key.startswith('peak_') else r
                target[key] = value
                with self.assertRaises(ValueError): validate(r)

    def test_rejects_in_range_but_wrong_analytical_tail(self):
        for value in ('0.5', '0.68359375000000000000001'):
            with self.subTest(value=value):
                r = copy.deepcopy(self.report)
                r['rows'][0]['analytical_tail'] = value
                with self.assertRaises(ValueError):
                    validate(r)

    def test_accepts_distinct_severity_same_tail(self):
        r = copy.deepcopy(self.report)
        r['rows'][0].update(pattern='distinct', expected_states=16)
        self.assertEqual(validate(r), 1)

    def test_rejects_in_range_tail_for_wrong_borrower_count(self):
        r = copy.deepcopy(self.report)
        r['rows'][0].update(borrowers=8, expected_states=9)
        with self.assertRaises(ValueError):
            validate(r)

    def test_accepts_tolerance_boundary(self):
        r = copy.deepcopy(self.report)
        r['rows'][0]['analytical_tail'] = '0.683593750000000000000001'
        self.assertEqual(validate(r), 1)

    def test_rejects_tolerance_exceedance(self):
        r = copy.deepcopy(self.report)
        r['rows'][0]['analytical_tail'] = '0.683593750000000000000002'
        with self.assertRaises(ValueError):
            validate(r)

    def test_rejects_duplicate(self):
        self.report['rows'].append(copy.deepcopy(self.report['rows'][0]))
        with self.assertRaises(ValueError): validate(self.report)


if __name__ == '__main__': unittest.main()
