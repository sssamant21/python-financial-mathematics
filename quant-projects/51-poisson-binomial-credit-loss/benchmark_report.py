"""Reproducible *scenario definitions* for observational synthetic scaling runs.

Timing and traced allocations depend on the machine, interpreter and load.
No real credit observations are loaded. This is not a capacity benchmark.
"""
import argparse
import json
import platform
import sys
import time
from datetime import datetime, timezone

from memory_comparison import compare_patterns


def collect_report(sizes=(4, 8, 12, 16, 20), precision=100, max_states=10000):
    """Run bounded cases once; record wall-clock time around the complete batch."""
    start = time.perf_counter()
    rows = compare_patterns(sizes, precision, max_states)
    elapsed = time.perf_counter() - start
    return {
        "schema_version": 1,
        "synthetic_only": True,
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version.split()[0],
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "scenario_sizes": list(sizes),
        "precision_digits": precision,
        "max_states": max_states,
        "batch_elapsed_seconds": elapsed,
        "elapsed_scope": "complete batch including tracing, validation, and Python overhead",
        "memory_scope": "per-case tracemalloc traced allocations; not process RSS",
        "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", nargs="+", type=int, default=[4, 8, 12, 16, 20])
    parser.add_argument("--precision", type=int, default=100)
    parser.add_argument("--max-states", type=int, default=10000)
    parser.add_argument("--output", help="optional JSON path; no data files are bundled")
    args = parser.parse_args()
    report = collect_report(tuple(args.sizes), args.precision, args.max_states)
    payload = json.dumps(report, indent=2) + "\n"
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
