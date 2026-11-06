"""Supplemental reference for the applied exercises; not manuscript code."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from itertools import combinations
from math import prod


def root(value, n=2):
    value=F(value)
    with localcontext() as ctx:
        ctx.prec=55
        return (D(value.numerator)/D(value.denominator))**(D(1)/n)


def sample_variance(xs):
    return sum((a-b)**2 for a,b in combinations(xs,2))/(len(xs)*(len(xs)-1))


def scorecard(xs, bench):
    mean=sum(xs)/len(xs)
    variance=sample_variance(xs)
    gross=prod(1+r for r in xs)
    path=[prod(1+r for r in xs[:i]) for i in range(len(xs)+1)]
    dd=min(F(x,y)-1 for i,x in enumerate(path) for y in path[:i+1])
    downvar=sum(r*r for r in xs if r<0)/len(xs)
    active=[x-y for x,y in zip(xs,bench)]
    active_mean=sum(active)/len(active)
    return dict(mean=mean,geo=root(gross,len(xs))-1,cumulative=gross-1,vol=root(variance),
                annual_vol=root(12*variance),mdd=dd,sharpe=root(12*(mean-F('.002'))**2/variance),
                downside=root(downvar),sortino=root(12*mean**2/downvar),
                information=root(12*active_mean**2/sample_variance(active)))
