# Project 21 — Sector Performance Attribution (Brinson–Fachler)

**Business question:** Why did a portfolio outperform or underperform its benchmark over one reporting period? Was it because of sector weights, sector returns, or their interaction?

This lab uses **invented, single-period sector weights and simple returns**. It is an educational accounting decomposition, not an investment strategy, stock recommendation, or production-grade performance measurement system.

## Mathematics

For sector `i`, let `wP_i` and `wB_i` be **beginning-of-period** portfolio and benchmark weights, and `rP_i`, `rB_i` their simple period returns. Both weight vectors must sum to 1, with the same exhaustive sector taxonomy.

- Benchmark return: `RB = sum(wB_i * rB_i)`
- Portfolio return: `RP = sum(wP_i * rP_i)`
- **Allocation:** `(wP_i - wB_i) * (rB_i - RB)`
- **Selection:** `wB_i * (rP_i - rB_i)`
- **Interaction:** `(wP_i - wB_i) * (rP_i - rB_i)`

Summing all three effects across sectors exactly reconciles arithmetic active return `RP - RB` (up to floating-point tolerance). Report effects in **percentage points**, not percentages of the portfolio return.

## Reproduce (Python 3.11+, standard library only)

```bash
cd quant-projects/21-sector-performance-attribution
python -m unittest -v test_attribution.py
python -m compileall -q attribution.py test_attribution.py
python attribution.py
```

The invented three-sector example yields allocation **+0.60**, selection **+0.20**, interaction **+0.30**, total active **+1.10 percentage points**. It uses no historical data or market-data license.

## Assumptions and guardrails

Weights are long-only, finite, sum to 100% for each portfolio, and refer to the **same starting date**. Sector names must be unique; all sectors must be present on both sides. Returns must be finite and at least -100%. Inputs are deliberately small (1–100 sectors). Missing sectors, changing classifications, leverage, derivatives, cash-flow timing, fees, corporate actions, taxes, and intra-period rebalancing are not modeled. Do not feed end-of-period weights into this single-period formula: that introduces hindsight bias.

This is **single-period arithmetic attribution** only. Do not add effects across periods as if they were linked compounded attribution; multi-period linking requires an explicitly chosen method and separate tests. Do not use future sector constituents or revised historical classifications for point-in-time studies. No live trading or brokerage integration.

## Validation

A standalone local Python run on 2026-11-10 passed **10/10 unittest tests**, compilation, and the synthetic CLI smoke test. Tests cover active-return reconciliation, pure allocation/selection, equal portfolios, one-sector case, repeatability, and invalid input rejection. **Exact published-revision GitHub Actions CI, independent review, real-world data validation, and production certification remain unverified.**

**Next exercise:** add a separate two-period linked attribution exercise with explicitly documented linking convention and fee/cash-flow limitations.
