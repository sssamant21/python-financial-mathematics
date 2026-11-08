"""Five-stock quantitative portfolio lab: Markowitz optimization + GBM Monte Carlo.

Illustrative assets and assumptions only; no market data or investment advice.
Run: python five_stock_quant_lab.py
Dependencies: numpy, scipy, matplotlib
"""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog, minimize

# Set parameters in one place to make experimentation straightforward.
NAMES = ["Technology", "Healthcare", "Banking", "Consumer", "Utilities"]
EXPECTED_SIMPLE_RETURNS = np.array([0.12, 0.09, 0.085, 0.075, 0.06])
ANNUAL_VOLATILITIES = np.array([0.30, 0.20, 0.25, 0.16, 0.13])
CORRELATION = np.array(
    [
        [1.00, 0.35, 0.45, 0.30, 0.10],
        [0.35, 1.00, 0.25, 0.40, 0.35],
        [0.45, 0.25, 1.00, 0.55, 0.30],
        [0.30, 0.40, 0.55, 1.00, 0.50],
        [0.10, 0.35, 0.30, 0.50, 1.00],
    ],
    dtype=float,
)

INITIAL_PORTFOLIO = 100_000.0
RISK_FREE_RATE = 0.03  # Illustrative, one-year simple return
MAX_SINGLE_ASSET_WEIGHT = 0.40
TARGET_MAX_VOLATILITY = 0.16
N_SCENARIOS = 10_000
SEED = 42
OUTPUT_DIR = Path(__file__).resolve().parent


def validate_inputs() -> None:
    assert len(NAMES) == EXPECTED_SIMPLE_RETURNS.size == ANNUAL_VOLATILITIES.size
    assert np.all(ANNUAL_VOLATILITIES > 0)
    assert np.all(EXPECTED_SIMPLE_RETURNS > -1)
    assert np.allclose(CORRELATION, CORRELATION.T)
    assert np.allclose(np.diag(CORRELATION), 1)
    if np.linalg.eigvalsh(CORRELATION).min() <= 0:
        raise ValueError("Correlation matrix is not positive definite")
    if len(NAMES) * MAX_SINGLE_ASSET_WEIGHT < 1:
        raise ValueError("Asset cap makes the allocation infeasible")


validate_inputs()
COVARIANCE = np.outer(ANNUAL_VOLATILITIES, ANNUAL_VOLATILITIES) * CORRELATION
N = len(NAMES)
EQUAL_WEIGHT = np.full(N, 1.0 / N)
BOUNDS = [(0.0, MAX_SINGLE_ASSET_WEIGHT)] * N
SUM_CONSTRAINT = {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}


def expected_return(weights: np.ndarray) -> float:
    return float(weights @ EXPECTED_SIMPLE_RETURNS)


def portfolio_volatility(weights: np.ndarray) -> float:
    return float(np.sqrt(weights @ COVARIANCE @ weights))


def sharpe(weights: np.ndarray) -> float:
    return (expected_return(weights) - RISK_FREE_RATE) / portfolio_volatility(weights)


def optimize(name: str, objective, constraints) -> np.ndarray:
    result = minimize(
        objective,
        EQUAL_WEIGHT,
        method="SLSQP",
        bounds=BOUNDS,
        constraints=constraints,
        options={"ftol": 1e-12, "maxiter": 3000},
    )
    if not result.success:
        raise RuntimeError(f"{name}: optimizer failed: {result.message}")
    w = np.asarray(result.x)
    if (np.min(w) < -1e-6 or np.max(w) > MAX_SINGLE_ASSET_WEIGHT + 1e-6
            or abs(w.sum() - 1.0) > 1e-6):
        raise RuntimeError(f"{name}: weight constraints not met")
    return w


def compute_strategies() -> dict[str, np.ndarray]:
    min_vol = optimize(
        "Minimum volatility",
        lambda w: w @ COVARIANCE @ w,
        [SUM_CONSTRAINT],
    )
    max_sharpe = optimize(
        "Maximum Sharpe",
        lambda w: -sharpe(w),
        [SUM_CONSTRAINT],
    )
    max_return_at_risk_cap = optimize(
        "Max return with 16% volatility cap",
        lambda w: -expected_return(w),
        [
            SUM_CONSTRAINT,
            {
                "type": "ineq",
                "fun": lambda w: TARGET_MAX_VOLATILITY ** 2 - w @ COVARIANCE @ w,
            },
        ],
    )
    if portfolio_volatility(max_return_at_risk_cap) > TARGET_MAX_VOLATILITY + 1e-6:
        raise RuntimeError("Volatility cap was violated")
    return {
        "Equal weight": EQUAL_WEIGHT,
        "Minimum volatility": min_vol,
        "Maximum Sharpe": max_sharpe,
        "Max return at 16% risk": max_return_at_risk_cap,
    }


def run_monte_carlo(strategies: dict[str, np.ndarray]):
    # Draw correlated *annual log-return shocks* once. Reuse across strategies
    # to make the comparison fair. This exactly samples one-year GBM endpoints.
    rng = np.random.default_rng(SEED)
    independent_normals = rng.standard_normal((N_SCENARIOS, N))
    correlated_normals = independent_normals @ np.linalg.cholesky(CORRELATION).T

    # Mapping a desired one-year arithmetic expected return r into GBM:
    # E[S(1)/S(0)] = exp(drift) = 1 + r.
    log_drift = np.log1p(EXPECTED_SIMPLE_RETURNS) - 0.5 * ANNUAL_VOLATILITIES**2
    gross_returns = np.exp(log_drift + correlated_normals * ANNUAL_VOLATILITIES)

    summary = []
    ending_values = {}
    for name, weights in strategies.items():
        # Initial holdings are fixed: buy-and-hold, no rebalancing within year.
        ending = INITIAL_PORTFOLIO * (gross_returns @ weights)
        loss = INITIAL_PORTFOLIO - ending
        var_95 = float(np.percentile(loss, 95))
        cvar_95 = float(np.mean(loss[loss >= var_95]))
        ending_values[name] = ending
        summary.append(
            {
                "strategy": name,
                "expected_return_pct": 100 * expected_return(weights),
                "initial_annualized_vol_pct": 100 * portfolio_volatility(weights),
                "sharpe_ratio": sharpe(weights),
                "mean_ending_value_usd": float(ending.mean()),
                "median_ending_value_usd": float(np.median(ending)),
                "ending_5th_percentile_usd": float(np.percentile(ending, 5)),
                "ending_95th_percentile_usd": float(np.percentile(ending, 95)),
                "loss_probability_pct": 100 * float(np.mean(ending < INITIAL_PORTFOLIO)),
                "var_95_usd": var_95,
                "cvar_95_usd": cvar_95,
            }
        )
    return summary, ending_values


def create_frontier(min_vol_weights: np.ndarray):
    # Find the maximum attainable expected return subject only to weight caps.
    lp = linprog(
        c=-EXPECTED_SIMPLE_RETURNS,
        A_eq=np.ones((1, N)),
        b_eq=np.array([1.0]),
        bounds=BOUNDS,
        method="highs",
    )
    if not lp.success:
        raise RuntimeError("Could not calculate max feasible return")

    target_returns = np.linspace(expected_return(min_vol_weights), expected_return(lp.x), 42)
    output = []
    prior = min_vol_weights
    for target in target_returns:
        result = minimize(
            lambda w: w @ COVARIANCE @ w,
            prior,
            method="SLSQP",
            bounds=BOUNDS,
            constraints=[
                SUM_CONSTRAINT,
                {"type": "eq", "fun": lambda w, t=target: w @ EXPECTED_SIMPLE_RETURNS - t},
            ],
            options={"ftol": 1e-12, "maxiter": 3000},
        )
        if not result.success or abs(expected_return(result.x) - target) > 1e-6:
            raise RuntimeError(f"Efficient-frontier optimization failed at {target:.6f}")
        prior = result.x
        output.append((portfolio_volatility(result.x), expected_return(result.x)))
    return np.array(output)


def save_csv(filename: str, rows: list[dict]) -> None:
    with (OUTPUT_DIR / filename).open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def draw_charts(strategies, ending_values, frontier):
    # Correlation matrix heatmap
    fig, ax = plt.subplots(figsize=(7.5, 6))
    plot = ax.imshow(CORRELATION, vmin=-1, vmax=1, cmap="coolwarm")
    ax.set_xticks(range(N), NAMES, rotation=35, ha="right")
    ax.set_yticks(range(N), NAMES)
    for i in range(N):
        for j in range(N):
            ax.text(j, i, f"{CORRELATION[i,j]:.2f}", ha="center", va="center")
    ax.set_title("Assumed annual return-shock correlations")
    fig.colorbar(plot, ax=ax, label="Pearson correlation")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "correlation_matrix.png", dpi=165)
    plt.close(fig)

    # Efficient frontier and strategies
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(100 * frontier[:, 0], 100 * frontier[:, 1], linewidth=2.5, label="Long-only efficient frontier")
    for name, weights in strategies.items():
        ax.scatter(100 * portfolio_volatility(weights), 100 * expected_return(weights), s=85)
        ax.annotate(name, (100 * portfolio_volatility(weights), 100 * expected_return(weights)),
                    xytext=(7, 5), textcoords="offset points", fontsize=9)
    ax.axvline(100 * TARGET_MAX_VOLATILITY, ls="--", alpha=0.6, label="16% risk cap")
    ax.set(xlabel="Initial annualized portfolio volatility (%)", ylabel="Expected one-year simple return (%)",
           title="Risk–return trade-off: five-stock portfolios")
    ax.grid(alpha=0.25)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "efficient_frontier.png", dpi=165)
    plt.close(fig)

    # Strategy weights
    fig, ax = plt.subplots(figsize=(10, 5.5))
    xs = np.arange(len(strategies))
    bottoms = np.zeros(len(strategies))
    for i, asset in enumerate(NAMES):
        vals = np.array([weights[i] for weights in strategies.values()]) * 100
        ax.bar(xs, vals, bottom=bottoms, label=asset)
        bottoms += vals
    ax.set_xticks(xs, list(strategies.keys()), rotation=12, ha="right")
    ax.set_ylabel("Starting allocation (%)")
    ax.set_ylim(0, 105)
    ax.set_title("Optimized portfolio allocations (40% max per stock)")
    ax.legend(ncol=3, bbox_to_anchor=(0.5, -0.18), loc="upper center")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "portfolio_allocations.png", dpi=165)
    plt.close(fig)

    # One-year terminal wealth distributions
    fig, ax = plt.subplots(figsize=(10, 6))
    for name, ending in ending_values.items():
        ax.hist(ending, bins=75, density=True, alpha=0.30, label=name)
    ax.axvline(INITIAL_PORTFOLIO, linestyle="--", linewidth=1.4, label="Starting value")
    ax.set(xlabel="Portfolio ending value ($)", ylabel="Probability density",
           title=f"One-year Monte Carlo distribution ({N_SCENARIOS:,} scenarios each)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "ending_value_distributions.png", dpi=165)
    plt.close(fig)


def main() -> None:
    strategies = compute_strategies()
    summary, ending_values = run_monte_carlo(strategies)
    frontier = create_frontier(strategies["Minimum volatility"])

    weights_rows = []
    for name, weights in strategies.items():
        weights_rows.append({"strategy": name, **{asset + "_weight_pct": 100 * float(w)
                                                  for asset, w in zip(NAMES, weights)}})
    save_csv("portfolio_weights.csv", weights_rows)
    save_csv("portfolio_risk_report.csv", summary)
    save_csv("correlation_matrix.csv", [dict(asset=NAMES[i], **{name: CORRELATION[i,j]
                                             for j, name in enumerate(NAMES)}) for i in range(N)])
    save_csv("covariance_matrix.csv", [dict(asset=NAMES[i], **{name: COVARIANCE[i,j]
                                           for j, name in enumerate(NAMES)}) for i in range(N)])
    draw_charts(strategies, ending_values, frontier)

    print("Five-stock Monte Carlo + portfolio optimization")
    print("Expected returns are simple one-year returns; volatility is initial annualized volatility.")
    print(f"Simulations: {N_SCENARIOS:,}; investment: ${INITIAL_PORTFOLIO:,.0f}; seed: {SEED}")
    print("Correlation eigenvalues:", np.round(np.linalg.eigvalsh(CORRELATION), 4))
    print()
    for row, wr in zip(summary, weights_rows):
        print(f"{row['strategy']}")
        print("  weights:", ", ".join(f"{n} {wr[n+'_weight_pct']:.1f}%" for n in NAMES))
        print(f"  expected return {row['expected_return_pct']:.2f}%; "
              f"annualized vol {row['initial_annualized_vol_pct']:.2f}%; "
              f"Sharpe {row['sharpe_ratio']:.3f}")
        print(f"  MC mean ${row['mean_ending_value_usd']:,.0f}; "
              f"5th percentile ${row['ending_5th_percentile_usd']:,.0f}; "
              f"P(loss) {row['loss_probability_pct']:.1f}%")
        print(f"  MC VaR95 ${row['var_95_usd']:,.0f}; CVaR95 ${row['cvar_95_usd']:,.0f}")
        print()
    print("Saved CSV reports and PNG charts in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()