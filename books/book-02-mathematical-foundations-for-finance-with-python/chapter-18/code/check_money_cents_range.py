"""Exact decimal-text cent rounding across magnitudes and caller contexts."""
from decimal import DecimalException, localcontext, ROUND_UP, Inexact
from fractions import Fraction
import json
import math
import sys
import section_18_01 as lab


def expected(value):
    cents=abs(round(100*Fraction(str(value))))
    sign='-' if math.copysign(1,value)<0 else ''
    return f'{sign}{cents//100}.{cents%100:02d}'


def check():
    cases=[2.675,2.685,-2.675,-2.685,0.,-0.,.005,-.005,.015,-.015,
           sys.float_info.max,-sys.float_info.max,math.ulp(0.),-math.ulp(0.),1e30]
    rows=[]
    for mode in ('default','restricted'):
        with localcontext() as ctx:
            if mode=='restricted':
                ctx.prec=2
                ctx.Emax=4
                ctx.Emin=-4
                ctx.rounding=ROUND_UP
                ctx.traps[Inexact]=True
            before=str(ctx)
            for v in cases:
                ref=expected(v)
                try:
                    actual=lab.money_cents(v)
                except DecimalException as exc:
                    actual=type(exc).__name__
                rows.append(dict(mode=mode,value=repr(v),expected=ref,actual=actual,
                                 passed=ref==actual))
            rows.append(dict(mode=mode,case='caller context unchanged',
                             passed=str(ctx)==before))
    print(json.dumps(rows,indent=2))
    assert all(r['passed'] for r in rows)


if __name__=='__main__':
    check()
