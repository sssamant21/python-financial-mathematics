"""Nested synthetic Brownian paths for matched delta-hedge grid comparisons."""
import argparse
import math
import random
from hedge import call_price_delta

def path(seed, steps=104, spot=100., maturity=1., rate=.02, vol=.2):
    if type(seed) is not int or seed<0 or type(steps) is not int or not 2<=steps<=5200:
        raise ValueError("invalid seed/grid")
    if not all(math.isfinite(x) for x in (spot,maturity,rate,vol)) or min(spot,maturity,vol)<=0 or abs(rate)>1:
        raise ValueError("invalid parameters")
    rng=random.Random(seed)
    dt=maturity/steps
    values=[spot]
    for _ in range(steps):
        values.append(values[-1]*math.exp((rate-vol*vol/2)*dt+vol*math.sqrt(dt)*rng.gauss(0,1)))
    return values

def hedge(values, intervals, cost_bps=0., strike=100., maturity=1., rate=.02, vol=.2):
    n=len(values)-1
    if (type(intervals) is not int or intervals<1 or n<2 or n%intervals
        or not all(math.isfinite(v) and v>0 for v in values)
        or not math.isfinite(cost_bps) or not 0<=cost_bps<=1000
        or not all(math.isfinite(v) for v in (strike,maturity,rate,vol))
        or min(strike,maturity,vol)<=0 or abs(rate)>1):
        raise ValueError("invalid hedge configuration")
    premium,shares=call_price_delta(values[0],strike,maturity,rate,vol)
    cash=premium-shares*values[0]
    turnover=abs(shares)*values[0]
    fees=turnover*cost_bps/10000
    cash-=fees
    for j in range(1,intervals+1):
        s=values[j*n//intervals]
        cash*=math.exp(rate*maturity/intervals)
        if j<intervals:
            _,target=call_price_delta(s,strike,maturity*(1-j/intervals),rate,vol)
            trade=target-shares
            amount=abs(trade)*s
            fee=amount*cost_bps/10000
            cash-=trade*s+fee
            turnover+=amount
            fees+=fee
            shares=target
    close=abs(shares)*values[-1]
    turnover+=close
    fees+=close*cost_bps/10000
    return {"pnl":cash+shares*values[-1]-max(values[-1]-strike,0)-close*cost_bps/10000,
            "turnover":turnover,"fees":fees,"terminal":values[-1]}

def experiment(paths=80, grids=(13,26,52,104), fine_steps=104, cost_bps=5., seed=2026):
    if (type(paths) is not int or not 2<=paths<=1000 or type(seed) is not int or seed<0
        or type(fine_steps) is not int or not 2<=fine_steps<=5200
        or not grids or any(type(g) is not int or g<1 or fine_steps%g for g in grids)
        or tuple(sorted(set(grids)))!=tuple(grids)
        or not isinstance(cost_bps,(int,float)) or not math.isfinite(cost_bps) or not 0<=cost_bps<=1000):
        raise ValueError("invalid experiment")
    observations={g:[] for g in grids}
    for i in range(paths):
        values=path(seed+i,fine_steps)
        for g in grids:
            free=hedge(values,g,0.)
            paid=hedge(values,g,cost_bps)
            observations[g].append((free,paid))
    rows=[]
    for g,pairs in observations.items():
        pnl=[b["pnl"] for _,b in pairs]
        free=[a["pnl"] for a,_ in pairs]
        rows.append({"hedge_steps":g,"paths":paths,
                     "rmse_pnl":math.sqrt(math.fsum(v*v for v in pnl)/paths),
                     "cost_free_rmse":math.sqrt(math.fsum(v*v for v in free)/paths),
                     "mean_turnover":math.fsum(b["turnover"] for _,b in pairs)/paths,
                     "mean_financed_cost_drag":math.fsum(a["pnl"]-b["pnl"] for a,b in pairs)/paths})
    return rows

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Offline synthetic nested-grid hedge comparison")
    parser.add_argument("--paths",type=int,default=40)
    args=parser.parse_args()
    for row in experiment(paths=args.paths): print(row)
