"""Optional QuantLib cross-check for synthetic fixed-coupon bond pricing.

Requires QuantLib==1.39 (install separately). No market data or live trading.
"""
from math import exp, isfinite

def manual_present_value(cashflows, settlement, annual_continuous_yield):
    """Discount (payment date offset in days, amount) at ACT/365 fixed."""
    if isinstance(annual_continuous_yield, bool) or not isinstance(annual_continuous_yield, (int, float)) or not isfinite(annual_continuous_yield):
        raise ValueError("finite numeric yield required")
    if not cashflows:
        raise ValueError("nonempty future cashflows required")
    total = 0.0
    for days, amount in cashflows:
        if isinstance(days, bool) or not isinstance(days, int) or days <= 0:
            raise ValueError("positive integer day offsets required")
        if isinstance(amount, bool) or not isinstance(amount, (int, float)) or not isfinite(amount) or amount <= 0:
            raise ValueError("positive finite cashflows required")
        exponent = -annual_continuous_yield * days / 365.0
        if abs(exponent) > 700:
            raise ValueError("discount exponent outside safe range")
        total += amount * exp(exponent)
    if not isfinite(total) or total <= 0:
        raise ValueError("invalid present value")
    return total

def compare_quantlib(coupon_rate=0.05, annual_continuous_yield=0.045):
    """Compare QuantLib's discounted bond NPV to separate Python PV summation.

    Settlement/evaluation: 2025-01-15; maturity: 2030-01-15.
    Semiannual coupons, Actual/365 Fixed accrual, unadjusted dates,
    continuous flat yield; excludes accrued/clean-price comparisons.
    """
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not isfinite(x) or x < 0 or x > 1 for x in (coupon_rate, annual_continuous_yield)):
        raise ValueError("rates must be finite in [0,1]")
    import QuantLib as ql  # optional; ImportError intentionally propagates
    settlement = ql.Date(15, 1, 2025)
    maturity = ql.Date(15, 1, 2030)
    previous = ql.Settings.instance().evaluationDate
    try:
        ql.Settings.instance().evaluationDate = settlement
        schedule = ql.Schedule(settlement, maturity, ql.Period(ql.Semiannual),
                               ql.NullCalendar(), ql.Unadjusted, ql.Unadjusted,
                               ql.DateGeneration.Forward, False)
        bond = ql.FixedRateBond(0, 100.0, schedule, [coupon_rate],
                                ql.Actual365Fixed(), ql.Unadjusted, 100.0, settlement)
        curve = ql.YieldTermStructureHandle(
            ql.FlatForward(settlement, annual_continuous_yield,
                           ql.Actual365Fixed(), ql.Continuous))
        bond.setPricingEngine(ql.DiscountingBondEngine(curve))
        external_npv = bond.NPV()
        future = [(int(cf.date() - settlement), float(cf.amount()))
                  for cf in bond.cashflows() if cf.date() > settlement]
        manual_npv = manual_present_value(future, settlement, annual_continuous_yield)
        return {"external_npv": external_npv, "manual_npv": manual_npv,
                "absolute_difference": abs(external_npv - manual_npv),
                "cashflow_count": len(future)}
    finally:
        ql.Settings.instance().evaluationDate = previous

if __name__ == "__main__":
    result = compare_quantlib()
    print(result)
