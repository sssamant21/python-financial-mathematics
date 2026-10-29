"""Known-value tests for section 20.5; validation pending."""
import math
import unittest
from section_20_05 import close_to_reference, errors

class ToleranceChecks(unittest.TestCase):
    def test_absolute_error_overflow(self):
        for a,b in ((1e308,-1e308),(-1e308,1e308)):
            with self.subTest(a=a,b=b), self.assertRaisesRegex(OverflowError,"absolute error"):
                errors(a,b)

    def test_relative_error_overflow(self):
        for reference in (5e-324,-5e-324):
            with self.subTest(reference=reference), self.assertRaisesRegex(OverflowError,"relative error"):
                errors(1,reference)

    def test_finite_extreme_errors(self):
        maximum=float.fromhex("0x1.fffffffffffffp+1023")
        self.assertEqual(errors(maximum,0),(maximum,None))
        self.assertEqual(errors(0,maximum),(maximum,1))
        self.assertEqual(errors(maximum,maximum),(0,0))
        self.assertEqual(errors(5e-324,0),(5e-324,None))
        self.assertEqual(errors(0,5e-324),(5e-324,1))
        self.assertEqual(errors(-5e-324,5e-324),(1e-323,2))

    def test_negative_reference_scale(self):
        self.assertEqual(errors(-101,-100),(1,.01))
        self.assertEqual(errors(1,-1),(2,2))

    def test_errors_invalid_inputs(self):
        for actual,reference in ((math.inf,1),(1,math.nan),(1,-math.inf)):
            with self.subTest(actual=actual,reference=reference), self.assertRaises(ValueError):
                errors(actual,reference)
        for actual,reference in ((True,1),(1,False)):
            with self.subTest(actual=actual,reference=reference), self.assertRaises(TypeError):
                errors(actual,reference)

    def test_comparison_independent_of_error_report_range(self):
        # Exact represented-float comparison remains available even when the
        # separately requested error magnitudes cannot be represented.
        self.assertTrue(close_to_reference(1e308,-1e308,atol=0,rtol=2))
        self.assertFalse(close_to_reference(1,-5e-324,atol=0,rtol=1))

    def test_errors(self): self.assertEqual(errors(101, 100), (1.0, .01))
    def test_zero_reference(self): self.assertEqual(errors(.125, 0), (.125, None))
    def test_exact(self): self.assertTrue(close_to_reference(1, 1, atol=0, rtol=0))
    def test_boundary(self): self.assertTrue(close_to_reference(1.125, 1, atol=.0625, rtol=.0625))
    def test_outside(self): self.assertFalse(close_to_reference(1.25, 1, atol=.0625, rtol=.0625))
    def test_absolute(self): self.assertTrue(close_to_reference(.125, 0, atol=.125, rtol=0))
    def test_relative(self): self.assertTrue(close_to_reference(101, 100, atol=0, rtol=.011))
    def test_zero_tolerance(self): self.assertFalse(close_to_reference(.125, 0, atol=0, rtol=0))
    def test_adjacent_values_with_zero_tolerance(self):
        self.assertFalse(close_to_reference(math.nextafter(1.0, math.inf), 1.0, atol=0, rtol=0))
    def test_large_opposite_signs(self):
        self.assertFalse(close_to_reference(1e308, -1e308, atol=0, rtol=1))
    def test_negative_tolerance(self):
        with self.assertRaises(ValueError): close_to_reference(1, 1, atol=-1, rtol=0)
    def test_nonfinite(self):
        for x in (math.nan, math.inf, -math.inf):
            with self.subTest(x=x), self.assertRaises(ValueError): close_to_reference(x, 1, atol=0, rtol=0)
    def test_type(self):
        with self.assertRaises(TypeError): close_to_reference(True, 1, atol=0, rtol=0)
    def test_max_rule_differs(self):
        self.assertTrue(close_to_reference(1.125, 1, atol=.0625, rtol=.0625))
        self.assertFalse(math.isclose(1.125, 1, abs_tol=.0625, rel_tol=.0625))

if __name__ == "__main__": unittest.main()
