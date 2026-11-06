"""Supplemental independent terminal-value solver using Decimal Newton steps."""
from datetime import date
from decimal import Decimal as D, localcontext


def project_rows():
    return [(date(2025,1,1),-10000),(date(2025,4,1),-2000),
            (date(2025,9,1),500),(date(2026,1,1),12700)]


def terminal_root(flows, powers):
    with localcontext() as ctx:
        ctx.prec = 55
        terms = [(D(cf),D(n)/d) for cf,(n,d) in zip(flows,powers)]
        gross = D(1)
        for _ in range(25):
            value = sum(cf*gross**t for cf,t in terms)
            if abs(value) < D('1e-44'):
                return gross-1
            slope = sum(cf*t*gross**(t-1) for cf,t in terms if t)
            gross -= value/slope
        raise RuntimeError('independent terminal-value benchmark did not converge')
