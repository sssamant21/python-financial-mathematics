"""Educational fixed-for-floating swap with supplied hypothetical discount factors."""
import argparse
import math


def value_swap(notional, fixed_rate, accruals, discounts, *, pay_fixed=True):
    """Single-curve par-floating swap starting at time zero, no principal exchange.

    Floating coupon PV is N*(1-D_last); fixed coupon PV is N*K*sum(a_i*D_i).
    Assumes D(0)=1, matching fixed/floating payment dates and no spreads.
    """
    if not isinstance(pay_fixed, bool):
        raise ValueError('pay_fixed must be boolean')
    if not math.isfinite(notional) or notional <= 0 or not math.isfinite(fixed_rate):
        raise ValueError('notional must be positive finite and fixed_rate finite')
    a, d = list(accruals), list(discounts)
    if not a or len(a) != len(d):
        raise ValueError('nonempty matching accruals and discounts required')
    if any(not math.isfinite(x) or x <= 0 for x in a):
        raise ValueError('accruals must be positive finite')
    if any(not math.isfinite(x) or x <= 0 for x in d):
        raise ValueError('discounts must be positive finite')
    # Positive forwards and nonincreasing D are not mandatory: negative rates exist.
    annuity = math.fsum(x*y for x, y in zip(a, d))
    fixed_pv = notional * fixed_rate * annuity
    floating_pv = notional * (1.0 - d[-1])
    par_rate = (1.0 - d[-1]) / annuity
    net = floating_pv - fixed_pv
    if not pay_fixed:
        net = -net
    if not all(math.isfinite(x) for x in (annuity, fixed_pv, floating_pv, par_rate, net)):
        raise ValueError('nonfinite valuation: reduce input magnitudes')
    return {'annuity': annuity, 'par_rate': par_rate, 'fixed_pv': fixed_pv,
            'floating_pv': floating_pv, 'net_pv': net}


def main():
    p = argparse.ArgumentParser(description='Synthetic single-curve spot-start swap valuation')
    p.add_argument('--notional', type=float, default=1_000_000)
    p.add_argument('--fixed-rate', type=float, default=0.04)
    p.add_argument('--receive-fixed', action='store_true')
    args = p.parse_args()
    result = value_swap(args.notional, args.fixed_rate, [0.5, 0.5, 0.5, 0.5],
                        [0.98, 0.96, 0.94, 0.92], pay_fixed=not args.receive_fixed)
    for key, val in result.items():
        print(f'{key}: {val:.8f}')


if __name__ == '__main__':
    main()
