"""Supplemental extension API. Canonical nonnegative financial library is unchanged."""
from decimal import Decimal, ROUND_HALF_UP, localcontext
from pathlib import Path
import re
import types

SOURCE=Path(__file__).resolve().parents[2]/'chapter-03/3.14-chapter-project-financial-mathematics-function-library.md'
CODE=re.findall(r'^```python\n(.*?)^```',SOURCE.read_text(),re.M|re.S)[0]
finance=types.ModuleType('canonical_finance')
exec(compile(CODE,str(SOURCE),'exec'),finance.__dict__)


def signed_present_value(flow:Decimal,*,periodic_rate:Decimal,periods:int)->Decimal:
    """Discount a signed period-n cash flow to period0 in the same currency.

    Positive means receipt; negative means payment, from one stated owner's
    perspective. Finite Decimal flow required. Rate/count/failure/context
    contracts delegate to canonical present_value on the absolute amount.
    No intervening flows, fees/tax/inflation/currency conversion or explicit
    cents. Restore the sign after calculation; signed zero normalized to +0.
    """
    if not isinstance(flow,Decimal):raise TypeError('flow must be Decimal')
    if not flow.is_finite():raise ValueError('flow must be finite')
    result=finance.present_value(flow.copy_abs(),periodic_rate=periodic_rate,periods=periods)
    return result.copy_negate() if flow<0 else result


def post_usd_cents(raw:Decimal)->Decimal:
    """Post one final signed USD amount, .01 quantum, HALF_UP, after valuation.

    Finite Decimal |raw|<=1e24. Use fixed40-digit context; no mutation.
    TypeError for representation; ValueError for domain. This is an explicit
    teaching posting policy, not a universal currency/accounting rule.
    Later calculations use this posted amount only when that policy is chosen.
    """
    if not isinstance(raw,Decimal):raise TypeError('raw must be Decimal')
    if not raw.is_finite() or raw.copy_abs()>Decimal('1e24'):raise ValueError('unsupported posting amount')
    with localcontext(finance._policy()):return raw.quantize(Decimal('.01'),rounding=ROUND_HALF_UP)


def scenario_report(principal:Decimal,nominal_rates:list[Decimal],*,frequency:int,periods:int,currency:str)->list[dict]:
    """Report nominal-to-periodic FV scenarios; metadata supplied explicitly.

    Rates and results remain numeric; no probability or ranking is inferred.
    Currency is a label, not validated against monetary input metadata.
    Canonical validation/errors propagate; this helper does not persist data.
    """
    if not isinstance(currency,str) or not currency:raise ValueError('currency label required')
    rows=[]
    for nominal in nominal_rates:
        periodic=finance.periodic_rate_from_nominal(nominal,periods_per_year=frequency)
        future=finance.future_value(principal,periodic_rate=periodic,periods=periods)
        rows.append(dict(principal=principal,currency=currency,valuation_period=0,rate_convention='nominal annual convertible at stated frequency',nominal_annual_rate=nominal,periodic_effective_rate=periodic,periods_per_year=frequency,periods=periods,future_valuation_period=periods,future_amount=future,numerical_policy='40-digit HALF_EVEN; no explicit quantization',assumptions='constant rate; single amount; no intervening flows/fees/taxes/inflation/conversion'))
    return rows
