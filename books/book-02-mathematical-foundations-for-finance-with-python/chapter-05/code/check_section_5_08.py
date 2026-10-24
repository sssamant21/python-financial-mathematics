"""Reference checks for Section 5.8."""
import math
from section_5_08 import number, simulate_withdrawals, zero_rate_first_infeasible

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-10), (a, b)

def rejects(error, function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    zero = simulate_withdrawals(500, (0,)*3, (200,)*3)
    assert zero["first_infeasible"] == 3
    close(zero["ledger"][0]["closing"], 300)
    close(zero["ledger"][1]["closing"], 100)
    close(zero["ledger"][2]["paid"], 0)
    close(zero["closing_balance"], 100)
    partial = simulate_withdrawals(500, (0,)*3, (200,)*3, policy="partial")
    assert partial["first_infeasible"] == 3
    close(partial["ledger"][2]["paid"], 100)
    close(partial["closing_balance"], 0)
    interest = simulate_withdrawals(500, (0.01,)*3, (200,)*3)
    assert interest["first_infeasible"] == 3
    close(interest["ledger"][2]["available"], 109.1305)
    exact = simulate_withdrawals(1000, (0,)*5, (250,)*5)
    assert exact["first_infeasible"] == 5
    close(exact["ledger"][3]["closing"], 0)
    assert exact["ledger"][3]["feasible"]
    begin = simulate_withdrawals(100, (0.1,), (105,), timing="begin")
    assert begin["first_infeasible"] == 1
    end = simulate_withdrawals(100, (0.1,), (105,), timing="end")
    assert end["first_infeasible"] is None
    close(end["closing_balance"], 5)
    assert zero_rate_first_infeasible(500, 200) == 3
    assert zero_rate_first_infeasible(1000, 250) == 5
    assert simulate_withdrawals(0, (), ())["first_infeasible"] is None
    rejects(ValueError, simulate_withdrawals, -1, (), ())
    rejects(ValueError, simulate_withdrawals, 100, (0,), (1, 2))
    rejects(ValueError, simulate_withdrawals, 100, (-1,), (1,))
    rejects(ValueError, simulate_withdrawals, 100, (0,), (-1,))
    rejects(ValueError, simulate_withdrawals, 100, (0,), (1,), "bad")
    rejects(ValueError, zero_rate_first_infeasible, 100, 0)
    rejects(TypeError, number, True, "x")
    rejects(ValueError, number, float("nan"), "x")
    print("PASS: Section 5.8 reference checks")

if __name__ == "__main__":
    run()
