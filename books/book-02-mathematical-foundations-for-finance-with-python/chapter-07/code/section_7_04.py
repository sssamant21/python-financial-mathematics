"""Section 7.4: limits at infinity, asymptotes and steady states."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric")
    x = float(value)
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def rational(x):
    x = finite(x, "x")
    if abs(x) >= 1:
        y = 1/x
        return (4+3*y+y*y)/(2+7*y*y)
    return (4*x*x+3*x+1)/(2*x*x+7)

def reciprocal(x):
    x = finite(x, "x")
    if x == 2:
        raise ValueError("vertical asymptote")
    return 1/(x-2)

def steady_state(initial, contribution, multiplier):
    finite(initial, "initial")
    c = finite(contribution, "contribution")
    q = finite(multiplier, "multiplier")
    if not 0 <= q < 1:
        raise ValueError("requires 0 <= multiplier < 1")
    return c/(1-q)

def balance(initial, contribution, multiplier, periods):
    b0 = finite(initial, "initial")
    c = finite(contribution, "contribution")
    q = finite(multiplier, "multiplier")
    if q < 0:
        raise ValueError("multiplier must be nonnegative")
    if type(periods) is not int:
        raise TypeError("periods must be an integer")
    if periods < 0:
        raise ValueError("periods must be nonnegative")
    if q == 1:
        result = b0+periods*c
    else:
        fixed = c/(1-q)
        result = fixed+q**periods*(b0-fixed)
    if not math.isfinite(result):
        raise OverflowError("balance overflow")
    return result

def iterative_balance(initial, contribution, multiplier, periods):
    b = finite(initial, "initial")
    c = finite(contribution, "contribution")
    q = finite(multiplier, "multiplier")
    if q < 0 or type(periods) is not int or periods < 0:
        raise ValueError("invalid recurrence inputs")
    for _ in range(periods):
        b = q*b+c
    if not math.isfinite(b):
        raise OverflowError("balance overflow")
    return b

def perpetuity(first_payment, growth, rate):
    c = finite(first_payment, "first_payment")
    g = finite(growth, "growth")
    r = finite(rate, "rate")
    if g <= -1 or r <= -1:
        raise ValueError("rates must exceed -1")
    if c == 0:
        return 0.0
    if r <= g:
        raise ValueError("nonzero perpetuity requires rate > growth")
    return c/(r-g)

def tail(first_payment, growth, rate, periods):
    if type(periods) is not int:
        raise TypeError("periods must be an integer")
    if periods < 0:
        raise ValueError("periods must be nonnegative")
    total = perpetuity(first_payment, growth, rate)
    g = finite(growth, "growth")
    r = finite(rate, "rate")
    return total*math.exp(periods*(math.log1p(g)-math.log1p(r)))

if __name__ == "__main__":
    for x in (10, 100, 1000, 1e10, -1e10):
        print(f"x={x:.6g}, rational={rational(x):.12f}")
    for n in (0, 1, 5, 10, 50, 200):
        print(f"n={n}, balance={balance(100, 50, 0.9, n):.8f}")
    print("steady state:", steady_state(100, 50, 0.9))
    print("perpetuity:", perpetuity(100, 0.02, 0.06))
