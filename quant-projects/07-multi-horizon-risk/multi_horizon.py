"""Horizon-aligned historical and normal portfolio VaR, educational only."""
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import norm

ASSETS=("TECH","BANK","HEALTH")
WEIGHTS=np.array([.4,.3,.3])

def synthetic_prices(n=360, seed=2026):
    if n<80: raise ValueError("n>=80 required")
    rng=np.random.default_rng(seed)
    corr=np.array([[1,.55,.2],[.55,1,.35],[.2,.35,1]])
    z=rng.standard_normal((n-1,3))@np.linalg.cholesky(corr).T
    regime=np.ones(n-1); regime[n//3:n//3+20]=2.5; regime[2*n//3:2*n//3+20]=1.7
    r=.0008+z*np.array([.03,.024,.018])*regime[:,None]
    p=np.vstack([np.full(3,100.),100*np.cumprod(1+r,axis=0)])
    return pd.DataFrame({"Date":pd.date_range("2019-01-04",periods=n,freq="W-FRI"),
                         **{k:p[:,i] for i,k in enumerate(ASSETS)}})

def portfolio_returns(prices, weights=WEIGHTS):
    if not {"Date",*ASSETS}.issubset(prices): raise ValueError("Missing columns")
    df=prices[["Date",*ASSETS]].copy()
    df.Date=pd.to_datetime(df.Date,errors="raise")
    if df.Date.isna().any() or df.Date.duplicated().any() or not df.Date.is_monotonic_increasing:
        raise ValueError("Dates must be increasing, unique, nonmissing")
    if not (df.Date.dt.dayofweek==4).all() or not (df.Date.diff().dropna()==pd.Timedelta(days=7)).all():
        raise ValueError("Require consecutive Friday observations")
    for c in ASSETS: df[c]=pd.to_numeric(df[c],errors="raise")
    values=df[list(ASSETS)].to_numpy(dtype=float)
    if not np.isfinite(values).all() or np.any(values<=0): raise ValueError("Prices must be positive and finite")
    w=np.asarray(weights,dtype=float)
    if w.shape!=(3,) or not np.isfinite(w).all() or np.any(w<0) or not np.isclose(w.sum(),1):
        raise ValueError("Weights must be long-only, finite and sum to one")
    r=df[list(ASSETS)].pct_change(fill_method=None).iloc[1:].to_numpy()@w
    if np.any(r<=-1): raise ValueError("Invalid portfolio log return")
    return pd.DataFrame({"Date":df.Date.iloc[1:].to_numpy(),"Return":r})

def horizon_risk(weekly, horizon=4, lookback=104, alpha=.05):
    """At t, train on [t-lookback,t), score [t,t+h); scored windows do not overlap."""
    h=horizon
    if type(h)!=int or h<1 or type(lookback)!=int or lookback<max(30,5*h):
        raise ValueError("Invalid horizon or lookback")
    if not np.isfinite(alpha) or not 0<alpha<.5: raise ValueError("Invalid alpha")
    if not {"Date","Return"}.issubset(weekly): raise ValueError("Require Date,Return")
    d=pd.to_datetime(weekly.Date,errors="raise")
    r=pd.to_numeric(weekly.Return,errors="raise").to_numpy(dtype=float)
    if d.isna().any() or d.duplicated().any() or not d.is_monotonic_increasing:
        raise ValueError("Invalid dates")
    if not (d.diff().dropna()==pd.Timedelta(days=7)).all(): raise ValueError("Non-weekly data")
    if not np.isfinite(r).all() or np.any(r<=-1): raise ValueError("Invalid returns")
    if len(r)<lookback+h: raise ValueError("Insufficient history")
    logs=np.log1p(r); rows=[]
    for t in range(lookback,len(r)-h+1,h):
        train=logs[t-lookback:t]
        train_losses=-np.expm1(np.convolve(train,np.ones(h),mode="valid"))
        cutoff=np.quantile(train_losses,1-alpha)
        var=max(0.,float(cutoff))
        cvar=max(0.,float(np.mean(train_losses[train_losses>=cutoff])))
        mu=float(np.mean(train)); sd=float(np.std(train,ddof=1))
        normal=max(0.,float(-np.expm1(h*mu+np.sqrt(h)*sd*norm.ppf(alpha))))
        realized=float(-np.expm1(np.sum(logs[t:t+h])))
        rows.append({"OriginDate":d.iloc[t-1].date().isoformat(),
                     "OutcomeStart":d.iloc[t].date().isoformat(),
                     "OutcomeEnd":d.iloc[t+h-1].date().isoformat(),
                     "TrainingStart":d.iloc[t-lookback].date().isoformat(),
                     "TrainingEnd":d.iloc[t-1].date().isoformat(),
                     "HorizonWeeks":h,"RealizedLoss":realized,
                     "HistoricalVaR95":var,"HistoricalCVaR95":cvar,"NormalVaR95":normal,
                     "HistoricalBreach":int(realized>var),"NormalBreach":int(realized>normal)})
    return pd.DataFrame(rows)

def summarize(scored):
    if scored.empty: raise ValueError("No scored windows")
    return {"horizon_weeks":int(scored.HorizonWeeks.iloc[0]),"scored_periods":len(scored),
            "historical_breaches":int(scored.HistoricalBreach.sum()),
            "normal_breaches":int(scored.NormalBreach.sum()),
            "historical_breach_rate":float(scored.HistoricalBreach.mean()),
            "normal_breach_rate":float(scored.NormalBreach.mean()),
            "mean_historical_var":float(scored.HistoricalVaR95.mean()),
            "mean_historical_cvar":float(scored.HistoricalCVaR95.mean()),
            "mean_normal_var":float(scored.NormalVaR95.mean())}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prices",type=Path,help="Licensed consecutive-Friday CSV: Date,TECH,BANK,HEALTH")
    p.add_argument("--output",type=Path,default=Path(__file__).parent/"reports")
    p.add_argument("--lookback",type=int,default=104)
    p.add_argument("--horizons",type=int,nargs="+",default=[1,4,13])
    a=p.parse_args()
    prices=pd.read_csv(a.prices) if a.prices else synthetic_prices()
    weekly=portfolio_returns(prices)
    if len(set(a.horizons))!=len(a.horizons): p.error("Horizons must be distinct")
    a.output.mkdir(parents=True,exist_ok=True); summary=[]
    for h in a.horizons:
        s=horizon_risk(weekly,h,a.lookback)
        s.to_csv(a.output/f"horizon_{h}_weeks.csv",index=False)
        summary.append(summarize(s))
    pd.DataFrame(summary).to_csv(a.output/"summary.csv",index=False)
    meta={"source":str(a.prices) if a.prices else "synthetic_seed_2026",
          "first_date":str(pd.to_datetime(prices.Date.iloc[0]).date()),
          "last_date":str(pd.to_datetime(prices.Date.iloc[-1]).date()),
          "lookback_weeks":a.lookback,"horizons":a.horizons,
          "weights":dict(zip(ASSETS,WEIGHTS.tolist())),"alpha":.05,
          "assumptions":"Weekly constant-mix, no trading costs; non-overlapping scored horizons."}
    (a.output/"metadata.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    print(pd.DataFrame(summary).to_string(index=False))
    print("Synthetic by default; not real historical evidence or investment advice.")

if __name__=="__main__": main()
