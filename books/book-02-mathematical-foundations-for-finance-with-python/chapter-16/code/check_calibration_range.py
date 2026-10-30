"""Exact-case/independent Decimal references for Section 16.8 arithmetic."""
from decimal import Decimal,localcontext
from fractions import Fraction
from itertools import permutations
import math
from section_16_08 import fit_rate,gradient,curvature,weighted_loss


def rejected(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError('expected ValueError')


def decimal_fit(rows):
    # Direct independent normal equation at enough precision to retain the
    # selected extreme binary inputs and offset cancellation exactly.
    with localcontext() as ctx:
        ctx.prec=2500
        a=[Decimal(1000)*Decimal.from_float(float(t)) for t,y in rows]
        b=[Decimal.from_float(float(y))-Decimal(1000) for t,y in rows]
        return float(sum(x*y for x,y in zip(a,b))/sum(x*x for x in a))


def check():
    rows_cases=[((2.0**k,2000.),) for k in (-600,-500,0,500,600,1015)]
    rows_cases += [((1.,1e308),(1.,-1e308)),
                   ((2.0**-600,2000.),(2.0**600,2000.)),
                   ((math.ulp(0.),1000.),)]
    for rows in rows_cases:
        expected=decimal_fit(rows)
        assert fit_rate(rows)==expected,(rows,fit_rate(rows),expected)
    # Equal-time opposing observations imply rate -1 algebraically; at that
    # rate the two rounded price residuals cancel the gradient exactly.
    assert fit_rate(((1.,1e308),(1.,-1e308))) == -1.0
    assert gradient(-1,((1.,1e308),(1.,-1e308))) == 0.0
    cancellation_rows=((1.,-1e308),(1.,999.),(1.,1e308))
    for rows in permutations(cancellation_rows):
        assert gradient(0,rows)==1000.0
    # The sensitivity exceeds float range, but its product with the finite
    # rounded residual is representable. At this rate the model price is zero.
    assert gradient(-2.0**-1015,((2.0**1015,-2.0**-1000),)) == 1000*2.0**15
    for exponent in (-500,-20,0,20,500):
        rows=((2.0**exponent,1000.),)
        exact=(1000*Fraction(2.0**exponent))**2
        assert curvature(rows)==float(exact)
    # Half of an overflowing square/sum can still be a finite weighted loss.
    weighted_cases=(
        (((1.,-2.0**512),),(1.,),Fraction(2)**1023),
        (((1.,-2.0**511),)*4,(1.,)*4,Fraction(2)**1023),
        (((1.,-2.0**600),),(2.0**-1000,),Fraction(2)**199),
        (((1.,-2.0**-500),),(1.,),Fraction(2)**-1001),
    )
    for rows,weights,expected in weighted_cases:
        assert weighted_loss(-1,rows,weights)==float(expected)
    # Nonzero unrepresentable results must not masquerade as zero curvature,
    # zero loss, a zero gradient certificate, or a valid fitted rate.
    invalid_calls=(
        lambda:fit_rate(((math.ulp(0.),2000.),)),
        lambda:fit_rate(((1e308,math.nextafter(1000.,math.inf)),)),
        lambda:curvature(((2.0**-600,1000.),)),
        lambda:curvature(((2.0**600,1000.),)),
        lambda:gradient(-2.0**600,((2.0**-600,-2.0**-600),)),
        lambda:gradient(-1,((1.,-1e308),)),
        lambda:weighted_loss(-1,((1.,-2.0**600),),(1.,)),
        lambda:weighted_loss(-1,((1.,-2.0**-600),),(1.,)),
    )
    for call in invalid_calls:
        rejected(call)
    return {'decimal_fit_cases':len(rows_cases),'gradient_references':8,
            'curvature_references':5,'weighted_loss_references':4,
            'unrepresentable_result_rejections':len(invalid_calls)}


if __name__=='__main__':
    print(check())
