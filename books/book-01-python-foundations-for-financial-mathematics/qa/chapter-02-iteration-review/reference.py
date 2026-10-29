"""Supplemental runnable answers for 2.13.14–32; teaching models, finite Decimal inputs."""
from decimal import Decimal, localcontext


def validate(principal, rate, contribution, years, target=None):
    values=[principal,rate,contribution]+([] if target is None else [target])
    if any(not isinstance(x,Decimal) or not x.is_finite() for x in values):
        raise ValueError('Finite Decimal inputs required')
    if principal < 0 or contribution < 0 or rate <= -1 or (target is not None and target <= 0):
        raise ValueError('Unsupported teaching model domain')
    if isinstance(years,bool) or not isinstance(years,int) or not 0 <= years <= 100:
        raise ValueError('Whole horizon in 0..100 required')


def annual_schedule(principal, rate, contribution, years, beginning=False):
    validate(principal,rate,contribution,years)
    with localcontext() as context:
        context.prec=28
        balance=principal
        rows=[]
        for year in range(1,years+1):
            if beginning:
                balance=(balance+contribution)*(1+rate)
            else:
                balance=balance*(1+rate)+contribution
            rows.append((year,balance))
        return rows


def print_schedule(rows):
    for year,balance in rows:
        print(f'Year {year}: {balance:,.2f}')


def crossing_while(principal,rate,contribution,target,horizon):
    validate(principal,rate,contribution,horizon,target)
    with localcontext() as context:
        context.prec=28
        balance=principal;year=0
        while balance < target and year < horizon:
            balance=balance*(1+rate)+contribution
            year+=1
        return dict(reached=balance>=target,first_year=year if balance>=target else None,ending_year=year,balance=balance)


def crossing_break(principal,rate,target,horizon):
    validate(principal,rate,Decimal(0),horizon,target)
    with localcontext() as context:
        context.prec=28
        balance=principal
        if balance>=target:return dict(reached=True,first_year=0,ending_year=0,balance=balance)
        year=0;first=None
        for year in range(1,horizon+1):
            balance*=1+rate
            if balance>=target:
                first=year
                break
        return dict(reached=first is not None,first_year=first,ending_year=year,balance=balance)


def search_loop_else(principal,rate,target,horizon=25):
    validate(principal,rate,Decimal(0),horizon,target)
    with localcontext() as context:
        context.prec=28
        balance=principal
        if balance>=target:return 'Reached at period 0'
        for year in range(1,horizon+1):
            balance*=1+rate
            if balance>=target:
                return_message=f'Reached in year {year}'
                break
        else:
            return f'Not reached within {horizon} years'
        return return_message


def cashflow_counts(cashflows):
    positive=negative=zero=0
    for value in cashflows:
        if value > 0:positive+=1
        elif value < 0:negative+=1
        else:zero+=1
    assert positive+negative+zero==len(cashflows)
    return dict(positive=positive,negative=negative,zero=zero,total=sum(cashflows,Decimal(0)))


def discounted_cashflows(cashflows,rate):
    if not isinstance(rate,Decimal) or not rate.is_finite() or rate<=-1:
        raise ValueError('Finite effective annual Decimal rate > -1 required')
    with localcontext() as context:
        context.prec=28
        rows=[];total=Decimal(0)
        for period,cash in enumerate(cashflows,start=1):
            value=cash/(1+rate)**period
            rows.append((period,value));total+=value
        return rows,total


def scenario_projection(rates):
    results=[]
    for rate in rates:
        # Every scenario initializes its own balance inside annual_schedule.
        results.append((rate,annual_schedule(Decimal(10000),rate,Decimal(0),5)))
    return results


def quarters(years):
    rows=[]
    for year in range(1,years+1):
        for quarter in range(1,5):
            period=(year-1)*4+quarter
            rows.append((year,quarter,period))
    return rows


def process_missing(cashflows):
    processed=missing=0;total=Decimal(0)
    for cash in cashflows:
        if cash is None:
            missing+=1
            continue
        processed+=1;total+=cash
    assert processed+missing==len(cashflows)
    return processed,missing,total


def reject_scenarios(rates):
    accepted=[];rejected=[]
    for rate in rates:
        if not isinstance(rate,Decimal):
            rejected.append((repr(rate),'representation'))
            continue
        if not rate.is_finite():
            rejected.append((str(rate),'nonfinite'))
            continue
        if rate<=-1:
            rejected.append((str(rate),'return must exceed -100%'))
            continue
        accepted.append(rate)
    assert len(accepted)+len(rejected)==len(rates)
    return accepted,rejected
