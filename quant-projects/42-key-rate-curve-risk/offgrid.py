"""Off-grid zero-curve risk: linear interpolation in continuously compounded rates.

Synthetic teaching model, not calibrated market risk. Standard library only.
"""
import math

def _validate(nodes, rates, payments):
    if not nodes or len(nodes) != len(rates):
        raise ValueError("nonempty matched curve nodes and rates required")
    if any(not math.isfinite(x) for x in (*nodes, *rates)):
        raise ValueError("curve inputs must be finite")
    if any(t <= 0 or (i > 0 and t <= nodes[i-1]) for i, t in enumerate(nodes)):
        raise ValueError("curve nodes must be positive and strictly increasing")
    if any(abs(r) > 1 for r in rates):
        raise ValueError("rate outside educational +/-100% bound")
    if not payments:
        raise ValueError("at least one cash flow required")
    for t, amount in payments:
        if not math.isfinite(t) or not math.isfinite(amount) or t <= 0:
            raise ValueError("cash flows must have finite positive dates and finite amounts")
        if t < nodes[0] or t > nodes[-1]:
            raise ValueError("cash flow outside curve nodes: extrapolation forbidden")

def weights(t, nodes):
    """Interpolation coefficients, no extrapolation; exact endpoints are supported."""
    if not math.isfinite(t) or t < nodes[0] or t > nodes[-1]:
        raise ValueError("off-curve cash flow")
    for i, node in enumerate(nodes):
        if t == node:
            return {i: 1.0}
        if t < node:
            left = i - 1
            right_weight = (t - nodes[left]) / (node - nodes[left])
            return {left: 1.0 - right_weight, i: right_weight}
    return {len(nodes)-1: 1.0}

def value_and_gradient(nodes, rates, payments):
    """Return PV and exact dPV/dz_j for node zero rates (per unit decimal rate)."""
    _validate(nodes, rates, payments)
    terms = []
    gradients = [[] for _ in nodes]
    for t, amount in payments:
        w = weights(t, nodes)
        z = math.fsum(rates[j] * v for j, v in w.items())
        discounted = amount * math.exp(-t*z)
        terms.append(discounted)
        for j, v in w.items():
            gradients[j].append(-t * v * discounted)
    pv = math.fsum(terms)
    gradient = tuple(math.fsum(g) for g in gradients)
    if not all(math.isfinite(x) for x in (pv, *gradient)):
        raise ValueError("nonfinite valuation or sensitivity")
    return pv, gradient

def finite_difference_pv01(nodes, rates, payments, bump=0.0001):
    """Central-difference node PV01; returned values are currency per chosen bump."""
    if not math.isfinite(bump) or not 0 < bump <= 0.01:
        raise ValueError("bump must be finite and within (0, 100] bp")
    _validate(nodes, rates, payments)
    result = []
    for j in range(len(nodes)):
        up, down = list(rates), list(rates)
        up[j] += bump
        down[j] -= bump
        result.append((value_and_gradient(nodes, down, payments)[0] -
                       value_and_gradient(nodes, up, payments)[0]) / 2)
    return tuple(result)

def parallel_pv01(nodes, rates, payments, bump=0.0001):
    if not math.isfinite(bump) or not 0 < bump <= 0.01:
        raise ValueError("invalid bump")
    _validate(nodes, rates, payments)
    return (value_and_gradient(nodes, [r-bump for r in rates], payments)[0] -
            value_and_gradient(nodes, [r+bump for r in rates], payments)[0]) / 2

if __name__ == "__main__":
    nodes = (1.0, 3.0, 5.0)
    rates = (0.02, 0.03, 0.04)
    payments = ((1.5, 3.0), (2.5, 3.0), (4.0, 103.0))
    pv, gradient = value_and_gradient(nodes, rates, payments)
    bumps = finite_difference_pv01(nodes, rates, payments)
    print(f"Synthetic off-grid PV: {pv:.6f}")
    for t, risk, derivative in zip(nodes, bumps, gradient):
        print(f"{t:g}Y PV01: {risk:.6f}; analytic approximation: {-0.0001*derivative:.6f}")
    print(f"Parallel PV01: {parallel_pv01(nodes, rates, payments):.6f}")
