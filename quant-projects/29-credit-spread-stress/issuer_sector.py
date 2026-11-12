"""Issuer/sector credit-spread stress and concentration; synthetic Python 3.11+."""
from dataclasses import dataclass
from spread_stress import Position, validate, _finite

@dataclass(frozen=True)
class CreditHolding:
    position: Position
    issuer: str
    sector: str

def evaluate(holdings: list[CreditHolding], sector_shocks: dict[str, float],
             issuer_shocks: dict[str, float] | None = None) -> dict:
    """Predeclared sector + issuer bp shocks; no market data or trading."""
    if not holdings or any(not isinstance(h, CreditHolding) for h in holdings):
        raise ValueError("nonempty CreditHolding list required")
    if not isinstance(sector_shocks, dict) or not isinstance(issuer_shocks, (dict, type(None))):
        raise ValueError("shock maps must be dictionaries")
    issuer_shocks = {} if issuer_shocks is None else issuer_shocks
    validate([h.position for h in holdings])
    for h in holdings:
        if not isinstance(h.issuer, str) or not h.issuer.strip() or not isinstance(h.sector, str) or not h.sector.strip():
            raise ValueError("issuer and sector must be nonempty strings")
    sectors = {h.sector for h in holdings}
    issuers = {h.issuer for h in holdings}
    if set(sector_shocks) != sectors or not set(issuer_shocks).issubset(issuers):
        raise ValueError("sector shocks must match held sectors; issuer shocks must reference held issuers")
    for mapping in (sector_shocks, issuer_shocks):
        for key, value in mapping.items():
            if not isinstance(key, str) or not key.strip() or abs(_finite(value, "shock")) > 2000:
                raise ValueError("invalid shock key or magnitude")
    position_pnl = {}
    sector_pnl = {s: 0.0 for s in sorted(sectors)}
    issuer_pnl = {i: 0.0 for i in sorted(issuers)}
    sector_value = {s: 0.0 for s in sorted(sectors)}
    issuer_value = {i: 0.0 for i in sorted(issuers)}
    total_value = sum(h.position.market_value for h in holdings)
    for h in holdings:
        p = h.position
        bps = sector_shocks[h.sector] + issuer_shocks.get(h.issuer, 0.0)
        if abs(bps) > 2000:
            raise ValueError("combined shock exceeds ±2000 bp")
        ds = bps / 10000.0
        pnl = p.market_value * (-p.spread_duration * ds + 0.5 * p.spread_convexity * ds ** 2)
        position_pnl[p.identifier] = pnl
        sector_pnl[h.sector] += pnl
        issuer_pnl[h.issuer] += pnl
        sector_value[h.sector] += p.market_value
        issuer_value[h.issuer] += p.market_value
    pnl = sum(position_pnl.values())
    issuer_weights = {k: v / total_value for k, v in issuer_value.items()}
    sector_weights = {k: v / total_value for k, v in sector_value.items()}
    return {"pnl": pnl, "loss": -pnl, "position_pnl": position_pnl,
            "sector_pnl": sector_pnl, "issuer_pnl": issuer_pnl,
            "issuer_weights": issuer_weights, "sector_weights": sector_weights,
            "issuer_hhi": sum(w*w for w in issuer_weights.values()),
            "sector_hhi": sum(w*w for w in sector_weights.values())}

def example() -> dict:
    holdings = [CreditHolding(Position("A1", 1_000_000, 4, 18), "A", "Tech"),
                CreditHolding(Position("B1", 500_000, 2, 5), "B", "Energy"),
                CreditHolding(Position("A2", 500_000, 3, 10), "A", "Tech")]
    return evaluate(holdings, {"Tech": 100, "Energy": 50}, {"A": 25})

if __name__ == "__main__":
    result = example()
    print(f"Synthetic portfolio P&L: {result['pnl']:,.2f}; issuer HHI: {result['issuer_hhi']:.4f}")
    print("Issuer P&L:", result["issuer_pnl"])
