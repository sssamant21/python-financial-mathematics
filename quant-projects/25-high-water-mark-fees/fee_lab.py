"""Educational high-water-mark performance fee accounting; synthetic data only."""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Period:
    gross_return: float
    starting_nav: float
    pre_fee_nav: float
    management_fee: float
    performance_fee: float
    ending_nav: float
    high_water_mark: float


def _number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number, not boolean")
    return float(value)


def simulate(returns, initial_nav=100.0, management_rate=0.02,
             performance_rate=0.20, periods_per_year=12):
    """Apply periodic management fee, then performance fee above post-fee HWM.

    Returns are gross simple period returns; fee rates are annual management
    fraction and performance fraction of gains above prior net NAV high water mark.
    Management fees are charged on beginning NAV at annual_rate/periods_per_year.
    Performance fees crystallize each period (not just at year-end).
    """
    nav = _number(initial_nav, "initial_nav")
    mgmt = _number(management_rate, "management_rate")
    perf = _number(performance_rate, "performance_rate")
    if nav <= 0 or not 0 <= mgmt < 1 or not 0 <= perf <= 1:
        raise ValueError("initial NAV must be positive and fee rates in valid ranges")
    if isinstance(periods_per_year, bool) or not isinstance(periods_per_year, int) or periods_per_year < 1:
        raise ValueError("periods_per_year must be a positive integer")
    if not isinstance(returns, (list, tuple)) or not returns:
        raise ValueError("returns must be a nonempty list or tuple")
    if len(returns) > 100000:
        raise ValueError("too many periods")
    hwm = nav
    result = []
    for i, raw in enumerate(returns):
        r = _number(raw, f"return[{i}]")
        if r < -1:
            raise ValueError("simple returns cannot be below -100%")
        start = nav
        pre_fee = start * (1 + r)
        management_fee = min(pre_fee, start * mgmt / periods_per_year)
        after_mgmt = pre_fee - management_fee
        performance_fee = perf * max(0.0, after_mgmt - hwm)
        nav = after_mgmt - performance_fee
        if not math.isfinite(nav):
            raise ValueError("NAV overflow")
        hwm = max(hwm, nav)
        result.append(Period(r, start, pre_fee, management_fee, performance_fee, nav, hwm))
    return result


if __name__ == "__main__":
    demo = simulate([0.10, -0.15, 0.12, 0.08], management_rate=0.0)
    print("period  gross_return  end_NAV  performance_fee  HWM")
    for i, p in enumerate(demo, 1):
        print(f"{i:>6}  {p.gross_return:>12.1%}  {p.ending_nav:>7.3f}  {p.performance_fee:>15.3f}  {p.high_water_mark:>7.3f}")
