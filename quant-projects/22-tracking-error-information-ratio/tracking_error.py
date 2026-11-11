"""Educational ex-post active-risk diagnostics; synthetic data only."""
import math
import statistics

def diagnostics(portfolio, benchmark, periods_per_year=12):
    p, b = list(portfolio), list(benchmark)
    if len(p) != len(b) or len(p) < 3:
        raise ValueError("Need at least three aligned paired observations")
    if not isinstance(periods_per_year, int) or isinstance(periods_per_year, bool) or not 1 <= periods_per_year <= 366:
        raise ValueError("Invalid periods per year")
    if any(not isinstance(x, (float, int)) or isinstance(x, bool) or not math.isfinite(x) or x < -1 for x in p + b):
        raise ValueError("Returns must be finite simple returns >= -1")
    active = [x-y for x,y in zip(p,b)]
    mean = statistics.mean(active)
    sd = statistics.stdev(active)
    annual_te = sd * math.sqrt(periods_per_year)
    annual_active = mean * periods_per_year
    return {"observations":len(active), "mean_active":mean,
            "tracking_error":annual_te, "annualized_active":annual_active,
            "information_ratio":None if sd == 0 else annual_active / annual_te}

def rolling_diagnostics(portfolio, benchmark, window=6, periods_per_year=12):
    p,b=list(portfolio),list(benchmark)
    if len(p)!=len(b) or not isinstance(window,int) or isinstance(window,bool) or window<3 or window>len(p):
        raise ValueError("Invalid aligned observations or rolling window")
    return [diagnostics(p[i-window:i],b[i-window:i],periods_per_year)
            for i in range(window,len(p)+1)]

if __name__ == "__main__":
    p=[.02,-.01,.03,.01,-.02,.04,.00,.02]
    b=[.01,.00,.02,.02,-.01,.02,.01,.01]
    print(diagnostics(p,b))
    print("Rolling windows:",len(rolling_diagnostics(p,b)))
