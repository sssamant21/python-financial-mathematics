# Project 38 — European Put–Call Parity and Bid/Ask Consistency

**Business question:** Are contemporaneous European call and put quote intervals consistent with one shared forward/financing convention?

For the same strike and expiry, European parity with continuous deterministic dividend yield `q` and continuously compounded risk-free rate `r` is

`C - P = S exp(-qT) - K exp(-rT)`.

The difference between any theoretical call and put inside the quoted bid/ask ranges lies in `[call_bid - put_ask, call_ask - put_bid]`. The lab tests whether parity falls inside that interval. A failed test flags a **necessary-condition inconsistency**, not a realizable profit: financing, stock borrow, fees, latency, exercise styles and executable size are not modeled. Midpoint differences alone do not imply an arbitrage.

## Reproduce

Python 3.11+ standard library only, no market data or external dependencies:

```sh
cd quant-projects/38-put-call-parity
python -m unittest -v test_parity.py
python -m compileall -q parity.py test_parity.py
python parity.py
```

The examples are synthetic and do not provide financial advice or broker actions. Inputs require positive spot/strike and maturity, finite quotes, nonnegative ordered bid/ask prices, and bounded rate/yield conventions. Assumes same timestamp, currency, underlying, exercise style, maturity and strike, with deterministic rates and dividend yield. Real equity options with early exercise, discrete dividends or borrow constraints require different treatment. Floating-point boundary equality may need independent high-precision review.

**Validation:** see the master tracker for exact execution evidence. No independent review, licensed live quote validation, or production certification is claimed.

## Independent numerical reference and boundary tests

`test_decimal_reference.py` computes the parity target separately with Python's
60-digit `decimal.Decimal.exp()`, using decimal-string inputs. Four test methods
cover zero/negative/positive discount rates, dividend-yield sensitivity, quote
intervals deliberately separated from the theoretical boundary by 0.000001,
and an exactly representable zero-rate case. The interval test leaves a
positive ask spread and tests a lower-bound crossing; it does **not** assert
bitwise equality at a floating-point boundary.

From this folder:

```sh
python -m unittest -v test_parity.py test_decimal_reference.py
python -m compileall -q parity.py test_parity.py test_decimal_reference.py
```

A high-precision cross-check is useful evidence but is not an independent
financial-model audit. Inputs are synthetic; the assumed continuously
compounded rates and continuous dividend yield are not a verified
executable-market financing model.
