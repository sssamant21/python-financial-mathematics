"""Supplemental mini-project export; calls the verbatim manuscript listing."""
import csv
import json
import re
import sys
import types
from pathlib import Path
from benchmark import project_rows


def export(out):
    source = Path(__file__).resolve().parents[2] / 'chapter-13/13.10-money-weighted-return.md'
    code, = re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60', source.read_bytes(), re.M | re.S)
    m = types.ModuleType('source_mwr')
    exec(compile(code, str(source), 'exec'), m.__dict__)
    rows = project_rows()
    labels = ['initial contribution', 'additional contribution', 'distribution', 'terminal valuation']
    xirr = m.xirr_bisection(rows)
    stress = rows[:-1] + [(rows[-1][0], 10795)]
    stress_xirr = m.xirr_bisection(stress)
    periodic = m.irr_bisection([cf for _, cf in rows])
    multiple = (rows[-2][1] + rows[-1][1]) / 12000
    both = [-100, 230, -132]
    roots = [m.irr_bisection(both, low=0, high=.15),
             m.irr_bisection(both, low=.15, high=.25)]
    summary = dict(day_count='Actual/365 Fixed', xirr_bracket=[-.9,1.0], xirr=xirr, xnpv=m.xnpv(xirr, rows),
                   invested=12000, distributed=500, terminal=12700, multiple=multiple,
                   periodic_irr=periodic, annualized_equal_intervals=(1+periodic)**3-1,
                   stressed_terminal=10795, stressed_xirr=stress_xirr,
                   stressed_xnpv=m.xnpv(stress_xirr, stress), synthetic_periodic_roots=roots)
    out.mkdir(parents=True, exist_ok=True)
    with (out / 'ledger.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(['date', 'event', 'cash_flow'])
        writer.writerows((d.isoformat(), label, cf) for (d, cf), label in zip(rows, labels))
    (out / 'summary.json').write_text(json.dumps(summary, indent=2, allow_nan=False)+'\n', encoding='utf-8')


if __name__ == '__main__':
    export(Path(sys.argv[1]))
