"""Synthetic one-year credit expected loss and concentration stress (stdlib only)."""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Exposure:
    name: str
    ead: float
    pd: float
    lgd: float

def validate(exposures):
    if not exposures:
        raise ValueError('at least one exposure required')
    names = set()
    for x in exposures:
        if not isinstance(x.name, str) or not x.name.strip() or x.name in names:
            raise ValueError('names must be unique and nonempty')
        names.add(x.name)
        for v in (x.ead, x.pd, x.lgd):
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not isfinite(v):
                raise ValueError('inputs must be finite numbers')
        if x.ead < 0 or not (0 <= x.pd <= 1) or not (0 <= x.lgd <= 1):
            raise ValueError('ead >= 0; pd and lgd in [0,1]')

def summarize(exposures, pd_multiplier=1.0, lgd_add=0.0):
    """Stress PD by multiplier (capped at 1), LGD by additive shift (capped at 1)."""
    exposures = tuple(exposures)
    validate(exposures)
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not isfinite(v) for v in (pd_multiplier, lgd_add)):
        raise ValueError('stress parameters must be finite numbers')
    if pd_multiplier < 0 or lgd_add < 0:
        raise ValueError('stress parameters must be nonnegative')
    total_ead = sum(x.ead for x in exposures)
    if total_ead <= 0:
        raise ValueError('total exposure must be positive')
    losses = {x.name: x.ead * min(1.0, x.pd * pd_multiplier) * min(1.0, x.lgd + lgd_add) for x in exposures}
    shares = [x.ead / total_ead for x in exposures]
    return {'total_ead': total_ead, 'expected_loss': sum(losses.values()),
            'loss_by_name': losses, 'ead_hhi': sum(w*w for w in shares),
            'largest_ead_share': max(shares)}

def demo():
    book = (Exposure('A', 1_000_000, 0.01, 0.45),
            Exposure('B', 500_000, 0.03, 0.60),
            Exposure('C', 250_000, 0.06, 0.50))
    for label, kwargs in [('base', {}), ('stress', {'pd_multiplier': 2.0, 'lgd_add': 0.1})]:
        result = summarize(book, **kwargs)
        print(f"{label}: EAD={result['total_ead']:.0f} EL={result['expected_loss']:.2f} HHI={result['ead_hhi']:.4f}")

if __name__ == '__main__':
    demo()
