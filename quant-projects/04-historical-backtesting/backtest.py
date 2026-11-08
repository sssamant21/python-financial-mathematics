"""Five-stock walk-forward portfolio backtest, using a bundled real-price snapshot.

Research/education only. All five companies were selected with hindsight and the
historical adjusted-price snapshot is not point-in-time investable data.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import norm, chi2

TICKERS = ["AAPL", "JNJ", "JPM", "PG", "NEE"]
N = len(TICKERS)
START_CAPITAL = 100_000.0
LOOKBACK = 52
PER_YEAR = 52
MAX_WEIGHT = 0.40
RISK_CAP = 0.16
RISK_FREE = 0.03
COST_RATE = 0.001     # 10 bps per dollar traded / portfolio value
SHRINKAGE = 0.20     # diagonal covariance shrinkage
STRATEGIES = ["Equal weight", "Minimum volatility", "Maximum Sharpe", "Risk capped (16%)"]


def read_prices(path: Path) -> pd.DataFrame:
    p = pd.read_csv(path, parse_dates=["Date"]).set_index("Date")
    if list(p.columns) != TICKERS:
        raise ValueError(f"Expected exactly {TICKERS}; found {list(p.columns)}")
    if p.isna().any().any() or not (p > 0).all().all():
        raise ValueError("Prices must be positive and complete; do not forward-fill missing data.")
    if not p.index.is_monotonic_increasing or p.index.has_duplicates:
        raise ValueError("Dates must be unique and sorted")
    if len(p) < LOOKBACK + 55:
        raise ValueError("Need one estimation year and at least one validation year")
    return p


def estimate(window: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    assert len(window) == LOOKBACK and not window.isna().any().any()
    mu = window.mean().to_numpy() * PER_YEAR
    cov_sample = window.cov().to_numpy() * PER_YEAR
    cov = (1 - SHRINKAGE) * cov_sample + SHRINKAGE * np.diag(np.diag(cov_sample))
    assert np.linalg.eigvalsh(cov).min() > -1e-10
    return mu, cov, window.mean().to_numpy()


def vol(w: np.ndarray, cov: np.ndarray) -> float:
    return float(np.sqrt(max(0.0, w @ cov @ w)))


def run_solver(objective, constraints=(), guesses=None) -> np.ndarray:
    bounds = [(0.0, MAX_WEIGHT)] * N
    equality = {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}
    guesses = guesses or [np.full(N, 1 / N)]
    results = [minimize(objective, g, method="SLSQP", bounds=bounds,
                        constraints=[equality, *constraints],
                        options={"ftol": 1e-11, "maxiter": 400}) for g in guesses]
    results = [r for r in results if r.success and abs(sum(r.x) - 1) < 1e-5
               and np.min(r.x) >= -1e-6 and np.max(r.x) <= MAX_WEIGHT + 1e-6]
    if not results:
        raise RuntimeError("Portfolio optimizer failed; refusing to substitute arbitrary weights")
    best = min(results, key=lambda x: x.fun)
    w = np.clip(best.x, 0.0, MAX_WEIGHT)
    return w / w.sum()


def optimal_weights(mu: np.ndarray, cov: np.ndarray) -> tuple[dict[str, np.ndarray], bool]:
    equal = np.full(N, 0.2)
    minvol = run_solver(lambda w: float(w @ cov @ w))
    starts = [equal, minvol]
    for j in range(N):
        other = np.full(N, 0.6 / (N - 1))
        other[j] = 0.4
        starts.append(other)
    sharpe = run_solver(lambda w: -(float(w @ mu) - RISK_FREE) / max(vol(w, cov), 1e-8),
                        guesses=starts)
    feasible = vol(minvol, cov) <= RISK_CAP + 1e-8
    if feasible:
        try:
            capped = run_solver(lambda w: -float(w @ mu),
                                constraints=[{"type": "ineq", "fun": lambda w: RISK_CAP**2 - float(w @ cov @ w)}],
                                guesses=starts)
            if vol(capped, cov) > RISK_CAP + 1e-4:
                raise RuntimeError("Risk cap not respected")
        except RuntimeError:
            # The feasible minimum-volatility solution is retained and flagged.
            capped = minvol.copy()
            feasible = False
    else:
        # Risk limit is infeasible under the training-window covariance matrix.
        capped = minvol.copy()
    return dict(zip(STRATEGIES, [equal, minvol, sharpe, capped])), feasible


def kupiec_pvalue(n: int, breaches: int, p0: float = 0.05) -> float:
    if n <= 0:
        return float("nan")
    # 0*log(0) contributes zero by continuity.
    phat = breaches / n
    ll_null = (n-breaches)*np.log1p(-p0) + breaches*np.log(p0)
    ll_alt = (n-breaches)*np.log1p(-phat) if phat < 1 else 0.0
    if breaches > 0:
        ll_alt += breaches*np.log(phat)
    return float(chi2.sf(max(0.0, -2*(ll_null-ll_alt)), df=1))


def backtest(prices: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    weekly = prices.pct_change(fill_method=None)
    records = []
    weights_records = []
    trackers = {s: {"wealth": START_CAPITAL, "weights": None, "month": None,
                    "fees": 0.0, "turnover": 0.0, "infeasible": 0}
                for s in STRATEGIES}

    for i in range(LOOKBACK + 1, len(prices)):
        date = prices.index[i]
        past = weekly.iloc[i-LOOKBACK:i]   # strictly earlier than the return being scored
        if past.isna().any().any():
            raise AssertionError("Training data has an unexpected gap")
        current = weekly.iloc[i].to_numpy()
        mu, cov, mu_week = estimate(past)
        current_month = date.to_period("M")
        rebalancing = any(x["month"] != current_month for x in trackers.values())
        if rebalancing:
            targets, feasible = optimal_weights(mu, cov)

        for name in STRATEGIES:
            state = trackers[name]
            fee_fraction = 0.0
            turn = 0.0
            if state["weights"] is None or state["month"] != current_month:
                target = targets[name]
                old = state["weights"] if state["weights"] is not None else np.zeros(N)
                turn = float(np.abs(target-old).sum())
                fee_fraction = COST_RATE * turn
                state["fees"] += state["wealth"]*fee_fraction
                state["turnover"] += turn
                state["weights"] = target.copy()
                state["month"] = current_month
                if name == "Risk capped (16%)" and not feasible:
                    state["infeasible"] += 1
                weights_records.append({"Date": date, "Strategy": name,
                                        "Forecast return %": float(target @ mu)*100,
                                        "Forecast vol %": vol(target, cov)*100,
                                        "Cap feasible": bool(feasible) if name == "Risk capped (16%)" else "",
                                        **{ticker: float(target[j]) for j, ticker in enumerate(TICKERS)}})
            w = state["weights"].copy()
            gross = float(w @ current)
            net = (1.0-fee_fraction)*(1.0+gross)-1.0
            state["wealth"] *= (1.0 + net)
            # Weekly 5% downside quantile forecast using only past 52 returns.
            weekly_cov = cov / PER_YEAR
            q05 = float(w @ mu_week) + norm.ppf(0.05)*np.sqrt(max(0.0, w @ weekly_cov @ w))
            breach = bool(gross < q05)
            # Shares naturally drift between rebalances (no daily rebalancing).
            state["weights"] = w*(1.0+current)/(1.0+gross)
            records.append({"Date": date, "Strategy": name,
                            "Equity": state["wealth"], "Gross weekly return": gross,
                            "Net weekly return": net, "Turnover": turn,
                            "Trading cost fraction": fee_fraction,
                            "VaR 95 weekly threshold %": q05*100,
                            "VaR breach": breach,
                            "Estimated annual volatility %": vol(w,cov)*100})

    timeseries = pd.DataFrame(records)
    allocations = pd.DataFrame(weights_records)
    metrics = []
    for name, state in trackers.items():
        subset = timeseries[timeseries.Strategy == name].sort_values("Date")
        r = subset["Net weekly return"].to_numpy()
        eq = np.r_[START_CAPITAL, subset["Equity"].to_numpy()]
        drawdowns = eq / np.maximum.accumulate(eq) - 1
        q05 = np.quantile(r, 0.05)
        breaches = int(subset["VaR breach"].sum())
        total_weeks = len(r)
        std = np.std(r, ddof=1)
        metrics.append({
            "Strategy":name,
            "First scored date":subset["Date"].iloc[0].date().isoformat(),
            "Last scored date":subset["Date"].iloc[-1].date().isoformat(),
            "Weeks":total_weeks,
            "Ending $":float(eq[-1]),
            "CAGR %":((eq[-1]/START_CAPITAL)**(PER_YEAR/total_weeks)-1)*100,
            "Annualized volatility %":std*np.sqrt(PER_YEAR)*100,
            "Sharpe (rf=3%)":(np.mean(r)*PER_YEAR-RISK_FREE)/(std*np.sqrt(PER_YEAR)) if std>0 else float("nan"),
            "Maximum drawdown %":drawdowns.min()*100,
            "Worst weekly return %":r.min()*100,
            "Realized weekly loss 95% VaR %":max(0.0,-q05)*100,
            "Weekly VaR breaches":breaches,
            "Weekly VaR breach rate %":breaches/total_weeks*100,
            "Kupiec p-value":kupiec_pvalue(total_weeks, breaches),
            "Sum dollar-traded turnover":state["turnover"],
            "Total modeled fees $":state["fees"],
            "Risk-cap infeasible rebalances":state["infeasible"]})
    return timeseries, allocations, pd.DataFrame(metrics)


def plots(timeseries: pd.DataFrame, allocations: pd.DataFrame, out: Path) -> None:
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(11, 5.5))
    for name in STRATEGIES:
        g = timeseries[timeseries.Strategy == name]
        ax.plot(g.Date, g.Equity/1000, label=name, lw=1.7)
    ax.set(title="Walk-forward backtest: $100,000 starting capital", ylabel="Portfolio value ($000)", xlabel="Historical observation date")
    ax.legend(ncol=2, fontsize=9)
    ax.grid(alpha=.2)
    fig.tight_layout()
    fig.savefig(out/"equity_curves.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 5.5))
    for name in STRATEGIES:
        g = timeseries[timeseries.Strategy == name]
        vals = np.r_[START_CAPITAL, g.Equity.to_numpy()]
        dd = (vals/np.maximum.accumulate(vals)-1)[1:]*100
        ax.plot(g.Date, dd, lw=1.4, label=name)
    ax.set(title="Historical drawdown from each portfolio's previous peak", ylabel="Drawdown (%)")
    ax.legend(ncol=2, fontsize=9)
    ax.grid(alpha=.2)
    fig.tight_layout()
    fig.savefig(out/"drawdowns.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 5.5))
    g = timeseries[timeseries.Strategy == "Maximum Sharpe"]
    ax.plot(g.Date, g["Gross weekly return"]*100, lw=.9, label="Realized weekly return")
    ax.plot(g.Date, g["VaR 95 weekly threshold %"], lw=1.1, label="Ex-ante 5th-percentile forecast")
    b = g[g["VaR breach"]]
    ax.scatter(b.Date, b["Gross weekly return"]*100, marker="x", s=27, label="VaR breach")
    ax.set(title="Weekly out-of-sample VaR backtesting: maximum Sharpe strategy", ylabel="Weekly return (%)")
    ax.legend(fontsize=9)
    ax.grid(alpha=.2)
    fig.tight_layout()
    fig.savefig(out/"weekly_var_backtest.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 5.5))
    g = allocations[allocations.Strategy == "Maximum Sharpe"]
    ax.stackplot(g.Date, *[g[t] * 100 for t in TICKERS], labels=TICKERS, alpha=.9)
    ax.set(title="Walk-forward maximum-Sharpe portfolio allocations", ylabel="Target portfolio weight (%)", ylim=(0,100))
    ax.legend(ncol=5, loc="upper center", fontsize=9)
    fig.tight_layout()
    fig.savefig(out/"allocations_over_time.png", dpi=160)
    plt.close(fig)


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prices",type=Path,default=Path(__file__).with_name("weekly_adjusted_prices.csv"))
    parser.add_argument("--output",type=Path,default=Path(__file__).parent / "reports")
    args=parser.parse_args()
    args.output.mkdir(exist_ok=True,parents=True)
    prices=read_prices(args.prices)
    ts,w,report=backtest(prices)
    ts.to_csv(args.output/"weekly_backtest_timeseries.csv",index=False)
    w.to_csv(args.output/"monthly_target_allocations.csv",index=False)
    report.to_csv(args.output/"historical_risk_validation_report.csv",index=False)
    plots(ts,w,args.output)
    print(f"Historical sample: {prices.index[0].date()} through {prices.index[-1].date()}, {len(prices)} weekly closes")
    print(f"Out-of-sample: {report['First scored date'].iloc[0]} to {report['Last scored date'].iloc[0]}, {len(ts)//4} weeks")
    showcols=["Strategy","Ending $","CAGR %","Annualized volatility %","Maximum drawdown %","Weekly VaR breaches","Weekly VaR breach rate %","Kupiec p-value","Risk-cap infeasible rebalances"]
    print(report[showcols].round(3).to_string(index=False))
    print("Report directory:",args.output)


if __name__=="__main__":
    main()