"""Seeded one-factor Gaussian correlated-default stress (synthetic, educational)."""
import math
import random
from statistics import NormalDist
from tranche_loss import validate, tranche_loss, expected_tranche_loss

def simulate(n=20, pd=.03, lgd=.6, attachment=0., detachment=.1,
             rho=.25, paths=20000, seed=47):
    """Return mean tranche loss, Monte Carlo SE, approximate 95% CI and exact independent baseline."""
    validate(n, pd, lgd, attachment, detachment)
    if isinstance(rho, bool) or not isinstance(rho, (int, float)) or not math.isfinite(rho) or not 0 <= rho < 1:
        raise ValueError("rho must be finite in [0,1)")
    if isinstance(paths, bool) or not isinstance(paths, int) or not 2 <= paths <= 200000:
        raise ValueError("paths must be an integer in [2,200000]")
    if isinstance(seed, bool) or not isinstance(seed, int) or not 0 <= seed < 2**32:
        raise ValueError("seed must be an integer in [0,2**32)")
    if n * paths > 5_000_000:
        raise ValueError("n * paths exceeds computational guardrail")
    baseline = expected_tranche_loss(n, pd, lgd, attachment, detachment)
    if pd in (0, 1) or lgd == 0:
        loss = tranche_loss(lgd if pd == 1 else 0., attachment, detachment)
        return dict(mean=loss, se=0., ci95=(loss, loss), independent_exact=baseline)
    rng = random.Random(seed)
    threshold = NormalDist().inv_cdf(pd)
    common, unique = math.sqrt(rho), math.sqrt(1-rho)
    total = total_sq = 0.
    for _ in range(paths):
        systematic = common * rng.gauss(0, 1)
        defaults = sum(systematic + unique * rng.gauss(0, 1) < threshold for _ in range(n))
        loss = tranche_loss(lgd * defaults / n, attachment, detachment)
        total += loss
        total_sq += loss * loss
    mean = total / paths
    variance = max(0., (total_sq - paths * mean * mean) / (paths-1))
    se = math.sqrt(variance / paths)
    return dict(mean=mean, se=se,
                ci95=(max(0., mean-1.96*se), min(detachment-attachment, mean+1.96*se)),
                independent_exact=baseline)

if __name__ == "__main__":
    for rho in (0., .25, .6):
        x = simulate(rho=rho, paths=10000)
        print(f"rho={rho:.2f}: mean={x['mean']:.6f}, SE={x['se']:.6f}, CI95={x['ci95']}, independent={x['independent_exact']:.6f}")
