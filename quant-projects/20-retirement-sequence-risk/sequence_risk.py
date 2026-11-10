"""Synthetic retirement withdrawal sequence-risk lab; educational, no trading."""
import argparse
import math
import random


def simulate(initial, annual_withdrawal, returns, inflation=0.0):
    """Withdraw at start of each year, then apply that year's return.

    If withdrawal exceeds remaining wealth, ruin is recorded that year;
    no borrowing or negative wealth is permitted.
    """
    if not all(math.isfinite(x) for x in (initial, annual_withdrawal, inflation)):
        raise ValueError('inputs must be finite')
    if initial <= 0 or annual_withdrawal < 0 or inflation <= -1:
        raise ValueError('invalid capital, withdrawal, or inflation')
    if not returns or len(returns) > 120:
        raise ValueError('requires 1..120 annual returns')
    wealth = float(initial)
    path = [wealth]
    ruin_year = None
    for year, r in enumerate(returns, 1):
        if not math.isfinite(r) or r < -1:
            raise ValueError('returns must be finite and >= -100%')
        due = annual_withdrawal * (1 + inflation) ** (year - 1)
        if due > wealth and ruin_year is None:
            ruin_year = year
        wealth = max(0.0, wealth - due) * (1 + r)
        path.append(wealth)
    return {'terminal': wealth, 'ruin_year': ruin_year, 'path': path}


def permutation_stress(returns, initial, withdrawal, inflation=0.0, draws=500, seed=2026):
    """Shuffle the same synthetic annual return multiset; not a predictive model."""
    if not isinstance(draws, int) or not 1 <= draws <= 10000:
        raise ValueError('draws must be integer in 1..10000')
    simulate(initial, withdrawal, returns, inflation)
    rng = random.Random(seed)
    terminals, ruined = [], 0
    for _ in range(draws):
        shuffled = list(returns)
        rng.shuffle(shuffled)
        outcome = simulate(initial, withdrawal, shuffled, inflation)
        terminals.append(outcome['terminal'])
        ruined += outcome['ruin_year'] is not None
    terminals.sort()
    return {'ruin_fraction': ruined / draws, 'median_terminal': terminals[(draws - 1) // 2],
            'min_terminal': terminals[0], 'max_terminal': terminals[-1]}


def main():
    p = argparse.ArgumentParser(description='Synthetic sequence-of-returns risk demonstration')
    p.add_argument('--draws', type=int, default=500)
    p.add_argument('--seed', type=int, default=2026)
    args = p.parse_args()
    synthetic = [-0.30, -0.15, 0.22, 0.14, 0.09, 0.08, 0.07, 0.05, 0.04, 0.03]
    print('Early losses:', simulate(100, 7, synthetic))
    print('Late losses:', simulate(100, 7, list(reversed(synthetic))))
    print('Permutations:', permutation_stress(synthetic, 100, 7, draws=args.draws, seed=args.seed))


if __name__ == '__main__':
    main()
