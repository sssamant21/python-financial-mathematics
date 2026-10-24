"""Section 3.5 reference checks: thresholds, boundaries, and domains."""
from fractions import Fraction as F
from section_3_05 import (rational, flat_tier_fee, marginal_tier_fee,
                          unit_price, volume_revenue, step_fixed_cost,
                          step_profit)


def rejects(error, function, *args):
    try:
        function(*args)
    except error:
        return
    raise AssertionError(f"expected {error.__name__}")


def run():
    assert flat_tier_fee("99.99") == 2
    assert flat_tier_fee(100) == 2
    assert flat_tier_fee("100.01") == 5
    assert marginal_tier_fee(0) == 0
    assert marginal_tier_fee(100) == 1
    assert marginal_tier_fee("100.01") == F(5001,5000)
    assert marginal_tier_fee(200) == 3
    assert unit_price(9) == 12 and unit_price(10) == 10
    assert volume_revenue(9) == 108
    assert volume_revenue(10) == 100
    assert volume_revenue(11) == 110
    assert step_fixed_cost(10) == 40
    assert step_fixed_cost(11) == 70
    assert step_profit(10) == 30
    assert step_profit(11) == 7
    assert step_profit(12) == 14
    for amount in (0, "99.99", 100, "100.01", 1000):
        assert marginal_tier_fee(amount) >= 0
    for n in range(0, 25):
        assert step_profit(n) == 7*n-step_fixed_cost(n)
    rejects(ValueError, flat_tier_fee, -1)
    rejects(ValueError, marginal_tier_fee, -1)
    rejects(ValueError, unit_price, "1/2")
    rejects(ValueError, step_fixed_cost, "10.5")
    rejects(TypeError, rational, 0.1)
    rejects(TypeError, rational, True)
    print("PASS: Section 3.5 reference checks")


if __name__ == "__main__":
    run()
