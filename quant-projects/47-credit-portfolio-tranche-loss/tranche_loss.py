"""Educational one-period homogeneous independent-default portfolio tranche loss.

No market quotes, correlation calibration, or investment recommendation.
"""
import math
from math import comb


def validate(n, pd, lgd, attachment, detachment):
    if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= 200:
        raise ValueError("n must be an integer from 1 to 200")
    for name, value in (("pd", pd), ("lgd", lgd), ("attachment", attachment), ("detachment", detachment)):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{name} must be finite and numeric")
    if not 0 <= pd <= 1 or not 0 <= lgd <= 1:
        raise ValueError("pd and lgd must be between 0 and 1")
    if not 0 <= attachment < detachment <= 1:
        raise ValueError("require 0 <= attachment < detachment <= 1")


def tranche_loss(portfolio_loss, attachment, detachment):
    """Fraction of total portfolio notional lost by tranche (not tranche percentage)."""
    return min(max(portfolio_loss - attachment, 0.0), detachment - attachment)


def expected_tranche_loss(n=20, pd=0.03, lgd=0.6, attachment=0.0, detachment=0.1):
    """Exact binomial expectation; independent identical obligors and equal exposures."""
    validate(n, pd, lgd, attachment, detachment)
    if pd == 0:
        return 0.0
    if pd == 1:
        return tranche_loss(lgd, attachment, detachment)
    # Stable recurrence starting at the most probable number of defaults.
    mode = min(n, int((n + 1) * pd))
    log_p = (math.lgamma(n + 1) - math.lgamma(mode + 1)
             - math.lgamma(n - mode + 1) + mode * math.log(pd)
             + (n - mode) * math.log1p(-pd))
    probability = math.exp(log_p)
    total = probability * tranche_loss(lgd * mode / n, attachment, detachment)
    p = probability
    for k in range(mode + 1, n + 1):
        p *= (n - k + 1) * pd / (k * (1 - pd))
        total += p * tranche_loss(lgd * k / n, attachment, detachment)
    p = probability
    for k in range(mode - 1, -1, -1):
        p *= (k + 1) * (1 - pd) / ((n - k) * pd)
        total += p * tranche_loss(lgd * k / n, attachment, detachment)
    return total


def expected_portfolio_loss(n=20, pd=0.03, lgd=0.6):
    validate(n, pd, lgd, 0.0, 1.0)
    return pd * lgd


if __name__ == "__main__":
    for a, d in ((0, .03), (.03, .10), (.10, 1)):
        loss = expected_tranche_loss(20, .03, .6, a, d)
        print(f"Tranche [{a:.0%}, {d:.0%}]: expected loss / portfolio notional = {loss:.8f}; fraction of tranche = {loss/(d-a):.4%}")
