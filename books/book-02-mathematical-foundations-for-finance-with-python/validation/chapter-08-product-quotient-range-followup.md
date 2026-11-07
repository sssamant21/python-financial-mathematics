# Section 8.3 complete product and quotient derivative range

[Initial probes](chapter-08-product-quotient-range-baseline.md) · [Exact observations and source blobs](chapter-08-product-quotient-range-followup.json) · [Corrected source](https://github.com/sssamant21/python-financial-mathematics/blob/2f6b47559fc7baa82e59772bbdfbd6445e5374e1/books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/section_8_03.py).

Eleven of 34 observations failed on the baseline. An identical replay against the original module is retained. All 34 corrected observations pass, and the existing Section 8.3 regression suite passes against the corrected module.

The generic helpers combine complete expressions using exact rational arithmetic on finite callback results before converting to float. Finite derivatives hidden by intermediate product, subtraction or denominator-square range failures are retained; true final overflow raises ValueError. Subnormal results and signed underflow remain possible. A zero quotient denominator still rejects before the other callbacks.

The independent references extract the first coefficient of a product of local affine polynomials, or solve the first two coefficients of a quotient power series. They are separate derivations from the implemented combined formula. The checker also observes callback order and one evaluation per required callback, rejection of bool/NaN values, invalid x, zero denominators, genuine result overflow, and signed/subnormal outputs. It does not verify the mathematical correctness of caller-supplied derivative functions.

Run `python check_product_quotient_range.py` from `chapter-08/code` at revision `2f6b47559fc7baa82e59772bbdfbd6445e5374e1`. For baseline replay, pass the original checkout's absolute `chapter-08/code` path to that checker. Selected COV-51 evidence only; remaining financial/copied-helper ranges, independent review, supported-platform validation, release acceptance and canonical approval remain open. [Full candidate run](runtime-refresh-2026-11-07-r06.md).
