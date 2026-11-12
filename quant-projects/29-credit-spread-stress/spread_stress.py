"""Synthetic credit-spread duration/convexity stress, Python 3.11+."""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Position:
    identifier: str
    market_value: float
    spread_duration: float
    spread_convexity: float = 0.0


def _finite(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    return float(value)


def validate(positions: list[Position]) -> None:
    if not positions:
        raise ValueError("at least one position required")
    seen: set[str] = set()
    for p in positions:
        if not isinstance(p, Position):
            raise ValueError("positions must be Position objects")
        if not isinstance(p.identifier, str) or not p.identifier.strip() or p.identifier in seen:
            raise ValueError("position IDs must be unique and nonempty")
        seen.add(p.identifier)
        if _finite(p.market_value, "market_value") <= 0:
            raise ValueError("market_value must be positive")
        if _finite(p.spread_duration, "spread_duration") < 0:
            raise ValueError("spread_duration must be nonnegative")
        if _finite(p.spread_convexity, "spread_convexity") < 0:
            raise ValueError("spread_convexity must be nonnegative")


def scenario(positions: list[Position], shock_bps: float) -> dict:
    validate(positions)
    bps = _finite(shock_bps, "shock_bps")
    if abs(bps) > 2000:
        raise ValueError("shock exceeds educational ±2000 bp guardrail")
    delta = bps / 10000.0
    attribution = {
        p.identifier: p.market_value * (-p.spread_duration * delta + 0.5 * p.spread_convexity * delta ** 2)
        for p in positions
    }
    pnl = sum(attribution.values())
    dv01 = sum(p.market_value * p.spread_duration / 10000.0 for p in positions)
    return {"shock_bps": bps, "pnl": pnl, "loss": -pnl, "spread_dv01": dv01, "attribution": attribution}


def example_positions() -> list[Position]:
    return [Position("A", 1_000_000, 4.0, 18.0), Position("B", 500_000, 2.0, 5.0)]


if __name__ == "__main__":
    for shock in (50, 100, -50):
        result = scenario(example_positions(), shock)
        print(f"{shock:+} bp | P&L {result['pnl']:,.2f} | loss {result['loss']:,.2f} | DV01 {result['spread_dv01']:,.2f}")
