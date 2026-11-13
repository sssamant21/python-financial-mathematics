"""Offline European-call delta hedge with synthetic GBM; no live trading."""
import argparse
import math
import random

def call_price_delta(s, k, tau, r, sigma):
    if not all(math.isfinite(x) for x in (s,k,tau,r,sigma)) or min(s,k,sigma)<=0 or tau<0 or abs(r)>1:
        raise ValueError("invalid option parameters")
    if tau==0:
        return max(s-k,0.0), (1.0 if s>k else 0.0 if s<k else 0.5)
    d1=(math.log(s/k)+(r+sigma*sigma/2)*tau)/(sigma*math.sqrt(tau))
    d2=d1-sigma*math.sqrt(tau)
    n=lambda z: 0.5*math.erfc(-z/math.sqrt(2))
    return s*n(d1)-k*math.exp(-r*tau)*n(d2), n(d1)

def simulate(seed=2026, steps=52, rebalance_every=1, cost_bps=0.0, spot=100.0, strike=100.0, maturity=1.0, rate=0.02, volatility=0.2):
    if not all(isinstance(x,int) for x in (seed,steps,rebalance_every)) or not 2<=steps<=5000 or not 1<=rebalance_every<=steps:
        raise ValueError("invalid grid")
    if not math.isfinite(cost_bps) or not 0<=cost_bps<=1000 or not math.isfinite(maturity) or maturity<=0:
        raise ValueError("invalid cost/maturity")
    premium,shares=call_price_delta(spot,strike,maturity,rate,volatility)
    cash=premium-shares*spot
    fee=abs(shares)*spot*cost_bps/10000
    cash-=fee
    total_cost=fee
    turnover=abs(shares)*spot
    rng=random.Random(seed)
    dt=maturity/steps
    s=spot
    for t in range(1,steps+1):
        s*=math.exp((rate-volatility**2/2)*dt+volatility*math.sqrt(dt)*rng.gauss(0,1))
        cash*=math.exp(rate*dt)
        if t<steps and t%rebalance_every==0:
            _,target=call_price_delta(s,strike,maturity-t*dt,rate,volatility)
            trade=target-shares
            notional=abs(trade)*s
            fee=notional*cost_bps/10000
            cash-=trade*s+fee
            total_cost+=fee
            turnover+=notional
            shares=target
    close_fee=abs(shares)*s*cost_bps/10000
    total_cost+=close_fee
    turnover+=abs(shares)*s
    return {"terminal_spot":s,"hedge_pnl":cash+shares*s-max(s-strike,0)-close_fee,"turnover_notional":turnover,"transaction_cost":total_cost}

def experiment(seeds=range(2026,2126), frequencies=(1,4,13), costs=(0.0,5.0)):
    seeds=tuple(seeds)
    if not seeds: raise ValueError("seeds required")
    rows=[]
    for freq in frequencies:
        for bps in costs:
            vals=[simulate(seed=seed,rebalance_every=freq,cost_bps=bps) for seed in seeds]
            pnl=[v["hedge_pnl"] for v in vals]
            rows.append({"rebalance_every":freq,"cost_bps":bps,"mean_pnl":sum(pnl)/len(pnl),"rmse_pnl":math.sqrt(sum(x*x for x in pnl)/len(pnl)),"mean_cost":sum(v["transaction_cost"] for v in vals)/len(vals)})
    return rows

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Synthetic delta hedge (not investment advice)")
    parser.add_argument("--paths",type=int,default=100)
    args=parser.parse_args()
    if not 1<=args.paths<=10000: parser.error("--paths must be 1..10000")
    for row in experiment(range(2026,2026+args.paths)): print(row)
