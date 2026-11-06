"""Supplemental project CSV using the exact-source rolling calculation."""
import csv
import re
import sys
import types
from pathlib import Path


def main():
    source = Path(__file__).resolve().parents[2] / 'chapter-13/13.11-volatility.md'
    _, code = re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60', source.read_bytes(), re.M | re.S)
    m = types.ModuleType('source_volatility')
    exec(compile(code, str(source), 'exec'), m.__dict__)
    returns = [.01, -.005, .015, -.01, .007, -.008, .022, -.017, .004, -.003]
    rolling = [None, None, *m.rolling_sample_volatility(returns, 3)]
    writer = csv.writer(sys.stdout, lineterminator='\n')
    writer.writerow(['day', 'decimal_return', 'rolling_sample_volatility', 'observation_count'])
    for day, (r, sigma) in enumerate(zip(returns, rolling), 1):
        writer.writerow([day, r, sigma, min(day, 3)])


if __name__ == '__main__':
    main()
