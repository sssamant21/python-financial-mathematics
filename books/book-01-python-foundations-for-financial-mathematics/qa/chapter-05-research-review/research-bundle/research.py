"""Reproduce a synthetic same-currency cash-inflow aggregation."""
import argparse
from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext
import hashlib
import json
from pathlib import Path
import platform
import re


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON member')
        result[key] = value
    return result


def decode(raw: bytes):
    return json.loads(raw.decode('utf-8'), object_pairs_hook=unique_object)


def analyze(data_raw: bytes, config_raw: bytes) -> dict:
    config = decode(config_raw)
    if config != {'currency': 'USD', 'rounding': 'ROUND_HALF_EVEN', 'scale': '0.01'}:
        raise ValueError('unsupported configuration')
    rows = decode(data_raw)
    if type(rows) is not list or not 1 <= len(rows) <= 1000:
        raise ValueError('expected 1 to 1000 inflows')
    seen = set()
    amounts = []
    for row in rows:
        if type(row) is not dict or set(row) != {'id', 'currency', 'amount'}:
            raise ValueError('incorrect inflow schema')
        sid = row['id']
        if type(sid) is not str or not sid or sid.strip() != sid or sid in seen:
            raise ValueError('invalid or duplicate id')
        if row['currency'] != 'USD':
            raise ValueError('mixed or unsupported currency')
        text = row['amount']
        if type(text) is not str or re.fullmatch(r'(0|[1-9][0-9]{0,6})(\.[0-9]{1,4})?', text) is None:
            raise ValueError('invalid amount text')
        value = Decimal(text)
        if value > Decimal('1000000'):
            raise ValueError('inflow exceeds lab bound')
        seen.add(sid)
        amounts.append(value)
    # A fresh context prevents caller precision, rounding, or flags from leaking in.
    with localcontext(Context(prec=28, rounding=ROUND_HALF_EVEN)):
        total = sum(amounts, Decimal('0'))
        rounded = total.quantize(Decimal('0.01'))
    return {'currency': 'USD', 'count': len(rows), 'total': format(rounded, '.2f'),
            'method': 'sum_then_round', 'rounding': 'ROUND_HALF_EVEN'}


def bundle(data_raw: bytes, config_raw: bytes, source_raw: bytes) -> dict:
    result = analyze(data_raw, config_raw)
    return {'schema_version': 1, 'result': result,
            'evidence': {'input_sha256': digest(data_raw),
                         'config_sha256': digest(config_raw),
                         'source_sha256': digest(source_raw),
                         'python': platform.python_version(),
                         'implementation': platform.python_implementation(),
                         'system': platform.system(),
                         'third_party_runtime_dependencies': []}}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    # Read each input once: hash and analyze the same bytes.
    data_raw = args.input.read_bytes()
    config_raw = args.config.read_bytes()
    source_raw = Path(__file__).read_bytes()
    report = bundle(data_raw, config_raw, source_raw)
    encoded = json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + '\n'
    # Exclusive create: never overwrite inputs or an earlier research result.
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(encoded)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
