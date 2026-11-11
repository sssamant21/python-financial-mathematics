"""Synthetic benchmark and frequency sensitivity; no market data."""
import math
from tracking_error import diagnostics

def aggregate_compound(returns, block):
    values = list(returns)
    if not isinstance(block, int) or isinstance(block, bool) or block < 1 or not values or len(values) % block:
        raise ValueError("Block must divide a nonempty series")
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < -1 for x in values):
        raise ValueError("Invalid simple return")
    if block == 1:
        return values
    return [math.prod(1 + r for r in values[i:i + block]) - 1
            for i in range(0, len(values), block)]

def sensitivity(portfolio, benchmarks, periods_per_year=12, aggregation=(1, 3)):
    """Predeclared benchmark comparisons on matched ordered timestamps."""
    p = list(portfolio)
    if not isinstance(benchmarks, dict) or not benchmarks:
        raise ValueError("Provide named benchmark series")
    if not isinstance(periods_per_year, int) or isinstance(periods_per_year, bool) or not 1 <= periods_per_year <= 366:
        raise ValueError("Invalid frequency")
    if not aggregation or len(set(aggregation)) != len(aggregation):
        raise ValueError("Aggregation blocks must be distinct")
    output = {}
    for name, series in benchmarks.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid benchmark name")
        b = list(series)
        diagnostics(p, b, periods_per_year)
        output[name] = {}
        for block in aggregation:
            if not isinstance(block, int) or isinstance(block, bool) or block < 1 or periods_per_year % block:
                raise ValueError("Block must divide periods per year")
            pa, ba = aggregate_compound(p, block), aggregate_compound(b, block)
            output[name][block] = diagnostics(pa, ba, periods_per_year // block)
    return output

if __name__ == "__main__":
    p = [.02,-.01,.03,.01,-.02,.04,.00,.02,-.01,.03,.01,.02]
    a = [.01,0,.02,.02,-.01,.02,.01,.01,0,.01,.02,.01]
    b = [.015,-.005,.025,.015,-.015,.025,.005,.015,-.005,.02,.01,.015]
    for name, blocks in sensitivity(p, {"benchmark_A":a,"benchmark_B":b}).items():
        for block, result in blocks.items():
            print(name, f"{block}-month", result)
