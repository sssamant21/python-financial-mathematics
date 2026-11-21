"""Synthetic peak Python-allocation diagnostic; not process RSS or a memory limit."""
import argparse
import json
import tracemalloc
from sparse_monetary_tail import sparse_tail


def measure_peak_allocations(n=12, pattern="equal", max_states=10000, precision=100):
    """Measure traced peak allocations for a bounded, independent-default DP call."""
    if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= 20:
        raise ValueError("n must be an integer in [1,20]")
    if pattern not in ("equal", "distinct"):
        raise ValueError("pattern must be equal or distinct")
    if pattern == "distinct" and n > 12:
        raise ValueError("distinct pattern capped at 12")
    if isinstance(max_states, bool) or not isinstance(max_states, int) or not 2 <= max_states <= 100000:
        raise ValueError("max_states must be an integer in [2,100000]")
    if isinstance(precision, bool) or not isinstance(precision, int) or not 32 <= precision <= 1000:
        raise ValueError("precision must be an integer in [32,1000]")
    if tracemalloc.is_tracing():
        raise RuntimeError("tracemalloc already active; measurement would be ambiguous")
    exposures = [100] * n if pattern == "equal" else [2**i for i in range(n)]
    threshold = 1
    try:
        tracemalloc.start()
        probability, diagnostics = sparse_tail(
            ["0.25"] * n, exposures, [1] * n, threshold,
            precision=precision, max_states=max_states, return_diagnostics=True)
        current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return {"synthetic_only": True, "borrowers": n, "pattern": pattern,
            "precision_digits": precision, "max_states": max_states,
            "tail_probability": str(probability),
            "peak_traced_bytes": peak, "final_traced_bytes": current,
            "peak_states": diagnostics["peak_states"],
            "final_states": diagnostics["final_states"],
            "memory_metric": "tracemalloc Python allocations, not process RSS"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--borrowers", type=int, default=12)
    parser.add_argument("--pattern", choices=("equal", "distinct"), default="equal")
    parser.add_argument("--max-states", type=int, default=10000)
    parser.add_argument("--precision", type=int, default=100)
    args = parser.parse_args()
    print(json.dumps(measure_peak_allocations(args.borrowers, args.pattern,
                                              args.max_states, args.precision), indent=2))
