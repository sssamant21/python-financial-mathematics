"""Reference checks for the educational replication lab; validation pending."""
import math
import unittest
from section_21_05 import solve_2x2

class ReplicationChecks(unittest.TestCase):
    def test_worked_solution(self):
        x = solve_2x2([[1, 1], [1, 2]], [3, 5])["solution"]
        self.assertAlmostEqual(x[0], 1); self.assertAlmostEqual(x[1], 2)
    def test_residual(self):
        r = solve_2x2([[1, 1], [1, 2]], [3, 5])["residual"]
        self.assertTrue(all(abs(v) < 1e-12 for v in r))
    def test_identity(self): self.assertEqual(solve_2x2([[1, 0], [0, 1]], [2, -3])["solution"], (2, -3))
    def test_second_example(self):
        x = solve_2x2([[1, 1], [1, 3]], [4, 8])["solution"]
        self.assertAlmostEqual(x[0], 2); self.assertAlmostEqual(x[1], 2)
    def test_singular_consistent(self):
        with self.assertRaises(ValueError): solve_2x2([[1, 1], [2, 2]], [2, 4])
    def test_singular_inconsistent(self):
        with self.assertRaises(ValueError): solve_2x2([[1, 1], [2, 2]], [2, 5])
    def test_zero_matrix(self):
        with self.assertRaises(ValueError): solve_2x2([[0, 0], [0, 0]], [0, 0])
    def test_shape(self):
        with self.assertRaises(ValueError): solve_2x2([[1, 2]], [1, 2])
    def test_nonfinite(self):
        with self.assertRaises(ValueError): solve_2x2([[math.nan, 0], [0, 1]], [1, 1])
    def test_boolean(self):
        with self.assertRaises(TypeError): solve_2x2([[True, 0], [0, 1]], [1, 1])
    def test_negative_threshold(self):
        with self.assertRaises(ValueError): solve_2x2([[1, 0], [0, 1]], [1, 1], threshold=-1)
    def test_near_singular_screen(self):
        with self.assertRaises(ValueError): solve_2x2([[1, 1], [1, 1+1e-14]], [2, 2])

if __name__ == "__main__": unittest.main()
