"""Joint bid/ask interval feasibility for small same-expiry European call grids.

Fourier-Motzkin elimination of linear constraints; synthetic educational use only.
"""
import math

def joint_feasible(strikes, bids, asks, *, discount=1.0, tolerance=1e-9):
    n = len(strikes)
    if not 3 <= n <= 5 or len(bids) != n or len(asks) != n:
        raise ValueError("requires 3-5 aligned quotes")
    values = [*strikes, *bids, *asks, discount, tolerance]
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in values):
        raise ValueError("finite numeric inputs required")
    if not 0 < discount <= 2 or not 0 <= tolerance <= 1e-6:
        raise ValueError("invalid discount or tolerance")
    if any(k <= 0 for k in strikes) or any(y <= x for x, y in zip(strikes, strikes[1:])):
        raise ValueError("strikes must increase")
    if any(b < 0 or a < b for b, a in zip(bids, asks)):
        raise ValueError("invalid bid/ask")
    # Work in dimensionless strike/price units. A common positive scale preserves
    # all linear no-arbitrage inequalities while making tolerance unit-independent.
    unit = max(*strikes, *asks, 1e-300)
    strikes = [k / unit for k in strikes]
    bids = [b / unit for b in bids]
    asks = [a / unit for a in asks]
    constraints = []
    def add(coeff, rhs):
        scale = max([1.0, *(abs(x) for x in coeff)])
        constraints.append((tuple(x/scale for x in coeff), rhs/scale))
    for i in range(n):
        a = [0.0]*n
        a[i] = 1.0
        add(a, asks[i])
        a[i] = -1.0
        add(a, -bids[i])
    for i in range(n-1):
        a = [0.0]*n
        a[i], a[i+1] = -1.0, 1.0
        add(a, 0.0)
        add([-x for x in a], discount*(strikes[i+1]-strikes[i]))
    for i in range(1,n-1):
        left, right = strikes[i]-strikes[i-1], strikes[i+1]-strikes[i]
        a = [0.0]*n
        a[i-1], a[i], a[i+1] = -right, left+right, -left
        add(a, 0.0)
    for _ in range(n):
        pos, neg, zero = [], [], []
        for coeff, rhs in constraints:
            if coeff[-1] > 0: pos.append((coeff,rhs))
            elif coeff[-1] < 0: neg.append((coeff,rhs))
            else: zero.append((coeff[:-1],rhs))
        if len(pos)*len(neg)+len(zero) > 20000:
            raise ValueError("elimination growth limit exceeded")
        new = zero
        for p,bp in pos:
            for m,bm in neg:
                ap,am = -m[-1],p[-1]
                coeff = tuple(ap*x+am*y for x,y in zip(p[:-1],m[:-1]))
                rhs = ap*bp+am*bm
                scale = max([1.0, *(abs(x) for x in coeff)])
                new.append((tuple(x/scale for x in coeff),rhs/scale))
        dedup = {}
        for coeff,rhs in new:
            if not coeff and rhs < -tolerance:
                return {"joint_feasible":False,"method":"fourier_motzkin"}
            if coeff not in dedup or rhs < dedup[coeff]: dedup[coeff] = rhs
        constraints = list(dedup.items())
    return {"joint_feasible":True,"method":"fourier_motzkin"}

if __name__ == "__main__":
    import json
    print(json.dumps(joint_feasible([90,100,110],[14,9,5],[15,10,6]),indent=2))
