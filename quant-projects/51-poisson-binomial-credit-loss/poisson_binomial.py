"""Exact independent heterogeneous-obligor default-count distribution; synthetic educational lab."""
import argparse
import math

def distribution(probabilities):
    ps = list(probabilities)
    if not ps or len(ps) > 500:
        raise ValueError("require 1..500 obligors")
    if any(isinstance(p, bool) or not isinstance(p, (int, float)) or not math.isfinite(p) or not 0 <= p <= 1 for p in ps):
        raise ValueError("probabilities must be finite numbers in [0,1]")
    pmf = [1.0]
    for p in ps:
        nxt = [0.0] * (len(pmf) + 1)
        for k, mass in enumerate(pmf):
            nxt[k] += mass * (1-p)
            nxt[k+1] += mass * p
        pmf = nxt
    return pmf

def tail_probability(probabilities, threshold):
    ps = list(probabilities)
    if isinstance(threshold, bool) or not isinstance(threshold, int) or threshold < 0 or threshold > len(ps) + 1:
        raise ValueError("invalid threshold")
    return math.fsum(distribution(ps)[threshold:])

def expected_defaults(probabilities):
    return math.fsum(probabilities)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probabilities", nargs="+", type=float, default=[0.01, 0.02, 0.05, 0.10])
    parser.add_argument("--threshold", type=int, default=2)
    args = parser.parse_args()
    pmf = distribution(args.probabilities)
    if not 0 <= args.threshold <= len(args.probabilities) + 1:
        parser.error("threshold outside 0..n+1")
    print(f"obligors={len(args.probabilities)} expected_defaults={expected_defaults(args.probabilities):.8f}")
    print(f"tail_probability={math.fsum(pmf[args.threshold:]):.10f}")
    print("pmf=" + ",".join(f"{x:.10f}" for x in pmf))

if __name__ == "__main__":
    main()
