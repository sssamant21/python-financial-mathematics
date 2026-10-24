"""Reference checks for Section 4.9."""
import contextlib
import io
import json
import math
from section_4_09 import (
    finite, periodic_log_factor, periodic_result, continuous_result,
    convert_result, main)

def close(a, b, rel=1e-11, absolute=1e-10):
    assert math.isclose(a, b, rel_tol=rel, abs_tol=absolute), (a, b)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run_cli(argv):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        assert main(argv) == 0
    return json.loads(output.getvalue())

def run():
    p = periodic_result(10000, 0.06, 12, 36)
    close(p["future_value"], 10000 * 1.005**36)
    close(p["recovered_present_value"], 10000)
    close(p["effective_annual_rate"], 1.005**12 - 1)
    c = continuous_result(10000, p["equivalent_continuous_annual_rate"], 3)
    close(c["future_value"], p["future_value"])
    close(c["recovered_present_value"], 10000)
    close(c["relative_fv_sensitivity_to_10bp"], 0.003)
    close(c["exact_relative_fv_change_for_10bp"], math.expm1(0.003))
    for m in (1, 2, 4, 12, 365):
        for ear in (-0.2, 0, 1e-12, 0.05, 0.5):
            rates = convert_result(ear, m)
            again = periodic_result(100, rates["nominal_annual_rate"], m, m)
            close(again["effective_annual_rate"], ear)
            close(again["equivalent_continuous_annual_rate"],
                  rates["continuous_annual_rate"])
    close(periodic_log_factor(0, 12, 0), 0)
    close(periodic_result(1000, 0, 12, 12)["future_value"], 1000)
    close(continuous_result(1000, -0.05, 2)["future_value"],
          1000 * math.exp(-0.1))
    cli = run_cli(["periodic", "--principal", "10000", "--nominal-rate",
                   "0.06", "--frequency", "12", "--periods", "36"])
    close(cli["future_value"], p["future_value"])
    cli = run_cli(["continuous", "--principal", "1000",
                   "--continuous-rate", "0.05", "--years", "2"])
    close(cli["future_value"], 1000*math.exp(0.1))
    cli = run_cli(["convert", "--ear", "0.05", "--frequency", "12"])
    close(cli["continuous_annual_rate"], math.log1p(0.05))
    rejects(ValueError, periodic_result, -100, 0.05, 12, 12)
    rejects(ValueError, periodic_result, 100, -1, 1, 1)
    rejects(ValueError, periodic_result, 100, 0.05, 0, 1)
    rejects(ValueError, periodic_result, 100, 0.05, 12, -1)
    rejects(ValueError, continuous_result, 100, 0.05, -1)
    rejects(ValueError, convert_result, -1, 12)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    print("PASS: Section 4.9 reference checks")

if __name__ == "__main__":
    run()
