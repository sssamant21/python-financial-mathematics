"""Supplemental project example; no source listing implements this ledger."""
import csv
import io
from fractions import Fraction
from typing import NamedTuple


class Row(NamedTuple):
    event: int
    opening: Fraction
    pre_flow: Fraction
    flow: Fraction
    post_flow: Fraction
    period_return: Fraction
    index: Fraction


def ledger(initial, events):
    opening = Fraction(str(initial))
    if opening <= 0 or not events:
        raise ValueError('positive opening and at least one event required')
    previous = 0
    index = Fraction(100)
    rows = []
    for i, (event, raw_ending, raw_flow) in enumerate(events):
        if type(event) is not int or event <= previous:
            raise ValueError('event order must increase')
        ending, flow = Fraction(str(raw_ending)), Fraction(str(raw_flow))
        post = ending + flow
        final = i == len(events) - 1
        if ending < 0 or (final and flow != 0) or (not final and post <= 0):
            raise ValueError('invalid valuation, final flow, or next opening')
        factor = ending / opening
        index *= factor
        rows.append(Row(event, opening, ending, flow, post, factor - 1, index))
        opening, previous = post, event
    return rows


def csv_text(rows):
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(Row._fields)
    writer.writerows(rows)
    return stream.getvalue()
