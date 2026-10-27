"""Independent scenario benchmarks; runtime validation pending."""
import unittest
from section_21_09 import build_report

class IntegratedChecks(unittest.TestCase):
    def test_cash_flow(self): self.assertAlmostEqual(build_report()["cash_flow"]["value"], 50)
    def test_first_derivative(self): self.assertAlmostEqual(build_report()["sensitivity"]["first_second"][0], -200)
    def test_second_derivative(self): self.assertAlmostEqual(build_report()["sensitivity"]["first_second"][1], 400)
    def test_replication_x1(self): self.assertAlmostEqual(build_report()["replication"]["solution"][0], 1)
    def test_replication_x2(self): self.assertAlmostEqual(build_report()["replication"]["solution"][1], 2)
    def test_replication_residual(self):
        for r in build_report()["replication"]["residual"]: self.assertAlmostEqual(r, 0)
    def test_allocation(self):
        weights = build_report()["allocation"]["weights"]
        self.assertAlmostEqual(weights[0], .75); self.assertAlmostEqual(weights[1], .25)
    def test_allocation_objective(self): self.assertAlmostEqual(build_report()["allocation"]["objective"], .005)
    def test_allocation_feasible(self): self.assertTrue(build_report()["allocation"]["diagnostics"]["feasible"])
    def test_account(self): self.assertEqual(build_report()["account"]["ending_balance"], 1600)
    def test_evidence_pending(self):
        report = build_report()
        self.assertEqual(report["validation_execution"], "not run")
        self.assertEqual(report["independent_review"], "pending")
        self.assertEqual(report["approval"], "pending")
    def test_limitations(self): self.assertTrue(build_report()["limitations"])
    def test_replication_inputs_recorded(self):
        self.assertEqual(build_report()["replication"]["inputs"]["target"], [3, 5])
    def test_allocation_inputs_recorded(self):
        self.assertEqual(build_report()["allocation"]["inputs"]["target_a"], .7)

if __name__ == "__main__": unittest.main()
