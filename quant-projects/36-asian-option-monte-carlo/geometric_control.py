"""Discrete geometric Asian call benchmark and fixed-beta control variate."""
import math
import random
from statistics import mean, stdev

def geometric_call_exact(spot=100., strike=100., rate=.03, volatility=.2, maturity=1., observations=12):
    """Risk-neutral lognormal price for equally spaced post-initial observations."""
    if not all(math.isfinite(x) for x in (spot, strike, rate, volatility, maturity)):
        raise ValueError('nonfinite input')
    if spot <= 0 or strike <= 0 or volatility <= 0 or maturity <= 0:
        raise ValueError('positive spot, strike, volatility and maturity required')
    if type(observations) is not int or not 1 <= observations <= 1000:
        raise ValueError('observations outside 1..1000')
    if abs(rate*maturity)>50 or volatility*math.sqrt(maturity)>3:
        raise ValueError('unsafe exponent range')
    n = observations
    mu = math.log(spot) + (rate-volatility**2/2)*maturity*(n+1)/(2*n)
    var = volatility**2*maturity*(n+1)*(2*n+1)/(6*n*n)
    sd = math.sqrt(var)
    d1 = (mu + var - math.log(strike))/sd
    d2 = d1-sd
    phi = lambda x: .5*math.erfc(-x/math.sqrt(2))
    return math.exp(-rate*maturity)*(math.exp(mu+var/2)*phi(d1)-strike*phi(d2))

def compare_estimators(spot=100., strike=100., rate=.03, volatility=.2, maturity=1., observations=12, pairs=5000, seed=2026):
    """Paired antithetic arithmetic estimate and fixed-beta geometric control estimate."""
    exact = geometric_call_exact(spot,strike,rate,volatility,maturity,observations)
    if type(pairs) is not int or not 2 <= pairs <= 100000:
        raise ValueError('pairs outside 2..100000')
    if type(seed) is not int:
        raise ValueError('seed must be integer')
    rng = random.Random(seed)
    dt = maturity/observations
    drift = (rate-volatility**2/2)*dt
    vol = volatility*math.sqrt(dt)
    discount = math.exp(-rate*maturity)
    raw, controlled = [], []
    for _ in range(pairs):
        prices = [spot,spot]
        sums = [0.,0.]
        log_sums = [0.,0.]
        for _ in range(observations):
            z = rng.gauss(0,1)
            for j, sign in enumerate((1.,-1.)):
                prices[j] *= math.exp(drift+sign*vol*z)
                if not math.isfinite(prices[j]) or prices[j] <= 0:
                    raise ValueError('simulated price overflow or underflow')
                sums[j] += prices[j]
                log_sums[j] += math.log(prices[j])
        arithmetic = discount*sum(max(s/observations-strike,0.) for s in sums)/2
        geometric = discount*sum(max(math.exp(s/observations)-strike,0.) for s in log_sums)/2
        raw.append(arithmetic)
        controlled.append(arithmetic-(geometric-exact))
    return {'arithmetic_price':mean(raw), 'arithmetic_se':stdev(raw)/math.sqrt(pairs),
            'controlled_price':mean(controlled), 'controlled_se':stdev(controlled)/math.sqrt(pairs),
            'geometric_exact':exact, 'pairs':pairs, 'observations':observations}

if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--pairs',type=int,default=5000)
    parser.add_argument('--observations',type=int,default=12)
    parser.add_argument('--seed',type=int,default=2026)
    args=parser.parse_args()
    for k,v in compare_estimators(pairs=args.pairs,observations=args.observations,seed=args.seed).items():
        print(f'{k}: {v}')
