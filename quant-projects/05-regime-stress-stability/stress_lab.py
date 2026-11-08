"""Project 05: synthetic-first, walk-forward portfolio stress laboratory."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize

ASSETS = ("AAPL", "JNJ", "JPM", "PG", "NEE")
LOOKBACK = 52
REGIMES = {"2020 shock window": ("2020-02-21", "2020-06-26"),
           "2022 rates window": ("2022-01-07", "2022-12-30")}

def synthetic_prices(seed=2026):
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2018-01-05", "2025-12-26", freq="W-FRI")
    common = rng.normal(size=(len(dates), 1))
    independent = rng.normal(size=(len(dates), 5))
    shocks = (0.65*common + np.sqrt(1-0.65**2)*independent)*np.array([.038,.021,.030,.019,.032])
    shocks[(dates >= "2020-02-21") & (dates <= "2020-06-26")] *= 2.2
    shocks[(dates >= "2022-01-07") & (dates <= "2022-12-30")] *= 1.45
    prices = 100*np.cumprod(1+np.clip(shocks+.001,-.75,1.5),axis=0)
    return pd.DataFrame(prices,index=dates,columns=ASSETS).rename_axis("Date")

def validate_prices(prices):
    if list(prices.columns) != list(ASSETS):
        raise ValueError("Expected ordered asset columns: "+str(ASSETS))
    if not isinstance(prices.index,pd.DatetimeIndex) or len(prices)<LOOKBACK+30:
        raise ValueError("Require dated weekly prices and sufficient history")
    if prices.index.has_duplicates or not prices.index.is_monotonic_increasing or (prices.index.dayofweek != 4).any():
        raise ValueError("Require sorted, unique Friday-labeled observations")
    values=prices.to_numpy(dtype=float)
    if not np.isfinite(values).all() or (values<=0).any():
        raise ValueError("Require complete, finite, strictly positive prices")

def load_prices(path):
    frame=pd.read_csv(path,parse_dates=["Date"]).set_index("Date")
    validate_prices(frame)
    return frame

def forecast_cov(past,shrinkage=.20):
    if past.shape!=(LOOKBACK,5) or not np.isfinite(past).all() or not 0<=shrinkage<=1:
        raise ValueError("Require 52x5 finite returns and shrinkage in [0,1]")
    cov=np.cov(past,rowvar=False,ddof=1)
    return (1-shrinkage)*cov+shrinkage*np.diag(np.diag(cov))+np.eye(5)*1e-12

def weights(cov):
    result=minimize(lambda w:float(w@cov@w),np.full(5,.2),method="SLSQP",
                    bounds=[(0,.4)]*5,
                    constraints=[{"type":"eq","fun":lambda w:w.sum()-1}],
                    options={"ftol":1e-12,"maxiter":400})
    w=result.x
    if not result.success or abs(w.sum()-1)>1e-6 or w.min() < -1e-7 or w.max()>.4000001:
        raise RuntimeError("Optimization failed constraints")
    return w

def stress_cov(cov,correlation_shift=0.,vol_multiplier=1.):
    if not 0<=correlation_shift<=1 or vol_multiplier<1:
        raise ValueError("Invalid correlation or volatility shock")
    sd=np.sqrt(np.diag(cov))
    corr=cov/np.outer(sd,sd)
    return np.outer(sd,sd)*((1-correlation_shift)*corr+correlation_shift)*vol_multiplier**2

def walk_forward(prices,cost_bps=10.,shrinkage=.20,correlation_shift=0.,vol_multiplier=1.):
    validate_prices(prices)
    if not 0<=cost_bps<=1000:
        raise ValueError("Cost must be between 0 and 1000 bps")
    weekly=prices.pct_change(fill_method=None)
    wealth,w,last_month=1.,None,None
    rows,allocations=[],[]
    for i in range(LOOKBACK+1,len(prices)):
        date=prices.index[i]
        past=weekly.iloc[i-LOOKBACK:i].to_numpy(dtype=float)
        realized=weekly.iloc[i].to_numpy(dtype=float)
        cov=forecast_cov(past,shrinkage)
        turnover=0.
        month=date.to_period("M")
        if w is None or month!=last_month:
            target=weights(cov)
            turnover=float(np.abs(target-(w if w is not None else np.zeros(5))).sum())
            w=target
            last_month=month
            allocations.append({"Date":date.isoformat(),"Turnover":turnover,
                                **dict(zip(ASSETS,map(float,w)))})
        gross=float(w@realized)
        fee=turnover*cost_bps/10000
        net=(1-fee)*(1+gross)-1
        wealth*=1+net
        forecast=float(np.sqrt(w@stress_cov(cov,correlation_shift,vol_multiplier)@w)*np.sqrt(52))
        rows.append({"Date":date,"GrossReturn":gross,"NetReturn":net,
                     "Equity":wealth,"Turnover":turnover,"CostFraction":fee,
                     "ForecastAnnualVol":forecast})
        w=w*(1+realized)/(1+gross)
    return pd.DataFrame(rows),pd.DataFrame(allocations)

def summarize(ts):
    r=ts.NetReturn.to_numpy()
    equity=np.r_[1.,ts.Equity.to_numpy()]
    dd=equity/np.maximum.accumulate(equity)-1
    return {"Weeks":len(ts),"EndingWealthPerDollar":float(equity[-1]),
            "CAGR":float(equity[-1]**(52/len(ts))-1),
            "AnnualVol":float(np.std(r,ddof=1)*np.sqrt(52)),
            "MaxWeeklyDrawdown":float(dd.min()),
            "TotalTurnover":float(ts.Turnover.sum()),
            "TotalModeledCostFraction":float(ts.CostFraction.sum()),
            "ForecastVolStd":float(ts.ForecastAnnualVol.std(ddof=1))}

def run_study(prices):
    scenarios=[("baseline",10,0,1,.20),("zero_cost",0,0,1,.20),
               ("high_cost_25bps",25,0,1,.20),
               ("corr_to_one_50pct",10,.5,1,.20),
               ("double_vol",10,0,2,.20),
               ("shrinkage_50pct",10,0,1,.50)]
    summaries,regimes,timeseries,allocations=[],[],[],[]
    for name,cost,corr,vol,shrink in scenarios:
        ts,alloc=walk_forward(prices,cost_bps=cost,shrinkage=shrink,
                              correlation_shift=corr,vol_multiplier=vol)
        summaries.append({"Scenario":name,**summarize(ts)})
        for label,(start,end) in REGIMES.items():
            subset=ts[(ts.Date>=start)&(ts.Date<=end)]
            regimes.append({"Scenario":name,"Regime":label,"Weeks":len(subset),
                            "CompoundedReturn":float(np.prod(1+subset.NetReturn)-1) if len(subset) else None,
                            "Status":"DATE_WINDOW_ONLY" if len(subset) else "NO_OBSERVATIONS"})
        timeseries.append(ts.assign(Scenario=name))
        allocations.append(alloc.assign(Scenario=name))
    return (pd.DataFrame(summaries),pd.DataFrame(regimes),
            pd.concat(timeseries,ignore_index=True),pd.concat(allocations,ignore_index=True))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prices",type=Path,help="Authorized weekly adjusted-price CSV")
    parser.add_argument("--output",type=Path,default=Path(__file__).resolve().parent/"reports")
    args=parser.parse_args()
    prices=load_prices(args.prices) if args.prices else synthetic_prices()
    summary,regimes,ts,alloc=run_study(prices)
    args.output.mkdir(parents=True,exist_ok=True)
    for name,frame in [("scenario_summary.csv",summary),("regime_windows.csv",regimes),
                       ("weekly_results.csv",ts),("monthly_allocations.csv",alloc)]:
        frame.to_csv(args.output/name,index=False)
    meta={"data_type":"user_supplied" if args.prices else "synthetic_seed_2026",
          "source_path":str(args.prices) if args.prices else None,
          "first_date":str(prices.index[0].date()),"last_date":str(prices.index[-1].date()),
          "observations":len(prices),"lookback_weeks":LOOKBACK,
          "warning":"Correlation/volatility stresses affect forecast risk only, not realized returns."}
    (args.output/"run_metadata.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    print(summary.round(4).to_string(index=False))

if __name__=="__main__":
    main()
