"""Acceptance tests for the illustrative five-stock optimization model."""
import numpy as np
from five_stock_quant_lab import (
 ANNUAL_VOLATILITIES, CORRELATION, COVARIANCE, MAX_SINGLE_ASSET_WEIGHT,
 TARGET_MAX_VOLATILITY, compute_strategies, expected_return,
 portfolio_volatility, run_monte_carlo,
)

def test_valid_matrices():
 assert np.allclose(CORRELATION, CORRELATION.T)
 assert np.allclose(np.diag(CORRELATION), 1)
 assert np.min(np.linalg.eigvalsh(CORRELATION)) > 0
 assert np.allclose(np.diag(COVARIANCE), ANNUAL_VOLATILITIES ** 2)

def test_constraints():
 s=compute_strategies()
 for w in s.values():
  assert abs(w.sum()-1)<1e-6
  assert min(w)>=-1e-8 and max(w)<=MAX_SINGLE_ASSET_WEIGHT+1e-6
 assert portfolio_volatility(s["Minimum volatility"]) <= portfolio_volatility(s["Equal weight"])
 assert portfolio_volatility(s["Max return at 16% risk"]) <= TARGET_MAX_VOLATILITY+1e-6
 assert expected_return(s["Max return at 16% risk"]) >= expected_return(s["Equal weight"])

def test_reproducible_simulation():
 s=compute_strategies()
 a,x=run_monte_carlo(s); b,y=run_monte_carlo(s)
 for name in s: assert np.array_equal(x[name],y[name])
 assert len(a)==4
 for row in a:
  assert 0 <= row["loss_probability_pct"] <= 100
  assert row["cvar_95_usd"] >= row["var_95_usd"]
