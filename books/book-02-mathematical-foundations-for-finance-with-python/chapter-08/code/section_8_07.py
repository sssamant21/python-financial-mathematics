"""Section 8.7: implicit differentiation and financial sensitivity."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        x = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite float range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def circle_upper(x, radius=5):
    x, radius = finite(x, "x"), finite(radius, "radius")
    if radius <= 0 or abs(x) > radius:
        raise ValueError("radius must be positive and |x| <= radius")
    return math.sqrt((radius-x)*(radius+x))

def circle_slope(x, y):
    x, y = finite(x, "x"), finite(y, "y")
    if y == 0:
        raise ValueError("implicit slope undefined where y=0")
    return -x/y

def break_even_quantity(price, variable_cost, fixed_cost):
    p, c, k = finite(price, "price"), finite(variable_cost, "variable_cost"), finite(fixed_cost, "fixed_cost")
    if k <= 0 or p <= c:
        raise ValueError("require fixed_cost > 0 and price > variable_cost")
    return k/(p-c)

def break_even_sensitivity(price, variable_cost, fixed_cost):
    p, c = finite(price, "price"), finite(variable_cost, "variable_cost")
    q = break_even_quantity(p, c, fixed_cost)
    return -q/(p-c)

def bond_price(cash_flows, yield_per_period):
    y = finite(yield_per_period, "yield_per_period")
    if y <= -1:
        raise ValueError("yield_per_period must exceed -1")
    flows = tuple(finite(c, "cash_flow") for c in cash_flows)
    if not flows or any(c <= 0 for c in flows):
        raise ValueError("cash flows must be a nonempty positive sequence")
    return sum(c/(1+y)**i for i, c in enumerate(flows, 1))

def bond_price_derivative(cash_flows, yield_per_period):
    y = finite(yield_per_period, "yield_per_period")
    if y <= -1:
        raise ValueError("yield_per_period must exceed -1")
    flows = tuple(finite(c, "cash_flow") for c in cash_flows)
    if not flows or any(c <= 0 for c in flows):
        raise ValueError("cash flows must be a nonempty positive sequence")
    return -sum(i*c/(1+y)**(i+1) for i, c in enumerate(flows, 1))

def yield_price_sensitivity(cash_flows, yield_per_period):
    derivative = bond_price_derivative(cash_flows, yield_per_period)
    if derivative == 0:
        raise ValueError("price derivative is zero")
    return 1/derivative

def exposure_slope(x, y, a, b):
    x, y, a, b = (finite(v, n) for v, n in ((x,"x"),(y,"y"),(a,"a"),(b,"b")))
    if a <= 0 or b <= 0 or y == 0:
        raise ValueError("a and b must be positive and y nonzero")
    return -a*x/(b*y)

def centered_difference(function, x, step=1e-4):
    if not callable(function):
        raise TypeError("function must be callable")
    x, h = finite(x, "x"), finite(step, "step")
    if h == 0:
        raise ValueError("step must be nonzero")
    return (finite(function(x+h), "f(x+h)")-finite(function(x-h), "f(x-h)"))/(2*h)

if __name__ == "__main__":
    print("Circle slope at (3,4):", circle_slope(3, 4))
    print("Break-even quantity:", break_even_quantity(50, 20, 1200))
    print("Break-even sensitivity:", break_even_sensitivity(50, 20, 1200))
    print("One-period bond price:", bond_price((105,), 0.05))
    print("Bond yield sensitivity:", yield_price_sensitivity((105,), 0.05))
    print("Exposure slope:", exposure_slope(3, 4, 1, 1))
