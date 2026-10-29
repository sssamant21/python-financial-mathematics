# Chapter 1 — 40 short exercise answer records

Reviewed 2026-10-29 against source revision `ef9b06d8893c180b28a81de6dc07f0ba91fdf307`. Supplemental reference answers; no student submissions or independent human review are certified. IDs use section and local exercise number. Full source hashes are in [answers.json](answers.json). Runtime predicates are recorded separately.

## S06-E01 — FV display

P=5,000.00; rate=4.00% per period; n=5; FV=6,083.26. No interim rounding.

## S06-E02 — Scenario function

Use calculate_future_value for each rate: 13,439.16; 16,288.95; 19,671.51. For positive principal and positive horizons, higher assumed effective rates give larger FV. The derivative P*n*(1+r)**(n-1) shows horizon dependence; no forecast accuracy is implied.

## S06-E03 — Rate error

The integer 5 denotes a decimal rate of 500%, giving 216,000.00. Replace with 0.05 to model 5% annual effective growth; FV=1,157.625, displayed 1,157.62 using float formatting. Display rounding is not an accounting rule.

## S06-E04 — Independent validation

2500*(53/50)^4 = 3156.1924 exactly. Compare the float calculation to 3156.1924 with math.isclose using default arguments.

## S07-E01 — Types

Example principal 1000.0: float; rate .05: float; periods 3: int; currency USD: str; eligibility True: bool. Identical float types do not distinguish money from dimensionless rates or quote conventions.

## S07-E02 — Float/Decimal

Float sum is 0.30000000000000004; Decimal string construction gives exactly 0.3 under this context. Constructing Decimal from float would preserve its binary approximation.

## S07-E03 — Equality

Float sum == .3 is False; math.isclose is True with defaults. Approximate equality is not a universal monetary reconciliation policy.

## S07-E04 — Bond mapping

Provide name, face_value, coupon_rate, currency, maturity_date (datetime.date), callable (bool); see executable dictionary. Coupon convention and currency require metadata.

## S07-E05 — Basis points

250 / 10000 = .025 = 2.5%.

## S07-E06 — Missing coupon

Zero is a known coupon rate of zero. None represents unavailable data and must not silently become zero.

## S08-E01 — Revenue

Net 37,500 currency units; expense ratio .75 and net ratio .25 are dimensionless fractions of revenue.

## S08-E02 — Weights

Total 100,000 same-currency units; weights .75, .20, .05; sum approximately one. Same valuation date and currency are assumed.

## S08-E03 — Spread

150bp=.015=1.5%; combined .0525=5.25%, assuming compatible rate conventions.

## S08-E04 — Growth

FV=98,357.57; absolute growth=48,357.57 currency units; relative growth=.967151357289565... or 96.7151...%, over all ten years, not per year.

## S08-E05 — Division

100/12 is approximately 8.333333333333334; 100//12 is 8. Floor division discards the fractional quotient and can materially understate per-period amounts.

## S08-E06 — Exponent

Use principal * (1 + rate) ** years. The caret is bitwise XOR and is not exponentiation.

## S08-E07 — Asymmetric returns

1000*1.2*.8=960. The second percentage applies to 1200, producing a 240 loss after a 200 gain.

## S08-E08 — Units

100 USD + 5 years is dimensionally invalid, although Python integers can be added. Attach explicit units and validate financial meaning.

## S09-E01 — FV translation

future_value = principal * (1 + rate) ** periods. Addition forms the per-period factor, exponentiation compounds, multiplication scales by principal. The = symbol binds the result to the name (assignment statement); parentheses group the addition, and are not an arithmetic operator.

## S09-E02 — PV translation

present_value = future_value / (1 + rate) ** periods; equivalently growth_factor=(1+rate)**periods then present_value=future_value/growth_factor. Require a meaningful nonzero factor and compatible periods/rate.

## S09-E03 — Return grouping

return_rate=(final_price-initial_price)/initial_price, with nonzero initial_price. At 110 and 100 the correct return is .1; ungrouped form gives 109.

## S09-E04 — Average

average=(x1+x2+x3+x4)/4. For 1,2,3,4 the result is 2.5.

## S09-E05 — Unary precedence

-3**2=-9; (-3)**2=9; 3**-2=1/9 approximately .1111111111111111. The first groups as -(3**2); parentheses move the minus into the base in the second; the negative exponent in the third forms the reciprocal.

## S09-E06 — Associativity

2**3**2=512 (right grouping); (2**3)**2=64.

## S09-E07 — Portfolio return

portfolio_return = stock_weight * stock_return + bond_weight * bond_return + cash_weight * cash_return. Use compatible holding periods and return definitions; example .5*.1+.3*.04+.2*(-.02)=.058.

## S09-E08 — Spread

75bp=.0075; .0425+.0075=.05=5%.

## S09-E09 — Normalization

5 percent / 100 = .05 decimal rate; normalize once. Using 5 directly treats it as 500%, giving a factor of 6 per year; use annual_rate=annual_rate_percent/100.

## S09-E10 — Known cases

P=100, r=.05, n=0 gives 100; P=100, r=0, n=7 gives 100; P=100, r=.05, n=1 gives 105. Use default math.isclose for these float comparisons.

## S10-E01 — Acquire text

input returns str on successful input: entering 1000 produces string 1000. Tested with controlled StringIO stdin.

## S10-E02 — Parse principal

float(input(...)) gives 1000.0 and type float for text 1000. Parsing does not establish domain validity.

## S10-E03 — Normalize rate

float rate percent 6.25 / 100 gives .0625. This supplement assumes annual effective percent.

## S10-E04 — Whole periods

int("12") gives 12; int("12.5") raises ValueError; do not parse through float and truncate.

## S10-E05 — Conversion error

Catch ValueError and present a clear principal parsing message for abc; see reference helper.

## S10-E06 — Domain

Require finite P>0 and whole n>=0; reject P=0, negative P, negative n. This is a selected simplified contract, not a universal finance rule.

## S10-E07 — Finite checks

float accepts nan and inf; math.isfinite must reject both principal and rate before arithmetic.

## S10-E08 — Money display

f"${value:,.2f}" produces $1,234,567.89. Original float remains unchanged; no monetary posting/rounding policy follows.

## S10-E09 — Percent display

f"{rate:.2%}" produces 4.75%; stored rate remains .0475.

## S10-E10 — Input contract

Principal: USD decimal text, parsed finite positive float. Annual effective rate: percent text, finite float, strictly greater than -100%, normalized once to decimal. Years: whole integer text, nonnegative int. No fees, tax, cash flows, inflation or day-count conventions. Reject overflow/nonfinite computed values; not production precision policy.

## S10-E11 — Output contract

Name Future value; USD; money displayed with separators and two decimals; rate displayed as annual effective percent; years shown; disclose constant annual compounding, no intermediate rounding, no fees/tax/cash flows and float teaching arithmetic.

## S10-E12 — Pipeline

Acquire three text inputs; parse float/float/int; validate principal/rate/years; normalize percent; calculate; reject overflow/nonfinite result; format labeled units; print. See pipeline and CLI entry point in review.py.

