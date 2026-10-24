"""Exact equivalent forms with explicit mathematical and model domains."""
from fractions import Fraction


def rational(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("use an integer, rational string, or Fraction")
    return Fraction(value)


def net_return_forms(*, principal, period_rate, fixed_fee, fee_rate):
    p, r, fixed, k = map(rational, (principal, period_rate, fixed_fee, fee_rate))
    if p <= 0 or r <= -1 or fixed < 0 or k < 0:
        raise ValueError("require P > 0, r > -1, F >= 0, k >= 0")
    ending_value = p * (1 + r) - fixed - k * p
    forms = {
        "balance_quotient": (ending_value - p) / p,
        "collected_numerator": (p * (r - k) - fixed) / p,
        "rate_decomposition": r - k - fixed / p,
    }
    return {"ending_value": ending_value, "forms": forms,
            "agree": len(set(forms.values())) == 1}


def two_period_forms(*, principal, period_rate):
    p, r = map(rational, (principal, period_rate))
    if p < 0 or r <= -1:
        raise ValueError("require nonnegative principal and rate > -1")
    factored = p * (1 + r) ** 2
    expanded = p + 2 * p * r + p * r * r
    return {"factored": factored, "expanded": expanded,
            "agree": factored == expanded}


def cancellation_forms(rate):
    r = rational(rate)
    if r == 0:
        raise ValueError("original quotient excludes rate = 0")
    original = ((1 + r) ** 2 - 1) / r
    simplified = 2 + r
    return {"original": original, "simplified": simplified,
            "agree": original == simplified}


def main():
    for principal in (1000, 2000):
        report = net_return_forms(principal=principal, period_rate="0.06",
                                  fixed_fee=5, fee_rate="0.01")
        print(f"Principal {principal}: value={report['ending_value']}, "
              f"net return={report['forms']['rate_decomposition']}, "
              f"agree={report['agree']}")
    growth = two_period_forms(principal=100, period_rate="0.10")
    print(f"Growth: factored={growth['factored']}, "
          f"expanded={growth['expanded']}, agree={growth['agree']}")
    quotient = cancellation_forms("0.10")
    print(f"Cancellation at 0.10: {quotient['original']} = "
          f"{quotient['simplified']}")
    try:
        cancellation_forms(0)
    except ValueError:
        print("Cancellation at zero: excluded by original domain")


if __name__ == "__main__":
    main()
