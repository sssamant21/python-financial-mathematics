"""Independent scenario benchmarks; runtime validation pending."""
import unittest
import math
import json
from unittest.mock import patch
from section_21_09 import build_report

class IntegratedChecks(unittest.TestCase):
    def test_finite_difference(self):
        sensitivity=build_report()["sensitivity"]
        self.assertEqual(sensitivity["inputs"],{"amount":100,"rate":0,"years":2})
        diagnostic=sensitivity["finite_difference"]
        self.assertEqual(diagnostic["method"],"centered first derivative")
        self.assertEqual(diagnostic["step"],1e-5)
        # Independent exponential quotient: -100*sinh(2h)/h.
        expected=-100*math.sinh(2e-5)/1e-5
        self.assertAlmostEqual(diagnostic["estimate"],expected,places=8)
        self.assertAlmostEqual(diagnostic["estimate"],-200,places=6)
        self.assertAlmostEqual(diagnostic["signed_error"],expected+200,places=8)
        self.assertEqual(diagnostic["absolute_error"],abs(diagnostic["signed_error"]))
        self.assertEqual(diagnostic["units"],"currency per decimal-rate unit")

    def test_json_contract(self):
        report=build_report()
        required={"purpose","cash_flow","sensitivity","replication","allocation",
                  "account","limitations","validation_execution","independent_review","approval"}
        self.assertTrue(required.issubset(report))
        encoded=json.dumps(report,sort_keys=True,allow_nan=False)
        self.assertEqual(encoded,json.dumps(build_report(),sort_keys=True,allow_nan=False))
        decoded=json.loads(encoded)
        self.assertEqual(decoded["sensitivity"]["first_second"],[-200,400])
        self.assertEqual(decoded["replication"]["inputs"]["target"],[3,5])

    def test_numerical_failure_propagates(self):
        with patch("section_21_09.present_value",side_effect=OverflowError("reference failure")):
            with self.assertRaisesRegex(OverflowError,"reference failure"):
                build_report()

    def test_sensitivity_failure_propagates(self):
        with patch("section_21_09.central_difference",side_effect=ValueError("invalid step")):
            with self.assertRaisesRegex(ValueError,"invalid step"):
                build_report()

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
