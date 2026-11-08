# Next checkpoint: Section 8.5 stable exponential quotient

Executable revision `31c777e7b1e41eaa3913a5144a69c6cb56cf914a`. [Six actual probes and independent complete references](chapter-08-stable-exponential-quotient-baseline.json).

The helper computes exp(x)·expm1(h)/h. Four selected finite complete quotients are lost: x=1000 with a huge negative step raises OverflowError; x=-1000, h=1000 raises OverflowError despite a quotient 0.001; x=-750, h=100 returns zero instead of about 5.11e-285; x=700, h=10 returns infinity instead of about 2.23e307. Tiny-step and huge-negative-step controls retain working outputs.

Independent complete differences [exp(x+h)-exp(x)]/h at Decimal precisions 1600/2200 agree. Very negative exponential terms are replaced by zero only beyond a conservative bound far below output/working precision in these selected probes. Actual results replay identically beside the pinned, hash-verified source/dependency. Runnable probe code is in JSON.

Next establish complete coefficient/exponent/gap scaling, finite-output/underflow policy and represented x+h convention while preserving x/step validation and rejection of zero step. Preserve tiny-step accuracy, then continue the Section 8.5 centered-copy obligation. Resource limits and independent review remain open. Do not repeat completed log-return, rate-shock, PV or accumulation examples.
