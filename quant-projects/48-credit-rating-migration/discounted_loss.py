"""Synthetic credit migration: year-end discounted expected loss per initial notional."""
import math
from time_varying import annual_default_increments

def discounted_expected_loss(start='B', matrices=None, lgd=0.6, annual_discount_rate=0.04):
    """Discount each year's new-default loss at a flat effective annual rate."""
    from migration import BASE
    if matrices is None:
        matrices = (BASE, BASE, BASE)
    for name, value in [('lgd', lgd), ('annual_discount_rate', annual_discount_rate)]:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f'{name} must be finite numeric, not bool')
    if not 0 <= lgd <= 1:
        raise ValueError('LGD must be in [0,1]')
    if not 0 <= annual_discount_rate <= 1:
        raise ValueError('annual discount rate must be in [0,1]')
    if start == 'D':
        raise ValueError('initially defaulted exposure requires separate valuation')
    masses = annual_default_increments(start, matrices)
    annual_losses = [mass * lgd for mass in masses]
    pv_losses = [loss / (1 + annual_discount_rate) ** year
                 for year, loss in enumerate(annual_losses, start=1)]
    return {'annual_default_mass': masses, 'annual_loss_per_notional': annual_losses,
            'annual_discounted_loss_per_notional': pv_losses,
            'cumulative_pd': sum(masses), 'undiscounted_el_per_notional': sum(annual_losses),
            'discounted_el_per_notional': sum(pv_losses)}

if __name__ == '__main__':
    from migration import BASE, STRESS
    for name, matrices in [('baseline', (BASE,) * 3),
                           ('year-two shock', (BASE, STRESS, BASE)),
                           ('persistent stress', (STRESS,) * 3)]:
        result = discounted_expected_loss(matrices=matrices)
        print(f"{name}: PD={result['cumulative_pd']:.4%}; "
              f"undiscounted EL={result['undiscounted_el_per_notional']:.4%}; "
              f"discounted EL={result['discounted_el_per_notional']:.4%}")
