"""Bounded synthetic comparison of retained states and traced Python allocations.

Measurements are descriptive and platform-dependent, not memory limits or RSS.
"""
import argparse
import json
from decimal import Decimal, localcontext
from memory_benchmark import measure_peak_allocations


def compare_patterns(sizes=(4, 8, 12), precision=100, max_states=10000):
    """Return deterministic support checks alongside observed allocation metrics."""
    if not isinstance(sizes, (tuple, list)) or not sizes:
        raise ValueError("sizes must be a nonempty list or tuple")
    if any(isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 20 for n in sizes):
        raise ValueError("sizes must contain integers in [1,20]")
    rows = []
    for n in sizes:
        for pattern in (("equal", "distinct") if n <= 12 else ("equal",)):
            row = measure_peak_allocations(n, pattern, max_states, precision)
            expected_states = n + 1 if pattern == "equal" else 2 ** n
            if row["final_states"] != expected_states or row["peak_states"] != expected_states:
                raise AssertionError("unexpected sparse support size")
            with localcontext() as ctx:
                ctx.prec = precision
                expected_tail = Decimal(1) - Decimal("0.75") ** n
            if Decimal(row["tail_probability"]) != expected_tail:
                raise AssertionError("analytical tail mismatch")
            row["expected_states"] = expected_states
            row["analytical_tail"] = str(expected_tail)
            rows.append(row)
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", type=int, nargs="+", default=[4, 8, 12])
    parser.add_argument("--precision", type=int, default=100)
    parser.add_argument("--max-states", type=int, default=10000)
    args = parser.parse_args()
    print(json.dumps(compare_patterns(args.sizes, args.precision, args.max_states), indent=2))
