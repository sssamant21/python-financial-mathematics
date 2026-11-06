"""Supplemental scorecard orchestration for the exact source functions."""
import csv
import io
import math
from fractions import Fraction as F


def fixtures():
    def rates(points):
        return [F(x,100) for x in points]
    return {'A':rates([3,-2,4,-1,2,1]),'B':rates([2,-1,3,-2,1,2])},rates([2,-1,2,-1,1,1])


def scorecard(source, name, returns, bench):
    # Subtract decimal observations before converting to the source API.
    active=[float(F(str(x))-F(str(y))) for x,y in zip(returns,bench)]
    volatility=source.sample_std(returns)
    return dict(strategy=name,mean_monthly=source.mean(returns),vol_monthly=volatility,
                vol_annual=volatility*math.sqrt(12),sharpe_annual=source.sharpe_ratio(returns,.002,12),
                sortino_annual=source.sortino_ratio(returns,0,12),mdd=source.max_drawdown(returns),
                ir_annual=source.information_ratio(active,12),beta=source.beta(returns,bench))


def as_csv(rows):
    stream=io.StringIO()
    writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()
