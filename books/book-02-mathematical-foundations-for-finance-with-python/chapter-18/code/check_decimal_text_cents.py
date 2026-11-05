"""Decimal-text cents: independent rational ties, limits, context isolation."""
from decimal import DecimalException, localcontext, ROUND_UP, Inexact
from fractions import Fraction
import json

import section_18_02 as lab


def check():
    values=['2.675','2.685','-2.675','-0','0.005','-0.005','0.015',
            '1e-1000','9'*26+'.994','9'*26+'.995','1e26',
            'NaN','Infinity','invalid',2.675]
    rows=[]
    for restricted in (False,True):
        with localcontext() as ctx:
            if restricted:
                ctx.prec=2
                ctx.Emax=3
                ctx.rounding=ROUND_UP
                ctx.traps[Inexact]=True
            before=str(ctx)
            for v in values:
                if not isinstance(v,str):
                    expected='TypeError'
                else:
                    try:
                        cents=abs(round(100*Fraction(v)))
                        expected=('ValueError' if cents>=10**28 else
                                  f"{'-' if v.startswith('-') else ''}{cents//100}.{cents%100:02}")
                    except ValueError:
                        expected='ValueError'
                try:
                    actual=lab.decimal_cents(v)
                except (DecimalException,ValueError,TypeError) as exc:
                    actual=type(exc).__name__
                rows.append(dict(restricted=restricted,input=repr(v),actual=actual,
                                 expected=expected,passed=actual==expected))
            rows.append(dict(restricted=restricted,case='context isolation',passed=str(ctx)==before))
    print(json.dumps(rows,indent=2))
    assert all(r['passed'] for r in rows)


if __name__=='__main__':
    check()
