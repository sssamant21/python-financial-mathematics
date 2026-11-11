"""Synthetic withdrawal-rate and inflation sensitivity; educational only."""
import argparse
import math
from sequence_risk import simulate

RETURNS = (-0.30, -0.15, 0.22, 0.14, 0.09, 0.08, 0.07, 0.05, 0.04, 0.03)
RATES = (0.03, 0.05, 0.07, 0.09)
INFLATIONS = (0.0, 0.02, 0.04)


def funding_diagnostics(initial, first_withdrawal, returns, inflation=0.0):
    """Record funded and unfunded start-of-year withdrawals, without borrowing."""
    simulate(initial, first_withdrawal, returns, inflation)
    wealth = float(initial)
    rows = []
    for year, annual_return in enumerate(returns, 1):
        due = first_withdrawal * (1 + inflation) ** (year - 1)
        if not math.isfinite(due):
            raise ValueError('withdrawal schedule overflow')
        funded = min(wealth, due)
        shortfall = due - funded
        wealth = (wealth - funded) * (1 + annual_return)
        rows.append({'year': year, 'due': due, 'funded': funded,
                     'shortfall': shortfall, 'end_wealth': wealth})
    total_due = sum(row['due'] for row in rows)
    total_funded = sum(row['funded'] for row in rows)
    return {'terminal': wealth,
            'ruin_year': next((r['year'] for r in rows if r['shortfall'] > 0), None),
            'total_due': total_due, 'total_funded': total_funded,
            'total_shortfall': sum(r['shortfall'] for r in rows), 'rows': rows}


def sensitivity_grid(initial=100.0, returns=RETURNS, rates=RATES, inflations=INFLATIONS):
    """Fixed predeclared grid; no parameter selection on future outcomes."""
    if not math.isfinite(initial) or initial <= 0:
        raise ValueError('initial capital must be positive and finite')
    if not rates or not inflations or len(rates) * len(inflations) > 100:
        raise ValueError('grid must contain 1..100 scenarios')
    output = []
    for rate in rates:
        if not math.isfinite(rate) or not 0 <= rate <= 1:
            raise ValueError('withdrawal rates must be in [0,1]')
        for inflation in inflations:
            if not math.isfinite(inflation) or not -1 < inflation <= 1:
                raise ValueError('inflation must be in (-1,1]')
            result = funding_diagnostics(initial, initial * rate, returns, inflation)
            output.append({'withdrawal_rate': rate, 'inflation': inflation,
                           'terminal': result['terminal'], 'ruin_year': result['ruin_year'],
                           'total_shortfall': result['total_shortfall'],
                           'funded_fraction': result['total_funded'] / result['total_due']
                           if result['total_due'] else 1.0})
    return output


def main():
    parser = argparse.ArgumentParser(description='Synthetic retirement spending sensitivity grid')
    parser.add_argument('--initial', type=float, default=100.0)
    args = parser.parse_args()
    for row in sensitivity_grid(initial=args.initial):
        print(f"withdrawal={row['withdrawal_rate']:.0%} inflation={row['inflation']:.0%} "
              f"terminal={row['terminal']:.4f} shortfall={row['total_shortfall']:.4f} "
              f"funded={row['funded_fraction']:.2%} ruin_year={row['ruin_year']}")


if __name__ == '__main__':
    main()
