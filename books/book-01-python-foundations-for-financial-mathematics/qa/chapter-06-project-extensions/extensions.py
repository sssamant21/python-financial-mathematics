"""Scoped instructional extensions; not changes to the manuscript calculator."""
from collections.abc import Mapping
from numbers import Real
import statistics
import timeit
import numpy as np


def axis(labels):
    if type(labels) is not tuple or not labels or any(type(x) is not str or not x or x.strip()!=x for x in labels) or len(set(labels))!=len(labels):
        raise ValueError('unique nonempty trimmed tuple labels required')
    return labels


def lookup(report, name):
    if type(name) is not str or name not in report.scenarios:
        raise KeyError(name)
    index=report.scenarios.index(name)
    contributions=report.contributions[index].copy();contributions.setflags(write=False)
    return dict(name=name,row=index,assets=report.assets,contributions=contributions,
                portfolio_return=float(report.portfolio_returns[index]),
                ending_value=float(report.ending_values[index]),pnl=float(report.pnl[index]))


def render_contributions(report, name):
    row=lookup(report,name)
    return name+' (percentage points)\n'+''.join(f'{asset}: {100*value:+.4f} pp\n' for asset,value in zip(row['assets'],row['contributions']))


def align_prices(assets, labelled_values):
    """Mapping or lossless key/value pairs -> aligned nonnegative closing-price vector."""
    axis(assets)
    if isinstance(labelled_values,Mapping):
        pairs=list(labelled_values.items())
    elif type(labelled_values) in (list,tuple):
        pairs=list(labelled_values)
    else:
        raise ValueError('mapping or lossless key/value pairs required')
    values={}
    for pair in pairs:
        if type(pair) not in (list,tuple) or len(pair)!=2:
            raise ValueError('identifier/value pairs required')
        key,value=pair
        if type(key) is not str or not key or key.strip()!=key:
            raise ValueError('invalid identifier')
        if key in values:
            raise ValueError('duplicate identifier')
        values[key]=value
    if set(values)!=set(assets):
        raise ValueError('missing or extra identifier')
    # Reject raw Boolean mixtures before NumPy can erase their identity.
    ordered=[]
    for key in assets:
        value=values[key]
        if isinstance(value,(bool,np.bool_)) or not isinstance(value,Real):
            raise ValueError('real numeric price without Boolean/text coercion required')
        try:
            converted=float(value)
        except (OverflowError,ValueError,TypeError) as exc:
            raise ValueError('unsupported price conversion') from exc
        if not np.isfinite(converted) or converted<0:
            raise ValueError('finite nonnegative closing prices required')
        ordered.append(converted)
    return np.array(ordered,dtype=np.float64)


def exact_array(value, ndim):
    if type(value) is not np.ndarray or value.dtype!=np.dtype('float64'):
        raise ValueError('exact float64 array required')
    if value.ndim!=ndim or not value.size or not np.isfinite(value).all():
        raise ValueError('nonempty finite array with required rank required')


def batch_portfolios(assets, quantities, opening_prices, scenario_assets,
                     scenarios, closing_prices, portfolios, *, max_cells=100000):
    """Q:(P,N), p0:(N,), p1:(S,N) -> returns/values/P&L:(S,P), no contribution cube."""
    for labels in (assets,scenario_assets,scenarios,portfolios):axis(labels)
    if assets!=scenario_assets:raise ValueError('asset identity/order mismatch')
    if type(max_cells) is not int or not 1<=max_cells<=100000:raise ValueError('cell budget outside teaching policy')
    for value,rank in ((quantities,2),(opening_prices,1),(closing_prices,2)):exact_array(value,rank)
    n=len(assets);p=len(portfolios);s=len(scenarios)
    if quantities.shape!=(p,n) or opening_prices.shape!=(n,) or closing_prices.shape!=(s,n):raise ValueError('labelled shape mismatch')
    if any(rows*cols>max_cells for rows,cols in ((p,n),(s,n),(s,p))):raise ValueError('input/output cell budget exceeded')
    if (quantities<0).any() or (opening_prices<=0).any() or (closing_prices<0).any():raise ValueError('long-only positive-opening-price domain')
    with np.errstate(over='raise',under='raise',divide='raise',invalid='raise'):
        opening_positions=quantities*opening_prices
        opening_values=opening_positions.sum(axis=1,dtype=np.float64)
        if (opening_values<=0).any():raise ValueError('every portfolio requires positive opening value')
        weights=opening_positions/opening_values[:,None]
        returns=closing_prices/opening_prices-1
        portfolio_returns=returns@weights.T
        ending_values=closing_prices@quantities.T
        pnl=ending_values-opening_values[None,:]
    result=dict(assets=assets,scenarios=scenarios,portfolios=portfolios,opening_values=opening_values,weights=weights,
                asset_returns=returns,portfolio_returns=portfolio_returns,ending_values=ending_values,pnl=pnl)
    for value in result.values():
        if isinstance(value,np.ndarray):
            if not np.isfinite(value).all():raise ValueError('nonfinite batch output')
            value.setflags(write=False)
    return result


def distribution_report(source, args, cash_per_unit):
    """Unadjusted ex-distribution close + nonnegative cash credited once at horizon."""
    base=source.calculate(**args);exact_array(cash_per_unit,2)
    if cash_per_unit.shape!=base.asset_returns.shape or (cash_per_unit<0).any():raise ValueError('scenario-by-asset gross distribution shape/domain')
    q=source.numeric(args['quantities'],1,'quantities');p0=source.numeric(args['opening_prices'],1,'opening_prices');p1=source.numeric(args['closing_prices'],2,'closing_prices')
    with np.errstate(over='raise',under='raise',divide='raise',invalid='raise'):
        asset_returns=(p1+cash_per_unit)/p0-1
        contributions=asset_returns*base.weights
        returns=contributions.sum(axis=1,dtype=np.float64)
        cash=cash_per_unit@q
        ending_values=base.ending_values+cash
        pnl=ending_values-base.opening_value
    result=dict(assets=base.assets,scenarios=base.scenarios,opening_value=base.opening_value,asset_returns=asset_returns,
                contributions=contributions,portfolio_returns=returns,cash_received=cash,ending_values=ending_values,pnl=pnl)
    for value in result.values():
        if isinstance(value,np.ndarray):
            if not np.isfinite(value).all():raise ValueError('nonfinite distribution output')
            value.setflags(write=False)
    return result


def resident_snapshot(source,args):
    """Validate once outside timing; own read-only resident inputs, same Report outputs."""
    q=source.numeric(args['quantities'],1,'quantities');p0=source.numeric(args['opening_prices'],1,'opening_prices');p1=source.numeric(args['closing_prices'],2,'closing_prices')
    checked=dict(args,quantities=q,opening_prices=p0,closing_prices=p1)
    accepted=source.calculate(**checked)
    for array in (q,p0,p1):array.setflags(write=False)
    def calculate_resident():
        with np.errstate(over='raise',divide='raise',invalid='raise',under='raise'):
            values=q*p0;total=float(np.sum(values,dtype=np.float64));weights=values/total
            returns=p1/p0-1;contributions=returns*weights;portfolio_returns=returns@weights
            ending_values=p1@q;pnl=ending_values-total
        outputs=(weights,returns,contributions,portfolio_returns,ending_values,pnl)
        if not all(np.isfinite(x).all() for x in outputs):raise ValueError('nonfinite resident output')
        for array in outputs:array.setflags(write=False)
        return source.Report(accepted.assets,accepted.scenarios,total,*outputs)
    return calculate_resident


def measure(operation):
    operation()
    samples=[value/20 for value in timeit.repeat(operation,repeat=5,number=20)]
    return dict(repeat=5,number=20,seconds_per_call=samples,minimum=min(samples),median=statistics.median(samples))
