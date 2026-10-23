from math import isclose
from section_1_01 import compound_value


BASIS_POINTS_PER_UNIT = 10000


def annual_value(*, principal, annual_effective_rate, years):
    """Whole years; fixed annual effective rate; no fees or intervening flows."""
    return compound_value(principal, annual_effective_rate, years)


def rate_scenarios(*, principal, years, rates):
    """Keep principal/horizon fixed; return ordered (rate, value) records.

    Rates is a small finite iterable. The reused kernel validates each row.
    No output or input-repair policy is inferred from an empty rate list.
    """
    return tuple(
        (rate, annual_value(principal=principal,
                            annual_effective_rate=rate, years=years))
        for rate in rates
    )


def main():
    assumptions = {"principal": 1000.0, "years": 2}
    snapshot = assumptions.copy()  # scalar-valued dictionary in this example
    rows = rate_scenarios(**assumptions, rates=(0.0, 0.03, 0.05))
    assert assumptions == snapshot
    assert all(isclose(value, expected, rel_tol=1e-12)
               for (_, value), expected in zip(rows, (1000, 1060.9, 1102.5)))
    for rate, value in rows:
        print(f"Rate {rate:.2%}: {value:.2f}")
    before = annual_value(**assumptions, annual_effective_rate=0.05)
    after = annual_value(**assumptions, annual_effective_rate=0.06)
    exact_change = after - before
    h = 100 / BASIS_POINTS_PER_UNIT
    expanded_change = 1000 * (2 * (1 + 0.05) * h + h*h)
    assert isclose(exact_change, expanded_change, rel_tol=1e-12)
    assert isclose(exact_change, 21.1, rel_tol=1e-12)
    implied_one_year_rate = 110 / 100 - 1
    assert isclose(implied_one_year_rate, 0.1, rel_tol=1e-12)
    print(f"100-basis-point scenario change: {exact_change:.2f}")
    print(f"Implied one-year effective rate: {implied_one_year_rate:.2%}")


if __name__ == "__main__":
    main()
