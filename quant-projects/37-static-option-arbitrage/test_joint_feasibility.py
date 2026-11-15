import unittest
from joint_feasibility import joint_feasible

class JointFeasibilityTests(unittest.TestCase):
    def test_feasible_exact(self):
        self.assertTrue(joint_feasible([90,100,110],[15,10,6],[15,10,6])["joint_feasible"])
    def test_wide_intervals(self):
        self.assertTrue(joint_feasible([90,100,110],[7,6,2],[20,18,16])["joint_feasible"])
    def test_monotonicity(self):
        self.assertFalse(joint_feasible([90,100,110],[10,12,4],[11,13,5])["joint_feasible"])
    def test_joint_infeasibility(self):
        # All individually screened inequalities can pass, yet no joint fit exists.
        self.assertFalse(joint_feasible([90,100,110,120],[9,3,9,12],[17,9,17,17])["joint_feasible"])
    def test_guards(self):
        with self.assertRaises(ValueError):
            joint_feasible([90,90,110],[1,2,3],[2,3,4])
        with self.assertRaises(ValueError):
            joint_feasible([90,100,110],[1,2,3],[2,1,4])
        with self.assertRaises(ValueError):
            joint_feasible([90,100,110],[1,float("nan"),3],[2,3,4])
        with self.assertRaises(ValueError):
            joint_feasible([90,100,110],[1,2,3],[2,3,4],discount=True)
        with self.assertRaises(ValueError):
            joint_feasible([90,100,110,120,130,140],[1]*6,[2]*6)

if __name__ == "__main__":
    unittest.main()
