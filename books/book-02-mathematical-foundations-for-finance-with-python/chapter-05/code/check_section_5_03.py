"""Reference checks for Section 5.3."""
import math
from section_5_03 import (
    finite, balance_ledger, constant_rate_path, reconcile)

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-10), (a, b)

def rejects(error, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    balances, ledger = constant_rate_path(1000, 0.02, (100, 100, 100))
    for a, b in zip(balances, (1000, 1120, 1242.4, 1367.248)):
        close(a, b)
    close(ledger[0]["interest"], 20)
    close(ledger[0]["cash_flow"], 100)
    change, components = reconcile(1000, balances, ledger)
    close(change, components)
    begin, begin_ledger = constant_rate_path(
        1000, 0.02, (100, 100), timing="begin")
    close(begin[1], 1122)
    close(begin[2], 1246.44)
    close(begin_ledger[0]["interest"], 22)
    withdraw, _ = constant_rate_path(500, 0.01, (-200, -200, -200))
    close(withdraw[-1], -90.8695)
    varying, rows = balance_ledger(
        1000, (0.01, -0.02, 0.03), (100, 0, -50))
    for a, b in zip(varying, (1000, 1110, 1087.8, 1070.434)):
        close(a, b)
    close(*reconcile(1000, varying, rows))
    flat, flat_ledger = constant_rate_path(1000, 0, (100, -50))
    close(flat[-1], 1050)
    close(*reconcile(1000, flat, flat_ledger))
    empty, empty_ledger = constant_rate_path(1000, 0.05, ())
    assert empty == [1000] and empty_ledger == []
    close(*reconcile(1000, empty, empty_ledger))
    rejects(ValueError, balance_ledger, 1000, (0.01,), (100, 100))
    rejects(ValueError, balance_ledger, 1000, (-1,), (100,))
    rejects(ValueError, balance_ledger, 1000, (0.01,), (100,), "invalid")
    rejects(ValueError, constant_rate_path, 500, 0.01,
            (-200, -200, -200), allow_negative=False)
    rejects(ValueError, constant_rate_path, -1, 0.01,
            (), allow_negative=False)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    print("PASS: Section 5.3 reference checks")

if __name__ == "__main__":
    run()
