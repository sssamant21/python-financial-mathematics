"""Validate the bounded repeated synthetic benchmark JSON contract (no performance thresholds)."""
import argparse
import json
import math
from decimal import Decimal, InvalidOperation
from pathlib import Path


def validate(report):
    if not isinstance(report, dict) or report.get('schema_version') != 1 or report.get('synthetic_only') is not True:
        raise ValueError('unsupported schema or non-synthetic report')
    repetitions = report.get('repetitions')
    if type(repetitions) is not int or not 2 <= repetitions <= 10:
        raise ValueError('invalid repetitions')
    for key in ('python_version', 'platform'):
        if not isinstance(report.get(key), str) or not report[key].strip():
            raise ValueError(f'invalid {key}')
    values = [report.get(f'batch_seconds_{s}') for s in ('min', 'median', 'max')]
    if any(type(v) not in (int, float) or not math.isfinite(v) or v < 0 for v in values) or values != sorted(values):
        raise ValueError('invalid batch runtime ordering')
    rows = report.get('rows')
    if not isinstance(rows, list) or not rows or len(rows) > 40:
        raise ValueError('invalid row count')
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('invalid row')
        n, pattern, states = (row.get(k) for k in ('borrowers', 'pattern', 'expected_states'))
        if type(n) is not int or not 1 <= n <= 20 or pattern not in ('equal', 'distinct') or (pattern == 'distinct' and n > 12):
            raise ValueError('invalid scenario')
        if (n, pattern) in seen:
            raise ValueError('duplicate scenario')
        seen.add((n, pattern))
        if type(states) is not int or states != (n + 1 if pattern == 'equal' else 2 ** n):
            raise ValueError('invalid state count')
        try:
            tail = Decimal(row['analytical_tail'])
        except (KeyError, InvalidOperation, TypeError):
            raise ValueError('invalid tail probability') from None
        if not tail.is_finite() or not 0 <= tail <= 1:
            raise ValueError('tail probability out of bounds')
        values = [row.get(f'peak_traced_bytes_{s}') for s in ('min', 'median', 'max')]
        if any(type(v) not in (int, float) or not math.isfinite(v) or v < 0 for v in values) or values != sorted(values):
            raise ValueError('invalid memory ordering')
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('json_file', type=Path)
    args = parser.parse_args()
    print(f'Validated {validate(json.loads(args.json_file.read_text(encoding="utf-8")))} synthetic scenarios')


if __name__ == '__main__':
    main()
