"""Repeated synthetic observations; never treat timings as capacity promises."""
import argparse
import json
import math
import statistics
from benchmark_report import collect_report


def collect_repeated(repetitions=3, sizes=(4, 8, 12), precision=100, max_states=10000):
    if isinstance(repetitions, bool) or not isinstance(repetitions, int) or not 2 <= repetitions <= 10:
        raise ValueError("repetitions must be an integer from 2 to 10")
    runs = [collect_report(sizes, precision, max_states) for _ in range(repetitions)]
    signature = None
    for run in runs:
        if run["schema_version"] != 1 or run["synthetic_only"] is not True:
            raise AssertionError("unexpected benchmark report contract")
        current = []
        for row in run["rows"]:
            if row["final_states"] != row["expected_states"] or row["peak_states"] != row["expected_states"]:
                raise AssertionError("state count mismatch")
            if row["tail_probability"] != row["analytical_tail"]:
                raise AssertionError("tail mismatch")
            current.append((row["borrowers"], row["pattern"], row["expected_states"], row["tail_probability"]))
        if signature is not None and current != signature:
            raise AssertionError("non-deterministic mathematical outputs")
        signature = current
    times = [run["batch_elapsed_seconds"] for run in runs]
    if not all(math.isfinite(t) and t >= 0 for t in times):
        raise AssertionError("invalid elapsed time")
    rows = []
    for i, (borrowers, pattern, states, tail) in enumerate(signature):
        peaks = [run["rows"][i]["peak_traced_bytes"] for run in runs]
        if not all(isinstance(x, int) and x >= 0 for x in peaks):
            raise AssertionError("invalid traced memory")
        rows.append({"borrowers": borrowers, "pattern": pattern, "expected_states": states,
                     "analytical_tail": tail, "peak_traced_bytes_min": min(peaks),
                     "peak_traced_bytes_median": statistics.median(peaks),
                     "peak_traced_bytes_max": max(peaks)})
    return {"schema_version": 1, "synthetic_only": True, "repetitions": repetitions,
            "python_version": runs[0]["python_version"], "platform": runs[0]["platform"],
            "batch_seconds_min": min(times), "batch_seconds_median": statistics.median(times),
            "batch_seconds_max": max(times), "rows": rows,
            "caveat": "Sequential same-process measurements; tracemalloc is not RSS; no capacity or independent-validation claim."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--sizes", type=int, nargs="+", default=[4, 8, 12])
    parser.add_argument("--precision", type=int, default=100)
    parser.add_argument("--max-states", type=int, default=10000)
    args = parser.parse_args()
    print(json.dumps(collect_repeated(args.repetitions, tuple(args.sizes), args.precision, args.max_states), indent=2))


if __name__ == "__main__":
    main()
