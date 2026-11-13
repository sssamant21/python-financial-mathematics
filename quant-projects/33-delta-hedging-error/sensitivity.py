"""Predeclared paired synthetic delta-hedge sensitivity; no market data."""
import argparse
import math
from hedge import simulate

def summarize(values):
    """Mean, sample SE, RMSE, and descriptive normal 95% Monte Carlo interval."""
    if len(values) < 2 or not all(math.isfinite(v) for v in values):
        raise ValueError("at least two finite observations required")
    n = len(values)
    mean = math.fsum(values) / n
    variance = math.fsum((v - mean)**2 for v in values) / (n-1)
    se = math.sqrt(variance/n)
    return {"n":n, "mean_pnl":mean, "rmse_pnl":math.sqrt(math.fsum(v*v for v in values)/n),
            "mc_se_mean":se, "mc_ci95_low":mean-1.96*se, "mc_ci95_high":mean+1.96*se}

def sensitivity(path_counts=(40,160,640), volatilities=(0.1,0.2,0.4),
                frequencies=(1,4,13), cost_bps=5.0, base_seed=2026):
    """Nested seed prefixes; common shocks, not identical spot paths, across volatilities."""
    counts, vols, freqs = tuple(path_counts), tuple(volatilities), tuple(frequencies)
    if (not counts or not vols or not freqs or any(type(n) is not int or n<2 for n in counts)
            or sorted(set(counts)) != list(counts) or counts[-1]>10000
            or any(not isinstance(v,(int,float)) or not math.isfinite(v) or not 0<v<=2 for v in vols)
            or any(type(f) is not int or f<1 or f>52 for f in freqs)
            or type(base_seed) is not int or base_seed<0
            or not isinstance(cost_bps,(int,float)) or not math.isfinite(cost_bps)
            or not 0<=cost_bps<=1000):
        raise ValueError("invalid predeclared sensitivity configuration")
    results=[]
    for vol in vols:
        for freq in freqs:
            zero,charged=[],[]
            for i in range(counts[-1]):
                params=dict(seed=base_seed+i,volatility=vol,rebalance_every=freq)
                zero.append(simulate(cost_bps=0.0,**params)["hedge_pnl"])
                charged.append(simulate(cost_bps=cost_bps,**params)["hedge_pnl"])
            for n in counts:
                stats=summarize(charged[:n])
                drag=[x-y for x,y in zip(zero[:n],charged[:n])]
                results.append({"volatility":vol,"rebalance_every":freq,"cost_bps":cost_bps,
                                **stats,"mean_cost_drag":math.fsum(drag)/n,
                                "mc_se_cost_drag":summarize(drag)["mc_se_mean"]})
    return results

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Offline paired delta-hedge sensitivity")
    parser.add_argument("--paths",type=int,default=40)
    args=parser.parse_args()
    if not 2<=args.paths<=10000: parser.error("--paths must be 2..10000")
    for row in sensitivity(path_counts=(args.paths,)): print(row)
