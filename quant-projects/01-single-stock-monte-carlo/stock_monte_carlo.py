"""Quant Project 01: geometric Brownian motion stock-price Monte Carlo."""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INITIAL_PRICE = 100.0
ANNUAL_DRIFT = 0.08
ANNUAL_VOL = 0.20
TRADING_DAYS = 252
N_PATHS = 10_000
SEED = 42

def simulate(seed=SEED, initial=INITIAL_PRICE, drift=ANNUAL_DRIFT,
             volatility=ANNUAL_VOL, days=TRADING_DAYS, paths=N_PATHS):
    """Return a (days + 1, paths) price matrix; rows are successive days."""
    if initial <= 0 or volatility < 0 or days <= 0 or paths <= 0:
        raise ValueError("Invalid simulation parameters")
    rng = np.random.default_rng(seed)
    dt = 1.0 / 252
    shocks = rng.standard_normal((days, paths))
    growth = np.exp((drift - 0.5 * volatility**2) * dt
                    + volatility * np.sqrt(dt) * shocks)
    return np.vstack((np.full(paths, initial),
                      initial * np.cumprod(growth, axis=0)))

def statistics(ending, start=INITIAL_PRICE):
    p05, p50, p95 = np.percentile(ending, [5, 50, 95])
    losses = start - ending
    tail = losses[ending <= p05]
    return {
        "mean_price": float(np.mean(ending)),
        "median_price": float(p50),
        "p05_price": float(p05),
        "p95_price": float(p95),
        "loss_probability": float(np.mean(ending < start)),
        "var95_per_share": max(0., float(start-p05)),
        "cvar95_per_share": float(np.mean(tail)),
    }

def main():
    paths = simulate()
    report = statistics(paths[-1])
    out = Path(__file__).resolve().parent / "reports"
    out.mkdir(parents=True, exist_ok=True)
    with (out / "summary.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, report.keys())
        writer.writeheader()
        writer.writerow(report)
    fig, ax = plt.subplots(figsize=(10, 5))
    for i in range(30):
        ax.plot(paths[:, i], linewidth=0.8, alpha=0.4)
    ax.plot(paths.mean(axis=1), label="Mean of 10,000 paths", linewidth=2)
    ax.axhline(INITIAL_PRICE, linestyle="--", color="gray", label="Start")
    ax.set(title="GBM: sample simulated stock prices", xlabel="Trading day",
           ylabel="Price (USD)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "stock_paths.png", dpi=140)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(paths[-1], bins=70)
    ax.axvline(INITIAL_PRICE, linestyle="--", color="gray")
    ax.set(title="One-year simulated ending prices", xlabel="Price (USD)",
           ylabel="Number of paths")
    fig.tight_layout()
    fig.savefig(out / "ending_price_histogram.png", dpi=140)
    plt.close(fig)
    print("One-year GBM Monte Carlo; hypothetical inputs only")
    for key, value in report.items():
        print(f"{key}: {value:.4f}")
    print("Reports:", out)

if __name__ == "__main__":
    main()
