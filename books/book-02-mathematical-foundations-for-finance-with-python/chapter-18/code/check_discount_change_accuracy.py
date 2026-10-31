"""Independent small-rate discount-change references for Section 18.2."""
from decimal import Decimal as D, localcontext
import json
import math
import section_18_02 as lab


def audit(actual,reference):
    expected=float(reference)
    assert math.isfinite(actual)
    assert abs(D(actual)-reference)<=4*D(math.ulp(expected))
    assert (actual==0)==(expected==0)
    if expected:
        assert (actual>0)==(expected>0)


def check():
    tiny=math.nextafter(0.0,1.0)
    rates=[sign*r for r in (2**-54,1e-20,1e-12,1e-100,1e-300) for sign in (-1,1)]
    cases=[(r,n) for r in rates for n in (1,12,360,0.5,2.5)]
    cases += [(r,n) for r in (-tiny,tiny) for n in (1,12,360)]
    cases += [(0.0,n) for n in (0,12,360)]
    rows=[]; false_zeros=0; wrong=0
    with localcontext() as ctx:
        ctx.prec=1200
        for r,n in cases:
            # Direct high-precision compound discount, independent of log1p/expm1.
            reference=(1+D(r))**(-D(n))-1
            actual=lab.discount_change(r,n)
            audit(actual,reference)
            naive=(1+r)**(-n)-1
            false_zeros += naive==0 and float(reference)!=0
            rows.append({'rate':r,'periods':n,'actual':actual,'naive':naive,
                         'decimal_reference':str(reference),
                         'absolute_error':str(abs(D(actual)-reference)),
                         'ulp_allowance':str(4*D(math.ulp(float(reference))))})
        reference=(1+D(1e-20))**(-D(12))-1
        for altered in (0.0,-float(reference),(1+1e-20)**-12-1):
            try:
                audit(altered,reference)
            except AssertionError:
                wrong+=1
        assert wrong==3 and false_zeros>0
    return {'references':rows,'naive_false_zero_cases':false_zeros,
            'wrong_variants_detected':wrong,
            'scope':'59 selected small-rate represented-input values;4-ulp allowance; fractional periods are the implemented analytic extension, not a cash-flow timing convention; no all-range guarantee'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
