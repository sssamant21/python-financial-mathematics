"""Inspect theoretical state growth in a bounded synthetic benchmark report.

State counts are mathematical support sizes, not measured RAM or runtime bounds.
"""
import argparse
import json
from pathlib import Path

from validate_benchmark import validate


def summarize(report):
    """Return deterministic growth diagnostics; reject malformed evidence first."""
    validate(report)
    result = []
    for pattern in ('equal', 'distinct'):
        rows = sorted((r for r in report['rows'] if r['pattern'] == pattern),
                      key=lambda r: r['borrowers'])
        previous = None
        for row in rows:
            n = row['borrowers']
            states = row['expected_states']
            ratio = None if previous is None else states / previous['expected_states']
            result.append({'pattern': pattern, 'borrowers': n, 'states': states,
                           'state_growth_from_previous': ratio,
                           'peak_traced_bytes_median': row['peak_traced_bytes_median']})
            previous = row
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('json_file', type=Path)
    args = parser.parse_args()
    report = json.loads(args.json_file.read_text(encoding='utf-8'))
    print(json.dumps({'synthetic_only': True, 'state_growth': summarize(report),
                      'caveat': 'State growth is exact for these synthetic fixtures; traced allocations are not RSS, and no runtime or memory SLA is inferred.'}, indent=2))


if __name__ == '__main__':
    main()
