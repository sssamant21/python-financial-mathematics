"""Section 5.2: arithmetic and geometric sequences and finite sums."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be int or float, excluding bool")
    try:
        number = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside finite float range") from exc
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number

def count(value):
    if type(value) is not int:
        raise TypeError("term count or index must be an integer")
    if value < 0:
        raise ValueError("term count or index must be nonnegative")
    return value

def arithmetic_term(first, difference, index):
    return finite(first, "first") + count(index) * finite(difference, "difference")

def arithmetic_sum(first, difference, terms):
    a = finite(first, "first")
    d = finite(difference, "difference")
    n = count(terms)
    return n * (2 * a + (n - 1) * d) / 2 if n else 0.0

def geometric_term(first, ratio, index):
    return finite(first, "first") * finite(ratio, "ratio") ** count(index)

def geometric_sum(first, ratio, terms):
    a = finite(first, "first")
    q = finite(ratio, "ratio")
    n = count(terms)
    if n == 0:
        return 0.0
    if q == 1:
        return a * n
    if q > 0:
        i = q - 1
        if i > -1:
            return a * math.expm1(n * math.log1p(i)) / i
    return a * (q ** n - 1) / (q - 1)

def future_value_end_deposits(deposit, periodic_rate, periods):
    c = finite(deposit, "deposit")
    i = finite(periodic_rate, "periodic_rate")
    n = count(periods)
    if i <= -1:
        raise ValueError("periodic accumulation factor must be positive")
    if n == 0:
        return 0.0
    if i == 0:
        return c * n
    return c * math.expm1(n * math.log1p(i)) / i

if __name__ == "__main__":
    print("Arithmetic sequence:", [arithmetic_term(100, 10, n) for n in range(4)])
    print("Arithmetic sum:", arithmetic_sum(100, 10, 4))
    print("Geometric sequence:", [geometric_term(1000, 1.05, n) for n in range(4)])
    print("Three end-period deposits:", future_value_end_deposits(100, 0.10, 3))
