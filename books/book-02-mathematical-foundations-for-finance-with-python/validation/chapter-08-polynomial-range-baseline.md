# Next checkpoint: Section 8.2 polynomial range

Source revision `a6441d707337946a76e059c6cf53a5b05291afa0`; unchanged `chapter-08/code/section_8_02.py` blob `c625e24ea17d574f4d60ec335b315216893b3ca1`.

Actual probes on this source:

```python
import sys
from section_8_02 import polynomial, polynomial_derivative
M = sys.float_info.max
polynomial([-M, M], 2.0)  # raises OverflowError: polynomial overflow
polynomial_derivative([0.0, 0.0, M], 0.0)  # raises ValueError: coefficient must be finite
```

Independent algebra gives -M + 2M = M for the first result and 2M·0 = 0 for the second. Both final results are representable; intermediate floating products or derivative coefficients are not. These are two substantiated next-batch failures, not corrected passes. Preserve this baseline and derive exact rational full-polynomial and point-specific derivative references before changing behavior. Distinguish an unrepresentable coefficient-returning API from a finite derivative value and preserve documented exception conventions. The Section 8.2 centered-difference copy is also still open.

COV-51 stays partial. Resume here; do not repeat completed Section 8.1 financial or Section 8.3 wrapper examples. Independent review/platform/release decisions remain separate.
