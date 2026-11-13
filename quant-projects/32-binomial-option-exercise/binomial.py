"""Educational Cox-Ross-Rubinstein European/American put pricer (no market data)."""
import argparse
import math


def price_put(spot=100.0, strike=100.0, rate=0.05, dividend=0.0,
              volatility=0.2, years=1.0, steps=200, american=False):
    values = (spot, strike, rate, dividend, volatility, years)
    if any(not math.isfinite(x) for x in values):
        raise ValueError("parameters must be finite")
    if spot <= 0 or strike <= 0 or volatility <= 0 or years <= 0:
        raise ValueError("spot, strike, volatility and years must be positive")
    if not (-0.2 <= rate <= 0.5 and -0.2 <= dividend <= 0.5):
        raise ValueError("rate/dividend outside educational limits")
    if not isinstance(steps, int) or isinstance(steps, bool) or not 1 <= steps <= 2000:
        raise ValueError("steps must be an integer in [1, 2000]")
    dt = years / steps
    u = math.exp(volatility * math.sqrt(dt))
    d = 1.0 / u
    p = (math.exp((rate - dividend) * dt) - d) / (u - d)
    if not 0 <= p <= 1:
        raise ValueError("invalid risk-neutral probability; increase steps")
    discount = math.exp(-rate * dt)
    payoffs = [max(strike - spot * u ** j * d ** (steps - j), 0.0)
               for j in range(steps + 1)]
    for i in range(steps - 1, -1, -1):
        for j in range(i + 1):
            continuation = discount * (p * payoffs[j + 1] + (1 - p) * payoffs[j])
            exercise = max(strike - spot * u ** j * d ** (i - j), 0.0)
            payoffs[j] = max(continuation, exercise) if american else continuation
    return payoffs[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthetic CRR put valuation")
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--spot", type=float, default=100.0)
    parser.add_argument("--strike", type=float, default=100.0)
    parser.add_argument("--rate", type=float, default=0.05)
    parser.add_argument("--dividend", type=float, default=0.0)
    parser.add_argument("--volatility", type=float, default=0.2)
    parser.add_argument("--years", type=float, default=1.0)
    args = parser.parse_args()
    kwargs = vars(args)
    print(f"European put: {price_put(**kwargs):.6f}")
    print(f"American put: {price_put(**kwargs, american=True):.6f}")
