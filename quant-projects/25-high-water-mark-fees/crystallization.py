"""Synthetic fee crystallization frequency and simple hurdle sensitivity.

Management fee assessed monthly on starting NAV; performance fee charged only
at crystallization dates on gains above max(previous net HWM, hurdle floor).
"""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class FeePeriod:
    month: int
    ending_nav: float
    management_fee: float
    performance_fee: float
    high_water_mark: float
    hurdle_floor: float


def _finite(value, name):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
        raise ValueError(f"{name} must be finite numeric, not boolean")
    return float(value)


def simulate_schedule(returns, initial_nav=100.0, annual_management_rate=0.0,
                      performance_rate=0.20, annual_hurdle_rate=0.0,
                      crystallize_every=1):
    """Simple non-compounding annual hurdle on net HWM since last crystallization.

    Hurdle resets on every crystallization, whether or not a performance fee is
    due; hurdle is not accrued on intra-period contributions (none modeled).
    No catch-up; hurdle is a hard floor, not a soft hurdle.
    """
    if not isinstance(returns, (list, tuple)) or not returns or len(returns) > 1200:
        raise ValueError("returns must be a nonempty list/tuple of at most 1200 months")
    if isinstance(crystallize_every, bool) or not isinstance(crystallize_every, int) or crystallize_every not in (1, 3, 6, 12):
        raise ValueError("crystallize_every must be 1, 3, 6 or 12 months")
    nav = _finite(initial_nav, "initial_nav")
    mgmt = _finite(annual_management_rate, "annual_management_rate")
    perf = _finite(performance_rate, "performance_rate")
    hurdle = _finite(annual_hurdle_rate, "annual_hurdle_rate")
    if nav <= 0 or not 0 <= mgmt < 1 or not 0 <= perf <= 1 or not 0 <= hurdle < 1:
        raise ValueError("invalid NAV or fee/hurdle rates")
    hwm = nav
    floor_base = nav
    elapsed = 0
    rows = []
    for month, raw in enumerate(returns, 1):
        r = _finite(raw, f"return[{month}]")
        if r < -1:
            raise ValueError("monthly simple return below -100%")
        start = nav
        gross = start * (1 + r)
        if not math.isfinite(gross):
            raise ValueError("NAV overflow")
        management_fee = min(gross, start * mgmt / 12)
        nav = gross - management_fee
        elapsed += 1
        hurdle_floor = floor_base * (1 + hurdle * elapsed / 12)
        performance_fee = 0.0
        if month % crystallize_every == 0:
            performance_fee = perf * max(0.0, nav - max(hwm, hurdle_floor))
            nav -= performance_fee
            hwm = max(hwm, nav)
            floor_base = hwm
            elapsed = 0
        if not math.isfinite(nav):
            raise ValueError("NAV overflow")
        rows.append(FeePeriod(month, nav, management_fee, performance_fee, hwm, hurdle_floor))
    return rows


if __name__ == "__main__":
    returns = [0.10, -0.05] + [0.0] * 10
    for frequency in (1, 12):
        for hurdle in (0.0, 0.05):
            rows = simulate_schedule(returns, annual_hurdle_rate=hurdle,
                                     crystallize_every=frequency)
            print(f"frequency={frequency:2d} months hurdle={hurdle:.0%} "
                  f"final_NAV={rows[-1].ending_nav:.6f} "
                  f"fees={sum(x.performance_fee for x in rows):.6f}")
