"""Supplemental drawdown dashboard with alert thresholds and CSV rendering."""
import csv
import io
from fractions import Fraction


def dashboard(values, source):
    depths = source.drawdown_series(values)
    rows = []
    peak = values[0]
    for i, (value, depth) in enumerate(zip(values, depths)):
        peak = max(peak, value)
        exact = Fraction(value, peak) - 1
        alert = 'critical' if exact <= Fraction(-15, 100) else 'warning' if exact <= Fraction(-1, 10) else 'ok'
        rows.append((i, value, peak, depth, alert))
    return rows


def ledger_csv(rows):
    out = io.StringIO()
    writer = csv.writer(out, lineterminator='\n')
    writer.writerow(['observation','wealth','running_peak','drawdown','alert'])
    writer.writerows(rows)
    return out.getvalue()
