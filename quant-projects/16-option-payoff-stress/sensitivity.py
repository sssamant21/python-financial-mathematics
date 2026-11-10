"""Deterministic European option volatility/time sensitivity; synthetic inputs only."""
import argparse
import math
from black_scholes import price, parity_residual

def sensitivity_grid(kind='call', spot=100.0, strike=100.0, rate=0.05,
                     dividend=0.0, volatilities=(0.1, 0.2, 0.4),
                     maturities=(0.25, 1.0, 2.0)):
    """Predeclared grid, no calibration, selection, or market observations."""
    if kind not in ('call', 'put'):
        raise ValueError('kind must be call or put')
    if not volatilities or not maturities or len(volatilities)*len(maturities)>100:
        raise ValueError('grid must have 1..100 points')
    if any(not isinstance(x, (int, float)) or isinstance(x, bool) or not math.isfinite(x) or x <= 0 for x in (*volatilities, *maturities)):
        raise ValueError('volatility and maturity must be finite positive numbers')
    rows=[]
    for years in maturities:
        for sigma in volatilities:
            value=price(kind, spot, strike, years, rate, sigma, dividend)
            residual=parity_residual(spot, strike, years, rate, sigma, dividend)
            if abs(residual)>1e-8*max(1, spot, strike):
                raise ArithmeticError('put-call parity numerical residual too large')
            rows.append({'years': float(years), 'volatility': float(sigma), 'value': value, 'parity_residual': residual})
    return rows

def main():
    p=argparse.ArgumentParser(description='Hypothetical European option sensitivity')
    p.add_argument('--kind', choices=('call','put'), default='call')
    a=p.parse_args()
    for row in sensitivity_grid(kind=a.kind):
        print(f"T={row['years']:.2f} sigma={row['volatility']:.2f} price={row['value']:.6f} parity_error={row['parity_residual']:.2g}")
    print('Synthetic educational model only; not market quotes or financial advice.')

if __name__=='__main__':
    main()
