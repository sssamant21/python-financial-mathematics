"""Synthetic one-year Gaussian exposure/default dependence stress; not regulatory CVA."""
import argparse
import math
import random
from statistics import NormalDist

NORMAL = NormalDist()

def analytical_epe(notional, volatility, threshold):
    sigma = notional * volatility
    if sigma == 0:
        return 0.0
    k = threshold / sigma
    return sigma * NORMAL.pdf(k) - threshold * NORMAL.cdf(-k)

def estimate(*, paths=20000, seed=49, rho=0.0, notional=1_000_000.0,
             volatility=0.2, threshold=0.0, default_probability=0.02,
             lgd=0.6, rate=0.03):
    """Common random numbers across rho values; joint normal latent default model."""
    if type(paths) is not int or not 100 <= paths <= 200000 or type(seed) is not int:
        raise ValueError("paths must be 100..200000 and seed an integer")
    numbers = (rho, notional, volatility, threshold, default_probability, lgd, rate)
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in numbers):
        raise ValueError("all economic inputs must be finite real numbers")
    if not -0.99 <= rho <= 0.99 or notional <= 0 or volatility < 0 or threshold < 0 or not 0 < default_probability < 1 or not 0 <= lgd <= 1 or rate < 0:
        raise ValueError("invalid economic inputs")
    rng = random.Random(seed)
    cutoff = NORMAL.inv_cdf(default_probability)
    scale = math.sqrt(1 - rho * rho)
    exposure_sum = loss_sum = loss_sq_sum = defaults = 0.0
    for _ in range(paths):
        z = rng.gauss(0, 1)
        independent = rng.gauss(0, 1)
        exposure = max(notional * volatility * z - threshold, 0.0)
        # Default when latent variable is low: negative rho increases wrong-way risk.
        event = rho * z + scale * independent < cutoff
        loss = exposure if event else 0.0
        exposure_sum += exposure
        loss_sum += loss
        loss_sq_sum += loss * loss
        defaults += event
    factor = lgd * math.exp(-rate)
    cva = factor * loss_sum / paths
    sample_var = max((loss_sq_sum - loss_sum * loss_sum / paths) / (paths - 1), 0.0)
    return {"cva": cva, "standard_error": factor * math.sqrt(sample_var / paths),
            "epe": exposure_sum / paths, "realized_default_rate": defaults / paths,
            "independent_benchmark": factor * default_probability * analytical_epe(notional, volatility, threshold)}

def main():
    p = argparse.ArgumentParser(description="One-year synthetic Gaussian default/exposure dependence")
    p.add_argument("--paths", type=int, default=20000)
    p.add_argument("--seed", type=int, default=49)
    args = p.parse_args()
    print("rho,cva,standard_error,independent_benchmark,realized_default_rate")
    for rho in (0.6, 0.0, -0.6):
        x = estimate(paths=args.paths, seed=args.seed, rho=rho)
        print(f"{rho:.1f},{x['cva']:.2f},{x['standard_error']:.2f},{x['independent_benchmark']:.2f},{x['realized_default_rate']:.5f}")

if __name__ == "__main__":
    main()
