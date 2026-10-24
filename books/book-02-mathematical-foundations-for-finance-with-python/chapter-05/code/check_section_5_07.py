"""Reference checks for Section 5.7."""
import math
from section_5_07 import number, schedule, closed_end_balance, reconcile

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-10), (a, b)

def rejects(error, function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    rates = (0.02, -0.01, 0.03)
    flows = (100, -50, 0)
    balances, ledger = schedule(1000, rates, flows)
    for actual, expected in zip(balances, (1000, 1120, 1058.8, 1090.564)):
        close(actual, expected)
    close(ledger[0]["interest"], 20)
    close(ledger[1]["interest"], -11.2)
    close(ledger[2]["interest"], 31.764)
    close(*reconcile(1000, balances, ledger))
    close(closed_end_balance(1000, rates, flows), balances[-1])
    begin, begin_ledger = schedule(1000, rates, flows, "begin")
    for actual, expected in zip(begin, (1000, 1122, 1061.28, 1093.1184)):
        close(actual, expected)
    close(*reconcile(1000, begin, begin_ledger))
    close(schedule(1000, (), ())[0][-1], 1000)
    close(closed_end_balance(1000, (), ()), 1000)
    close(schedule(1000, (0, 0), (100, -50))[0][-1], 1050)
    close(schedule(1000, (0, 0), (100, -50), "begin")[0][-1], 1050)
    rejects(ValueError, schedule, 1000, (0.01,), (100, 100))
    rejects(ValueError, schedule, 1000, (-1,), (100,))
    rejects(ValueError, schedule, 1000, (0.01,), (100,), "bad")
    rejects(ValueError, schedule, 100, (0,), (-200,), allow_negative=False)
    rejects(TypeError, schedule, 100, (), (), "end", 1)
    rejects(TypeError, number, True, "value")
    rejects(ValueError, number, float("nan"), "value")
    print("PASS: Section 5.7 reference checks")

if __name__ == "__main__":
    run()
