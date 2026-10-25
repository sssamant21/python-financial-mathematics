"""Independent reference checks for Section 9.9 chapter project."""
import json
import math
from section_9_09 import finite, validate_flows, baseline, scenario, project_report

def close(a, b, rel_tol=1e-9, abs_tol=1e-8):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected " + exc.__name__)

def run():
    sample = [(120, 0.5), (120, 1), (120, 2), (1120, 3)]
    r = 0.04
    discounted = [c * math.exp(-r * t) for c, t in sample]
    expected_v = math.fsum(discounted)
    expected_d1 = -math.fsum(t * v for (_, t), v in zip(sample, discounted))
    expected_d2 = math.fsum(t*t*v for (_, t), v in zip(sample, discounted))
    b = baseline(sample, r)
    close(b["value"], expected_v)
    close(b["first"], expected_d1)
    close(b["second"], expected_d2)
    assert b["convexity"] + 1e-12 >= b["duration"]**2
    one = baseline([(10000, 5)], 0.04)
    close(one["duration"], 5)
    close(one["convexity"], 25)
    report = project_report(sample, r, [-100, -50, 0, 50, 100])
    assert len(report["scenarios"]) == 5
    assert report["validation"]["in_model_bound_checks_pass"]
    assert not report["validation"]["runtime_certified"]
    assert not report["validation"]["independent_review_completed"]
    json.dumps(report, allow_nan=False)
    for row in report["scenarios"]:
        h = row["shock_bp"] / 10000
        exact = math.fsum(v * math.expm1(-t*h)
                          for (_, t), v in zip(sample, discounted))
        close(row["exact_change"], exact)
        close(row["linear_change"], expected_d1*h)
        close(row["quadratic_change"], expected_d1*h + 0.5*expected_d2*h*h)
        assert row["linear_bound_pass"] and row["quadratic_bound_pass"]
        if h > 0:
            assert row["exact_change"] < 0
        if h < 0:
            assert row["exact_change"] > 0
        if h == 0:
            close(row["exact_change"], 0)
            close(row["linear_change"], 0)
            close(row["quadratic_change"], 0)
    for h_bp in (-100, -1, 0, 1, 100):
        row = scenario([(10000, 5)], 0.04, h_bp)
        v = 10000*math.exp(-0.2)
        h = h_bp/10000
        close(row["exact_change"], v*math.expm1(-5*h))
        assert row["linear_bound_pass"] and row["quadratic_bound_pass"]
    rejects(ValueError, validate_flows, [])
    rejects(ValueError, baseline, [(0, 1)], 0.04)
    rejects(ValueError, baseline, [(100, -1)], 0.04)
    rejects(ValueError, project_report, sample, 0.04, [0, 50])
    rejects(ValueError, project_report, sample, 0.04, [-50, 50])
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 9.9 project reference checks")

if __name__ == "__main__":
    run()
