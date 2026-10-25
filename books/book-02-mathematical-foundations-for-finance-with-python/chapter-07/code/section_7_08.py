"""Section 7.8: numerical investigation versus proof."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric (excluding bool)")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} out of finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def removable_expression(x):
    x = finite(x, "x")
    if x == 1:
        raise ValueError("expression undefined at x=1")
    return (x*x-1)/(x-1)

def removable_stable(x):
    x = finite(x, "x")
    if x == 1:
        raise ValueError("original expression undefined at x=1")
    return x+1

def oscillation_sequences(n):
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")
    x = 1/(2*math.pi*n)
    y = 1/(math.pi/2+2*math.pi*n)
    return x, y

def exponential_quotient(h):
    h = finite(h, "h")
    if h == 0:
        return 1.0
    value = math.expm1(h)/h
    if not math.isfinite(value):
        raise OverflowError("quotient overflow")
    return value

def present_value_direct(amount, rate, periods):
    c = finite(amount, "amount")
    r = finite(rate, "rate")
    if r <= -1:
        raise ValueError("rate must exceed -1")
    if type(periods) is not int:
        raise TypeError("periods must be an integer")
    if periods < 0:
        raise ValueError("periods must be nonnegative")
    value = c/((1+r)**periods)
    if not math.isfinite(value):
        raise OverflowError("present value overflow")
    return value

def present_value_log(amount, rate, periods):
    c = finite(amount, "amount")
    r = finite(rate, "rate")
    if r <= -1:
        raise ValueError("rate must exceed -1")
    if type(periods) is not int:
        raise TypeError("periods must be an integer")
    if periods < 0:
        raise ValueError("periods must be nonnegative")
    value = c*math.exp(-periods*math.log1p(r))
    if not math.isfinite(value):
        raise OverflowError("present value overflow")
    return value

if __name__ == "__main__":
    for h in (1e-2, 1e-6, 1e-10):
        print(f"h={h:.1e}, removable raw={removable_expression(1+h):.12f}, stable={removable_stable(1+h):.12f}")
        print(f"  expm1(h)/h={exponential_quotient(h):.12f}")
    for n in (1, 2, 10):
        x, y = oscillation_sequences(n)
        print(f"n={n}: x={x:.9g}, sin(1/x)={math.sin(1/x):.8f}; y={y:.9g}, sin(1/y)={math.sin(1/y):.8f}")
    print("PV direct:", present_value_direct(1000, 0.05, 10))
    print("PV log:", present_value_log(1000, 0.05, 10))
