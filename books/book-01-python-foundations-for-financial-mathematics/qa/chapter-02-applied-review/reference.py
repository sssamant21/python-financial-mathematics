"""Supplemental applied answers. Typed finite Decimal teaching models, precision 28."""
from decimal import Decimal, localcontext
import importlib.util
from pathlib import Path

PATH=Path(__file__).resolve().parent.parent/'chapter-02-iteration-review/reference.py'
SPEC=importlib.util.spec_from_file_location('iteration_reference',PATH)
ITERATION=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ITERATION)
annual_schedule=ITERATION.annual_schedule


def finite_decimal(value):
    return isinstance(value,Decimal) and value.is_finite()


def investment_valid(value):
    return finite_decimal(value) and value>0


def contribution_valid(value):
    return finite_decimal(value) and value>=0


def period_valid(years):
    return isinstance(years,int) and not isinstance(years,bool) and 0<years<=100


def rate_error(rate):
    if rate is None:return 'missing rate'
    if not isinstance(rate,Decimal):return 'rate must be Decimal'
    if not rate.is_finite():return 'annual return is non-finite'
    if rate<=-1:return 'annual return must exceed -100%'
    return None


def analyze(principal,contribution,target,years,rates):
    if not investment_valid(principal):raise ValueError('principal must be positive finite Decimal')
    if not contribution_valid(contribution):raise ValueError('contribution must be nonnegative finite Decimal')
    if not investment_valid(target):raise ValueError('target must be positive finite Decimal')
    if not period_valid(years):raise ValueError('years must be non-Boolean integer in 1..100')
    results=[];rejected=[]
    with localcontext() as context:
        context.prec=28
        for index,rate in enumerate(rates):
            reason=rate_error(rate)
            if reason:
                rejected.append(dict(index=index,rate=str(rate),reason=reason))
                continue
            balance=principal;first_year=None;ending_year=0
            if balance>=target:first_year=0
            else:
                for year in range(1,years+1):
                    balance=balance*(1+rate)+contribution
                    ending_year=year
                    if balance>=target:
                        first_year=year
                        break
            results.append(dict(index=index,rate=rate,first_year=first_year,ending_year=ending_year,balance=balance,reached=first_year is not None))
    reached=[r for r in results if r['reached']]
    earliest=min((r['first_year'] for r in reached),default=None)
    ties=[r['index'] for r in reached if r['first_year']==earliest]
    counts=dict(total=len(rates),evaluated=len(results),rejected=len(rejected),reached=len(reached),not_reached=len(results)-len(reached))
    if counts['evaluated']+counts['rejected']!=counts['total'] or counts['reached']+counts['not_reached']!=counts['evaluated']:
        raise RuntimeError('Scenario counts do not reconcile')
    return dict(results=results,rejections=rejected,counts=counts,earliest_year=earliest,earliest_indices=ties)


def report(model):
    lines=['Nominal amounts; constant effective annual return; end-of-year contributions; no inflation, tax or fees.']
    for row in model['results']:
        status=f"reached at year {row['first_year']}" if row['reached'] else f"not reached within {row['ending_year']} years"
        lines.append(f"Scenario {row['index']}: rate {row['rate']:.2%}; {status}; ending USD {row['balance']:,.2f}")
    for row in model['rejections']:lines.append(f"Scenario {row['index']} rejected: {row['reason']}")
    lines.append(f"Counts: {model['counts']}")
    lines.append(f"Earliest year: {model['earliest_year']}; tied scenario indices: {model['earliest_indices']}")
    lines.append('Earliest target attainment is not an investment recommendation.')
    return '\n'.join(lines)


def quality(cashflows):
    counts=dict(processed=0,missing=0,rejected=0,positive=0,negative=0,zero=0);reasons=[]
    for index,cash in enumerate(cashflows):
        if cash is None:
            counts['missing']+=1
            continue
        if not finite_decimal(cash):
            counts['rejected']+=1;reasons.append((index,'finite Decimal cash flow required'))
            continue
        counts['processed']+=1
        if cash>0:counts['positive']+=1
        elif cash<0:counts['negative']+=1
        else:counts['zero']+=1
    assert counts['processed']+counts['missing']+counts['rejected']==len(cashflows)
    assert counts['positive']+counts['negative']+counts['zero']==counts['processed']
    return counts,reasons


def pv_grid(cashflows,rates):
    values=[];rejected=[]
    for index,rate in enumerate(rates):
        reason=rate_error(rate)
        if reason:
            rejected.append((index,reason));continue
        rows,total=ITERATION.discounted_cashflows(cashflows,rate)
        values.append((rate,rows,total))
    return values,rejected
